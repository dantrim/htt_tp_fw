import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb.decorators import coroutine
from cocotb.result import TestFailure, TestSuccess
from tptest import events, util

##
## CONSTANTS
##
CLOCK_SPEED = 200 # ns

def initialize_wires(dut) :
    wires = [dut.buffer_write_enable, dut.buffer_read_enable, dut.input_data, dut.output_data]
    for wire in wires :
        wire <= 0

    #inputs
    in_buffers = dut.input_cluster_SpyBuffer
    for ibuff, buff in enumerate(in_buffers) :
        dut.cluster_wren[ibuff] <= 0
        dut.cluster_rd_req[ibuff] <= 0
        dut.input_data[ibuff] <= 0
        dut.cluster_data[ibuff] <= 0

    #outputs
    out_buffers = dut.output_cluster_SpyBuffer
    for ibuff, buff in enumerate(out_buffers) :
        dut.board_wren[ibuff] <= 0
        dut.board_ren[ibuff] <= 0
        dut.board_cluster_data[ibuff] <= 0
        dut.output_data[ibuff] <= 0
        

@cocotb.coroutine
def reset(dut) :
    dut.reset <= 1
    yield ClockCycles(dut.clock, 1)
    dut.reset <= 0
    yield ClockCycles(dut.clock, 1)
    dut.reset <= 1

@cocotb.test()
def initial_b2b_test(dut) :

    sim_clock = Clock(dut.clock, CLOCK_SPEED)
    cocotb.fork(sim_clock.start())

    initialize_wires(dut)
