from collections import deque, Counter

import cocotb
from cocotb.triggers import RisingEdge, Event, ReadOnly, NextTimeStep, Timer

from tp_tb.utils import utils
from tp_tb.utils import software_block


class CREATORCLASSNAMEBlock(software_block.SoftwareBlock):
    def __init__(self, clock, name):
        super().__init__(clock, name)

    def input_callback_gen(self, input_num):
        return self._default_input_data_handler

    def output_handler_gen(self, output_num):
        return self._default_output_handler

    def _default_input_data_handler(self, transaction):
        data, timestamp = transaction

        ##
        ## here you would feed the data to the corresponding drivers where all of
        ## the block's logic will be defined (perhaps on a per-input level)
        ##
        # self.output_drivers[0].append(transaction)
        raise NotImplementedError("ERROR User must implement this method")

    @cocotb.coroutine
    def _default_output_handler(self, transaction):
        data, timestamp = transaction

        ##
        ## here you implement your logic, using all the tools of CocoTB coroutines
        ## available to you (yield, etc...)
        ##
        # driver = self.output_drivers[0]
        ## do stuff

        ##
        ## and when ready, push data to the output fifo
        ##
        # yield driver.write_to_fifo(data)
        raise NotImplementedError("ERROR User must implement this method")
