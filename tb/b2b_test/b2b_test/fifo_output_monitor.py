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

    def __init__(self, fifo_block, clock, name, dut, io_num, callbacks = [], event = None, obs_list = []) :

        self._io_num = io_num
        self._dut = dut
        self._fifo = fifo_block
        self._clock = clock
        self._name = name
        self.expected_words = deque()
        self.expect_empty = False
        self.on_empty = Event()

        self.observed_words = obs_list

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
        return len(self.expected_words) != 0

    def n_words_received(self) :
        return len(self.observed_words)

    ##
    ## cocotb coroutines
    ##

    @cocotb.coroutine
    def _monitor_recv(self) :

        while True :
            #self.fifo.write_enable <= 1
            #self.fifo.read_enable <= 1
            yield RisingEdge(self.clock)
            yield ReadOnly()
            #val = self._dut.output_cluster_SpyBuffer[1].output_buffer.write_data.value
            sep = "BLAH " + 55 * "="
            sep2 = "BLAH " + 55 * "-"
            cocotb.log.info(sep)
            din = self._dut.input_cluster_SpyBuffer[0].input_buffer.write_data.value
            dout = self._dut.input_cluster_SpyBuffer[0].input_buffer.read_data.value
            ren = self._dut.input_cluster_SpyBuffer[0].input_buffer.read_enable.value
            clus_req = self._dut.board2board_switching_inst.cluster_req[0].value
            clus_din = self._dut.board2board_switching_inst.cluster_data[0].value
            cocotb.log.info("BLAH {} {} {} {} {}".format(
                hex(din)
                ,hex(dout)
                ,hex(ren)
                ,hex(clus_req)
                ,hex(clus_din)
            ))

            cocotb.log.info(sep2)

            din2 = self._dut.board2board_switching_inst.output_board_event[1].value
            wren2 = self._dut.board2board_switching_inst.output_board_wren[1].value
            fifo_write_data = self._dut.output_cluster_SpyBuffer[1].output_buffer.write_data.value
            fifo_write_en = self._dut.output_cluster_SpyBuffer[1].output_buffer.write_enable.value
            fifo_empty = self._dut.output_cluster_SpyBuffer[1].output_buffer.empty.value
            cocotb.log.info("BLAH {} {} {} {} {}".format(
                hex(din2)
                ,hex(wren2)
                ,hex(fifo_write_data)
                ,hex(fifo_write_en)
                ,hex(fifo_empty)
            ))
            cocotb.log.info(sep)


            #yield RisingEdge(self.clock)
            #cocotb.log.info("OUTPUT FIFO WRITE ENABLE: {}".format(self.fifo.write_enable.value))



            if self.fifo.empty.value == 0 :
            #if self._dut.board_empty[self._io_num] == 0 :
                transaction = self.fifo.read_data.value
                yield NextTimeStep()
                self.fifo.read_enable <= 1 # not sure why we manually toggle read_eanble
                #self._dut.board_ren[self._io_num] <= 1
                cocotb.log.info("MONITOR RECEIVED TRANSACTION {}".format(hex(transaction)))
                self._recv(transaction)
            else :
                yield NextTimeStep()
                self.fifo.read_enable <= 0
                #self._dut.board_ren[self._io_num] <= 0
                #val = self._dut.board_cluster_data[self._io_num].value
                #cocotb.log.info("MONITOR EMPTY")



    ##
    ## callbacks
    ##

    def simple_callback(self, transaction) :
        if "input" in self.name.lower() :
            self.expected_words.pop()
            if self.expect_empty and len(self.expected_words) == 0 :
                self.on_empty.set()
        #else :
        self.observed_words.append(transaction)
        #self._fifo._log.info("{} MONITOR CALLBACK {}".format(self.name, hex(transaction)))# {}".format(self.name), self.n_words_received())
        
