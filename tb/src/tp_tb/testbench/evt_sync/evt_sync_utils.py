import enum


class EvtSyncIO:
    class Inputs(enum.Enum):
        Input_0 = 0

    class Outputs(enum.Enum):
        Output_0 = 0

    @staticmethod
    def allowed_outputs():
        outputs = set()
        for output in EvtSyncIO.Outputs:
            outputs.add(str(output.name))
        return outputs

    @staticmethod
    def simplename(io_enum):
        return str(io_enum.name).replace("_", "")
