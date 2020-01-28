import cocotb
from cocotb import triggers, monitors

from . import events, util

# this class needs additional features. It needs to construct events!
# And then store htem and offload them somewhere.

# Where do the events go from FifoMonitor?
# One option: fifo monitor simply creates an output file and writes to it.

class FifoMonitor(monitors.Monitor):

    def __init__(self, fifo, clock):
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

        super(FifoMonitor, self).__init__()

        # Add callbacks.
        self.add_callback(self.build_event)

    @cocotb.coroutine
    def _monitor_recv(self):

        # Receive words while the FIFO is not empty.
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
            self.fifo._log.debug("Word had flag: " + hex(word.flag)[:-1])

        # Build up the Event object as we go (for better monitoring).
        # If there is a problem while doing so, we set an event trigger that another coroutine is
        # blocking on. I worry this will be really inefficient.
        if word.is_start_of_event():
            l0id = events.get_l0id_from_event(word)
            if self.pending_event is None:
                self.pending_event = events.DataEvent(l0id)
                self.pending_event.add_word(word)
                self.fifo._log.info("Spy buffer received start of event, L0 ID = " + hex(l0id)[:-1])
            else:
                self.on_error.set("Error: received start of event (L0 ID " + hex(l0id)[:-1] +
                                  ") while processing event for L0 ID " + hex(self.pending_event.l0id)[:-1] + ".")
        elif word.is_end_of_event():
            if self.pending_event is not None:
                self.pending_event.add_word(word)
                self.fifo._log.info("Spy buffer finished parsing event, L0 ID = " + hex(self.pending_event.l0id)[:-1])
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

    def process_event(self, event):
        """ Processes a pending event when it is completed."""

        # TODO: we want to add functionality here!
        # Processing could include:
        #  * Storing in a list or queue for online analysis
        #  * Writing to a binary file for offline analysis (add support to events module).
        #  * or more things!

        # NOTE: now that there are callbacks for this, this function could perhaps
        # be deleted (or at least, made a callback).

        pass
