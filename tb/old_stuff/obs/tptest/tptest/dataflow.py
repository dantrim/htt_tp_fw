import cocotb
from cocotb import triggers, result

from . import block, driver, monitor, events, util

class DataflowController(object):

    def __init__(self, dut, clock):
        self.dut = dut
        self.clock = clock

        self.fifos = {}
        self.input_fifos = {}
        self.output_fifos = {}

        # We should maybe give these names?
        self.empty_blocks = {}

        # Store a record of the events which were sent for each input.
        # Currently, this isn't actually used.
        self.input_log = {}
        self.fifo_log = {}

        self.on_error_coroutine = None

    # TODO: guards should be added here to check that the paths are _actually_ FIFOs.

    def add_input_fifo(self, name, path):
        """ Add an input FIFO driver. Returns reference to the object."""
        if name not in self.input_fifos:
            # Create the FIFO driver object; it starts automatically.
            self.input_fifos[name] = driver.FifoDriver(path, self.clock)
            self.input_log[name] = []
        return self.input_fifos[name]

    def add_output_fifo(self, name, path, output_file=None):
        """ Add an output FIFO monitor. Returns reference to the object."""
        if name not in self.output_fifos:
            # Create the FIFO monitor object; it also starts automatically.
            self.output_fifos[name] = monitor.FifoMonitor(path, self.clock, output_file)
        return self.output_fifos[name]

    def add_buffer(self, buffer_name, buffer_path) :
        """
        Add a SpyBuffer block driver and return an instance to that object.
        """
        if buffer_name not in self.fifos :
            self.fifos[buffer_name] = driver.FifoDriver(buffer_path, self.clock)
            self.fifo_log[buffer_name] = []
        return self.fifos[buffer_name]


    def add_empty_block(self, name, input_path, output_path, callback=None, event_callback=None):
        """ Creates an "empty block"-- another monitor/driver pair to create fake data flow."""

        # Create the empty block if it doesn't already exist.
        # This allows empty blocks to be created between _any_ two spy buffers.
        if name not in self.empty_blocks:
            empty_block = block.EmptyBlock(self.dut, input_path, output_path, self.clock, callback, event_callback)
            self.empty_blocks[name] = empty_block

        return self.empty_blocks[name]

    def stop_dantrim(self) :
        """
        Stop all co-routines?
        """

        for driver in self.fifos.values() :
            driver.kill()

        if self.on_error_coroutine is not None :
            self.on_error_coroutine.kill()
            self.on_error_coroutine = None

    def stop(self):
        """ Stop all coroutines. Not sure this is necessary."""
        for driver in self.input_fifos.values():
            driver.kill()

        for monitor in self.output_fifos.values():
            monitor.kill()

            # Closes connected output file (if one was configured).
            if monitor.output_file != None:
                monitor.output_file.close()

        for empty_block in self.empty_blocks.values():
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

    def send_event_dantrim(self, event, name) :

        self.fifo_log[name].append(event.l0id)
        words = list(event)
        for word in words[:-1] :
            self.fifos[name].append(word.get_binary())
        else :
            hook = triggers.Event()
            self.fifos[name].append(words[-1].get_binary(), event = hook)

        self.dut._log.info("Dataflow sent full event (L0ID {}) to FIFO {}".format(util.hex(event.l0id), name))
        return hook

    def send_event(self, event, name):
        """ Sends an event to input 'name'. Does not block."""
        # Store the L0ID that we're sending. Also dispatch it to the monitors.
        self.input_log[name].append(event.l0id)
        for output_fifo in self.output_fifos.values():
            output_fifo.expected_ids.add(event.l0id)

        # Send it!
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

    def send_events_from_file_dantrim(self, filename, buffer_name) :

        input_events = events.read_events_from_file(filename)
        self.dut._log.info("Sending {} input events".format(len(input_events)))
        if len(input_events) != 0 :
            for event in input_events :
                hook = self.send_event_dantrim(event, buffer_name)
            else :
                return hook
        return None

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
    def check_outstanding(self, timeout=-1, units='ns'):
        """ Coroutine that blocks until there are no outstanding events anywhere."""

        done = True
        hooks = []
        for output_fifo in self.output_fifos.values():
            # We can't exit if there are still events.
            # If there are still events: tell the output FIFO to fire a trigger
            # once there are no more.
            if len(output_fifo.expected_ids) != 0:
                output_fifo.on_empty.clear()
                hooks.append(output_fifo.on_empty.wait())
                output_fifo.expect_empty = True
                done = False

        # If there are still pending events:
        # Use the with_timeout() + combine triggers.
        # Exit either on timeout or after all the combined triggers fire.
        if not done:
            self.dut._log.info("Waiting for outstanding events...")
            tr = triggers.Combine(*hooks)
            if timeout == -1:
                yield tr
            else:
                yield triggers.with_timeout(tr, timeout, units)

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
