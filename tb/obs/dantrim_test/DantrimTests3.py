import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb.decorators import coroutine
from cocotb.result import TestFailure, TestSuccess

from fifo_wrapper import FifoWrapper

CLOCK_SPEED = 200 # ns

def initialize_wires(dut) :

    ##
    ## zero some signals
    ##
    wires = [dut.buffer_write_enable, dut.buffer_read_enable, dut.input_data, dut.output_data]
    for wire in wires :
        wire <= 0

@cocotb.coroutine
def reset(dut) :

    ##
    ## reset is active LOW
    ##

    dut.reset <= 1
    yield ClockCycles(dut.clock, 1)
    dut.reset <= 0
    yield ClockCycles(dut.clock, 1)
    dut.reset <= 1

@cocotb.test()
def test_fifo(dut) :

    sim_clock = Clock(dut.clock, CLOCK_SPEED)
    cocotb.fork(sim_clock.start())

    initialize_wires(dut)
    yield reset(dut)

    fifo_wrapper = FifoWrapper(fifo = dut.spybuffer, clock = dut.clock, name = "SpyBufferFifo")
    input_event_file = "../input_files/BoardToBoardInput_AMTP0_Strip0.evt"
    events_sent = fifo_wrapper.send_data_from_file(filename = input_event_file, build_events = False, num_events = -1)
    yield events_sent.wait()
    yield fifo_wrapper.wait_for_events(timeout = 10000, units = "ns")

    ok = fifo_wrapper.compare_with_expected()
    if not ok :
        raise TestFailure
    else :
        raise TestSuccess