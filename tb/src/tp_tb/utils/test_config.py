import json
import os
from pathlib import Path

from tp_tb.utils import utils


TEST_CONFIG_ENV = "COCOTB_TEST_CONFIG_FILE"


def get_testvector_files_from_config(test_config):

    testvector_config = test_config["testvectors"]

    input_testvectors = []
    output_testvectors = []
    testvec_dir = testvector_config["testvector_dir"]
    inputs = testvector_config["input"]
    outputs = testvector_config["output"]

    for i, port_config in enumerate([inputs, outputs]):
        n_ports = len(port_config)
        for j in range(n_ports):
            for pc in port_config:
                port_num, filename = zip(*pc.items())
                port_num = int(port_num[0])
                filename = str(filename[0])
                if port_num == j:
                    complete_filename = f"{testvec_dir}/{filename}"
                    p_testvec = Path(complete_filename)
                    file_ok = p_testvec.exists() and p_testvec.is_file()
                    if not file_ok:
                        raise Exception(
                            f"ERROR Expected testvector file (={complete_filename}) could not be found"
                        )
                    if i == 0:
                        input_testvectors.append(str(p_testvec))
                    else:
                        output_testvectors.append(str(p_testvec))
    return input_testvectors, output_testvectors


def get_valid_test_configs():

    p_test_config = utils.tb_test_config_directory()

    if p_test_config is None:
        return [], []

    good_tb = []
    bad_tb = []

    for itest, test_config in enumerate(p_test_config.glob("config_*.json")):
        valid, _ = check_and_inspect_config_file(test_config)

        if valid:
            good_tb.append(test_config)
        else:
            bad_tb.append(test_config)
    return good_tb, bad_tb


def get_config(config_filename=""):

    ##
    ## if nothing passed, try from ENV
    ##
    if not config_filename:
        config_filename = os.environ.get(TEST_CONFIG_ENV, "")
        if not config_filename:
            raise Exception(
                f"ERROR Could not get test configuration file from environment (={TEST_CONFIG_ENV})"
            )
    p = Path(config_filename)
    file_ok = p.exists() and p.is_file()
    if not file_ok:
        raise Exception(
            f"ERROR Test configuration file (={config_filename}) could not be found/opened"
        )
    return testbench_config_from_file(config_filename)


def testbench_config_from_file(config_file):

    with open(config_file, "r") as infile:
        config_data = json.load(infile)
        config = config_data["testbench_config"]
    return config


def input_args_from_config(config):
    with open(config, "r") as infile:
        data = json.load(infile)
        if "testbench_config" not in data:
            raise Exception(
                f'ERROR Top-level node "testbench_config" not found in provided test config file (={config}).'
            )
        test_config = data["testbench_config"]
        if "input_args" not in test_config:
            raise Exception(
                f'ERROR "input_args" not found in provided test config file (={config}).'
            )
        return test_config["input_args"]


def check_config_file(config_file):

    ##
    ## check that the file is OK
    ##
    p = Path(config_file)
    file_ok = p.exists() and p.is_file()
    if not file_ok:
        return False, f"Test config file (={config_file} could not be found or opened"

    ##
    ## schema is valid
    ##
    try:
        with open(config_file, "r") as infile:  # , open(schema_file) as schemafile:
            config_data = json.load(infile)
    except json.JSONDecodeError as ex:
        return False, f"Unable to decode JSON configuration file: {ex}"

    try:
        valid_ok, err = utils.validate_against_schema(
            config_data, schema_type="test_config"
        )
    except Exception as ex:
        return False, str(ex)
    return valid_ok, err


def find_toplevel_module_in_file(filename, top_level_name):
    """
    Looks for Verilog module named "top_level_name" in provided file "filename".

    Note: This method assumes that the format of the module definition is:
        ...
        module <top_level_name> #(
        ...

        If this fails, we can probably split all text by the module parameter
        list token "#(" instead as an alternative.
    """

    top_level_name = top_level_name.replace(".v", "")
    with open(filename, "r") as infile:
        for line in infile:
            line = line.strip()
            if "module" not in line:
                continue
            if "endmodule" in line:
                continue
            cols = line.split()
            module_name = cols[1]
            if module_name == top_level_name:
                return True
    return False


def inspect_test_config(config_file):

    config = testbench_config_from_file(config_file)
    run_config = config["run_config"]
    test_name = config["test_name"]

    ##
    ## check that the test area is setup
    ##
    test_location = Path(run_config["test_location"])

    expected_test_module = f"test_{test_name}.py"
    expected_makefile = "Makefile"
    expected_top_level_name = f"TopLevel_{test_name}.v"

    expected_test_module = test_location / Path(expected_test_module)
    expected_makefile = test_location / Path(expected_makefile)
    expected_top_level = test_location / Path(expected_top_level_name)

    file_ok = expected_test_module.exists() and expected_test_module.is_file()
    if not file_ok:
        return (
            False,
            f"ERROR Expected test module (={str(expected_test_module)}) not found",
        )
    file_ok = expected_top_level.exists() and expected_top_level.is_file()
    if not file_ok:
        return (
            False,
            f"ERROR Expected top level verilog (={str(expected_top_level)}) not found",
        )

    file_ok = find_toplevel_module_in_file(
        filename=str(expected_top_level), top_level_name=expected_top_level_name
    )
    if not file_ok:
        return (
            False,
            f"ERROR Expected top level module (={str(expected_top_level_name).replace('.v','')}) does not appear to be defined in file \"{str(expected_top_level)}\"",
        )

    file_ok = expected_makefile.exists() and expected_makefile.is_file()
    if not file_ok:
        return (
            False,
            f"ERROR Expected test Makefile (={str(expected_makefile)}) not found",
        )

    return True, None


def check_and_inspect_config_file(config_file):

    ##
    ## validate the provided configuration file
    ##
    config_ok, err = check_config_file(config_file)
    if not config_ok:
        return False, err

    ##
    ## insect the test configuration data itself
    ##
    config_ok, err = inspect_test_config(config_file)
    if not config_ok:
        return False, err

    return True, None


def config_from_file(config_file):

    config_ok, err = check_and_inspect_config_file(config_file)
    if not config_ok:
        return None, err

    config = testbench_config_from_file(config_file)
    return config, None
