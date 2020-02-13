import cocotb
from cocotb.clock import Clock
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep, Event, ClockCycles, Combine, with_timeout
from cocotb.monitors import Monitor
from cocotb.drivers import Driver, BitDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure, TestSuccess
from collections import deque

from tptest import events, util

CLOCK_SPEED = 200 # ns

class OutputMonitor(Monitor) :

    def __init__(self, fifo, clock, callback = None, event = None) :
        self.fifo = fifo
        self.clock = clock
        self.expected_ids = deque()
        self.expect_empty = False
        self.on_empty = Event()
        super(OutputMonitor, self).__init__(callback = callback)


    @coroutine
    def _monitor_recv(self) :
        while True :

            yield RisingEdge(self.clock)
            yield ReadOnly()

            if self.fifo.empty.value == 0 :
                transaction = self.fifo.read_data.value
                yield NextTimeStep()
                self.fifo.read_enable <= 1
                self._recv(transaction)
            else :
                yield NextTimeStep()
                self.fifo.read_enable <= 0

class FifoMonitor(Monitor) :

    def __init__(self, name, fifo, clock, is_output = True, callback = None, event = None) :
        self.name = name
        self.signal = { True : fifo.read_data
                        ,False : fifo.write_data
                      } [is_output]
        self.is_empty = { True : fifo.empty
                            ,False : None
                        } [is_output]
        self.read_enable = { True : fifo.read_enable
                            , False : None
                        } [is_output]
        self.clock = clock
        super(FifoMonitor, self).__init__()

    @coroutine
    def _monitor_recv(self) :

        """
        This coroutine is running in a parallel thread once the
        monitor is activated.
        """

        pos_edge = RisingEdge(self.clock)
        read_only = ReadOnly()
        while True :
            # check values synchronously

            # this is an output FIFO
            if self.is_empty is not None :
                yield pos_edge
                yield read_only # ensure values are stable
                if self.is_empty.value == 0 :
                    transaction = self.signal.value
                    #cocotb.log.info("FIFO Received transaction OUTPUT : {}".format(util.hex(self.signal.value)))
                    yield NextTimeStep()
                    self.read_enable <= 1
                    self._recv(transaction)
                else :
                    yield NextTimeStep()
                    self.read_enable <= 0
            else :
                transaction = self.signal.value
                #cocotb.log.info("FIFO Received transaction INPUT  : {}".format(util.hex(self.signal.value)))
                self._recv(transaction)

N_WORDS_SENT = 0
N_EXP_CALLS = 0
N_DRIVEN = 0
N_OUTPUT_APP = 0
                

class FifoDriver(Driver) :

    def __init__(self, name, fifo, clock) :
        self.name = name
        self.fifo = fifo # this is the SpyBuffer block
        self.clock = clock
        super(FifoDriver, self).__init__()

    @coroutine
    def _driver_send(self, transaction, sync = True, **kwargs) :
        global N_DRIVEN
        if sync :
            yield RisingEdge(self.clock)
            self.fifo.write_enable <= 0

        while self.fifo.almost_full != 0 :
            yield RisingEdge(self.clock)
        
        N_DRIVEN += 1
        self.fifo.write_data <= int(transaction)
        self.fifo.write_enable <= 1
        yield RisingEdge(self.clock)

        self.fifo.write_enable <= 0

class FifoTB(object) :

    def __init__(self, dut) :

        """
        Class to hold the test bench for verifying that the
        FIFO in the SpyBuffer produces the expected
        output.
        Does not do any inspection of the data, just ensures
        that the input words are the same as the output words.
        """

        self.dut = dut
        self.stopped = False

        self.fifo_driver = FifoDriver(name = "SpyFifoDriver_00", fifo = dut.spybuffer, clock = dut.clock)#, callback = self.fifo_input_callbacks)
        self.fifo_output_monitor = OutputMonitor(dut.spybuffer, dut.clock, callback = self.fifo_output_callback)
        #self.fifo_output_monitor = FifoMonitor(name = "SpyOutputMonitor_00", fifo = dut.spybuffer, clock = dut.clock, callback = self.fifo_output_callback)

        self.expected_output = []
        self.output = []
        #self.scoreboard = Scoreboard(dut, fail_immediately = False)
        #self.scoreboard.add_interface(self.fifo_output_monitor, self.expected_output)

        #self.fifo_input_monitor = FifoMonitor(name = "SpyInputMonitor_00", fifo = dut.spybuffer, clock = dut.clock, is_output = False, callback = self.fifo_input_callback)
        #self.fifo_input_monitor = InputMonitor(fifo = dut.spybuffer, clock = dut.clock, callback = self.fifo_input_callback)

    def fifo_input_callback(self, transaction) :
        global N_EXP_CALLS
        N_EXP_CALLS += 1
        self.expected_output.append(transaction)
        #cocotb.log.info("FifoTB input len      : {}".format(len(self.expected_output)))
        #cocotb.log.info("FifoTB input len      : {}".format(util.hex(transaction)))
    

    def fifo_output_callback(self, transaction) :
        global N_OUTPUT_APP
        N_OUTPUT_APP += 1
        output_mon = self.fifo_output_monitor
        output_mon.expected_ids.pop()
        if output_mon.expect_empty and len(output_mon.expected_ids) == 0 :
            output_mon.on_empty.set()
        self.output.append(transaction)
        #cocotb.log.info("FifoTB output recv len: {}".format(len(self.output)))
        #cocotb.log.info("FifoTB output recv len: {}".format(util.hex(transaction)))

    def start(self) :
        self.stopped = False
        filename = "../input_files/BoardToBoardInput_AMTP0_Strip0.evt"
        hook = self.send_events_from_file(filename)
        return hook

    def stop(self) :
        self.stopped = True

    def send_event(self, event) :
        words = list(event)
        global N_WORDS_SENT

        #self.fifo_output_monitor.expected_ids.add(event.l0id)

        for iword, word in enumerate(words[:-1]) :
            self.fifo_driver.append(word.get_binary(), callback = self.fifo_input_callback)
            self.fifo_output_monitor.expected_ids.append(word)
            N_WORDS_SENT += 1
        else :
            hook = Event()
            self.fifo_driver.append(words[-1].get_binary(), callback = self.fifo_input_callback, event = hook)
            self.fifo_output_monitor.expected_ids.append(word)
            N_WORDS_SENT += 1
        #hook = Event()
        #cocotb.log.info(sep)
        #cocotb.log.info(" > Sending word {}".format(len(words)-1))
        #self.fifo_driver.append(words[-1].get_binary(), event = hook)
        self.dut._log.info("Sent full event L0ID {}".format(util.hex(event.l0id)))
        return hook

    def send_events_from_file(self, filename) :
        input_events = events.read_events_from_file(filename)
        cocotb.log.info("Sending {} input events".format(len(input_events)))
        if len(input_events) != 0 :
            #for ievent, event in enumerate(input_events) :
            for ievent, event in enumerate(input_events[:1]) :
                #if ievent > 1 : break
                #sep = 80 * "="
                #cocotb.log.info(sep)
                #cocotb.log.info("Sending event {}".format(ievent))
                hook = self.send_event(event)
            else :
                return hook
        return None

    @cocotb.coroutine
    def wait_for_remaining_events(self, timeout = -1, units = "ns") :
        done = True
        hooks = []
        output_mon = self.fifo_output_monitor
        n_rem = len(output_mon.expected_ids)
        self.dut._log.info("Waiting for remaining events... -> {}".format(n_rem))
        if len(output_mon.expected_ids) != 0 :
            output_mon.on_empty.clear()
            hooks.append(output_mon.on_empty.wait())
            output_mon.expect_empty = True
            done = False
        if not done :
            tr = Combine(*hooks)
            if timeout == -1 :
                yield tr
            else :
                yield with_timeout(tr, timeout, units)

def initialize_wires(dut) :
    wires = [dut.buffer_write_enable, dut.buffer_read_enable, dut.input_data, dut.output_data]
    for wire in wires :
        wire <= 0

@cocotb.coroutine
def reset(dut) :
    dut.reset <= 1
    yield ClockCycles(dut.clock, 1)
    dut.reset <= 0
    yield ClockCycles(dut.clock, 1)
    dut.reset <= 1

@cocotb.test()
def test_fifo(dut) :

    simulation_clock = Clock(dut.clock, CLOCK_SPEED)
    cocotb.fork(simulation_clock.start())

    initialize_wires(dut)
    yield reset(dut)


    pos_edge = RisingEdge(dut.clock)

    fifo_tb = FifoTB(dut)
    hook = fifo_tb.start()
    yield hook.wait()
    yield fifo_tb.wait_for_remaining_events(timeout = 100, units = "ns")
    fifo_tb.stop()
    dut._log.info("N_OUTPUT_APP = {}, N_WORDS_SENT = {}, N_EXP_APP = {}, N_DRIVEN = {}".format(N_OUTPUT_APP, N_WORDS_SENT, N_EXP_CALLS, N_DRIVEN))
    exp = fifo_tb.expected_output
    got = fifo_tb.output
    for i, e in enumerate(exp) :
        exp_word = e
        if i == len(got) :
            dut._log.info("Number of received transactions not equal to expected!")
            break
        got_word = got[i]
        they_equal = (exp_word == got_word)
        #dut._log.info("[{}] GOT: {}, EXP: {} --> EQUAL? {}".format(i, util.hex(exp_word), util.hex(got_word), they_equal))
    #n = len(fifo_tb.expected_output)
    #sep = 80 * "="
    #cocotb.log.info(sep)
    #cocotb.log.info(sep)
    #for i in range(n) :
    #    exp = fifo_tb.expected_output[i]
    #    got = fifo_tb.output[i]
    #    cocotb.log.info("Event[{}] Expected: {}, Got: {}".format(i, util.hex(exp), util.hex(got)))
    #raise fifo_tb.scoreboard.result

    
