import sys, os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Combine, Timer
from cocotb.result import TestFailure, TestSuccess


from tb_b2b import b2b_utils


##
## TEST CONSTANTS
##
CLOCK_SPEED = 5 # ns

def initialize_spybuffers(fifos = []) :

    for ififo, fifo in enumerate(fifos) :
        fifo.read_enable <= 0
        fifo.write_enable <= 0
        fifo.empty <= 1
        fifo.almost_full <= 0
        fifo.read_data <= 0
        fifo.write_data <= 0

def initialize_test_state(dut) :

    ##
    ## initialize the FIFOs
    ##

    input_fifos = [x.spybuffer for x in dut.input_spybuffers]
    n_inputs_ok = len(input_fifos) == len(b2b_utils.B2BIO.Inputs)

    output_fifos = [x.spybuffer for x in dut.output_spybuffers]
    n_outputs_ok = len(output_fifos) == len(b2b_utils.B2BIO.Outputs)
    n_io_ports_ok = n_inputs_ok and n_outputs_ok
    if not n_io_ports_ok :
        raise Exception("ERROR # of B2B io ports differ between CocoTB and RTL simulation: \
                CocoTB expects (IN,OUT)=({},{})\n\t -> RTL expects (IN,OUT)=({},{})".
                format( len(b2b_utils.B2BIO.Inputs), len(b2b_utils.B2BIO.Outputs),
                        len(input_fifos), len(output_fifos)))

    initialize_spybuffers(fifos = input_fifos)
    initialize_spybuffers(fifos = output_fifos)

    #initialize_b2b(dut)

#    #inputs
#    in_buffers = [x.input_buffer for x in dut.input_cluster_SpyBuffer]
#
#    #outputs
#    out_buffers = [x.output_buffer for x in dut.output_cluster_SpyBuffer]
#
#    n_in_ok = len(in_buffers) == len(b2b_utils.B2BIO.Inputs)
#    n_out_ok = len(out_buffers) == len(b2b_utils.B2BIO.Outputs)
#    io_ok = n_in_ok and n_out_ok
#    if not io_ok :
#        raise Exception("ERROR # of B2B inputs or outputs between CocoTB and RTL simulation \
#                do not match:\n\t -> CocoTB expects (IN,OUT)=({},{})\n\t -> RTL expects    \
#                (IN,OUT)=({},{})".format( len(b2b_utils.B2BIO.Inputs)
#                                            ,len(b2b_utils.B2BIO.Outputs)
#                                            ,len(in_buffers), len(out_buffers)))
#
#    # initialize the input spybuffer fifos
#    for ibuff, buff in enumerate(in_buffers) :
#
#        #kludgedut.cluster_data_reg[ibuff] <= 0
#        #dut.cluster_data[ibuff] <= 0
#        dut.cluster_wren[ibuff] <= 0
#        dut.cluster_rd_req[ibuff] <= 0
#        dut.cluster_empty[ibuff] <= 1
#        dut.cluster_almost_full[ibuff] <= 0
#        dut.input_data[ibuff] <= 0
#        dut.cluster_data[ibuff] <= 0
#        buff.write_data <= 0
#
#
#    # initialize the output spybuffer fifos
#    for ibuff, buff in enumerate(out_buffers) :
#        dut.board_wren[ibuff] <= 0
#        dut.board_ren[ibuff] <= 0
#        dut.board_empty[ibuff] <= 1
#        dut.board_cluster_data[ibuff] <= 0
#        dut.board_almost_full[ibuff] <= 0
#        dut.output_data[ibuff] <= 0
#

@cocotb.coroutine
def reset(dut) :

    """
    Resets the B2B testbench, having reset active LOW.
    """

    dut.reset_n <= 1
    yield ClockCycles(dut.clock, 20)
    dut.reset_n <= 0
    yield ClockCycles(dut.clock, 20)
    dut.reset_n <= 1

##
## TEST0
##
@cocotb.test()
def b2b_test_0(dut) :

    this_tp = b2b_utils.B2BIO.Outputs.AMTP_0 # hardcode for now, later take BOARD_ID from env and set the B2B inst to this value

    ##
    ## clock
    ##
    sim_clock = Clock(dut.clock, CLOCK_SPEED, "ns")
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

    




