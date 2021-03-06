import sys
import os
import json

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Combine, Timer
from cocotb.result import TestFailure, TestSuccess

import tp_tb.testbench.example_sw_block.sw_switcher_wrapper as wrapper
import tp_tb.testbench.example_sw_block.sw_switcher_block as sw_switcher_block
from tp_tb.testbench.example_sw_block.sw_switcher_ports import SWSwitcherPorts

from tp_tb.utils import test_config
from tp_tb.utils import events, tb_diff, result_handler
from tp_tb.utils.fifo_wrapper import FifoDriver, FifoMonitor


def initialize_spybuffers(fifos=[]):

    for ififo, fifo in enumerate(fifos):
        fifo.read_enable <= 0
        fifo.write_enable <= 0
        fifo.empty <= 1
        fifo.almost_full <= 0
        fifo.read_data <= 0
        fifo.write_data <= 0


def initialize_dut(dut):

    ##
    ## initialize the FIFOs
    ##
    input_fifos = [x.spybuffer for x in dut.input_spybuffers]
    n_inputs_ok = len(input_fifos) == len(SWSwitcherPorts.Inputs)

    output_fifos = [x.spybuffer for x in dut.output_spybuffers]
    n_outputs_ok = len(output_fifos) == len(SWSwitcherPorts.Outputs)

    n_io_ports_ok = n_inputs_ok and n_outputs_ok
    if not n_io_ports_ok:
        raise Exception(
            f"ERROR # of SWSwitcher io ports differ between CocoTB and RTL simulation:\n -> CocoTB expects (IN,OUT)=({len(SWSwitcherPorts.Inputs)},{len(SWSwitcherPorts.Outputs)})\n -> RTL expects (IN,OUT)=({len(input_fifos)},{len(output_fifos)})"
        )
    initialize_spybuffers(input_fifos)
    initialize_spybuffers(output_fifos)


@cocotb.coroutine
def reset(dut):
    """
    Resets the testbench, assuming reset is active LOW
    """

    dut.reset_n <= 1
    yield ClockCycles(dut.clock, 10)
    dut.reset_n <= 0
    yield ClockCycles(dut.clock, 10)
    dut.reset_n <= 1


##
## TEST
##
@cocotb.test()
def sw_block_test(dut):

    ##
    ## first grab the testbench configuration
    ##
    config = test_config.get_config()

    ##
    ## process input arguments for this test
    ##
    input_args = config["input_args"]
    num_events_to_process = int(input_args["n_events"])

    ##
    ## create the software DUT
    ##
    switcher_block = sw_switcher_block.SWSwitcherBlock(dut.clock, "SWSwitcherBlock")
    for i, io in enumerate(SWSwitcherPorts.Inputs):
        switcher_block.add_fifo(
            dut.input_spybuffers[i].spybuffer,
            dut.clock,
            f"{switcher_block.name}_Input_{i}",
            io,
            direction="in",
        )
    for i, io in enumerate(SWSwitcherPorts.Outputs):
        switcher_block.add_fifo(
            dut.output_spybuffers[i].spybuffer,
            dut.clock,
            f"{switcher_block.name}_Output_{i}",
            io,
            direction="out",
        )
    switcher_block.start()

    ##
    ## setup the clock and start it running
    ##
    sim_clock = Clock(
        dut.clock, int(input_args["clock_period"]), input_args["clock_time_unit"]
    )
    cocotb.fork(sim_clock.start())

    ##
    ## initialize dut
    ##
    initialize_dut(dut)

    ##
    ## reset the testbench
    ##
    dut._log.info("Resetting DUT")
    yield reset(dut)

    ##
    ## get the testvectors
    ##
    (
        input_testvector_files,
        output_testvector_files,
    ) = test_config.get_testvector_files_from_config(config)

    ##
    ## initialize the (software-based) block wrapper
    ##
    sw_switcher_wrapper = wrapper.SWSwitcherWrapper(dut.clock, name="SWSwitcherWrapper")
    for i, io in enumerate(SWSwitcherPorts.Inputs):
        port_num = io.value
        driver = FifoDriver(
            dut.input_spybuffers[port_num].spybuffer,
            dut.clock,
            "SWSwitcher",
            io,
            write_out=True,
        )
        sw_switcher_wrapper.add_input_driver(driver, io)

    for i, io in enumerate(SWSwitcherPorts.Outputs):
        monitor = FifoMonitor(
            dut.output_spybuffers[i].spybuffer,
            dut.clock,
            "SWSwitcher",
            io,
            write_out=True,
        )
        sw_switcher_wrapper.add_output_monitor(monitor, io, active=True)
    sw_switcher_wrapper.sort_ports()

    ##
    ## send input events
    ##
    dut._log.info("Sending input events")
    send_finished_signal = sw_switcher_wrapper.send_input_events(
        input_testvector_files, n_to_send=num_events_to_process
    )
    if not send_finished_signal:
        raise cocotb.result.TestFailure("ERROR Event sending timed out!")
    yield Combine(*send_finished_signal)
    dut._log.info("Sending finished!")

    timer = Timer(500, "us")
    dut._log.info("Going to wait 20 microseconds")
    yield timer

    ##
    ## perform testvector comparison test
    ##
    all_tests_passed = True
    all_test_results = []
    for oport in sw_switcher_wrapper.output_ports:

        ##
        ## extract the observed data for this output
        ##
        monitor, io, _ = oport
        words = monitor.observed_words
        recvd_events = events.load_events(words, "little")
        cocotb.log.info(
            f"Output for {io.name} (output port num {io.value}) received {len(recvd_events)} events"
        )

        ##
        ## extract the expected data for this output
        ##
        if config["run_config"]["expected_is_observed"]:
            # map the "expected" to be the same as the "observed"
            dut._log.warning(
                "WARNING Taking expected events to be the same as the observed events!"
            )
            output_testvector_file = "expected_is_observed"
            expected_output_events = recvd_events
        else:
            output_testvector_file = output_testvector_files[io.value]
            expected_output_events = events.load_events_from_file(
                output_testvector_file, n_to_load=num_events_to_process
            )

        ##
        ## perform test by comparison with expected testvectors
        ##
        events_equal, test_results = tb_diff.events_are_equal(
            recvd_events, expected_output_events, verbose=False
        )
        result_summary = result_handler.result_summary_dict(
            f"SWSwitcher_Output_{io.value:02}",
            str(output_testvector_file),
            test_name=f"TEST_SWSWITCHER_DEST{io.value:02}",
            test_results=test_results,
        )

        all_tests_passed = (
            all_tests_passed and result_summary["test_results"]["test_success"]
        )
        all_test_results.append(result_summary)

        output_json_name = f"test_results_summary_SWSwitcher_dest{io.value:02}.json"
        with open(output_json_name, "w", encoding="utf-8") as f:
            json.dump(result_summary, f, ensure_ascii=False, indent=4)

    result_handler.dump_test_results(all_test_results, event_detail=False)

    cocotb_result = {True: cocotb.result.TestSuccess, False: cocotb.result.TestFailure}[
        all_tests_passed
    ]

    raise cocotb_result
