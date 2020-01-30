import cocotb
from cocotb import triggers, drivers

from cocotb import binary

# Is all the functionality here?
# I think so. We might want a wrapper around append() to
# automatically fill in a callback/event trigger.

# We need, at some point, to specify the right size being stored.

class FifoDriver(drivers.Driver):

    def __init__(self, fifo, clock):
        # This is a pointer to a spy buffer / FIFO object.
        # It must have two wires:
        #  * almost_full = is the FIFO almost full?
        #  * write_data = data to write in.
        #  * write_enable = write.
        self.fifo = fifo

        # This is the clock.
        self.clock = clock

        # As currently written, there's no circumstance under which
        # the driver can fail the testbench.
        self.on_error = None

        # Invoke the parent constructor.
        super(FifoDriver, self).__init__()

    @cocotb.coroutine
    def _driver_send(self, transaction, sync=True, **kwargs):

        # The driver will set sync = True for the first word in
        # a batch of back-to-back words.
        if sync:
            yield triggers.RisingEdge(self.clock)
            self.fifo.write_enable <= 0

        # Wait until the FIFO is not almost full to actually
        # set the write enable high.
        while self.fifo.almost_full != 0:
            yield triggers.RisingEdge(self.clock)

        # Perform the write by setting write enable high.
        # Wait for a rising edge for this to take affect.
        self.fifo.write_data <= int(transaction)
        self.fifo.write_enable <= 1
        yield triggers.RisingEdge(self.clock)

        # Set the write enable back to zero.
        self.fifo.write_enable <= 0
        self.fifo._log.debug("Sent word: " + str(transaction))
