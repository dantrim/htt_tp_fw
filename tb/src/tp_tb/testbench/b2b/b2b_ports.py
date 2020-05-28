import enum

from tp_tb.utils import port_descriptor


class B2BPorts(port_descriptor.PortDescriptor):
    def __init__(self):
        super().__init__()

    class Inputs(enum.Enum):
        PIXEL_0 = 0
        PIXEL_1 = 1
        STRIP_0 = 2
        STRIP_1 = 3

    class Outputs(enum.Enum):
        AMTP_0 = 0
        AMTP_1 = 1
        AMTP_2 = 2
        AMTP_3 = 3
        AMTP_4 = 4
        AMTP_5 = 5
        AMTP_6 = 6
        AMTP_7 = 7
        AMTP_8 = 8
        AMTP_9 = 9
        AMTP_10 = 10
        AMTP_11 = 11
        SSTP_0 = 12
        SSTP_1 = 13
