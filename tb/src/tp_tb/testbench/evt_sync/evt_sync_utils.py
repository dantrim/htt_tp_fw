import enum
from pathlib import Path

import cocotb


class EvtSyncIO:
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

    @staticmethod
    def allowed_outputs():
        outputs = set()
        for output in EvtSyncIO.Outputs:
            outputs.add(str(output.name))
        return outputs

    @staticmethod
    def simplename(io_enum):
        return str(io_enum.name).replace("_", "")


def get_testvector_files(
    testvec_dir, base_tp=EvtSyncIO.Outputs.OUTPUT_0, which="input"
):

    if type(base_tp) != EvtSyncIO.Outputs:
        raise Exception(f"ERROR base_tp must be of type {type(EvtSyncIO.Outputs)}")

    tdir = Path(str(testvec_dir))
    ok = tdir.exists() and tdir.is_dir()
    if not ok:
        raise Exception(
            f"ERROR Provided testvector directory (={str(testvec_dir)}) not found"
        )

    if which.lower() == "output":
        raise Exception(
            "ERROR Test evt_sync does not yet handle finding output testvector files"
        )

    cocotb.log.warning("WARNING Setting SRC as AMTP_0 when grabbing testvectors")
    base_tp_str = "AMTP0"

    b2b_inputs_fmt = f"TPtoSync_src{base_tp_str}"
    b2b_inputs = [
        f"{b2b_inputs_fmt}_dest{x}.evt"
        for x in [
            "AMTP1",
            "AMTP2",
            "AMTP3",
            "AMTP4",
            "AMTP5",
            "AMTP6",
            "AMTP7",
            "AMTP8",
            "AMTP9",
            "AMTP10",
            "AMTP11",
            "SSTP0",
            "SSTP1",
        ]
    ]

    cluster_inputs_fmt = f"ClusterToSyncEngine_{base_tp_str}"
    cluster_inputs = [
        f"{cluster_inputs_fmt}_{x}.evt"
        for x in ["Pixel0", "Pixel1", "Strip0", "Strip1"]
    ]

    ordered_files = b2b_inputs
    ordered_files += cluster_inputs
    ordered_files = [f"{testvec_dir}/{x}" for x in ordered_files]
    return ordered_files
