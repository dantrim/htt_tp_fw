import cocotb
from cocotb.triggers import Event, Combine, with_timeout, Tier

from tp_tb.testbench.evt_sync import evt_sync_utils

from tp_tb.utils import events
from tp_tb.utils import block_wrapper


class EvtSyncWrapper(block_wrapper.BlockWrapper):
    def __init__(self, clock, name):
        super().__init__(
            clock,
            name,
            len(evt_sync_utils.EvtSyncIO.Inputs),
            len(evt_sync_utils.EvtSyncIO.Outputs),
        )
