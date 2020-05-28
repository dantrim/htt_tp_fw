import enum

from tp_tb.utils import port_descriptor


class EvtSyncPorts(port_descriptor.PortDescriptor):
    def __init__(self):
        super().__init__()

    class Inputs(enum.Enum):
        B2B_0 = 0
        B2B_1 = 1
        B2B_2 = 2
        B2B_3 = 3
        B2B_4 = 4
        B2B_5 = 5
        B2B_6 = 6
        B2B_7 = 7
        B2B_8 = 8
        B2B_9 = 9
        B2B_10 = 10
        B2B_11 = 11
        B2B_12 = 12
        CLUSTER_PIX_0 = 13
        CLUSTER_PIX_1 = 14
        CLUSTER_STRIP_0 = 15
        CLUSTER_STRIP_1 = 16

    class Outputs(enum.Enum):
        OUTPUT_0 = 0
        OUTPUT_1 = 1
        OUTPUT_2 = 2
        OUTPUT_3 = 3
