
from __future__ import print_function
from argparse import ArgumentParser

import event_table
import decoder

def main() :

    parser = ArgumentParser()
    parser.add_argument("-i", "--in-file", required = True
        ,help = "Input events file to parse"
    )
    parser.add_argument("-v", "--verbose", default = False, action = "store_true"
        ,help = "Set verbose mode on"
    )
    parser.add_argument("-n", "--n-events", default = -1)
    parser.add_argument("--dump", default = "",
        help = "Dump contents for specified L0ID (hex string)"
    )
    args = parser.parse_args()

    events = decoder.load_events_from_file(args.in_file, args.verbose, int(args.n_events))
    print("Loaded {} events from file {}".format(len(events), args.in_file))

    table = event_table.EventTable()
    table.add_events(events) # auto-sorts by L0ID

    for i, l0id in enumerate(table.l0ids) :
        print("{} : {}".format(i, hex(l0id)))
    print("===")

    if args.dump :
        l0id_request = int(str(args.dump), 16)
        requested_event = table.event_at_l0id(l0id_request)

        if requested_event :
            print(80 * "=")
            print("Retrieved event with L0ID={}, N_WORDS_TOTAL={}, EMPTY={}".format(hex(requested_event.header_l0id), requested_event.n_words_total, requested_event.empty))
            requested_event.word_dump()
            print(80 * "=")
        else :
            print("Requested event with L0ID={} not found".format(hex(l0id_request)))
#    ee = table.event_at_l0id(0x16)
#    if ee :
#        print("Retrieved event with L0ID={}, N_WORDS_TOTAL={}, EMPTY={}".format(hex(ee.header_l0id), ee.n_words_total, ee.empty))
#        ee.word_dump()
#    else :
#        print("No event at requested L0ID")

    #print("XXX " + 55 * '-')
    #print("XXX module routing flags for {}:".format(args.input_file.split("/")[-1]))
    #for i, m in enumerate(et.mod_routing) :
    #    print("XXX {} : {} ({})".format(i, hex(m), m))

if __name__ == "__main__" :
    main()
