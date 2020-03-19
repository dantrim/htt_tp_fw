import cocotb
from cocotb.drivers import Driver
from cocotb.triggers import RisingEdge, Event, Timer

from tptest import util
from b2b_test import fifo_utils
#import fifo_utils

class BasicFifoDriver(Driver) :

    """
    Basic Driver that inputs events into a SpyBuffer
    FIFO queue
    """

    def __init__(self, fifo_block, clock, name, dut, io_num) :

        self._io_num = io_num
        self._dut = dut
        self._fifo = fifo_block
        self._clock = clock
        self._name = name
        self._sent_words = []

        if not fifo_utils.check_fifo_block(fifo_block) :
            raise Exception("Unable to set FIFO block for FIFO with name={}"
                .format(self.name))

        super().__init__()

    ##
    ## class properties
    ##

    @property
    def name(self) :
        return self._name

    @property
    def fifo(self) :
        return self._fifo

    @property
    def clock(self) :
        return self._clock

    ##
    ## callbacks
    ##

    def input_word_monitor(self, transaction) :
        self._sent_words.append(transaction)

    ##
    ## cocotb coroutines
    ##

    @cocotb.coroutine
    def _driver_send(self, transaction, sync = True, **kwargs) :

        """
        Provide an implementation of Driver._driver_send for
        our specific case for driving signals onto a SpyBuffer FIFO
        input

        Parameters:

        transaction: data word to be driven onto FIFO input
        sync:

        """

        # sync is set to True at the start of a transaction by cocotb
        # TODO: check/understand this and where it's done in cocotb
        if sync :
#            self.fifo.write_enable <= 1
            #self.fifo.read_enable <= 1
            yield RisingEdge(self.clock)
            #self._dut.cluster_wren[self._io_num] <= 0
            self.fifo.write_enable <= 0 # dantrim: not sure why this is done

        # wait until the FIFO has room for the next transaction
        while self.fifo.almost_full != 0 :
        #while self._dut.cluster_almost_full[self._io_num] != 0 :
        #    self.fifo._log.info("IN DRIVER SEND ALMOST FULL LOOP: {}".format(self.fifo.read_enable.value))
            yield RisingEdge(self.clock)

        #self._dut.input_data[self._io_num] <= int(transaction)
        #self._dut.cluster_data[self._io_num] <= int(transaction)
        self.fifo.write_data <= int(transaction)
        #self.fifo._log.info("{} DRIVER SENDING {} ({})".format(self.name, hex(transaction), self.fifo.read_enable.value))
        self.fifo.write_enable <= 1
        #self._dut.cluster_wren[self._io_num] <= 1
        yield RisingEdge(self.clock)

        self.fifo.write_enable <= 0 # dantrim: not sure why we manually toggle the FIFO write_enable
        #self._dut.cluster_wren[self._io_num] <= 0
        

