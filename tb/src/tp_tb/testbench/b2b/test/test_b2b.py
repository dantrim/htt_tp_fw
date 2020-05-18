import sys
import os
import json

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Combine, Timer
from cocotb.result import TestFailure, TestSuccess

from tp_tb.testbench.b2b import b2b_utils
import tp_tb.testbench.b2b.b2b_wrapper as wrapper

from tp_tb.utils import test_config
from tp_tb.utils import events, tb_diff, result_handler
from tp_tb.utils.fifo_wrapper import FifoDriver, FifoMonitor

##
## CONSTANTS
##
# CLOCK_PERIOD = 5 # ns
TEST_CONFIG_ENV = "COCOTB_TEST_CONFIG_FILE"

##
## communicate "command line arguments"
##
test_args = {
    "N_EVENTS": 2,
    "EVENT_DELAYS": False,
    "EVENT_DETAIL": False,
    "CLOCK_PERIOD": 5,  # ns period
    "CLOCK_TIME_UNIT": "ns",
}


def check_input_args():
    global test_args
    for input_arg, default_value in test_args.items():
        test_args[input_arg] = os.environ.get(input_arg, default_value)


check_input_args()


def initialize_spybuffers(fifos=[]):

    for ififo, fifo in enumerate(fifos):
        fifo.read_enable <= 0
        fifo.write_enable <= 0
        fifo.empty <= 1
        fifo.almost_full <= 0
        fifo.read_data <= 0
        fifo.write_data <= 0


def initialize_test_state(dut):

    ##
    ## initialize the FIFOs
    ##

    input_fifos = [x.spybuffer for x in dut.input_spybuffers]
    n_inputs_ok = len(input_fifos) == len(b2b_utils.B2BIO.Inputs)

    output_fifos = [x.spybuffer for x in dut.output_spybuffers]
    n_outputs_ok = len(output_fifos) == len(b2b_utils.B2BIO.Outputs)
    n_io_ports_ok = n_inputs_ok and n_outputs_ok
    if not n_io_ports_ok:
        raise Exception(
            "ERROR # of B2B io ports differ between CocoTB and RTL simulation: \
                CocoTB expects (IN,OUT)=({},{})\n\t -> RTL expects (IN,OUT)=({},{})".format(
                len(b2b_utils.B2BIO.Inputs),
                len(b2b_utils.B2BIO.Outputs),
                len(input_fifos),
                len(output_fifos),
            )
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
    ## process input arguments for this test
    ##
    input_args = test_config.input_args_from_config(os.environ.get(TEST_CONFIG_ENV, ""))
    num_events_to_process = int(input_args["n_events"])
    event_delays = bool(input_args["event_delays"])
    event_level_detail_in_summary = bool(input_args["event_detail"])

    ##
    ## Mark the current board
    ##

    this_tp = (
        b2b_utils.B2BIO.Outputs.AMTP_0
    )  # hardcode for now, later take BOARD_ID from env and set the B2B inst to this value
    board_id = int(dut.board2board_switching_inst.BOARD_ID)
    dut._log.info("Instantiating B2B block with BOARD_ID = {}".format(board_id))
    this_tp = None
    for io in b2b_utils.B2BIO.Outputs:
        if int(io.value) == board_id:
            this_tp = io
            break
    if not this_tp:
        raise ValueError(
            "Unable to find associated IO for B2B BOARD_ID={}".format(board_id)
        )
    dut._log.info(
        "Setting test IO with base (port_name, port_num) = ({}, {})".format(
            this_tp.name, this_tp.value
        )
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
    initialize_test_state(dut)

    ##
    ## reset testbench
    ##
    dut._log.info("Resetting DUT")
    yield reset(dut)

    ##
    ## get testvectors
    ##
    testvector_dir = b2b_utils.testvec_dir_from_env()
    input_testvector_files = b2b_utils.get_testvector_files(
        this_tp, testvector_dir, "input"
    )
    output_testvector_files = b2b_utils.get_testvector_files(
        this_tp, testvector_dir, "output"
    )

    ##
    ## initialize B2B block wrapper
    ##
    b2b = wrapper.B2BWrapper(clock=dut.clock, name="B2BWrapper")
    for i, io in enumerate(b2b_utils.B2BIO.Inputs):
        port_num = io.value
        driver = FifoDriver(
            dut.input_spybuffers[port_num].spybuffer,
            dut.clock,
            "B2B",
            io,
            write_out=True,
        )
        b2b.add_input_driver(driver, io)

    for i, io in enumerate(b2b_utils.B2BIO.Outputs):
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
            "ERROR Event sending timed out! Number of expected inputs with events = {}".format(
                len(send_finished_signal)
            )
        )
    yield Combine(*send_finished_signal)
    dut._log.info("Sending finished!")

    timer = Timer(20, "us")
    dut._log.info("Going to wait 20 microseconds")
    yield timer

    ##
    ## dump monitors
    ##
    expected_output_events = []
    for port_num, testvec in enumerate(output_testvector_files):
        out_events = events.load_events_from_file(
            testvec, n_to_load=num_events_to_process
        )
        expected_output_events.append(out_events)

    all_tests_passed = True
    all_test_results = []
    for oport in b2b.output_ports:
        monitor, io, _ = oport
        words = monitor.observed_words
        recvd_events = events.load_events(words, "little")
        cocotb.log.info(
            "Output for {} (output port num {}) received {} events".format(
                io.name, io.value, len(recvd_events)
            )
        )

        ##
        ## we expect nothing from the current board but there may be testvectors,
        ## so "zero" out any testvectors for this output
        ##
        if io.value == this_tp.value:
            expected_output_events[io.value] = []

        ## test
        events_equal, test_results = tb_diff.events_are_equal(
            recvd_events, expected_output_events[io.value], verbose=False
        )
        result_summary = result_handler.result_summary_dict(
            "B2B_Output_{:02}".format(io.value),
            str(output_testvector_files[io.value]),
            test_name="TEST_B2B_SRC{:02}_DEST{:02}".format(this_tp.value, io.value),
            test_results=test_results,
        )
        all_tests_passed = (
            all_tests_passed and result_summary["test_results"]["test_success"]
        )
        all_test_results.append(result_summary)

        output_json_name = "test_results_summary_B2B_src{}_dest{}.json".format(
            "{}{:02}".format(
                this_tp.name.split("_")[0], int(this_tp.name.split("_")[1])
            ),
            "{}{:02}".format(io.name.split("_")[0], int(io.name.split("_")[1])),
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
