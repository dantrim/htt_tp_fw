from collections import deque, Counter

import cocotb
from cocotb.triggers import RisingEdge, Event, ReadOnly, NextTimeStep, Timer

from tp_tb.utils import utils
from tp_tb.utils import software_block


class SWSwitcherBlock(software_block.SoftwareBlock):
    def __init__(self, clock, name):
        super().__init__(clock, name)

        self._dummy_delay_0 = 100
        self._dummy_delay_1 = 0
        self._dummy_delay_unit_str = "ns"

        self._l0id_recvd = []
        self._event_hook = Event()

    def input_callback_gen(self, input_num):
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
            return True
        elif c[l0id] >= 1:
            return False
        return None

    @cocotb.coroutine
    def _output_port_0_handler(self, transaction):
        data, timestamp = transaction
        driver = self.output_drivers[0]
        # time = cocotb.utils.get_sim_time(units="ns")
        # l0id = events.l0id_from_word(events.raw_to_word(data))
        # event_is_ready = self.event_is_ready(l0id)
        # if event_is_ready is None :
        #    self._event_hook.clear()
        # elif event_is_ready :
        #    self._event_hook.set()
        # else :
        #    print(f"FOO going to wait for EVENT_ HOOK L0iD={hex(l0id)}: {time}")
        #    yield self._event_hook.wait()
        #    time = cocotb.utils.get_sim_time(units="ns")
        #    print(f"FOO DONE WAITING FOR EVENT_HOOK L0ID={hex(l0id)}: {time}")

        ##
        ## mimic some logic taking some time
        ##
        time_delay = Timer(100, "ns")
        yield time_delay

        ##
        ## write the output
        ##
        yield driver.write_to_fifo(data)

    @cocotb.coroutine
    def _output_port_1_handler(self, transaction):
        data, timestamp = transaction
        driver = self.output_drivers[1]
        # data_word = utils.transaction_to_data_word(data)
        # l0id = utils.l0id_from_data_word(data_word)
        # l0id = events.l0id_from_word(events.raw_to_word(int(data)))
        # event_is_ready = self.event_is_ready(l0id)
        # if event_is_ready is None :
        #    self._event_hook.clear()
        # elif event_is_ready :
        #    self._event_hook.set()
        # else :
        #    print(f"FOO going to wait for EVENT_ HOOK L0iD={hex(l0id)}: {time}")
        #    yield self._event_hook.wait()
        #    time = cocotb.utils.get_sim_time(units="ns")
        #    print(f"FOO DONE WAITING FOR EVENT_HOOK L0ID={hex(l0id)}: {time}")

        ##
        ## write the output
        ##
        yield driver.write_to_fifo(data)
