import sys
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Combine, Timer
from cocotb.result import TestFailure, TestSuccess

from tp_tb.testbench.example_sw_block import sw_switcher_utils

# import tp_tb.testbench.b2b.b2b_wrapper as wrapper
import tp_tb.testbench.example_sw_block.sw_switcher_wrapper as wrapper
import tp_tb.testbench.example_sw_block.sw_switcher_block as sw_switcher_block

from tp_tb.utils import test_config
from tp_tb.utils import events, tb_diff, result_handler
from tp_tb.utils.fifo_wrapper import FifoDriver, FifoMonitor

##
## CONSTANTS
##
TEST_CONFIG_ENV = "COCOTB_TEST_CONFIG_FILE"


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
    n_inputs_ok = len(input_fifos) == len(sw_switcher_utils.SWSwitcherIO.Inputs)

    output_fifos = [x.spybuffer for x in dut.output_spybuffers]
    n_outputs_ok = len(output_fifos) == len(sw_switcher_utils.SWSwitcherIO.Outputs)

    n_io_ports_ok = n_inputs_ok and n_outputs_ok
    if not n_io_ports_ok:
        raise Exception(
            f"ERROR # of SWSwitcher io ports differ between CocoTB and RTL simulation:\n -> CocoTB expects (IN,OUT)=({len(sw_switcher_utils.SWSwitcherIO.Inputs)},{len(sw_switcher_utils.SWSwitcherIO.Outputs)})\n -> RTL expects (IN,OUT)=({len(input_fifos)},{len(output_fifos)})"
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
    ## process input arguments for this test
    ##
    input_args = test_config.input_args_from_config(os.environ.get(TEST_CONFIG_ENV, ""))
    num_events_to_process = int(input_args["n_events"])
    # event_delay = int(input_args["event_delay"])

    ##
    ## create the software DUT
    ##
    switcher_block = sw_switcher_block.SWSwitcherBlock(dut.clock, "SWSwitcherBlock")
    for i, io in enumerate(sw_switcher_utils.SWSwitcherIO.Inputs):
        switcher_block.add_fifo(
            dut.input_spybuffers[i].spybuffer,
            dut.clock,
            f"{switcher_block.name}_Input_{i}",
            io,
            direction="in",
        )
    for i, io in enumerate(sw_switcher_utils.SWSwitcherIO.Outputs):
        switcher_block.add_fifo(
            dut.output_spybuffers[i].spybuffer,
            dut.clock,
            f"{switcher_block.name}_Output_{i}",
            io,
            direction="out",
        )

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
    initialize_test_state(dut)

    ##
    ## reset the testbench
    ##
    dut._log.info("Resetting DUT")
    yield reset(dut)

    ##
    ## get the testvectors
    ##
    testvector_dir = "/home/dantrim/work/tdaq-htt-firmware/testvecs/20200410/"
    input_testvector_files = sw_switcher_utils.get_testvector_files(
        testvector_dir, "input"
    )
    # output_testvector_files = sw_switcher_utils.get_testvector_files(
    #    testvector_dir, "output"
    # )[::-1]

    ##
    ## initialize the (software-based) block wrapper
    ##
    swblock_wrapper = wrapper.SWSwitcherWrapper(dut.clock, name="SWSwitcherWrapper")
    for i, io in enumerate(sw_switcher_utils.SWSwitcherIO.Inputs):
        port_num = io.value
        driver = FifoDriver(
            dut.input_spybuffers[port_num].spybuffer,
            dut.clock,
            "SWSwitcher",
            io,
            write_out=True,
        )
        swblock_wrapper.add_input_driver(driver, io)

    for i, io in enumerate(sw_switcher_utils.SWSwitcherIO.Outputs):
        monitor = FifoMonitor(
            dut.output_spybuffers[i].spybuffer,
            dut.clock,
            "SWSwitcher",
            io,
            write_out=True,
        )
        swblock_wrapper.add_output_monitor(monitor, io, active=True)
    swblock_wrapper.sort_ports()

    ##
    ## send input events
    ##
    dut._log.info("Sending input events")
    send_finished_signal = swblock_wrapper.send_input_events(
        input_testvector_files, n_to_send=num_events_to_process
    )
    if not send_finished_signal:
        raise cocotb.result.TestFailure("ERROR Event sending timed out!")
    yield Combine(*send_finished_signal)
    dut._log.info("Sending finished!")

    timer = Timer(20, "us")
    dut._log.info("Going to wait 20 microseconds")
    yield timer
