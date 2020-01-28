import cocotb
from cocotb import triggers, monitors

from . import events, util

class FifoMonitor(monitors.Monitor):

    def __init__(self, fifo, clock, output_name=None, process_events=True):
        # The fifo to monitor.
        # It must have three wires:
        #  * empty: is the FIFO empty?
        #  * read_enable: we've read the current word.
        #  * read_data: the data read out.
        self.fifo = fifo

        # The clock.
        self.clock = clock

        # Event being built; it goes TODO somewhere.
        self.pending_event = None

        # Event coroutine on error.
        self.on_error = triggers.Event()

        # Add another callback mechanism for processing events.
        self.event_callbacks = []

        # Store a set of expected (e.g. outstanding) events.
        # NOTE: this assumes L0IDs won't reoccur over short timescales!
        # But it's useful to use a set here, because we can have multiple configured inputs.
        # At least, I think it's useful...
        self.expected_ids = set()

        # When expect_empty is set to True
        self.expect_empty = False
        self.on_empty = triggers.Event()

        self.process_events = process_events

        super(FifoMonitor, self).__init__()

        # Add callbacks.
        self.add_callback(self.build_event)

        # Create output file if configured.
        # If that was configured-- add a callback to write to it.
        self.output_name = output_name
        self.output_file = None
        if output_name is not None:
            self.output_file = open(self.output_name, 'wb')
            self.add_callback(self.write_words)

    @cocotb.coroutine
    def _monitor_recv(self):

        # Receive words while the FIFO is not empty.
        # NOTE: this can probably be rewritten to sleep until empty goes from 1 -> 0.
        while True:

            yield triggers.RisingEdge(self.clock)
            yield triggers.ReadOnly()

            # If the FIFO is not empty, read it.
            if self.fifo.empty.value == 0:
                transaction = self.fifo.read_data.value
                self.fifo._log.debug("Received transaction: " + bin(self.fifo.read_data.value))
                # Need to get back to R/W phase.
                yield triggers.NextTimeStep()
                self.fifo.read_enable <= 1

                # Call the _recv() method in the base class.
                self._recv(transaction)
            else:
                yield triggers.NextTimeStep()
                self.fifo.read_enable <= 0

    def add_event_callback(self, callback):
        self.event_callbacks.append(callback)

    def build_event(self, transaction):
        """ Callback that constructs event objects."""

        # Convert "transaction" to a little endian object because ???
        # Hm, this hardcodes the size, which isn't ideal?
        transaction = util.BinaryValue(int(transaction), n_bits=65)

        # Now create a word.
        is_metadata = bool(transaction[64])
        contents = int(transaction[63:0])
        word = events.DataWord(contents, is_metadata)

        self.fifo._log.debug("Received word: " + str(word))

        if is_metadata:
            self.fifo._log.debug("Word had flag: " + util.hex(word.flag))

        # Build up the Event object as we go (for better monitoring).
        # If there is a problem while doing so, we set an event trigger that another coroutine is
        # blocking on. I worry this will be really inefficient.
        if word.is_start_of_event():
            l0id = events.get_l0id_from_event(word)
            if self.pending_event is None:
                self.pending_event = events.DataEvent(l0id)
                self.pending_event.add_word(word)
                self.fifo._log.info("Spy buffer received start of event, L0 ID = " + util.hex(l0id))
            else:
                self.on_error.set("Error: received start of event (L0 ID " + util.hex(l0id) +
                                  ") while processing event for L0 ID " + util.hex(self.pending_event.l0id) + ".")
        elif word.is_end_of_event():
            if self.pending_event is not None:
                self.pending_event.add_word(word)
                self.fifo._log.info("Spy buffer finished parsing event, L0 ID = " + util.hex(self.pending_event.l0id))

                if self.process_events:
                    self.process_event(self.pending_event)

                # Support for callbacks when we finish processing an event!
                for event_callback in self.event_callbacks:
                    event_callback(self.pending_event)

                # Clear the pending event.
                self.pending_event = None

            else:
                self.on_error.set("Error: received end of event without start of event.")

        else:
            if self.pending_event is not None:
                self.pending_event.add_word(word)
            else:
                self.on_error.set("Error: received word without start of event.")

    def write_words(self, transaction):
        """ Writes a received transaction to the binary log file."""

        # Create the word object.
        # NOTE: This is duplicated as part of build_event... maybe I should override the bit that
        # calls callbacks?
        transaction = util.BinaryValue(int(transaction), n_bits=65)
        is_metadata = bool(transaction[64])
        contents = int(transaction[63:0])
        word = events.DataWord(contents, is_metadata)

        # Write the word to the output file.
        word.write(self.output_file)

    def process_event(self, event):
        """ Processes a pending event when it is completed."""

        # Complain if we got an unexpected L0ID.
        if event.l0id not in self.expected_ids:
            self.on_error.set("Error: got an unexpected L0ID at output FIFO monitor: " + util.hex(event.l0id))

        # Otherwise, remove the L0ID from the list of expected IDs now that we've seen it.
        self.expected_ids.remove(event.l0id)

        # If the expect_empty flag is set, and we've just emptied expected_ids, fire the trigger.
        if self.expect_empty and len(self.expected_ids) == 0:
            self.on_empty.set()

        # NOTE: could always add more functionality here.
