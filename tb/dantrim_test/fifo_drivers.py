

import cocotb
from cocotb.drivers import Driver
from cocotb.triggers import RisingEdge, Event

from tptest import util

def check_fifo_block(fifo) :

    required_signals = [
        "write_enable"
        ,"read_enable"
        ,"write_data"
        ,"almost_full"
        ,"empty"
    ]

    for req_sig in required_signals :
        if not hasattr(fifo, req_sig) :
            cocotb.error("Provided FIFO block missing required signal: {}".format(req_sig))
            return False
    return True


class BasicFifoDriver(Driver) :

    def __init__(self, name, fifo, clock) :

        self.name = "BasicFifoDriver_{}".format(name)
        self.fifo = fifo
        self.clock = clock

        if not check_fifo_block(fifo) :
            raise Exception("Fifo block not valid")

        super(BasicFifoDriver, self).__init__()

    @cocotb.coroutine
    def _driver_send(self, transaction, sync = True, **kwargs) :
        
        # sync is set to True at the start of a transaction by cocotb
        if sync :
            yield RisingEdge(self.clock)
            self.fifo.write_enable <= 0 # not sure why we do this

        while self.fifo.almost_full != 0 :
            yield RisingEdge(self.clock)

        self.fifo.write_data <= int(transaction)
        self.fifo.write_enable <= 1
        yield RisingEdge(self.clock)

        self.fifo.write_enable <= 0 # generally, I'm not sure why we have to toggle write_enable
        
        
