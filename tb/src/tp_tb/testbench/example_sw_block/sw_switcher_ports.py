import enum

from tp_tb.utils import port_descriptor


class SWSwitcherPorts(port_descriptor.PortDescriptor):
    def __init__(self):
        super().__init__()

    class Inputs(enum.Enum):
        Input_0 = 0
        Input_1 = 1

    class Outputs(enum.Enum):
        Output_0 = 0
        Outupt_1 = 1
