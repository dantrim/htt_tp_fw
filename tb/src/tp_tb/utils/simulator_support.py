import subprocess
import os
import sys
import shutil
from pathlib import Path
from .utils import tp_fw_path


def update_questa_makefile(verbose=False):
    """
    Update the QuestaSim makefile used by CocoTB to be able to
    show the full hierarchy of the design under test in the
    waveform viewer.
    """

    p_tp_fw = tp_fw_path()
    p_tb = p_tp_fw / "tb"
    if p_tb is None:
        err = "Could not find tp-fw/tb/ directory in current working directory"
        return False, err

    env_dir = p_tb / "env"
    if not env_dir.is_dir():
        err = f'Could not find expected "env" directory (={env_dir})'
        return False, err

    cocotb_cfg = env_dir / "bin" / "cocotb-config"
    if not cocotb_cfg.is_file():
        err = f"Could not find cocotb-config (={cocotb_cfg})"
        return False, err

    res = subprocess.run(
        [cocotb_cfg, "--makefiles"], stdout=subprocess.PIPE, encoding="utf-8"
    )
    if res.returncode:
        err = f"Unable to obtain makefile directory from cocotb-config: {res.stdout}"
        return False, err

    makefile_dir = str(res.stdout).strip()

    questa_makefile = Path(makefile_dir) / "simulators" / "Makefile.questa"
    if not questa_makefile.is_file():
        err = f"Unable to locate QuestaSim makefile (={questa_makefile})"
        return False, err

    default_makefile_dir = p_tb / "default_makefiles"
    default_questa_makefile = None
    if default_makefile_dir.is_dir():
        default_questa_makefile = default_makefile_dir / "Makefile.questa"
        if not default_questa_makefile.is_file():
            default_questa_makefile = None
            err = f'Failed to find default "Makefile.questa" file in {default_makefile_dir}'
            return False, err
    else:
        err = f"Failed to find {default_makefile_dir}"
        return False, err

    previous_mkfile_name = "prev_Makefile.questa"
    shutil.copy(questa_makefile, previous_mkfile_name)
    if verbose:
        print(
            f"Previous QuestaSim makefile stored at: {os.path.abspath(previous_mkfile_name)}"
        )

    add_lines = [
        'set WildcardFilter \\"Variable Constant Generic Parameter SpecParam Assertion Cover Endpoint ScVariable CellInternal ImmediateAssert VHDLFile\\"',
        "add wave -r /*",
        "set StdArithNoWarnings 1",
        "set NumericStdNoWarnings 1",
    ]

    with open(questa_makefile, "w") as ofile:
        with open(default_questa_makefile, "r") as ifile:

            waves_cmd_line_no = -1
            for iline, line in enumerate(ifile):

                if "ifeq" in line and "WAVES" in line:
                    waves_cmd_line_no = iline
                if iline == waves_cmd_line_no + 1 and waves_cmd_line_no > 0:
                    for inew, new_line in enumerate(add_lines):
                        new_line = f'@echo "{new_line}" >> $@'
                        ofile.write(f"\t{new_line}\n")
                ofile.write(f"{line}")
    if verbose:
        print(f"Updated QuestaSim Makefile: {questa_makefile}")
    return True, None
