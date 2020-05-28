import os
from pathlib import Path

from tp_tb.utils import utils


def creator_dir():
    p_tp_fw = utils.tp_fw_path()
    p_creator = p_tp_fw / "tb" / "src" / "tp_tb" / "creator"
    return p_creator


def test_dir_from_test_name(test_name):

    p_tp_fw = utils.tp_fw_path()
    p_testbench = p_tp_fw / "tb" / "src" / "tp_tb" / "testbench"
    p_test_dir = p_testbench / test_name
    return p_test_dir


def test_class_name(test_name):

    splits = test_name.strip().replace("-", "_").split("_")
    capital_splits = []
    for s in splits:
        capital_splits.append(s.capitalize())
    class_name = "".join(capital_splits)
    return class_name


def create_directory(path_string=""):

    if not path_string:
        return False, f"ERROR Empty path provided (={path_string})"

    try:
        os.mkdir(path_string)
    except OSError as ex:
        return False, f"{ex}"
    return True, None


def create_initial_directory_structure(test_name=""):

    # p_tp_fw = utils.tp_fw_path()
    # p_testbench = p_tp_fw / "tb" / "src" / "tp_tb" / "testbench"
    # dir_ok = p_testbench.exists() and p_testbench.is_dir()
    # if not dir_ok :
    #    return False, f"ERROR Could not find {p_testbench} directory"

    ##
    ## create directory for the new test
    ##
    p_test_dir = test_dir_from_test_name(test_name)
    ok, err = create_directory(str(p_test_dir))
    if not ok:
        return False, f"ERROR Could not create test directory: {err}"

    ##
    ## create __init__.py
    ##
    p_init_py_file = p_test_dir / "__init__.py"
    p_init_py_file.touch()
    file_ok = p_init_py_file.exists() and p_init_py_file.is_file()
    if not file_ok:
        return False, f"ERROR Could not create file: {p_init_py_file}"

    ##
    ## create generic readme file
    ##
    ok = create_readme(test_name, p_test_dir)
    if not ok:
        return False, "ERROR Failed ot create test README"

    ##
    ## create test/ directory
    ##
    p_test_subdir = p_test_dir / "test"
    ok, err = create_directory(str(p_test_subdir))
    if not ok:
        return False, f"ERROR Could not create the test sub-directory: {err}"

    return True, None


def create_readme(test_name, p_test_dir):

    p_readme = p_test_dir / "README.md"
    with open(str(p_readme), "w") as ofile:
        ofile.write(f"# Testbench for {test_name}\n")

    file_ok = p_readme.exists() and p_readme.is_file()
    return file_ok


def create_test_utils_file(test_name):

    p_test_dir = test_dir_from_test_name(test_name)
    p_test_utils_file = p_test_dir / f"{test_name}_utils.py"
    class_name = test_class_name(test_name)

    lines = [
        "",
        "def get_testvector_files(testvector_dir):",
        '\t"""',
        f"\t{class_name} specific testvector getter",
        '\t"""',
    ]

    with open(str(p_test_utils_file), "w") as ofile:
        for line in lines:
            ofile.write(f"{line}\n")

    file_ok = p_test_utils_file.exists() and p_test_utils_file.is_file()
    if not file_ok:
        return False, f'ERROR Could not create file "{str(p_test_utils_file)}"'
    return True, None


def create_test_ports_file(test_name, n_inputs, n_outputs):

    p_test_dir = test_dir_from_test_name(test_name)
    p_ports_file = p_test_dir / f"{test_name}_ports.py"
    class_name = test_class_name(test_name)

    lines = []
    lines.append("import enum")
    lines.append("")
    lines.append("from tp_tb.utils import port_descriptor")
    lines.append("")
    lines.append("")
    lines.append(f"class {class_name}Ports(port_descriptor.PortDescriptor):")
    lines.append("\tdef __init__(self):")
    lines.append("\t\tsuper().__init__()")
    lines.append("")
    lines.append("\tclass Inputs(enum.Enum):")
    for i in range(n_inputs):
        lines.append(f"\t\tInput_{i} = {i}")
    lines.append("")
    lines.append("\tclass Outputs(enum.Enum):")
    for i in range(n_outputs):
        lines.append(f"\t\tOutput_{i} = {i}")

    with open(str(p_ports_file), "w") as ofile:
        for line in lines:
            ofile.write(f"{line}\n")

    file_ok = p_ports_file.exists() and p_ports_file.is_file()
    if not file_ok:
        return False, f'ERROR Could not create file "{str(p_ports_file)}"'
    return True, None


def create_test_wrapper(test_name):

    p_test_dir = test_dir_from_test_name(test_name)
    p_wrapper_file = p_test_dir / f"{test_name}_wrapper.py"
    class_name = test_class_name(test_name)

    p_creator_dir = creator_dir()
    p_skeleton_wrapper = p_creator_dir / "CREATOR_SKELETON_wrapper.py"

    skeleton_ok = p_skeleton_wrapper.exists() and p_skeleton_wrapper.is_file()
    if not skeleton_ok:
        return (
            False,
            f'ERROR Creator skeleton file "{str(p_skeleton_wrapper)}" could not be found',
        )

    with open(str(p_wrapper_file), "w") as ofile:
        with open(str(p_skeleton_wrapper), "r") as skeleton_file:

            for skeleton_line in skeleton_file:
                new_line = skeleton_line.replace("CREATORTESTNAME", test_name).replace(
                    "CREATORCLASSNAME", class_name
                )
                ofile.write(new_line)

    file_ok = p_wrapper_file.exists() and p_wrapper_file.is_file()
    if not file_ok:
        return (
            False,
            f'ERROR Could not create test wrapper file "{str(p_wrapper_file)}"',
        )
    return True, None
