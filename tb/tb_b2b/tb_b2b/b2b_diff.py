from argparse import ArgumentParser
from pathlib import Path

from tb_b2b import b2b_utils
from tb_utils import events, utils

def check_input(args) :

    for input in args.input :
        p = Path(input)
        exists = p.exists()
        is_file = p.is_file()
        if not (exists and is_file) :
            raise Exception("ERROR Input file (={}) not found".format(p))

    ##
    ## l0id
    ##
    if args.l0id > 0 :
        args.l0id = int(args.l0id, 16)

def load_events_from_inputs(args) :

    input_files = args.input
    endian = args.endian
    n_events_request = int(args.n_events)
    l0id_request = int(args.l0id)

    out = []
    for filename in input_files :
        loaded_events = events.load_events_from_file(filename = filename
                                                ,endian = endian
                                                ,n_to_load = n_events_request
                                                ,l0id_request = l0id_request
        )
        if len(loaded_events) :
            out.append(loaded_events)

    if len(out) != len(input_files) :
        raise Exception("ERROR Unable to load events from all inputs")

    return dict(zip(input_files, out))

def check_events_map(events_map, n_events_request = -1, l0id_request = -1) :

    ok = True
    for filename, event_list in events_map :
        n_events = len(event_list)
        l0ids = set( [x.l0id for x in event_list] )

        if n_events_request > 0 and n_events != n_events_request :
            ok = False
            print("ERROR Input (={}) does not have requested number of events (={})"
                .format(filename, n_events_request))

        if l0id_request > 0 and l0id_reqest not in l0ids :
            ok = False
            print("ERROR Requested L0ID (={}) is not found in input file (={})"
                .format(hex(l0id_request), filename))


def main() :

    parser = ArgumentParser(description = "Script to inspect/compare output event files")
    parser.add_argument("-i", "--input", nargs = 2,
        help = "File to inspect. Will compare side-by-side if two files provided."
    )
    parser.add_argument("--dump-modules", action = "store_true", default = False,
        help = "Report cluster data from each module"
    )
    parser.add_argument("-e", "--endian", default = "little",
        help = "Endian-ness of input data."
    )
    parser.add_argument("-n", "--n-events", default = -1, type = int,
        help = "Number of events to load from input."
    )
    parser.add_argument("-l", "--l0id", default = -1, type = str,
        help = "Specific L0ID to inspect (hexadecimal)."
    )

    ##
    ## get the inputs
    ##

    args = parser.parse_args()
    check_input(args)

    ##
    ## load
    ##

    events_map = load_events_from_inputs(args)
    check_events_map(events_map
            ,n_events = args.n_events
            ,l0id_request = args.l0id
    )


if __name__ == "__main__" :
    main()

