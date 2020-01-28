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
def test_initial_dataflow(dut):
    """ Initial test of dataflow driver and monitor."""
    # Default: 25ns clock for now. Change later!
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
    flow.add_output_fifo("Output", dut.output_buffer)

    # Add an empty block that sits between input and output.
    # By default the empty block just copies input -> output.
    # But you can add callback functions to mutate and/or delay the data.
    flow.add_empty_block("Input", "Output")

    # Start the dataflow checker.
    # Right now, this only checks that start/end of event words
    # are in the right place.
    flow.start()

    # TODO: add a way to configure where the output events go.

    # Let's generate some random fake events.
    # Yield on the return, which blocks until all the events are sent.
    # We could load a file here instead!
    hook = flow.send_random_events("Input", 10)

    yield hook.wait()

    # Hmm... we don't actually have a way to wait for the receipt
    # of all pending events yet. Just wait for some time.
    yield triggers.Timer(1, "us")

# TODO: write a version of the above test, but it loads events
# from a file instead.

# TODO: write version of this test which also freezes a spy buffer
# and dumps the contents. Require porting over spy buffer protocol
# to a new class from the old testbench.
