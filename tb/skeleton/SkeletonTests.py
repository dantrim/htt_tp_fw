# Example skeleton/dataflow tests for the TP.
# Ben Rosser <bjr@sas.upenn.edu>

# Import cocotb.
import cocotb
from cocotb import triggers, result, clock

# Import our own packages.
from tptest import dataflow

# Default clock speed. (ns)
clock_speed = 200

def initialize_wires(dut):
    """ Initializes top-level signals to zero in the wrapper.
        By setting things to zero explicitly, stops high z states."""
    wires = [dut.input_we, dut.input_re, dut.output_we, dut.output_re, dut.input_data, dut.output_data_in]
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

@cocotb.test()
def test_001_initial_dataflow(dut):
    """ Initial test of dataflow driver and monitor."""
    # Default: one 200ns clock for now. Could be changed!
    # This can be moved to a testbench class later.
    sim_clock = clock.Clock(dut.clock, clock_speed, 'ns')
    cocotb.fork(sim_clock.start())

    # Reset everything?
    initialize_wires(dut)
    yield reset(dut)

    dut._log.info("Initialized and reset TP skeleton.")

    # Initialize a data flow object.
    flow = dataflow.DataflowController(dut, dut.clock)

    # Add a driver to the input; let's call it "Input".
    flow.add_input_fifo("Input", dut.input_buffer)

    # Add a driver to the output; let's call it "Output".
    # Add a binary log file, so events read from the output buffer get saved.
    flow.add_output_fifo("Output", dut.output_buffer, "test_001_output_buffer.evt")

    # Add an empty block that sits between input and output.
    # By default the empty block just copies input -> output.
    # But you can add callback functions to mutate and/or delay the data.
    flow.add_empty_block("EmptyBlock", dut.input_buffer, dut.output_buffer)

    # Start the dataflow checker.
    # Right now, this only checks that start/end of event words
    # are in the right place.
    flow.start()

    # Let's generate some random fake events.
    # Yield on the return, which blocks until all the events are sent.
    # We could load a file here instead!
    hook = flow.send_random_events("Input", 10)
    yield hook.wait()

    # Now that we've finished sending data. Wait until all the monitors are finished.
    yield flow.check_outstanding(timeout=10000, units='ns')

    # We probably _do_ want to explicitly call the stop() function here
    # since it enables us to have a place to close output files.
    flow.stop()

@cocotb.test()
def test_002_dataflow_from_file(dut):
    """ Version of test 1, but with events coming from an input file."""
    # Start a clock and reset.
    sim_clock = clock.Clock(dut.clock, clock_speed, 'ns')
    cocotb.fork(sim_clock.start())
    initialize_wires(dut)
    yield reset(dut)

    dut._log.info("Initialized and reset TP skeleton.")

    # Initialize a data flow object, with a driver and monitor.
    flow = dataflow.DataflowController(dut, dut.clock)
    flow.add_input_fifo("Input", dut.input_buffer)
    # NOTE: it might be nice to automatically name these (or have an option to do so).
    flow.add_output_fifo("Output", dut.output_buffer, "test_002_output_buffer.evt")

    # Add empty block; start dataflow.
    flow.add_empty_block("EmptyBlock", dut.input_buffer, dut.output_buffer)
    flow.start()

    # Load one of Elliot's binary files.
    # The file to load could be passed in via configuration, environment variables,
    # or some other way (a test could be written that loads all files in a directory!)
    # NOTE: careful with relative paths! Questa runs from inside the "sim_build" directory,
    # NOT inside the directory with the makefile.
    filename = "../input_files/BoardToBoardInput_AMTP0_Strip0.evt"
    hook = flow.send_events_from_file(filename, "Input")
    if hook is None:
        raise result.TestFailure("Error: failed to load events from input file: " + filename)
    yield hook.wait()

    # Now that we've finished sending data. Wait until all the monitors are finished.
    yield flow.check_outstanding(timeout=10000, units='ns')

    # We probably _do_ want to explicitly call the stop() function here
    # since it enables us to have a place to close output files.
    flow.stop()

# TODO: write version of this test which also freezes a spy buffer
# and dumps the contents. Require porting over spy buffer protocol
# to a new class from the old testbench.
