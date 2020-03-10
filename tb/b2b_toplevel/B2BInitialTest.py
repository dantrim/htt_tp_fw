import sys
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Combine
from cocotb.decorators import coroutine
from cocotb.result import TestFailure, TestSuccess
from tptest import events, util

from b2b_test.blocks.b2b_input_driver import B2BInputDriver
from b2b_test.blocks import b2b_utils

##
## CONSTANTS
##
CLOCK_SPEED = 200 # ns

def initialize_wires(dut) :

    #inputs
    in_buffers = dut.input_cluster_SpyBuffer

    #outputs
    out_buffers = dut.output_cluster_SpyBuffer

    n_in_ok = len(in_buffers) == len(b2b_utils.B2BIO.B2BInputs)
    n_out_ok = len(out_buffers) == len(b2b_utils.B2BIO.B2BOutputs)
    io_ok = n_in_ok and n_out_ok
    if not io_ok :
        raise Exception("ERROR # of B2B inputs or outputs between CocoTB and RTL simulation \
                do not match:\n\t -> CocoTB expects (IN,OUT)=({},{})\n\t -> RTL expects    \
                (IN,OUT)=({},{})".format( len(b2b_utils.B2BIO.B2BInputs)
                                            ,len(b2b_utils.B2BIO.B2BOutputs)
                                            ,len(in_buffers), len(out_buffers)))

    # initialize the input spybuffer fifos
    for ibuff, buff in enumerate(in_buffers) :
        dut.cluster_wren[ibuff] <= 0
        dut.cluster_rd_req[ibuff] <= 0
        dut.input_data[ibuff] <= 0
        dut.cluster_data[ibuff] <= 0

    # initialize the output spybuffer fifos
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
    yield reset(dut)
    dut._log.info("Resetting DUT")

    testvecdir = b2b_utils.testvec_dir_from_env()
    dut._log.info("Using testvec directory: {}".format(testvecdir))

    input_driver = B2BInputDriver(dut, b2b_utils.B2BIO.B2BOutputs.AMTP_0)
    signal_events_sent = input_driver.send_events_from_testvecs(testvecdir, num_events_to_send = 10)
    dut._log.info("Going to wait for signal_events_sent")
    yield Combine(*signal_events_sent)
    dut._log.info("signal_events_sent is over!")
    dut._log.info("Going to wait for events")
    yield input_driver.wait_for_events(timeout = 10000, units = "ns")
    dut._log.info("Done waiting for events!")

    in_word_counts, out_word_counts = input_driver.word_count()
    for i, in_word in enumerate(in_word_counts) :
        cocotb.log.info("INPUT {} : (IN, OUT) = ({}, {}) - {}".format(i, in_word, out_word_counts[i], in_word == out_word_counts[i]))
    

