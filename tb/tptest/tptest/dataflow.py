import cocotb
from cocotb import triggers, result

from . import block, driver, monitor, events

class DataflowController(object):

    def __init__(self, dut, clock):
        self.dut = dut
        self.clock = clock

        self.input_fifos = {}
        self.output_fifos = {}

        # We should maybe give these names?
        self.empty_blocks = []

        self.on_error_coroutine = None

    # TODO: the FIFOs should know their names, so they can print them in debug messages etc.
    # Or perhaps this works automatically.
    # TODO: guards should be added here to check that the paths are _actually_ FIFOs.

    def add_input_fifo(self, name, path, enable_port, data_port):
        """ Add an input FIFO driver."""
        if name in self.input_fifos:
            return False

        # Create the FIFO driver object; it starts automatically.
        self.input_fifos[name] = driver.FifoDriver(path, self.clock, enable_port, data_port)
        return True

    def add_output_fifo(self, name, path, enable_port):
        """ Add an output FIFO monitor."""
        if name in self.output_fifos:
            return True

        # Create the FIFO monitor object; it also starts automatically.
        # TODO: register callback?
        self.output_fifos[name] = monitor.FifoMonitor(path, self.clock, enable_port)

    def add_empty_block(self, input_name, output_name, if_output_enable, of_input_enable, of_data,
                        callback=None, event_callback=None):
        """ Creates an "empty block"-- another monitor/driver pair to create fake data flow."""

        # Don't allow this to happen if we already have a driver or monitor.
        if input_name in self.output_fifos:
            raise result.TestFailure("Error: cannot use output-side external FIFO as input to empty block.")
        if output_name in self.input_fifos:
            raise result.TestFailure("Error: cannot use input-side external FIFO as output from empty block.")

        # Look up references to the RTL spybuffer objects.
        # TODO: this is not really right, since it requires there to be a driver and monitor
        # already. Needs to be fixed to support creating empty blocks that take input from real ones.
        try:
            input_fifo = self.input_fifos[input_name].fifo
            output_fifo = self.output_fifos[output_name].fifo
        except:
            raise result.TestFailure("Error: cannot create empty block without first creating a driver and monitor.")

        empty_block = block.EmptyBlock(self.dut, input_fifo, output_fifo, self.clock, if_output_enable, of_input_enable, of_data,
                                       callback, event_callback)
        self.empty_blocks.append(empty_block)

    def stop(self):
        """ Stop all coroutines. Not sure this is necessary."""
        for name, driver in self.input_fifos.items():
            driver.kill()
        for name, driver in self.output_fifos.items():
            driver.kill()

        for empty_block in self.empty_blocks:
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
        for event in input_events:
            hook = self.send_event(event, name)
        else:
            return hook

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

        # TODO: add cleanup methods here!
        # e.g. close files opened by monitors.

        # This could be configured to allow other things to happen. e.g., continue after
        # failure but perform a reset.

        # Fail the test! Print out relevant message.
        raise result.TestFailure("Error: failure from FIFO: " + str(on_error.data))
