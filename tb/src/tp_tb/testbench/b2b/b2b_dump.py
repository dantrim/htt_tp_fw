##
## Some utility to load event files and dump their contents in a useful
## way. Can be executed with file inputs, or used in an external module by
## passing in lists of events.
##
## NB For the most part this script is not B2B-specific, but is here for
## sand-boxing.
##
## author: Daniel Joseph Antrim // daniel.joseph.antrim@CERN.CH
## date: April 2020
##

import os
import struct
from argparse import ArgumentParser
from pathlib import Path

# from tb_utils import events, utils
from tp_tb.utils import events, utils


def check_input(args):

    for input in args.input:
        p = Path(input)
        exists = p.exists()
        is_file = p.is_file()
        if not (exists and is_file):
            raise Exception(f"ERROR Input file(={p}) not found")

    ##
    ## l0id
    ##
    if args.l0id == "":
        args.l0id = -1
    else:
        args.l0id = int(args.l0id, 16)


def load_events_from_inputs(args):

    input_files = args.input
    endian = args.endian
    n_events_request = int(args.n_events)
    l0id_request = int(args.l0id)

    out = []
    for filename in input_files:
        loaded_events = events.load_events_from_file(
            filename=filename,
            endian=endian,
            n_to_load=n_events_request,
            l0id_request=l0id_request,
            load_timing_info=args.time,
        )
        if len(loaded_events):
            out.append(loaded_events)

    if len(out) != len(input_files):
        raise Exception("ERROR Unable to load events from all inputs")

    return dict(zip(input_files, out))


def check_events_map(events_map, n_events_request=-1, l0id_request=-1):

    ok = True
    for filename, event_list in events_map.items():
        n_events = len(event_list)
        l0ids = set([x.l0id for x in event_list])

        if n_events_request > 0 and n_events != n_events_request:
            ok = False
            print(
                f"ERROR Input (={filename}) does not have requested number of events (={n_events_request})"
            )

        if l0id_request > 0 and l0id_request not in l0ids:
            ok = False
            print(
                f"ERROR Requested L0ID (={hex(l0id_request)}) is not found in input file (={filename})"
            )

    return ok


def dump_words(filename, endian="little", load_timing_info=False):

    path = Path(filename)
    ok = path.exists() and path.is_file()
    if not ok:
        raise Exception(f"Cannot find provided file {filename}")

    with open(filename, "rb") as input_file:
        filesize = os.stat(filename).st_size
        for _ in range(0, filesize, 9):
            data = input_file.read(9)
            if len(data) != 9:
                raise Exception(f"Malformed event data file {filename}")
            fmt = {"little": "<?Q", "big": ">?Q"}[endian]
            is_metadata, contents = struct.unpack(fmt, data)
            word = events.DataWord(contents, is_metadata)

            if load_timing_info:
                timestamp_str = f"{word.timestamp} ns"
                print(f"{timestamp_str: <15} : {word}")
            else:
                print(word)


def dump_events(filename, event_list, detailed_modules=False, load_timing_info=False):

    print(80 * "=")

    pad = 32 * "="
    print(f"{pad} DUMPING EVENTS {pad}")
    print(f"Input file : {filename}")
    print(f"Number of loaded events : {len(event_list)}")

    for ievent, event in enumerate(event_list):

        word_count = 0

        pad = 31 * "="
        print(f"{pad} NEW EVENT {ievent:03} {pad}")
        pad = 20 * "="
        print(
            "{pad} L0ID={hex(event.l0id)}, N_Modules={event.n_modules}, N_Words={len(event)} {pad}"
        )
        pad = 77 * "="
        print(pad)
        pad = 30 * "-"
        print(f"{pad} EVENT HEADER {ievent:03} {pad}")

        header_desc = event.header_description_strings()

        time_units = None
        if load_timing_info:
            time_units = event.header_words[0].timestamp_units

        ##
        ## event header
        ##
        for iheader, header in enumerate(header_desc):
            word_str = "{word_count: <6} {event.header_words[iheader]}"
            if load_timing_info:
                timestamp_str = f"{event.header_words[iheader].timestamp} {time_units}"
                word_str = f"{word_count: <6} {timestamp_str: <15} {event.header_words[iheader]}"
            print(f"{word_str}  HEADER[{iheader:03}] {header}")
            word_count += 1

        ##
        ## module data
        ##
        modules = event.get_modules()
        for imodule, module in enumerate(modules):
            pad = 15 * "- "
            print(
                f"{pad} MODULE HEADER {ievent:03}/{imodule:03} - N_Words={len(module)} {pad}"
            )

            header_desc = module.header_description_strings()
            footer_desc = module.footer_description_strings()

            for i, dw in enumerate(module.data_words):
                word_str = f"{word_count: <6} {dw}"
                if load_timing_info:
                    timestamp_str = f"{dw.timestamp} {time_units}"
                    word_str = f"{word_count: <6} {timestamp_str} {dw}"
                description = ""
                if i == 0:
                    description = header_desc[0]
                elif i == 1:
                    description = header_desc[1]
                elif i == (len(module) - 1):
                    description = footer_desc[0]
                print(f"{word_str}  MODULE[{i:03}] {description}")
                word_count += 1

        ##
        ## event footer
        ##
        footer_desc = event.footer_description_strings()
        pad = 15 * "- "
        print(f"{pad} EVENT FOOTER {ievent:03} {pad}")
        for ifooter, footer in enumerate(footer_desc):
            word_str = f"{word_count: <6} {event.footer_words[ifooter]}"
            if load_timing_info:
                timestamp_str = f"{event.footer_words[ifooter].timestamp} {time_units}"
                word_str = (
                    f"{word_count} {timestamp_str: <15} {event.footer_words[ifooter]}"
                )
            print(f"{word_str}  FOOTER[{ifooter:03}]  {footer}")
            word_count += 1


def main():

    parser = ArgumentParser(description="Script to inspect/compare output event files")
    parser.add_argument("-i", "--input", nargs="*", help="File(s) to inspect.")
    parser.add_argument(
        "--dump-modules",
        action="store_true",
        default=False,
        help="Report cluster data from each module",
    )
    parser.add_argument(
        "-e", "--endian", default="little", help="Endian-ness of input data."
    )
    parser.add_argument(
        "-n",
        "--n-events",
        default=-1,
        type=int,
        help="Number of events to load from input.",
    )
    parser.add_argument(
        "-l",
        "--l0id",
        default="",
        type=str,
        help="Specific L0ID to inspect (hexadecimal).",
    )
    parser.add_argument(
        "-t",
        "--time",
        default=False,
        action="store_true",
        help="Load timing files if found.",
    )
    parser.add_argument(
        "--raw",
        default=False,
        action="store_true",
        help="Simply dump the contents of the file, word by word",
    )

    ##
    ## get the inputs
    ##

    args = parser.parse_args()
    check_input(args)

    ##
    ## load
    ##

    if args.raw:
        for input_file in args.input:
            dump_words(input_file, load_timing_info=args.time)
    else:

        events_map = load_events_from_inputs(args)
        _ = check_events_map(
            events_map, n_events_request=args.n_events, l0id_request=args.l0id
        )
        # right now don't do anything with this...

        for filename, event_list in events_map.items():
            dump_events(filename, event_list, load_timing_info=args.time)


if __name__ == "__main__":
    main()
