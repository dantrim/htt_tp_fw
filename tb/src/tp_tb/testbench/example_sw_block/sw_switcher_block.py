from collections import deque, Counter

import cocotb
from cocotb.triggers import RisingEdge, Event, ReadOnly, NextTimeStep, Timer

from tp_tb.utils import utils
from tp_tb.utils import software_block


class SWSwitcherBlock(software_block.SoftwareBlock):
    def __init__(self, clock, name):
        super().__init__(clock, name)

        self._l0id_recvd = []
        self._event_hook = Event()  # used to sync up writing to outputs

    def input_handler_gen(self, input_num):
        if input_num == 0:
            return self._port_0_handle_input_data
        elif input_num == 1:
            return self._port_1_handle_input_data

    def output_handler_gen(self, output_num):
        if output_num == 0:
            return self._output_port_0_handler
        elif output_num == 1:
            return self._output_port_1_handler

    def _port_0_handle_input_data(self, transaction):
        data, timestamp = transaction

        ##
        ## input 0 --> output 1
        ##
        self.output_drivers[1].append(transaction)

    def _port_1_handle_input_data(self, transaction):
        data, timestamp = transaction

        ##
        ## input 1 --> output 0
        ##
        self.output_drivers[0].append(transaction)

    def event_is_ready(self, l0id):
        self._l0id_recvd.append(l0id)
        c = Counter(self._l0id_recvd)
        if c[l0id] >= len(self.output_drivers):
            self._event_hook.set()
            return True
        elif c[l0id] >= 1:
            return False
        else:
            self._event_hook.clear()
            return False

    @cocotb.coroutine
    def _sync_event_header(self, l0id, output_num=-1, data_word=-1):
        if l0id and not self.event_is_ready(l0id):
            yield self._event_hook.wait()
            self._event_hook.clear()

    @cocotb.coroutine
    def _output_port_0_handler(self, transaction):
        data, timestamp = transaction
        driver = self.output_drivers[0]
        data_word = utils.transaction_to_data_word(data)
        l0id = utils.l0id_from_data_word(data_word)

        ##
        ## mimic some logic taking some time
        ##
        time_delay = Timer(50, "ns")
        yield time_delay

        ##
        ## sync up the writing of output data between the
        ## two outputs, based on event-boundaries
        ##
        yield self._sync_event_header(l0id)

        ##
        ## write the output
        ##
        yield driver.write_to_fifo(data)

    @cocotb.coroutine
    def _output_port_1_handler(self, transaction):
        data, timestamp = transaction
        driver = self.output_drivers[1]
        data_word = utils.transaction_to_data_word(data)
        l0id = utils.l0id_from_data_word(data_word)

        ##
        ## mimic some logic taking some time
        ##
        time_delay = Timer(200, "ns")
        yield time_delay

        ##
        ## sync up the writing of output data between the
        ## two outputs, based on event-boundaries
        ##
        yield self._sync_event_header(l0id)

        ##
        ## write the output
        ##
        yield driver.write_to_fifo(data)
