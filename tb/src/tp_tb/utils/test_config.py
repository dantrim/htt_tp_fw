import json
from pathlib import Path


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
        return (
            False,
            f"ERROR Test config file (={config_file}) could not be found or opened",
        )

    ##
    ## parse the json configuration
    ##
    try:
        with open(config_file, "r") as infile:
            data = json.load(infile)
    except Exception:
        return False, f"ERROR Test config file (={config_file}) could not be parsed"

    ##
    ## TODO: rely on jsonschema to validate json data?
    ##

    config = data["testbench_config"]
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

    return config, None
