from difflib import Differ
from argparse import ArgumentParser
import numpy as np
from columnar import columnar

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

    #if not bad_pos :
    #    return hex_string

    tmp = ""
    for idx, char in enumerate(hex_string) :

        if idx in bad_pos :
            tmp += Fore.RED + char
            tmp += Style.RESET_ALL
        else :
            # make it green for fun
            #tmp += Fore.RESET + char
            tmp += Fore.GREEN + char
    #print("{} ({}) : {} ({})".format(len(hex_string), hex_string, len(tmp), tmp))
    return tmp

def meta_field_diff(event0, event1, meta_type = "event_header") :

    h0 = [] 
    
    meta_field_names = None
    field_func0 = None
    field_func1 = None
    if meta_type == "event_header" :
        meta_field_names = event0.header_field_names()
        field_func0 = event0.header_field
        field_func1 = event1.header_field
    elif meta_type == "event_footer" :
        meta_field_names = event0.footer_field_names()
        field_func0 = event0.footer_field
        field_func1 = event1.footer_field

    for ih, field_names_i in enumerate(meta_field_names) :
        h0_i = []
        for ifield, field_name in enumerate(field_names_i) :
            field0 = field_func0(field_name)
            field1 = field_func1(field_name)
    
            error = ""
            if field0 != field1 :
                color = Fore.RED
                error = " ERROR"
            else :
                color = Fore.GREEN
            prev0 = "{}{}:{}".format(field_name, error, hex(int(field0)))
            prev1 = "{}{}:{}".format(field_name, error, hex(int(field1)))
            out_str = color + "{} / {}".format(prev0.replace(":",": "), prev1.split(":")[-1])
            h0_i.append(out_str)
        h0.append(h0_i)

    ##
    ## set all strings to be fixed length
    ##
    col_width_0 = max(len(word) for row in h0 for word in row) + 2

    tmp0 = []
    for row in h0 :
        tmp = [word.ljust(col_width_0) for word in row]
        tmp0.append(tmp)
    h0 = tmp0
    return h0

def diff_data_words(word0, word1, pass_through = False, mask = []) :

    word0_nibbles, word1_nibbles = list(str(word0)), list(str(word1))
    # the str representation of events.DataWord should always represent data as 65-bits
    if len(word0_nibbles) != len(word1_nibbles) :
        raise Exception("ERROR Incorrect data word lengths (word0={}, word1={})".format(len(str(word0)), len(str(word1))))

    bad_nibbles = []
    for i in range(len(word0_nibbles)) :
        nibble0 = word0_nibbles[i]
        nibble1 = word1_nibbles[i]
        if nibble0 != nibble1 and i not in mask :
            bad_nibbles.append(i)

    if pass_through :
        bad_nibbles = []

    diff = []
    for i in range(len(word0_nibbles)) :
        if i in bad_nibbles and i not in mask :
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

def diffprint(word0, word1, diff, indent = "", description = "") :

    if not description:
        print("{} {: <20}  {: <20}".format(indent, str(word0), str(word1)))
    else :
        print("{} {: <20}  {: <20}  {}".format(indent, str(word0), str(word1), description))

    if np.any(np.array(diff)) :
        dstr = diff_str(diff)
        print("{} {: <20} {: <20}".format(indent, dstr, dstr))

def order_modules(modules0, modules1) :

    idx0 = []
    idx1 = []

    out0 = []
    out1 = []
    remainders = []
    for i in range(len(modules0)) :
        mod0 = modules0[i]
        h0 = mod0.header_words[0]
        h01 = mod0.header_words[1]
        f = mod0.footer
        found_equal = False
        for j in range(len(modules1)) :
            mod1 = modules1[j]
            h1 = mod1.header_words[0]
            h11 = mod1.header_words[1] 
            f1 = mod1.footer
            if mod1 == mod0 :
                found_equal = True

                out0.append(mod0)
                out1.append(mod1)

                idx0.append(i)
                idx1.append(j)
                break

    for i, mod in enumerate(modules0) :
        if i not in idx0  and mod not in out0 :
            out0.append(mod)
    for i, mod in enumerate(modules1) :
        if i not in idx1 and mod not in out1 :
            out1.append(mod)

    return out0, out1

def compare_event(event0, event1, args) :

    l0id = event0.l0id
    indent = "{: <10}".format(" ")

    ##
    ## compare header words
    ##
    header_data_0, header_data_1 = event0.header_words, event1.header_words
    if len(header_data_0) != len(header_data_1) :
        raise Exception("ERROR Malformed headers")
    header_length = len(header_data_0)

    header_fields_0, header_fields_1 = event0.header_description_strings(), event1.header_description_strings()
    for i in range(header_length) :
        h0 = header_data_0[i]
        h1 = header_data_1[i]
        h0, h1, diff = diff_data_words(h0, h1)
        header_diff_strings = meta_field_diff(event0, event1, meta_type = "event_header")#, header_field_names)
        description = " ".join(header_diff_strings[i])
        diffprint(h0, h1, diff, indent = indent, description = description)

    ##
    ## compare modules
    ##
    modules_0, modules_1 = event0.get_modules(), event1.get_modules()
    n_modules_0, n_modules_1 = len(modules_0), len(modules_1)
    if n_modules_0 != n_modules_1 :
        print("{} Number of modules differ: {} / {}".format(indent, n_modules_0, n_modules_1))
    else :
        modules_0, modules_1 = order_modules(modules_0, modules_1)
        for i in range(len(modules_0)) :
            module0 = modules_0[i]
            module1 = modules_1[i]

            print("{} {}".format(indent, 40 * "-"))

            max_len = max( [len(module0), len(module1)] )
            for idx in range(max_len) :
                m0 = None
                m1 = None
                if idx < len(module0) :
                    m0 = module0.data_words[idx]
                if idx < len(module1) :
                    m1 = module1.data_words[idx]

                if m0 and m1 :
                    pass_through = False
                    mask = []
                    # mask out or ignore flagging module data as bad, only worry about module footer and header
                    if idx == 1 :
                        mask = np.arange(11, 19, 1)
                    elif idx >= 2 and idx != (len(module0) - 1):
                        pass_through = True
                    elif idx == (len(module0) - 1) : # footer
                        mask = np.arange(0, 11, 1)
                    m0, m1, diff = diff_data_words(m0, m1, pass_through = pass_through, mask = list(mask))
                    diffprint(m0, m1, diff, indent = indent)

                else :
                    if not m0 :
                        m0 = events.DataWord(0x0, False)
                    elif not m1 :
                        m1 = events.DataWord(0x0, False)
                    print("WARNING Module lengths are not the same!")
                    m0, m1, diff = diff_data_words(m0, m1, pass_through = pass_through, mask = np.arange(0, 19, 1))
                    diffprint(m0, m1, diff, indent = indent)
#
#            for idx, j in enumerate(range(len(module0))) :
#                m0 = module0.data_words[j]
#                m1 = module1.data_words[j]
#
#                pass_through = False
#                mask = []
#                # mask out or ignore flagging module data as bad, only worry about module footer and header
#                if idx == 1 :
#                    mask = np.arange(11, 19, 1)
#                elif idx >= 2 and idx != (len(module0) - 1):
#                    pass_through = True
#                elif idx == (len(module0) - 1) : # footer
#                    mask = np.arange(0, 11, 1)
#                m0, m1, diff = diff_data_words(m0, m1, pass_through = pass_through, mask = list(mask))
#                diffprint(m0, m1, diff, indent = indent)

    print("\n")
    ##
    ## compare footer words
    ##
    footer_data_0, footer_data_1 = event0.footer_words, event1.footer_words
    if len(footer_data_0) != len(footer_data_1) :
        raise Exception("ERROR Malformed footers")
    footer_length = len(footer_data_0)
    footer_fields_0, footer_fields_1 = event0.footer_description_strings(), event1.footer_description_strings()
    for i in range(footer_length) :
        f0 = footer_data_0[i]
        f1 = footer_data_1[i]
        f0, f1, diff = diff_data_words(f0, f1)
        footer_diff_strings = meta_field_diff(event0, event1, meta_type = "event_footer")
        description = " ".join(footer_diff_strings[i])
        diffprint(f0, f1, diff, indent = indent, description = description)

def compare_files(args) :

    filename0 = args.input[0]
    filename1 = args.input[1]
    print(80 * "=")
    print("File0: {}".format(filename0))
    print("File1: {}".format(filename1))

    l0id_request = -1
    if args.l0id :
        l0id_request = args.l0id
    events0 = events.load_events_from_file(filename0, endian = args.endian, n_to_load = args.n_events, l0id_request = l0id_request)
    events1 = events.load_events_from_file(filename1, endian = args.endian, n_to_load = args.n_events, l0id_request = l0id_request)

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
    parser.add_argument("-l", "--l0id", default = "", type = str
        ,help = "Request a specific L0ID to be diff'd [hex string format, e.g. 0x44]"
    )
    args = parser.parse_args()
    if args.l0id != "" :
        args.l0id = int(args.l0id, 16)

    ##
    ## diff
    ##
    compare_files(args)

if __name__ == "__main__" :
    main()
