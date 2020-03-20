
from pathlib import Path

import cocotb
from cocotb.triggers import Event, Combine, with_timeout, Timer

from tptest import events, util
from .b2b_utils import B2BIO, get_testvector_files
from b2b_test.fifo_driver import BasicFifoDriver
from b2b_test.fifo_output_monitor import WordMonitor

class B2BWrapper :

    def __init__(self, dut, base_tp) :

        if type(base_tp) != B2BIO.B2BOutputs :
            raise Exception("ERROR B2BWrapper base_tp must be of type {}".format(type(B2BIO.B2BOutputs)))

        self._dut = dut
        self._input_fifos = [x.input_buffer for x in dut.input_cluster_SpyBuffer]
        self._output_fifos = [x.output_buffer for x in dut.output_cluster_SpyBuffer]
        self._clock = dut.clock
        self._name = "B2BWrapper_{}".format(base_tp.name)
        self._base_tp = base_tp
        self._log = dut._log

        self._drivers = []
        self._n_words_input= 0
        self._sent_words = []

        self._monitors = []
        self._output_lists = []
        self._testvecs_expected = []
        self._n_words_output = 0

    @property
    def input_fifos(self) :
        return self._input_fifos

    @property
    def output_fifos(self) :
        return self._output_fifos

    @property
    def name(self) :
        return self._name

    @property
    def clock(self) :
        return self._clock

    @property
    def base_tp(self) :
        return self._base_tp

    def send_event(self, event, driver) : #input_num) :

        #driver = self._drivers[input_num]
        words = list(event)
        n_sent = 0
        for iword, word in enumerate(words[:-1]) :
            driver.append(word.get_binary(), callback = driver.input_word_monitor)
            n_sent += 1
        else :
            hook = Event()
            driver.append(words[-1].get_binary(), callback = driver.input_word_monitor, event = hook)
            n_sent += 1
        cocotb.log.info("{} sent {} words".format(self.name, n_sent))
        return hook, n_sent

    def send_events_from_testvecs(self, testvecdir = "", num_events_to_send = -1) :

        self._log.info("Sending events from testvectors...")

        ##
        ## prepare the monitors
        ##

        self._log.info("Setting up B2B output monitors")
        for fifo in B2BIO.B2BOutputs :
            output_words = []
            output_num = int(fifo.value)
            self._log.info(" -> Preparing monitor {} ({})".format(output_num, fifo.name))
            monitor = WordMonitor(self.output_fifos[output_num], self.clock, "OutputFIFOMonitor_{}".format(output_num), obs_list = output_words, dut = self._dut, io_num = output_num)
            self._monitors.append(monitor)
            self._output_lists.append(output_words)

        input_testvec_files = get_testvector_files(self.base_tp, testvecdir, "input")

        self._log.info("Setting up B2B input drivers")

        hooks = []
        total_words_sent = 0
        for fifo in B2BIO.B2BInputs :
            input_num = int(fifo.value)
            #if input_num > 0  : break
            testvec = input_testvec_files[input_num]
            self._log.info(" -> Input {} ({}): {}".format(input_num, fifo.name, testvec))

            driver = BasicFifoDriver(self.input_fifos[input_num], self.clock, "InputFIFODriver_{}".format(input_num), dut = self._dut, io_num = input_num)
            self._drivers.append(driver)

            input_events = events.read_events_from_file(testvec)
            n_events_in_file = len(input_events)
            if num_events_to_send > 0 : n_events_in_file = num_events_to_send
            if input_events :
                if num_events_to_send > 0 :
                    if num_events_to_send >= len(input_events) :
                        pass
                    else :
                        input_events = input_events[:num_events_to_send]
                self.input_fifos[input_num]._log.info("Sending {} events to FIFO {}".format(num_events_to_send, self.name))

                for ievent, event in enumerate(input_events) :
                    hook, n_words = self.send_event(event, driver)#input_num)
                    total_words_sent += n_words
                else :
                    #hook = Timer(1000, "ns")
                    hooks.append(hook)#.wait())

        self._n_words_input = total_words_sent

        return hooks, total_words_sent

    @cocotb.coroutine
    def wait_for_events(self, timeout = -1, units = "ns") :

        done = True
        hooks = []
        for i, mon in enumerate(self._monitors) :
            #cocotb.log.info(" -> OUTPUT FIFO {} RECVD {} WORDS".format(mon.name, len(self._output_lists[i])))#mon.n_words_received()))
            self._n_words_output += mon.n_words_received()
        #cocotb.log.info(" ==> OUTPUT N WORDS RECVD: {}".format(self._n_words_output))
        all_recvd = self._n_words_output == self._n_words_input

        if not all_recvd :
            yield Timer(timeout, units)
