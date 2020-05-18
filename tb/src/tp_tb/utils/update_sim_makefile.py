#!/bin/env python

import subprocess
import os
import sys
import shutil
from pathlib import Path


def main():

    """
    Update the QuestaSim makefile to be able to show the full hierarchy
    of the design under test in the waveform viewer.
    """

    pwd = Path(os.getcwd())
    dir_above, found, dir_below = str(pwd).partition("tp-fw/tb")
    if not found:
        print(
            "Could not find tp-fw/tb directory in current working dir (={})".format(
                str(pwd)
            )
        )
        sys.exit(1)

    env_dir = Path(dir_above + found) / "env"
    if not env_dir.is_dir():
        print('Could not find expected "env" directory (={})'.format(env_dir))
        sys.exit(1)

    cocotb_cfg = env_dir / "bin" / "cocotb-config"
    if not cocotb_cfg.is_file():
        print("Could not find cocotb-config (={})".format(cocotb_cfg))
        sys.exit(1)

    res = subprocess.run(
        [cocotb_cfg, "--makefiles"], stdout=subprocess.PIPE, encoding="utf-8"
    )
    if res.returncode:
        print(
            "Unable to obtain makefile directory from cocotb-config: {}".format(
                res.stdout
            )
        )
        sys.exit(1)

    makefile_dir = str(res.stdout).strip()

    questa_makefile = Path(makefile_dir) / "simulators" / "Makefile.questa"
    if not questa_makefile.is_file():
        print("Unable to locate QuestaSim makefile (={})".format(questa_makefile))
        sys.exit(1)

    default_makefile_dir = pwd / "default_makefiles"
    default_questa_makefile = None
    if default_makefile_dir.is_dir():
        default_questa_makefile = default_makefile_dir / "Makefile.questa"
        if default_questa_makefile.is_file():
            print(
                "Using default QuestaSim makefile found in {}".format(
                    default_makefile_dir
                )
            )
    else:
        # copy cocotb one
        mkfile_name = str(questa_makefile).split("/")[-1]
        shutil.copy(questa_makefile, "default_{}".format(mkfile_name))
        print(
            'Created default QuestaSim makefile (="{}") in current directory'.format(
                mkfile_name
            )
        )

        default_questa_makefile = pwd / mkfile_name
        if default_questa_makefile.is_file():
            print(
                "Using default QuestaSim makefile found in {}".format(
                    default_questa_makefile
                )
            )

    if not default_questa_makefile:
        print("Unable to find default QuestaSim makefile")
        sys.exit(1)

    previous_mkfile_name = "prev_Makefile.questa"
    shutil.copy(questa_makefile, previous_mkfile_name)
    print(
        "Previous QuestaSim makefile stored at {}".format(
            os.path.abspath(previous_mkfile_name)
        )
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
                    for new_line in add_lines:
                        new_line = '@echo "{}" >> $@'.format(new_line)
                        ofile.write("\t{}\n".format(new_line))
                ofile.write("{}".format(line))
    print("Updated QuestSim Makefile: {}".format(questa_makefile))


if __name__ == "__main__":
    main()
