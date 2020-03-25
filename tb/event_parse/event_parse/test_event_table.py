
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
    args = parser.parse_args()

    events = []
    with open(args.in_file, "rb") as input_file :
        events = decoder.load_events_from_file(input_file, args.verbose, int(args.n_events))
    print("Loaded {} events from file {}".format(len(events), args.in_file))

    table = event_table.EventTable()
    for ev in events :
        table.add_event(ev)
    table.sort_events_by_l0id()

    for i, l0id in enumerate(table.l0ids) :
        print("{} : {}".format(i, hex(l0id)))
    print("===")
    ee = table.event_at_l0id(0x16)
    if ee :
        print("Retrieved event with L0ID={}, N_WORDS_TOTAL={}, EMPTY={}".format(hex(ee.header_l0id), ee.n_words_total, ee.empty))
        ee.word_dump()
    else :
        print("No event at requested L0ID")

    #print("XXX " + 55 * '-')
    #print("XXX module routing flags for {}:".format(args.input_file.split("/")[-1]))
    #for i, m in enumerate(et.mod_routing) :
    #    print("XXX {} : {} ({})".format(i, hex(m), m))

if __name__ == "__main__" :
    main()
