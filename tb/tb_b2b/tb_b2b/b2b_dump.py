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

from argparse import ArgumentParser
from pathlib import Path

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
    if args.l0id == "" :
        args.l0id = -1
    else :
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
    for filename, event_list in events_map.items() :
        n_events = len(event_list)
        l0ids = set( [x.l0id for x in event_list] )

        if n_events_request > 0 and n_events != n_events_request :
            ok = False
            print("ERROR Input (={}) does not have requested number of events (={})"
                .format(filename, n_events_request))

        if l0id_request > 0 and l0id_request not in l0ids :
            ok = False
            print("ERROR Requested L0ID (={}) is not found in input file (={})"
                .format(hex(l0id_request), filename))

    return ok

def dump_events(filename, event_list, detailed_modules = False, write_out = False) :

    meta_output = []
    output = []
    meta_output.append(95 * "=")
    meta_output.append("Filename: {}".format(filename))
    for ievent, event in enumerate(event_list) :
        output.append("EVENTINFO  {}".format(93 * "-"))
        output.append("EVENTINFO  Event #{:03}: L0ID={}, N_modules={}".format(ievent, hex(event.l0id), event.n_modules))

        header_desc = event.header_description_strings()
        footer_desc = event.footer_description_strings()


        ##
        ## event header
        ##
        for iheader, header in enumerate(header_desc) :
            output.append("{}  HEADER[{:03}]  {}".format(event.header_words[iheader], iheader, header))

        ##
        ## module data
        ##
        modules = event.get_modules()
        for imodule, module in enumerate(modules) :

            desc = "MODULE[{:03}]".format(imodule)
            det_type = module.header_field("TYPE")
            
            for i, dw in enumerate(module.data_words) :
                if i == 0 :
                    module_desc = "  {}".format(", ".join(module.header_description_strings()[0].split(",")[:4]))
                # right now the footer (and cluster data besides the header) is meangingless
                #elif i == 1 :
                #    module_desc = "  {}".format(module.footer_description_strings()[0])
                else :
                    module_desc = ""
                mod_str = "{}  {}{}".format(dw, desc, module_desc)
                output.append(mod_str)
                #output.append("{}  {}".format(dw, desc))

            #module_header_desc = module.header_description_strings()
            #module_footer_desc = module.footer_description_strings()

            #spacer = "     "
            #for iheader, header in enumerate(module_header_desc) :
            #    dword = events.DataWord(module.header_words[iheader].value, iheader==0)
            #    desc = "MODULE[{:02}]".format(imodule)
            #    output.append("  {:04}  {}  {}  {}".format(word_cnt, dword, desc, header))
            #    word_cnt += 1

            #for icluster, cluster in enumerate(module.cluster_data) :
            #    dword = events.DataWorld(cluster.value)
            #    output.append("  {:04}  MODULE[{:02}]\t{}{}".format(word_cnt, imodule, dword, spacer))
            #    word_cnt += 1

            #for ifooter, footer in enumerate(module_footer_desc) :
            #    dword = events.DataWord(module.footer.value)
            #    output.append("  {:04}  MODULE[{:02}]\t{}{}{}".format(word_cnt, imodule, dword, spacer, footer))
            #    word_cnt += 1

        ##
        ## event footer
        ##
        for ifooter, footer in enumerate(footer_desc) :
            output.append("{}  FOOTER[{:03}]  {}".format(event.footer_words[ifooter], ifooter, footer))

    for line in meta_output :
        print(line)
    data_word_cnt = 0
    for line in output :
        if "EVENTINFO" in line :    
            print("{}".format(line.replace("EVENTINFO","").strip()))
            data_word_cnt = 0
        else :
            print("  {:04}  {}".format(data_word_cnt, line))
            data_word_cnt += 1

def main() :

    parser = ArgumentParser(description = "Script to inspect/compare output event files")
    parser.add_argument("-i", "--input", nargs = '*',
        help = "File(s) to inspect."
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
    parser.add_argument("-l", "--l0id", default = "", type = str,
        help = "Specific L0ID to inspect (hexadecimal)."
    )
    parser.add_argument("-w", "--write", action = "store_true", default = False,
        help = "Dump output to a text file."
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
    events_ok = check_events_map(events_map
            ,n_events_request = args.n_events
            ,l0id_request = args.l0id)
    # right now don't do anything with this...

    for filename, event_list in events_map.items() :
        dump_events(filename, event_list
            ,detailed_modules = args.dump_modules, write_out = args.write
        )


if __name__ == "__main__" :
    main()

