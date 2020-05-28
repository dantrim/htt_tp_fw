from pathlib import Path
import cocotb

from tp_tb.testbench.b2b.b2b_ports import B2BPorts


def get_testvector_files(testvector_dir="", base_tp=None):
    """
    Grabs testvectors for B2B testbench.
    """

    if type(base_tp) != B2BPorts.Outputs:
        raise Exception(f"ERROR base_tp must be of type {type(B2BPorts.Outputs)}")
    tdir = Path(str(testvector_dir))
    ok = tdir.exists() and tdir.is_dir()
    if not ok:
        raise Exception(
            f"ERROR Provided testvector directory (={str(testvector_dir)}) not found"
        )

    input_testvectors = []
    output_testvectors = []
    for i, io_direction in enumerate(["input", "output"]):
        file_fmt = ["BoardToBoardInput_", "TPtoSync_src"][i]
        file_fmt += B2BPorts.simplename(base_tp)
        testvec_files = list(tdir.glob(f"{file_fmt}_*.evt"))
        io_enum = [B2BPorts.Inputs, B2BPorts.Outputs][i]
        n_io = len(io_enum)

        for j in range(n_io):
            for io in io_enum:
                if io.value == j:  # this is the io port that we want
                    name = B2BPorts.simplename(io).lower()
                    for tfile in testvec_files:
                        final_tag = (
                            str(tfile)
                            .split("_")[-1]
                            .replace(".evt", "")
                            .replace("dest", "")
                            .lower()
                        )
                        if final_tag == name:
                            if io_direction == "input":
                                input_testvectors.append(str(tfile))
                            elif io_direction == "output":
                                output_testvectors.append(str(tfile))
                            break

    return input_testvectors, output_testvectors
