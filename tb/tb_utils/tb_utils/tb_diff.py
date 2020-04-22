from difflib import Differ
from argparse import ArgumentParser

from tb_utils import events

def compare_files(args) :

    filename0 = args.input[0]
    filename1 = args.input[1]
    print(80 * "=")
    print("File0: {}".format(filename0))
    print("File1: {}".format(filename1))

    events0 = events.load_events_from_file(filename0, endian = args.endian, n_to_load = args.n_events)
    #dummy = events.DataEvent(0x44)
    #dummy1 = events.DataEvent(0x72)
    #events0.append(dummy)
    #events0.append(dummy1)
    events1 = events.load_events_from_file(filename1, endian = args.endian, n_to_load = args.n_events)
    #dummy10 = events.DataEvent(0x72)
    #dummy11 = events.DataEvent(0x44)
    #events1.append(dummy10)
    #events1.append(dummy11)

    ##
    ## number of events
    ##
    n_events_0, n_events_1 = len(events0), len(events1)
    if n_events_0 != n_events_1 :
        print("Number of events differ")
        print("{: <10} Number of events in File0: {}".format("", n_events_0))
        print("{: <10} Number of events in File1: {}".format("", n_events_1))
    
    l0ids_0, l0ids_1 = [x.l0id for x in events0], [x.l0id for x in events1]
    ##
    ## find L0IDs of events that differ
    ##
    l0ids_set_0, l0ids_set_1 = set(l0ids_0), set(l0ids_1)
    if l0ids_set_0 != l0ids_set_1 :
        in_0_not_1 = list(l0ids_set_0 - l0ids_set_1)
        in_1_not_0 = list(l0ids_set_1 - l0ids_set_0)
        n_max = max( [len(in_0_not_1), len(in_1_not_0)] )
        print("L0ID differences found:")
        print("{: <10} {: <30} {: <30}".format("", "L0IDs in File0 NOT in File1", "L0IDs In File1 NOT in File0"))
        print("{: <10} {: <60}".format("", "-" * 60))
        for i in range(n_max) :
            l0, l1 = "", ""
            if i < len(in_0_not_1) :
                l0 = hex(in_0_not_1[i])
            if i < len(in_1_not_0) :
                l1 = hex(in_1_not_0[i])
            info_str = "{: <10} {: <30} {: <30}".format("", l0, l1)
            print(info_str)

    ##
    ## check of order of L0IDs is the same between the files (assuming that they are the same length)
    ##
    if n_events_0 == n_events_1 :
        if l0ids_0 != l0ids_1 and l0ids_set_0 == l0ids_set_1 :
            print("Events in different order between File0 and File1")
            print("{: <10} First event/L0ID where order differs:".format(""))
            for i in range(len(l0ids_0)) :
                if l0ids_0[i] != l0ids_1[i] :
                    print("{:<15} > Event #{}: File0 has L0ID={}, File1 has L0ID={}".format("", i, hex(l0ids_0[i]), hex(l0ids_1[i])))
                    break

    ##
    ## sort the events by L0ID
    ##

def main() :

    parser = ArgumentParser(description = "Simple diff between two evt files")
    parser.add_argument("-i", "--input", nargs = 2
        ,help = "The two files to be diff'd"
    )
    parser.add_argument("-n", "--n-events", default = -1, type = int
        ,help = "Number of events to load"
    )
    parser.add_argument("-e", "--endian", default = "little", type = str
        ,help = "Endian-ness of data evt files"
    )
    args = parser.parse_args()

    ##
    ## diff
    ##
    compare_files(args)

if __name__ == "__main__" :
    main()
