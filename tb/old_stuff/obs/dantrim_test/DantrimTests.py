# Import cocotb.
import cocotb
from cocotb import triggers, result, clock

# Import our own packages.
from tptest import dataflow
from tptest import driver, monitor, events, util

from collections import deque

# Default clock speed. (ns)
clock_speed = 50

def initialize_wires(dut):
    """ Initializes top-level signals to zero in the wrapper.
        By setting things to zero explicitly, stops high z states."""
    #wires = [dut.input_we, dut.input_re, dut.output_we, dut.output_re, dut.input_data, dut.output_data]
    wires = [dut.buffer_write_enable, dut.buffer_read_enable, dut.input_data, dut.output_data]
    for wire in wires:
        wire <= 0

@cocotb.coroutine
def reset(dut):
    """ Reset the blocks on start."""
    dut.reset <= 1
    yield triggers.ClockCycles(dut.clock, 1)
    dut.reset <= 0
    yield triggers.ClockCycles(dut.clock, 1)
    dut.reset <= 1

class SpyBufferStatus() :
    """
    Object representing the SpyBuffer fifo status
    """

    def __init__(self, spy_buffer) :
        self._spy_buffer = spy_buffer

    @cocotb.coroutine
    def update(self) :
        yield triggers.ReadOnly()
        self.write_enable = (self._spy_buffer.write_enable == 1)
        self.read_enable = (self._spy_buffer.read_enable == 1)
        self.almost_full = (self._spy_buffer.almost_full == 1)
        self.empty = (self._spy_buffer.empty == 1)

@cocotb.coroutine
def wait_50ns() :
    cocotb.log.info("About to wait 50 ns")
    yield triggers.Timer(50, units = "ns")
    cocotb.log.info("Simulation time has advanced by 50 ns")

@cocotb.coroutine
def wait_cycles(clock) :
    cocotb.log.info("About to wait 2 clock cycles")
    yield triggers.ClockCycles(signal = clock, num_cycles = 2, rising = True)
    cocotb.log.info("Simulation time has advanced by 2 clock cycles")

        
@cocotb.test()
def test_000_timestep(dut) :

    simulation_clock = clock.Clock(dut.clock, clock_speed, "ns")
    cocotb.fork(simulation_clock.start())
    #dut.buffer_write_enable <= 0
    #yield triggers.Timer(100, units = "ns")
    #yield wait_50ns()
    yield wait_cycles(dut.clock)
    for i in range(10) :
        val = (i %2 == 0)
        #if i < 5: val = 0
        #else :
        #    val = 1
        dut._log.info("New val: {}".format(val))
        dut.buffer_write_enable <= val
        yield triggers.NextTimeStep()

#@cocotb.test()
#def test_001_initialization(dut) :
#
#    import random
#
#    """
#    Initial test to build up familiarity with things
#    """
#
#    @cocotb.coroutine
#    def process_event(event_data, read_write, status) :
#        success = True
#        if read_write : # read
#            yield triggers.RisingEdge(dut.clock)
#            if status.empty :
#                success = False
#            else :
#                event_data = int(dut.output_data)
#            dut.buffer_read_enable <= 1
#            yield triggers.RisingEdge(dut.clock)
#            dut.buffer_read_enable <= 0
#        else : # write
#
#            yield triggers.RisingEdge(dut.clock)
#            dut.buffer_write_enable <= 0
#            while status.almost_full != 0 :
#                yield triggers.RisingEdge(dut.clock)
#
#            #yield triggers.RisingEdge(dut.clock)
#            dut.input_data <= event_data
#            dut.buffer_write_enable <= 1
#            yield triggers.RisingEdge(dut.clock)
#            dut.buffer_write_enable <= 0
#            if status.almost_full :
#                success = False
#        return event_data, success
#    
#
#
#    # Setup the clock to drive the DUT
#    simulation_clock = clock.Clock(dut.clock, clock_speed, "ns")
#    cocotb.fork(simulation_clock.start())
#    status = SpyBufferStatus(dut.spybuffer)
#
#    fifo_model = deque()
#
#    # reset the dut
#    initialize_wires(dut)
#    yield reset(dut)
#
#    filename = "../input_files/BoardToBoardInput_AMTP0_Strip0.evt"
#    input_events = events.read_events_from_file(filename)
#
#    for ievent, input_event in enumerate(input_events) :
#        sep = 45 * "="
#        dut._log.info(sep)
#
#        if ievent > 1 :
#            break
#
#        words = list(input_event)
#        for iword, word in enumerate(words[:-1]) :
#            sep = 22 * "- "
#            dut._log.info(sep)
#
#            data = word.get_binary()
#            for read_write in [False, True] :
#                yield status.update()
#                data, success = yield process_event(data, read_write, status)
#        
#                if read_write : # read
#                    if success and len(fifo_model)!=0 : #status.empty :
#                        fifo_current = fifo_model.pop() 
#                        dut._log.info(" -> POPPED  : %X", fifo_current)
#                    else :
#                        dut._log.info("{} Data not read from fifo, fifo EMPTY".format(iword))
#                else : # write
#                    if success :
#                        dut._log.info(" -> WRITTEN : %X", data)
#                        fifo_model.appendleft(data)
#                    else :
#                        dut._log.info("Data not written to fifo, fifo (ALMOST) FULL")
#        

    ## Not sure we need this
    #initialize_wires(dut)
    #yield reset(dut)
    #dut._log.info("Initialized wires and reset DUT")

    ## dataflow object to hold all spybuffer instances
    #flow = dataflow.DataflowController(dut, dut.clock)
    #flow.add_buffer("SpyBuffer", dut.spybuffer)

    #flow.start()
    #filename = "../input_files/BoardToBoardInput_AMTP0_Strip0.evt"
    #hook = flow.send_events_from_file_dantrim(filename, "SpyBuffer")
    #dut._log.info("HELLO WORLD")
    #if hook is None :
    #    raise result.TestFailure("ERROR: Failed to load events from input file: {}".format(filename))
    #yield hook.wait()

    ##yield flow
    #flow.stop_dantrim()

    

#@cocotb.test()
#def test_001_initial_dataflow(dut):
#    """ Initial test of dataflow driver and monitor."""
#    # Default: one 200ns clock for now. Could be changed!
#    # This can be moved to a testbench class later.
#    sim_clock = clock.Clock(dut.clock, clock_speed, 'ns')
#    cocotb.fork(sim_clock.start())
#
#    # Reset everything?
#    initialize_wires(dut)
#    yield reset(dut)
#
#    dut._log.info("Initialized and reset TP skeleton.")
#
#    # Initialize a data flow object.
#    flow = dataflow.DataflowController(dut, dut.clock)
#
#    # Add a driver to the input; let's call it "Input".
#    flow.add_input_fifo("Input", dut.input_buffer)
#
#    # Add a driver to the output; let's call it "Output".
#    # Add a binary log file, so events read from the output buffer get saved.
#    flow.add_output_fifo("Output", dut.output_buffer, "test_001_output_buffer.evt")
#
#    # Add an empty block that sits between input and output.
#    # By default the empty block just copies input -> output.
#    # But you can add callback functions to mutate and/or delay the data.
#    flow.add_empty_block("EmptyBlock", dut.input_buffer, dut.output_buffer)
#
#    # Start the dataflow checker.
#    # Right now, this only checks that start/end of event words
#    # are in the right place.
#    flow.start()
#
#    # Let's generate some random fake events.
#    # Yield on the return, which blocks until all the events are sent.
#    # We could load a file here instead!
#    hook = flow.send_random_events("Input", 10)
#    yield hook.wait()
#
#    # Now that we've finished sending data. Wait until all the monitors are finished.
#    yield flow.check_outstanding(timeout=10000, units='ns')
#
#    # We probably _do_ want to explicitly call the stop() function here
#    # since it enables us to have a place to close output files.
#    flow.stop()
#
#@cocotb.test()
#def test_002_dataflow_from_file(dut):
#    """ Version of test 1, but with events coming from an input file."""
#    # Start a clock and reset.
#    sim_clock = clock.Clock(dut.clock, clock_speed, 'ns')
#    cocotb.fork(sim_clock.start())
#    initialize_wires(dut)
#    yield reset(dut)
#
#    dut._log.info("Initialized and reset TP skeleton.")
#
#    # Initialize a data flow object, with a driver and monitor.
#    flow = dataflow.DataflowController(dut, dut.clock)
#    flow.add_input_fifo("Input", dut.input_buffer)
#    # NOTE: it might be nice to automatically name these (or have an option to do so).
#    flow.add_output_fifo("Output", dut.output_buffer, "test_002_output_buffer.evt")
#
#    # Add empty block; start dataflow.
#    flow.add_empty_block("EmptyBlock", dut.input_buffer, dut.output_buffer)
#    flow.start()
#
#    # Load one of Elliot's binary files.
#    # The file to load could be passed in via configuration, environment variables,
#    # or some other way (a test could be written that loads all files in a directory!)
#    # NOTE: careful with relative paths! Questa runs from inside the "sim_build" directory,
#    # NOT inside the directory with the makefile.
#    filename = "../input_files/BoardToBoardInput_AMTP0_Strip0.evt"
#    hook = flow.send_events_from_file(filename, "Input")
#    if hook is None:
#        raise result.TestFailure("Error: failed to load events from input file: " + filename)
#    yield hook.wait()
#
#    # Now that we've finished sending data. Wait until all the monitors are finished.
#    yield flow.check_outstanding(timeout=10000, units='ns')
#
#    # We probably _do_ want to explicitly call the stop() function here
#    # since it enables us to have a place to close output files.
#    flow.stop()
#
## TODO: write version of this test which also freezes a spy buffer
## and dumps the contents. Require porting over spy buffer protocol
## to a new class from the old testbench.