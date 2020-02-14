
import cocotb
from cocotb import monitors
from cocotb.triggers import RisingEdge, ReadOnly, NextTimeStep, Event
#from cocotb.monitors import Monitor

from collections import deque
from tptest import util

class WordMonitor(monitors.Monitor) :

    def __init__(self, fifo, clock, observed_output, callback = None, event = None) :

        self.fifo = fifo
        self.clock = clock
        self.expected_words = deque()
        self.expect_empty = False
        self.on_empty = Event()
        self.observed_output = observed_output

        super(WordMonitor, self).__init__(callback = self.simple_callback)
        #self.add_callback(self.simple_callback)

    def expect(self, transaction) :
        self.expected_words.append(transaction)

    def has_remaining_events(self) :
        return len(self.expected_words) != 0

    @cocotb.coroutine
    def _monitor_recv(self) :

        while True :

            yield RisingEdge(self.clock)
            yield ReadOnly()

            if self.fifo.empty.value == 0 :
                transaction = self.fifo.read_data.value
                yield NextTimeStep()
                self.fifo.read_enable <= 1 # not sure why we mess with the read_enable flag
                self._recv(transaction)
            else :
                yield NextTimeStep()
                self.fifo.read_enable <= 0

    def simple_callback(self, transaction) :

        self.expected_words.pop()
        if self.expect_empty and len(self.expected_words) == 0 :
            self.on_empty.set()
        self.observed_output.append(transaction)
