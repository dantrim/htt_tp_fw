"""The TB creator CLI group."""
import sys

import click

from tp_tb.creator import creator


@click.group(name="create")
def cli():
    """The create CLI group."""


@click.option("-t", "--test-name", help="Give the test a name")
@click.option(
    "-i", "--n-inputs", help="Specify the number of input ports for the DUT", type=int
)
@click.option(
    "-o", "--n-outputs", help="Specify the number of output ports for the DUT", type=int
)
@click.option(
    "--software-block",
    is_flag=True,
    help="Indicate if you require a software block to be generated",
)
@cli.command()
def create(test_name, n_inputs, n_outputs, software_block):
    """Create a new test."""

    print(
        f'Creating test "{test_name}" with {n_inputs} inputs and {n_outputs} outputs.'
    )

    ##
    ## initialize minimal directory structure
    ##
    ok, err = creator.create_initial_directory_structure(test_name)
    if not ok:
        print(err)
        sys.exit(1)

    ##
    ## create the test utils file
    ##
    ok, err = creator.create_test_utils_file(test_name)
    if not ok:
        print(err)
        sys.exit(1)

    ##
    ## create test ports file
    ##
    ok, err = creator.create_test_ports_file(test_name, n_inputs, n_outputs)
    if not ok:
        print(err)
        sys.exit(1)

    ##
    ## create the test wrapper file
    ##
    ok, err = creator.create_test_wrapper(test_name)
    if not ok:
        print(err)
        sys.exit(1)

    ##
    ## create test/Makefile
    ##
    ok, err = creator.create_test_makefile(test_name)
    if not ok:
        print(err)
        sys.exit(1)

    ##
    ## create test/TopLevel
    ##
    ok, err = creator.create_test_toplevel(test_name, n_inputs, n_outputs)
    if not ok:
        print(err)
        sys.exit(1)

    ##
    ## create test/module.py
    ##
    ok, err = creator.create_test_module(test_name)
    if not ok:
        print(err)
        sys.exit(1)

    ##
    ## create test configuration file
    ##
    ok, err = creator.create_test_configuration(test_name, n_inputs, n_outputs)
    if not ok:
        print(err)
        sys.exit(1)

    ##
    ## all done!
    ##
    sys.exit(0)
