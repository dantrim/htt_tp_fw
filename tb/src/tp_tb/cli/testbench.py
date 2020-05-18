import sys
import os
import click

from ..utils import test_config
from ..testbench import defined_testbenches


##
## B2B
##
@click.group(name="testbench")
def cli():
    """The testbench CLI group."""


@cli.command()
@click.argument("config")
def run(config):
    """Setup and run cocotb-based testbenches."""

    config_data, err = test_config.check_config_file(config)
    if err:
        print(f"Cannot run test: {err}")
        return

    run_config = config_data["run_config"]
    test_name = config_data["test_name"]

    test_location = run_config["test_location"]
    output_dir_name = run_config["output_directory_name"]

    ##
    ## communicate input args
    ##
    os.environ["COCOTB_TEST_CONFIG_FILE"] = os.path.abspath(config)

    ##
    ## start the test
    ##
    cwd_start = os.getcwd()
    relative_output_path = os.path.relpath(
        cwd_start, test_location
    )  # this is the output path relative to the test_location

    # I can't seem to get cocotb to run with absolute paths provided to the Makefile,
    # so I just move to the test_location here
    os.chdir(test_location)

    makefile = "Makefile"
    sim_build_out = f"{relative_output_path}/test_output/{output_dir_name}"
    cmd = f"SIM_BUILD={sim_build_out} TESTBENCH_TOPLEVEL=TopLevel_{test_name} TESTBENCH_TEST_MODULE=test_{test_name} WAVES=1 make -f {makefile}"
    cwd = os.getcwd()
    print(80 * "*")
    print(f"Beginning test: {test_name}")
    print(f"Current working directory: {cwd}")
    print(f"Running command: {cmd}")
    import subprocess

    subprocess.call(cmd, shell=True)


@cli.command()
def list():
    """List all available testbenches (and their tests)."""
    print("Defined testbenches:")
    for tb_name in defined_testbenches:
        print(f"{tb_name}")


@cli.command()
@click.argument("config")
@click.option("--dump", is_flag=True, help="Dump contents of valid test configuration.")
def check_config(config, dump):
    """Check/inspect a testbench's configuration (*.json) file."""
    parsed_config, err = test_config.check_config_file(config)
    if err:
        print(f"ERROR Provided test config (={config}) had errors encountered:")
        print(f" > {err}")
    else:
        print("Test configuration OK")
        if dump:
            import json

            test_name = parsed_config["test_name"]
            print(60 * "-")
            print(f'Configuration for test "{test_name}":')
            print(json.dumps(parsed_config, sort_keys=False, indent=4))
            print(60 * "-")
