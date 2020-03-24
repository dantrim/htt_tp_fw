import cocotb
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge, ReadOnly, NextTimeStep, Event

from collections import deque
from tptest import util

class WordMonitor(Monitor) :

    """
    Basic FIFO monitor that keep track of the words
    being read out of a SpyBuffer FIFO queue
    """

    def __init__(self, fifo_block, clock, name, dut, io_num, callbacks = [], event = None, obs_list = [], n_words_expected = 0) :

        self._io_num = io_num
        self._dut = dut
        self._fifo = fifo_block
        self._clock = clock
        self._name = name
        self.expected_words = deque()
        self.expect_empty = False
        self.n_words_expected = n_words_expected
        self.on_empty = Event()
        self.continue_loading = True

        self.observed_words = obs_list

        if self.n_words_expected == 0 :
            self.expect_empty = True
            self.on_empty.clear()
            self.on_empty.set()

        super().__init__(callback = self.simple_callback)
        if callbacks :
            for callback in callbacks :
                super().add_callback(callback = callback)

    ##
    ## properties
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
    ## methods
    ##

    def expect(self, data_word) :
        self.expected_words.append(data_word)

    def has_remaining_events(self) :
        return self.n_words_expected > 0
        #return len(self.expected_words) != 0

    def n_words_received(self) :
        return len(self.observed_words)

    ##
    ## cocotb coroutines
    ##

    @cocotb.coroutine
    def _monitor_recv(self) :

        #while True :
        n_empties = 0
        while self.continue_loading :


            yield RisingEdge(self.clock)
            yield ReadOnly()

            if self.fifo.empty.value == 0 :
                n_empties = 0
                transaction = self.fifo.read_data.value
                yield NextTimeStep()
                self.fifo.read_enable <= 1 # not sure why we manually toggle read_eanble
                self._recv(transaction)

            else :
                yield NextTimeStep()
                self.fifo.read_enable <= 0
                n_empties += 1
        self.fifo._log.info("{} MONITOR CONTINUE LOADING HAS BROKEN LOOP".format(self.name))

    ##
    ## callbacks
    ##

    def simple_callback(self, transaction) :
        #if "input" in self.name.lower() :
        #    self.expected_words.pop()
        #    if self.expect_empty and len(self.expected_words) == 0 :
        #        self.on_empty.set()
        #else :
        #if self.n_words_expected > 0 :
        self.n_words_expected = self.n_words_expected - 1 # decrement
        #self.n_words_expected = self.n_words_expected - 1

        form_str = "{0:#0{1}x}"
        x = form_str.format(int(transaction), 19)
        self._fifo._log.info("{} MONITOR CALLBACK  {} -> {} ({})".format(self.name, x, self.n_words_received(), self.n_words_expected))# {}".format(self.name), self.n_words_received())

        #if self.expect_empty and self.n_words_expected == 0 :
        if self.expect_empty and self.n_words_expected < 0 :
            self._fifo.log.info("{} MONITOR CALLBACK SETS EMPTY FLAG".format(self.name))
            #self.continue_loading = False
            self.on_empty.set()
            self.expect_empty = False
        #else :
        self.observed_words.append(transaction)
        #self._fifo._log.info("{} MONITOR CALLBACK {} -> {} ({})".format(self.name, hex(transaction), self.n_words_received(), self.n_words_expected))# {}".format(self.name), self.n_words_received())
        
