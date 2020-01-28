# Python controller for empty dataflow block.
# Practically speaking, this is just another driver and monitor,
# but the monitor sits on the "input" spy buffer and the driver on
# the "output". The user can override, or can rpovide

import cocotb
from cocotb import triggers, result

from . import driver, monitor

class EmptyBlock(object):

    def __init__(self, dut, input_fifo, output_fifo, clock, callback=None, event_callback=None):
        self.input_fifo = input_fifo
        self.output_fifo = output_fifo
        self.clock = clock
        self.dut = dut

        # Construct new input/output FIFO monitor/drivers.
        self.input_fifo_monitor = monitor.FifoMonitor(input_fifo, clock)
        self.output_fifo_driver = driver.FifoDriver(output_fifo, clock)

        # Callback that runs every time a word is seen.
        # Use a user-specified one if provided.
        if callback is None:
            self.input_fifo_monitor.add_callback(self.copy_input_to_output)
        else:
            self.input_fifo_monitor.add_callback(callback)

        # Callback that runs every time an _event_ is seen.
        # Use a user-specified one if provided.
        if event_callback is None:
            self.input_fifo_monitor.add_event_callback(self.check_complete_event)
        else:
            self.input_fifo_monitor.add_event_callback(callback)

    def kill(self):
        """ Stop both forked coroutines."""
        self.input_fifo_monitor.kill()
        self.output_fifo_driver.kill()

    def copy_input_to_output(self, transaction):
        """ Copies an input word from the monitor to the driver."""

        # NOTE: we could parse the word into a events.DataWord object
        # using the following:
        # is_metadata = transaction[0]
        # contents = transaction[1:]
        # word = event.DataWord(is_metadata, contents)

        # We could also wait for the entire event to be processed by
        # overriding or adding a callback to monitor.process_event(),
        # which is called when the monitor finishes examining a complete
        # event. This is only an example of how Python can control the
        # "empty" block between the spy buffers.
        self.dut._log.debug("Empty block received word, " + str(transaction))
        self.output_fifo_driver.append(transaction)

    def check_complete_event(self, event):
        """ Example callback that runs when we have a complete event."""

        # NOTE: this could be used to implement sophisticated dataflow.

        self.dut._log.info("Empty block received complete event, L0 ID " + hex(event.l0id)[:-1])
