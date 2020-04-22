from difflib import Differ
from argparse import ArgumentParser
import numpy as np

from tb_utils import events
from colorama import Fore, Back, Style, init
init(autoreset = True)
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

def event_at_l0id(events_list, l0id) :

    event = None
    for e in events_list :
        if int(e.l0id) == int(l0id) :
            return e
    return event

def colored_dataword(dataword, bad_pos = []) :

    hex_string = str(dataword)

    if not bad_pos :
        return hex_string

    tmp = ""
    for idx, char in enumerate(hex_string) :

        if idx in bad_pos :
            tmp += Fore.RED + char
            tmp += Style.RESET_ALL
        else :
            tmp += char
    return tmp

def diff_data_words(word0, word1) :

    word0_nibbles, word1_nibbles = list(str(word0)), list(str(word1))
    if word0.is_start_of_event() :
        for i in [4,5,6,7] :
            word0_nibbles[i] = "9"
    # the str representation of events.DataWord should always represent data as 65-bits
    if len(word0_nibbles) != len(word1_nibbles) :
        raise Exception("ERROR Incorrect data word lengths (word0={}, word1={})".format(len(str(word0)), len(str(word1))))

    bad_nibbles = []
    for i in range(len(word0_nibbles)) :
        nibble0 = word0_nibbles[i]
        nibble1 = word1_nibbles[i]
        if nibble0 != nibble1 :
            bad_nibbles.append(i)

    diff = []
    for i in range(len(word0_nibbles)) :
        if i in bad_nibbles :
            diff.append(True)
        else :
            diff.append(False)

    return colored_dataword(word0, bad_nibbles), colored_dataword(word1, bad_nibbles), diff

def diff_str(diff_arr) :

    d = ""
    for x in diff_arr :
        if x :
            d += "^"
        else :
            d += " "
    return d

def print_words_with_diff(word0, word1, diff, indent = "") :

    print("{} {: <20} {: <20}".format(indent, str(word0), str(word1)))
    if np.any(np.array(diff)) :
        dstr = diff_str(diff)
        print("{} {: <20}{: <20}".format(indent, dstr, dstr))


def compare_event(event0, event1, args) :

    l0id = event0.l0id
    indent = "{: <10}".format("")

    ##
    ## compare header words
    ##
    header_data_0, header_data_1 = event0.header_words, event1.header_words
    if len(header_data_0) != len(header_data_1) :
        raise Exception("ERROR Malformed headers")
    header_length = len(header_data_0)
    for i in range(header_length) :
        h0 = header_data_0[i]
        h1 = header_data_1[i]
        h0, h1, diff = diff_data_words(h0, h1)
        print_words_with_diff(h0, h1, diff, indent = indent)

def compare_files(args) :

    filename0 = args.input[0]
    filename1 = args.input[1]
    print(80 * "=")
    print("File0: {}".format(filename0))
    print("File1: {}".format(filename1))

    events0 = events.load_events_from_file(filename0, endian = args.endian, n_to_load = args.n_events)
    dummy = events.DataEvent(0x44)
    #dummy1 = events.DataEvent(0x72)
    events0.append(dummy)
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
    ## sort the events by L0ID for further comparison
    ##
    events0 = sorted(events0, key = lambda x : x.l0id)
    events1 = sorted(events1, key = lambda x : x.l0id)
    all_l0ids = sorted(list(set(l0ids_0 + l0ids_1)))
    for ievent, l0id in enumerate(all_l0ids) :
        print("{: <10}".format(100 * "="))
        in_both = l0id in l0ids_0 and l0id in l0ids_1
        if not in_both :
            print("L0ID {} not in both files, skipping detailed comparison".format(hex(l0id)))
            continue
        e0, e1 = event_at_l0id(events0, l0id), event_at_l0id(events1, l0id)
        print("Comparing event at L0ID={}".format(hex(l0id)))
        compare_event(e0, e1, args)

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
