import cocotb
from cocotb import triggers, result

from . import block, driver, monitor, events, util

class DataflowController(object):

    def __init__(self, dut, clock):
        self.dut = dut
        self.clock = clock

        self.input_fifos = {}
        self.output_fifos = {}

        # We should maybe give these names?
        self.empty_blocks = {}

        self.on_error_coroutine = None

    # TODO: guards should be added here to check that the paths are _actually_ FIFOs.

    def add_input_fifo(self, name, path):
        """ Add an input FIFO driver. Returns reference to the object."""
        if name not in self.input_fifos:
            # Create the FIFO driver object; it starts automatically.
            self.input_fifos[name] = driver.FifoDriver(path, self.clock)
        return self.input_fifos[name]

    def add_output_fifo(self, name, path, output_file=None):
        """ Add an output FIFO monitor. Returns reference to the object."""
        if name not in self.output_fifos:
            # Create the FIFO monitor object; it also starts automatically.
            self.output_fifos[name] = monitor.FifoMonitor(path, self.clock, output_file)
        return self.output_fifos[name]


    def add_empty_block(self, name, input_path, output_path, callback=None, event_callback=None):
        """ Creates an "empty block"-- another monitor/driver pair to create fake data flow."""

        # Create the empty block if it doesn't already exist.
        # This allows empty blocks to be created between _any_ two spy buffers.
        if name not in self.empty_blocks:
            empty_block = block.EmptyBlock(self.dut, input_path, output_path, self.clock, callback, event_callback)
            self.empty_blocks[name] = empty_block

        return self.empty_blocks[name]

    def stop(self):
        """ Stop all coroutines. Not sure this is necessary."""
        for name, driver in self.input_fifos.items():
            driver.kill()

        for name, monitor in self.output_fifos.items():
            monitor.kill()

            # Closes connected output file (if one was configured).
            if monitor.output_file != None:
                monitor.output_file.close()

        for name, empty_block in self.empty_blocks.items():
            empty_block.kill()

        # Kill the coroutine waiting for errors.
        if self.on_error_coroutine is not None:
            self.on_error_coroutine.kill()
            self.on_error_coroutine = None

    def start(self):
        """ Start any coroutines not automatically started."""

        # Start the coroutine which waits for errors.
        if not self.on_error_coroutine is None:
            self.on_error_coroutine = cocotb.fork(self.wait_for_errors())

    def send_event(self, event, name):
        """ Sends an event to input 'name'. Does not block."""
        words = list(event)
        for word in words[:-1]:
            self.input_fifos[name].append(word.get_binary())
        else:
            hook = triggers.Event()
            self.input_fifos[name].append(words[-1].get_binary(), event=hook)

        # Log once an event was sent.
        self.dut._log.info("Dataflow sent full event (L0ID " + util.hex(event.l0id) + ") to FIFO '" + name + "'")

        return hook

    @cocotb.coroutine
    def send_sync_event(self, event, name):
        """ Sends an event to input 'name'. Blocks until event is sent."""
        # Actually, how can this work?
        hook = self.send_event(event, name)
        yield hook.wait()

    def send_events_from_file(self, filename, name):
        """ Reads an event file (filename) and sends events to input 'name'.
            Returns hook which can be yielded."""
        input_events = events.read_events_from_file(filename)
        if len(input_events) != 0:
            for event in input_events:
                hook = self.send_event(event, name)
            else:
                return hook
        return None

    def send_random_events(self, name, n_random):
        """ Sends n_random random events to input 'name'.
            Returns hook which can be yielded."""
        random_events = events.get_random_events(n_random)
        for event in random_events:
            hook = self.send_event(event, name)
        else:
            return hook

    @cocotb.coroutine
    def wait_for_errors(self):
        """ Coroutine that waits for a driver or monitor to fail."""
        errors = []

        # There must be a cleaner way to iterate through both at the same time.
        for name, fifo in input_fifos.items():
            if fifo.on_error is not None:
                errors.append(fifo.on_error.wait())
        for name, fifo in output_fifos.items():
            if fifo.on_error is not None:
                errors.append(fifo.on_error.wait())

        # Yield the errors list!
        # This will resume only when one of the fifo on_error events fires.
        on_error = yield errors

        # This coroutine is forked. If we _ever_ get this far, it means something
        # has gone badly wrong (i.e. the test will fail).

        # Cleanup stage: call self.stop().
        # This should automatically force output files to close.
        self.stop()

        # This could be configured to allow other things to happen. e.g., continue after
        # failure but perform a reset.

        # Fail the test! Print out relevant message.
        raise result.TestFailure("Error: failure from FIFO: " + str(on_error.data))
