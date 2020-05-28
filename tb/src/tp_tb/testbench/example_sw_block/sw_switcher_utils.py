import enum
from pathlib import Path


class SWSwitcherIO:
    class Inputs(enum.Enum):
        Input_0 = 0
        Input_1 = 1

    class Outputs(enum.Enum):
        Output_0 = 0
        Output_1 = 1

    @staticmethod
    def allowed_outputs():
        outputs = set()
        for output in SWSwitcherIO.Outputs:
            outputs.add(str(output.name))
        return outputs

    @staticmethod
    def simplename(io_enum):
        return str(io_enum.name).replace("_", "")


def get_testvector_files(testvec_dir, which):

    tdir = Path(str(testvec_dir))
    ok = tdir.exists() and tdir.is_dir()
    if not ok:
        raise Exception(
            f"ERROR Provided testvector directory (={str(testvec_dir)}) not found"
        )

    ##
    ## for SWSwitcher example, take input == output
    fmt = "BoardToBoardInput_"
    file_fmt = {"input": fmt, "output": fmt}[which.lower()]
    file_fmt += "AMTP0"

    testvec_files = list(tdir.glob(f"{file_fmt}_*"))

    io_enum = SWSwitcherIO.Inputs
    n_io = len(io_enum)
    ordered_files = testvec_files[:n_io]
    return ordered_files