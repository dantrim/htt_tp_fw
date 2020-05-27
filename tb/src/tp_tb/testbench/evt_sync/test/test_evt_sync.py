import sys
import os
import json

import cocotb

from tp_tb.utils import test_config
from tp_tb.utils import events, tb_diff, result_handler
from tp_tb.utils.fifo_wrapper import FifoDriver, FifoMonitor


##
## TEST
##
@cocotb.test()
def evt_sync_test(dut):

    ##
    ## first grab the testbench configuration
    ##
    config = test_config.get_config()
    print(config)

    return True
