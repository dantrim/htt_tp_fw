
from pathlib import Path

import cocotb
from cocotb.triggers import Event, Combine, with_timeout

from tptest import events, util
from .b2b_utils import B2BIO, get_testvector_files
from b2b_test.fifo_driver import BasicFifoDriver
from b2b_test.fifo_output_monitor import WordMonitor
#import b2b_utils as b2b_utils


class B2BInputDriver :

    """
    A class to handle the input signals to the board-to-board block
    """

    def __init__(self, dut, base_tp) :

        if type(base_tp) != B2BIO.B2BOutputs :
            raise Exception("ERROR B2BInputDriver base_tp must be of type {}".format(type(B2BIO.B2BOutputs)))

        self._input_fifos = [x.input_buffer for x in dut.input_cluster_SpyBuffer] # expect the FIFO order to match indices of B2BIO.B2BInputs
        self._clock = dut.clock
        self._name = "B2BInputDriver_{}".format(base_tp.name)
        self._base_tp = base_tp
        self._log = dut._log

        self._log.info("B2BInputDriver (name={}) initialized with {} FIFOs".format(self.name, len(self.input_fifos)))

        self._drivers = []
        self._sent_words = []

        self._monitors = []
        self._observed_output_words = []

    ##
    ## properties
    ##

    @property
    def input_fifos(self) :
        return self._input_fifos

    @property
    def clock(self) :
        return self._clock

    @property
    def name(self) :
        return self._name

    @property
    def base_tp(self) :
        return self._base_tp

    ##
    ## methods
    ##

    def word_count(self) :
        exp_list = []#[len(x) for x in self._sent_words]
        obs_list = []

        idx = 3
        w5_in = []
        for driver in self._drivers :
            w5_in.append(hex(driver._sent_words[idx]))
            exp_list.append( len(driver._sent_words))

        w5_out = []
        for mon in self._monitors :
            w5_out.append(hex(mon.observed_words[idx]))
            obs_list.append( len(mon.observed_words) )
        self._log.info("W5_in : {}".format(w5_in))
        self._log.info("W5_out: {}".format(w5_out))
        return exp_list, obs_list

    def send_event(self, event, input_num) :

        current_driver = self._drivers[input_num]
        current_monitor = self._monitors[input_num]
        words = list(event)
        for iword, word in enumerate(words[:-1]) :
            current_driver.append(word.get_binary(), callback = current_driver.input_word_monitor)
            current_monitor.expect(word)
        else :
            hook = Event()
            current_driver.append(words[-1].get_binary(), callback = current_driver.input_word_monitor, event = hook)
            current_monitor.expect(words[-1])
        return hook

    def send_events_from_testvecs(self, testvecdir = "", num_events_to_send = -1) :

        input_testvec_files = get_testvector_files(self.base_tp, testvecdir, "input")
        self._log.info("Sending events from {} testvectors:".format(len(input_testvec_files)))

        hooks = []
        for fifo in B2BIO.B2BInputs :

            input_num = int(fifo.value)
            testvec = input_testvec_files[input_num]
            self._log.info(" -> Input {} ({}): {}".format(input_num, fifo.name, testvec))

            self._sent_words.append([])
            driver = BasicFifoDriver(self.input_fifos[input_num], self.clock, "InputFIFODriver_{}".format(input_num))
            self._drivers.append(driver)
            
            self._observed_output_words.append([])
            monitor = WordMonitor(self.input_fifos[input_num], self.clock,
                        "InputFIFOMonitor_{}".format(input_num))
            self._monitors.append(monitor)

            input_events = events.read_events_from_file(testvec)
            n_events_in_file = len(input_events)
            if num_events_to_send > 0 : n_events_in_file = num_events_to_send

            if input_events :
                if num_events_to_send > 0 :
                    if num_events_to_send >= len(input_events) :
                        pass
                    else :
                        input_events = input_events[:num_events_to_send]
                        num_events_to_send = len(input_events)

                self.input_fifos[input_num]._log.info("Sending {} events to FIFO {}".format(num_events_to_send, self.name))

                for ievent, event in enumerate(input_events) :
                    hook = self.send_event(event, input_num)
                else :
                    hooks.append(hook.wait())

        return hooks

    ##
    ## callbacks
    ##

    #def word_monitor(self, input_num) :
    #    aplist = self._sent_words[input_num]
    #    def input_word_monitor(self, transaction) :
    #        aplist.append(transaction)
    #        #self._sent_words[input_num].append(transaction)
    #    return input_word_monitor

    ##
    ## cocotb coroutines
    ##

    @cocotb.coroutine 
    def wait_for_events(self, timeout = -1, units = "ns") :

        done = True
        hooks = []
        for mon in self._monitors :
            if mon.has_remaining_events() :
                mon.on_empty.clear()
                hooks.append(mon.on_empty.wait())
                mon.expect_empty = True
                done = False
        if not done :
            tr = Combine(*hooks)
            if timeout == -1 :
                yield tr
            else :
                yield with_timeout(tr, timeout, units)

