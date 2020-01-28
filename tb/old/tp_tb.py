
#
# first attempt at cocotb module that does two things:
#   - flow data through top-level tb.v
#   - implement a dummy block that sits between SpyBuffer
#     instances 'sb1' and 'sb2' in 'tp.v' module 'tp'
#
# begun 2019-11-11
#

import cocotb
from cocotb.triggers import Timer, RisingEdge, ClockCycles
from cocotb.result import TestFailure
from cocotb.utils import get_sim_time

from testwrapper import CocotbTest


@CocotbTest("T01", skip=False)
def t01_hello(dut):
    "Hello world"
    tp = dut.dut
    info = dut._log.info
    info("hello world")
    yield ClockCycles(tp.clk, 100)
    info("bye")


