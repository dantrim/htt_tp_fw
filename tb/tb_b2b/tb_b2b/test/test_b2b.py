import sys, os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Combine, Timer
from cocotb.result import TestFailure, TestSuccess


from tb_b2b import b2b_utils
import tb_b2b.b2b_wrapper as wrapper
#from tb_b2b import fifo_wrapper
#from tb_utils import fifo_wrapper
from tb_utils.fifo_wrapper import FifoDriver, FifoMonitor
#from tb_b2b.fifo_wrapper import B2BFifoDriver, B2BFifoMonitor

from event_parse import event_table
from event_parse import decoder

from tb_utils import events


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
    yield ClockCycles(dut.clock, 10)
    dut.reset_n <= 0
    yield ClockCycles(dut.clock, 10)
    dut.reset_n <= 1

##
## TEST0
##
@cocotb.test()
def b2b_test_0(dut) :

    this_tp = b2b_utils.B2BIO.Outputs.AMTP_0 # hardcode for now, later take BOARD_ID from env and set the B2B inst to this value
    board_id = int(dut.board2board_switching_inst.BOARD_ID)
    dut._log.info("Instantiating B2B block with BOARD_ID = {}".format(board_id))
    this_tp = None
    for io in b2b_utils.B2BIO.Outputs :
        if int(io.value) == board_id :
            this_tp = io
            break
    if not this_tp :
        raise ValueError("Unable to find associated IO for B2B BOARD_ID={}".format(board_id))
    dut._log.info("Setting test IO with base (port_name, port_num) = ({}, {})".format(this_tp.name, this_tp.value))

    num_events_to_process = 50
    l0id_request = -1
    event_delays = True

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
    input_testvector_files = b2b_utils.get_testvector_files(this_tp, testvector_dir, "input")
    output_testvector_files = b2b_utils.get_testvector_files(this_tp, testvector_dir, "output")

    ##
    ## initialize B2B block wrapper
    ##
    b2b = wrapper.B2BWrapper(clock = dut.clock, name = "B2BWrapper")
    for i, io in enumerate(b2b_utils.B2BIO.Inputs) :
        port_num = io.value
        port_name = b2b_utils.B2BIO.simplename(io)
        driver = FifoDriver(dut.input_spybuffers[port_num].spybuffer, dut.clock, "B2B", io, write_out = True)
        b2b.add_input_driver(driver, io)

    for i, io in enumerate(b2b_utils.B2BIO.Outputs) :
        port_num = io.value
        port_name = b2b_utils.B2BIO.simplename(io)
        active = (this_tp.value != io.value)
        monitor = FifoMonitor(dut.output_spybuffers[i].spybuffer, dut.clock, "B2B", io, callbacks = [], write_out = True)
        b2b.add_output_monitor(monitor, io, active = active)
    b2b.sort_ports()

    ##
    ## send events
    ##
    dut._log.info("Sending input events")
    send_finished_signal = b2b.send_input_events(input_testvector_files, num_events_to_process, l0id_request, event_delays)
    if not send_finished_signal :
        raise cocotb.result.TestFailure("ERROR Event sending timed out! Number of expected inputs with events = {}".format(len(send_finished_signal)))
    yield Combine(*send_finished_signal)
    dut._log.info("Sending finished!")

    timer = Timer(int(num_events_to_process * 1.0 / 2), "us")
    dut._log.info("Going to wait 20 microseconds")
    yield timer

    ##
    ## dump monitors
    ##
    expected_output_events = []
    for port_num, testvec in enumerate(output_testvector_files) :
        out_events = events.load_events_from_file(testvec, n_to_load = num_events_to_process, l0id_request = l0id_request)
        expected_output_events.append(out_events)
        
    for oport in b2b.output_ports :
        monitor, io, _ = oport
        words = monitor.observed_words
        recvd_events = events.load_events(words, "little") 
        cocotb.log.info("Output for {} (output port num {}) received {} events".format(io.name, io.value, len(recvd_events)))
        
    test_passed = b2b.compare_outputs_with_expected(expected_output_events = expected_output_events)
    cocotb_result = { True : cocotb.result.TestSuccess, False : cocotb.result.TestFailure }[test_passed]

    print(b2b)
    raise cocotb_result
