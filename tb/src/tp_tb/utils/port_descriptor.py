import enum


class PortDescriptor:
    def __init__(self):
        pass

    class Inputs(enum.Enum):
        pass

    class Outputs(enum.Enum):
        pass

    @staticmethod
    def simplename(io_enum):
        return str(io_enum.name).replace("_", "")
