from pathlib import Path

import cocotb

from tp_tb.testbench.evt_sync.evt_sync_ports import EvtSyncPorts


def get_testvector_files(
    testvec_dir, base_tp=EvtSyncPorts.Outputs.OUTPUT_0, which="input"
):

    if type(base_tp) != EvtSyncPorts.Outputs:
        raise Exception(f"ERROR base_tp must be of type {type(EvtSyncPorts.Outputs)}")

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
