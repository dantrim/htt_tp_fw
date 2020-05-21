"""The TB diff CLI group."""

import sys
import click
from pathlib import Path

from ..utils import tb_diff
from ..utils import tb_dump
from ..utils import result_handler
from ..utils import simulator_support


def int_base_convert(value):
    value = str(value)
    if value[:2].lower() == "0x":
        return int(value[2:], 16)
    return int(value, 10)
    raise TypeError


class BasedIntParamType(click.ParamType):
    name = "integer"

    def convert(self, value, param, ctx):
        try:
            return int_base_convert(value)
        except TypeError:
            self.fail(
                "expected string for int() conversion, in either hexadecimal "
                '(leading "0x" required) or decimal value, got '
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        except ValueError:
            self.fail(
                f"{value!r} is not a valid integer, expecting "
                'either hexadecimal (leading "0x" required) or decimal input'
            )


BASED_INT = BasedIntParamType()


@click.group(name="diff")
def cli():
    """The diff CLI group."""


@cli.command()
@click.argument("input-file", type=click.File("rb", lazy=True))
@click.option(
    "-b", "--boundary", is_flag=True, help="Indicate event and module boundaries."
)
@click.option(
    "-p", "--parse", is_flag=True, help="Print out (any) decoded information."
)
@click.option(
    "-t",
    "--timestamp",
    is_flag=True,
    help="Indicate timestamps of each word in the file (if available).",
)
@click.option(
    "-n", "--n-events", default=0, type=int, help="Dump a specific number of events."
)
@click.option(
    "-l",
    "--l0id",
    default="",
    type=str,
    help="Print out a specific L0ID (can be comma-separated list for multiple, or a range indicated via <min>-<max>, e.g. 0x1-0x20).",
)
@click.option(
    "-c", "--word-count", is_flag=True, help="Indicate the overall word count."
)
@click.option(
    "-e",
    "--event-word-count",
    is_flag=True,
    help="Indicate the word count within each event.",
)
@click.option(
    "-a", "--all-opt", is_flag=True, help="Set all options (except for timestamp)."
)
@click.option(
    "--start-l0id", type=BASED_INT, help='Dump events with L0ID >= "start-l0id".'
)
@click.option(
    "--stop-l0id", type=BASED_INT, help='Do not dump events with L0ID > "stop-l0id".'
)
@click.option(
    "--list-l0id", is_flag=True, help="Print L0IDs for the events in the input file."
)
def dump(
    input_file,
    boundary,
    parse,
    timestamp,
    n_events,
    l0id,
    word_count,
    event_word_count,
    start_l0id,
    stop_l0id,
    list_l0id,
    all_opt,
):
    """Dump the contents of an *.evt file."""

    ##
    ## requested l0id
    ##
    l0id_to_load = []
    if "-" in l0id:
        l0id_to_load = list(
            range(
                int_base_convert(l0id.split("-")[0]),
                int_base_convert(l0id.split("-")[1]) + 1,
                1,
            )
        )
    if "," in l0id:
        l0id_to_load = [int_base_convert(x.strip()) for x in l0id.split(",") if x]
    if start_l0id or stop_l0id:
        if start_l0id and stop_l0id:
            l0id_to_load = list(
                range(int_base_convert(start_l0id), int_base_convert(stop_l0id) + 1, 1)
            )
        elif start_l0id and not stop_l0id:
            l0id_to_load = list(range(int_base_convert(start_l0id), 2 ** 16 + 1, 1))
        elif stop_l0id and not start_l0id:
            l0id_to_load = list(range(0, int_base_convert(stop_l0id) + 1, 1))

    ##
    ## this case doesn't make sense
    ##
    if l0id_to_load and n_events:
        print("ERROR Cannot request L0ID and N_EVENTS simultaneously")
        sys.exit(1)

    if all_opt:
        boundary = True
        parse = True
        timestamp = True
        word_count = True
        event_word_count = True

    tb_dump.dump_evt_file(
        input_file.name,
        do_boundary=boundary,
        do_parse=parse,
        do_timestamp=timestamp,
        n_events=n_events,
        l0id_to_load=l0id_to_load,
        do_total_word_count=word_count,
        do_event_word_count=event_word_count,
        list_l0id=list_l0id,
    )


@cli.command()
@click.argument("input", nargs=-1)
@click.option(
    "-q", "--quiet", is_flag=True, help="Do not print anything to standard output."
)
@click.option(
    "-r",
    "--result-only",
    is_flag=True,
    help="Simply return whether the test is passed or not.",
)
@click.option(
    "-e", "--event-detail", is_flag=True, help="Report event-level test details."
)
@click.option(
    "-d",
    "--detail",
    is_flag=True,
    help="Report test details in addition to final summary.",
)
def test_summary(input, result_only, event_detail, detail, quiet):
    """Dump the test results *.json file."""

    input_files = [str(x) for x in input]

    for i, f in enumerate(input_files):
        p = Path(f)
        if not (p.exists() and p.is_file()):
            print(f"ERROR Input file (={f}) could not be found.")
            sys.exit(1)
    import json

    data_results = []
    test_passed = True
    for ifile, filename in enumerate(input_files):
        with open(filename, "r") as infile:
            data = json.load(infile)
        data_results.append(data)
        test_passed = (
            test_passed and str(data["test_results"]["test_success"]).lower() == "true"
        )
    test_result_str = {True: "PASS", False: "FAIL"}[test_passed]
    if result_only or quiet:
        if not quiet:
            print(f"Test result: {test_result_str}")
        sys.exit({True: 0, False: 1}[test_passed])
    result_handler.dump_test_results(
        data_results, event_detail=event_detail, full_detail=detail
    )
    sys.exit({True: 0, False: 1}[test_passed])


@cli.command()
@click.argument("inputs", nargs=2)
@click.option(
    "-n",
    "--n-events",
    default=-1,
    type=int,
    help="The number of events to load and be diffed.",
)
@click.option(
    "-e",
    "--endian",
    default="little",
    type=click.Choice(["little", "big"], case_sensitive=True),
    help="Endian-ness of data within the files to load.",
)
@click.option(
    "-l",
    "--l0id",
    default=-1,
    type=BASED_INT,
    help="Select an event with a specific L0ID from the input files to diff.",
)
@click.option("-v", "--verbose", is_flag=True)
@click.option(
    "-t",
    "--table",
    is_flag=True,
    help="Print out results of the diff in a table at the end.",
)
@click.option(
    "--event-detail",
    is_flag=True,
    help="Print out more detailed information for each event when tabling is enabled.",
)
def diff(inputs, n_events, endian, l0id, verbose, table, event_detail):
    """Diff two *.evt files and test for differences."""
    diff, _ = tb_diff.compare_files(
        inputs[0],
        inputs[1],
        l0id,
        endian=endian,
        n_events=n_events,
        verbose=verbose,
        tabulate=(table, event_detail),
    )

    sys.exit(int(not diff))


@cli.command()
@click.option("-v", "--verbose", is_flag=True, help="Print out detailed reporting")
def update_makefile(verbose):
    """
    Update the QuestaSim makefile used by CocoTB to dump all signals (external AND internal)
    to output waveform file.
    """

    updated_ok, err = simulator_support.update_questa_makefile(verbose=verbose)
    if not updated_ok:
        if verbose and err:
            print(f"Makefile update: FAIL\n{err}")
        sys.exit(1)
    if verbose:
        print("Makefile updated: SUCCESS")
    sys.exit(0)
