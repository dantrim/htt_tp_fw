import sys
import os
import json

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Combine, Timer
from cocotb.result import TestFailure, TestSuccess

from tp_tb.testbench.b2b.b2b_ports import B2BPorts
from tp_tb.testbench.b2b import b2b_utils
import tp_tb.testbench.b2b.b2b_wrapper as wrapper

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
    n_inputs_ok = len(input_fifos) == len(B2BPorts.Inputs)

    output_fifos = [x.spybuffer for x in dut.output_spybuffers]
    n_outputs_ok = len(output_fifos) == len(B2BPorts.Outputs)
    n_io_ports_ok = n_inputs_ok and n_outputs_ok
    if not n_io_ports_ok:
        raise Exception(
            f"ERROR # of B2B io ports differ between CocoTB and RTL simulation:\n -> CocoTB expects (IN,OUT)=({len(B2BPorts.Inputs)},{len(B2BPorts.Outputs)})\n -> RTL expects (IN,OUT)=({len(input_fifos)},{len(output_fifos)})"
        )

    initialize_spybuffers(fifos=input_fifos)
    initialize_spybuffers(fifos=output_fifos)


@cocotb.coroutine
def reset(dut):

    """
    Resets the B2B testbench, having reset active LOW.
    """

    dut.reset_n <= 1
    yield ClockCycles(dut.clock, 10)
    dut.reset_n <= 0
    yield ClockCycles(dut.clock, 10)
    dut.reset_n <= 1


##
## TEST0
##
@cocotb.test()
def b2b_test_0(dut):

    ##
    ## first grab the testbench configuration
    ##
    config = test_config.get_config()

    ##
    ## process input arguments for this test
    ##
    input_args = config["input_args"]
    num_events_to_process = int(input_args["n_events"])
    event_delays = bool(input_args["event_delays"])
    event_level_detail_in_summary = bool(input_args["event_detail"])

    ##
    ## Mark the current board
    ##

    this_tp = (
        B2BPorts.Outputs.AMTP_0
    )  # hardcode for now, later take BOARD_ID from env and set the B2B inst to this value
    board_id = int(dut.board2board_switching_inst.BOARD_ID)
    dut._log.info(f"Instantiating B2B block with BOARD_ID = {board_id}")
    this_tp = None
    for io in B2BPorts.Outputs:
        if int(io.value) == board_id:
            this_tp = io
            break
    if not this_tp:
        raise ValueError(f"Unable to find associated IO for B2B BOARD_ID={board_id}")
    dut._log.info(
        f"Setting test IO with base (port_name, port_num) = ({this_tp.name}, {this_tp.value})"
    )

    ##
    ## Setup the clock and start it running
    ##
    sim_clock = Clock(
        dut.clock, int(input_args["clock_period"]), input_args["clock_time_unit"]
    )
    cocotb.fork(sim_clock.start())

    ##
    ## initialize dut for test
    ##
    initialize_dut(dut)

    ##
    ## reset testbench
    ##
    dut._log.info("Resetting DUT")
    yield reset(dut)

    ##
    ## get testvectors
    ##
    (
        input_testvector_files,
        output_testvector_files,
    ) = test_config.get_testvector_files_from_config(config)

    ##
    ## initialize B2B block wrapper
    ##
    b2b = wrapper.B2BWrapper(
        clock=dut.clock, name=f"B2BWrapper_{B2BPorts.simplename(this_tp)}"
    )
    for i, io in enumerate(B2BPorts.Inputs):
        port_num = io.value
        driver = FifoDriver(
            dut.input_spybuffers[port_num].spybuffer,
            dut.clock,
            "B2B",
            io,
            write_out=True,
        )
        b2b.add_input_driver(driver, io)

    for i, io in enumerate(B2BPorts.Outputs):
        active = this_tp.value != io.value
        monitor = FifoMonitor(
            dut.output_spybuffers[i].spybuffer,
            dut.clock,
            "B2B",
            io,
            callbacks=[],
            write_out=True,
        )
        b2b.add_output_monitor(monitor, io, active=active)
    b2b.sort_ports()

    ##
    ## send events
    ##
    dut._log.info("Sending input events")
    send_finished_signal = b2b.send_input_events(
        input_testvector_files,
        n_to_send=num_events_to_process,
        event_delays=event_delays,
    )
    if not send_finished_signal:
        raise cocotb.result.TestFailure(
            f"ERROR Event sending timed out! Number of expected inputs with events = {len(send_finished_signal)}"
        )
    yield Combine(*send_finished_signal)
    dut._log.info("Sending finished!")

    timer = Timer(20, "us")
    dut._log.info("Going to wait 20 microseconds")
    yield timer

    ##
    ## perform testvector comparison test
    ##
    all_tests_passed = True
    all_test_results = []
    for oport in b2b.output_ports:

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
        ## we expect nothing from the current board but there may be testvectors,
        ## so "zero" out any testvectors for this output
        ##
        if io.value == this_tp.value:
            expected_output_events = []

        ## test
        events_equal, test_results = tb_diff.events_are_equal(
            recvd_events, expected_output_events, verbose=False
        )
        result_summary = result_handler.result_summary_dict(
            f"B2B_Output_{io.value:02}",
            str(output_testvector_file),
            test_name=f"TEST_B2B_SRC{this_tp.value:02}_DEST{io.value:02}",
            test_results=test_results,
        )
        all_tests_passed = (
            all_tests_passed and result_summary["test_results"]["test_success"]
        )
        all_test_results.append(result_summary)

        this_tp_name = (
            f"{this_tp.name.split('_')[0]}{int(this_tp.name.split('_')[1]):02}"
        )
        out_io_name = f"{io.name.split('_')[0]}{int(io.name.split('_')[1]):02}"
        output_json_name = (
            f"test_results_summary_B2B_src{this_tp_name}_dest{out_io_name}.json"
        )
        with open(output_json_name, "w", encoding="utf-8") as f:
            json.dump(result_summary, f, ensure_ascii=False, indent=4)

    result_handler.dump_test_results(
        all_test_results, event_detail=event_level_detail_in_summary
    )
    cocotb_result = {True: cocotb.result.TestSuccess, False: cocotb.result.TestFailure}[
        all_tests_passed
    ]

    raise cocotb_result
