import json
from pathlib import Path

from .utils import get_schema_file
from .utils import validate_against_schema


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
        valid_ok, err = validate_against_schema(config_data, schema_type="test_config")
    except Exception as ex:
        return False, str(ex)
    return valid_ok, err


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
    expected_top_level = f"TopLevel_{test_name}.v"

    expected_test_module = test_location / Path(expected_test_module)
    expected_makefile = test_location / Path(expected_makefile)
    expected_top_level = test_location / Path(expected_top_level)

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
