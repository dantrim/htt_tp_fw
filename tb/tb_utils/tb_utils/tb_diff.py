from difflib import Differ
import re
from argparse import ArgumentParser
import numpy as np
from columnar import columnar

from tb_utils import events
from colorama import Fore, Back, Style, init
init(autoreset = True)
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

def remove_ansi(instring) :

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', instring)

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

            bad_flag0 = False
            bad_flag1 = False
            valid_flags = [0xab, 0x55, 0x77, 0xcd]
            if field_name == "FLAG" and field0 not in valid_flags :
                bad_flag0 = True
            if field_name == "FLAG" and field1 not in valid_flags :
                bad_flag1 = True
            bad_flag = bad_flag0 or bad_flag1
    
            error = ""
            if field0 != field1 or bad_flag :
                color = Fore.RED
                error = " DIFFERROR"
            else :
                color = Fore.GREEN
            prev0 = "{}{}:{}".format(field_name, error, hex(int(field0)))
            prev1 = "{}{}:{}".format(field_name, error, hex(int(field1)))
            if event0 is event1 :
                out_str = color + "{}".format(prev0.replace(":",": "))
            else :
                out_str = color + "{} / {}".format(prev0.replace(":",": "), prev1.split(":")[-1])
            h0_i.append(out_str)
        h0.append(h0_i)

    ##
    ## set all strings to be fixed length
    ##
    col_width_0 = max(len(word) for row in h0 for word in row[:-1]) + 2

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

    if str(word0) == str(dummy_data_word()) or str(word1) == str(dummy_data_word()) :
        #bad_nibbles = [i for i in range(len(word0_nibbles))]
        bad_nibbles = [i for i in range(len(word1_nibbles))]
        yep = True

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

    word0_str = str(word0)
    word1_str = str(word1)

    is_uneven = False
    mod_0_is_short = remove_ansi(word0_str) == str(dummy_data_word())
    mod_1_is_short = remove_ansi(word1_str) == str(dummy_data_word())
    if mod_0_is_short or mod_1_is_short :
        is_uneven = True
        mod_short_str = ""
        if mod_0_is_short :
            mod_short_str = Fore.RED + "File0" + Fore.RESET
            word0_str = Fore.RED + 19 * "x" + Fore.RESET
        else :
            mod_short_str = Fore.RED + "File1" + Fore.RESET
            word1_str = Fore.RED + 19 * "x" + Fore.RESET
        description = "{} ".format(mod_short_str) + Fore.RED + "SHORT MODULE" + Fore.RESET + "{} {}".format(":" if description else "", description)

    if not description:
        print("{} {: <20}  {: <20}".format(indent, word0_str, word1_str))
    else :
        print("{} {: <20}  {: <20}  {}".format(indent, word0_str, word1_str, description))

    if not is_uneven :
        if np.any(np.array(diff)) :
            dstr = diff_str(diff)
            print("{} {: <20} {: <20}".format(indent, dstr, dstr))

def dummy_data_word() :

    return events.DataWord(contents = 0xdeadbeefc0cac01a, is_metadata = True)

def dummy_module(test_module) :

    n_words = len(test_module)
    dummy_data = [x for x in test_module.header_words]
    dummy_data.append( dummy_data_word() for _ in range(n_words - len(test_module.header_words - 1)) )
    dummy_data.append( test_module.footer )
    dummy = events.ModuleData(data_words = dummy_data)
    #dummy = events.ModuleData(data_words = [dummy_data_word() for _ in range(n_words)])
    return dummy

def order_modules(modules0, modules1) :

    ##
    ## assume same # of modules
    ##
    out_0, out_1 = [], []
    idx_matched_0, idx_matched_1 = [], []

    unmatched_0, unmatched_1 = [], []
    for imodule0 in range( len(modules0) ) :
        module0 = modules0[imodule0]
        for imodule1 in range( len(modules1) ) :
            module1 = modules1[imodule1]
            n_words_0, n_words_1 = len(module0), len(module1)

            ##
            ## equality based on header/footer
            ##
            h0, h1 = [x.value for x in module0.header_words], [x.value for x in module1.header_words]
            f0, f1 = module0.footer.value, module1.footer.value
            headers_equal = h0 == h1
            footers_equal = f0 == f1
            module_equal = (headers_equal and footers_equal)
            #print("-> {} {} --> ? {}".format([hex(x) for x in h0], [hex(x) for x in h1], headers_equal))
            #print("-> {} {} --> ? {}".format(hex(f0), hex(f1), footers_equal))
            if module0 == module1 : # and imodule0 != 0 :
            #if module_equal :
                #print("FOUND EQUAL MODS")
                already_matched = module0 in out_0
                already_matched = already_matched and (module1 in out_1)
                if not already_matched :
                    idx_matched_0.append(imodule0)
                    out_0.append(module0)
    
                    idx_matched_1.append(imodule1)
                    out_1.append(module1)
            #else :
            #    if imodule0 in idx_matched_0 : pass
            #    if imodule1 in idx_matched_1 : pass
            #    print("MODULE FOUND NOT EQUAL")
            #    print(" --> HEADERS = {} {} ? {}".format([hex(x) for x in h0], [hex(x) for x in h1], headers_equal))
            #    print(" --> FOOTERS = {} {} ? {}".format(hex(f0), hex(f1), footers_equal))

    for imodule0 in range(len(modules0)) :
        if imodule0 not in idx_matched_0 :
            #print(60 * "*")
            #print("MODULES FOUND TO NOT MATCH")
            #module0 = modules0[imodule0]
            #for imodule1 in range(len(modules1)) :
            #    if imodule1 not in idx_matched_1 :
            #        module1 = modules1[imodule1]  
            #        h0, h1 = [x.value for x in module0.header_words], [x.value for x in module1.header_words]
            #        f0, f1 = module0.footer.value, module1.footer.value
            #        headers_equal = h0 == h1
            #        footers_equal = f0 == f1
            #        module_equal = (headers_equal and footers_equal)
            #        #print(" --> HEADERS = {} {} ? {}".format([hex(x) for x in h0], [hex(x) for x in h1], headers_equal))
            #        #print(" --> FOOTERS = {} {} ? {}".format(hex(f0), hex(f1), footers_equal))
                    
            unmatched_0.append( modules0[imodule0] )
    for imodule1 in range(len(modules1)) :
        if imodule1 not in idx_matched_1 :
            unmatched_1.append( modules1[imodule1] )

#    for mod in modules0 :
#        if mod not in out_0 :
#            out_0.append(mod)
#            #out_1.append(dummy_module(mod))
#    for mod in modules1 :
#        if mod not in out_1 :
#            out_1.append(mod)
#            #out_0.append(dummy_module(mod))

    return out_0, out_1, unmatched_0, unmatched_1
        
#    ##
#    ## PREVIOUS
#    ##
#
#    idx0 = []
#    idx1 = []
#
#    out0 = []
#    out1 = []
#    remainders = []
#    for i in range(len(modules0)) :
#        mod0 = modules0[i]
#        h0 = mod0.header_words[0]
#        h01 = mod0.header_words[1]
#        f = mod0.footer
#        found_equal = False
#        for j in range(len(modules1)) :
#            mod1 = modules1[j]
#            h1 = mod1.header_words[0]
#            h11 = mod1.header_words[1] 
#            f1 = mod1.footer
#            if mod1 == mod0 :
#                found_equal = True
#
#                out0.append(mod0)
#                out1.append(mod1)
#
#                idx0.append(i)
#                idx1.append(j)
#                break
#
#    for i, mod in enumerate(modules0) :
#        if i not in idx0  and mod not in out0 :
#            out0.append(mod)
#    for i, mod in enumerate(modules1) :
#        if i not in idx1 and mod not in out1 :
#            out1.append(mod)
#
#    return out0, out1

def module_footer_start_idx(data_word) :

    hex_str = str(data_word)
    hex_str_rev = "".join(list(hex_str)[::-1])
    back_idx = -1
    for i in range(0, len(hex_str_rev)-1, 2) :
        byte = hex_str_rev[i:i+2]
        if byte == "77" :
            back_idx = i + 2
    idx = len(hex_str) - back_idx
    return idx
   

def compare_event(event0, event1, args) :

    all_ok = True
    l0id = event0.l0id
    indent = "{: <10}".format(" ")

    n_words_0, n_words_1 = len(event0), len(event1)
    n_mod_0, n_mod_1 = event0.n_modules, event1.n_modules
    word_str = "{: <20} {:<20}".format("NWORDS   = {}".format(n_words_0), "NWORDS   = {}".format(n_words_1))
    err = ""
    if n_words_0 != n_words_1 :
        word_str = Fore.RED + word_str + Fore.RESET
        err = Fore.RED + "DIFFERROR" + Fore.RESET
    print("{} {} {: <20}".format(indent, word_str, err))
    mod_str = "{: <20} {: <20}".format("NMODULES = {}".format(n_mod_0), "NMODULES = {}".format(n_mod_1))
    err = ""
    if n_mod_0 != n_mod_1 :
        mod_str = Fore.RED + mod_str + Fore.RESET
        err = Fore.RED + "DIFFERROR" + Fore.RESET
    print("{} {} {: <20}".format(indent, mod_str, err))

    ##
    ## compare event header words
    ##
    print("{} {}".format(indent, 40 * "-"))
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

        if np.any(np.array(diff)) :
            all_ok = False

    ##
    ## compare modules
    ##
    modules_0, modules_1 = event0.get_modules(), event1.get_modules()
    n_modules_0, n_modules_1 = len(modules_0), len(modules_1)
    modules_0, modules_1, unmatched_modules_0, unmatched_modules_1 = order_modules(modules_0, modules_1)

    #print("len matched_0={} matched_1={}, unmatched_0={}, unmatched_1={}".format(len(modules_0), len(modules_1), len(unmatched_modules_0), len(unmatched_modules_1)))
    #print(" --> ")
    #for i in range(len(modules_0)) :
    #    print("     [{}] {}  {}".format(i, modules_0[i], modules_1[i]))

    ## print matched modules
    for imodule in range(len(modules_0)) :
        #print(" -> accessing imodule={} (len modules_0={} modules_1={})".format(imodule, len(modules_0), len(modules_1)))
        module0 = modules_0[imodule]
        module1 = modules_1[imodule]
        #print(" ==> module lengths = {} {}".format(len(module0), len(module1)))

        print("{} {}".format(indent, 40 * "-"))
        for iword in range( len(module0) ) :
            #print("   --> accessing word {}".format(iword))
            module_word0 = module0.data_words[iword]
            module_word1 = module1.data_words[iword]

            pass_through = False
            mask = []
            if iword == 1 :
                mask = np.arange(11, 19, 1)
            elif iword >= 2 and iword != (len(module0) - 1) :
                pass_through = True
            else :
                footer_idx = module_footer_start_idx(module_word0)
                if footer_idx >= 0 :
                    mask = np.arange(0, footer_idx, 1)
            description = ""
            if iword < 2 :
                module_header_diff_strings = meta_field_diff(module0, module1, meta_type = "event_header")
                description = " ".join(module_header_diff_strings[iword])
                if iword == 0 :
                    description = "{: <10} {}".format(Fore.RESET + "MODULE #{:03}".format(imodule), description) 
            elif (iword == len(module0) - 1) : # footer
                module_footer_diff_strings = meta_field_diff(module0, module1, meta_type = "event_footer")
                description = " ".join(module_footer_diff_strings[0])
            module_word0, module_word1, diff = diff_data_words(module_word0, module_word1, pass_through = pass_through, mask = list(mask))
            diffprint(module_word0, module_word1, diff, indent = indent, description = description)

            if np.any(np.array(diff)) :
                all_ok = False

    ## print unmatched modules
    for iunmatched, unmatched_modules in enumerate( [unmatched_modules_0, unmatched_modules_1] ) :
        for imodule, module in enumerate(unmatched_modules) :

            all_ok = False # we got here, which means there are differences

            print("{} {}".format(indent, 40 * "-"))
            for iword in range( len(module) ) :
                module_word = module.data_words[iword]
                description = ""
                if iword < 2 :
                    module_header_diff_strings = meta_field_diff(module, module, meta_type = "event_header")
                    description = " ".join(module_header_diff_strings[iword])
                    if iword == 0 :
                        description = "{: <10} {}".format(Fore.RED + "MODULE #{}/{:03}".format(iunmatched, imodule) + Fore.RESET, description) 
                elif (iword == len(module) - 1) :
                    # this is assumed to contain the footer
                    module_footer_diff_strings = meta_field_diff(module, module, meta_type = "event_footer")
                    description = " ".join(module_footer_diff_strings[0])
                    description = Fore.GREEN + "(FOOTER={})".format(hex(module.footer.value)) + Fore.RESET + " {}".format(description)
                if iword >= 1 and len(module) == 2 :
                    module_footer_diff_strings = meta_field_diff(module, module, meta_type = "event_footer")
                    description = " ".join(module_footer_diff_strings[0])
                    description = Fore.GREEN + "(FOOTER={})".format(hex(module.footer.value)) + Fore.RESET + " {}".format(description)
                    description = Fore.RED + "SHORTMODULEWARN" + Fore.RESET + " {}".format(description)
                
                word_fmt = { 0 : Fore.RED + "{: <20} {: ^20}".format(str(module_word), "nomatch") + Fore.RESET
                            , 1 : Fore.RED + "{: ^20} {: <20}".format("nomatch", str(module_word)) + Fore.RESET } [iunmatched]

                if not description:
                    print("{} {}".format(indent, word_fmt))
                else :
                    print("{} {} {}".format(indent, word_fmt, description))

    ##
    ## check if any data words somehow did not get grouped into a module
    ## (this can happen if a header/META word is missing)
    ##
    unused_module_data_0, unused_module_data_1 = event0.unmatched_data_words(), event1.unmatched_data_words()
    has_unused = len(unused_module_data_0) or len(unused_module_data_1)
    if has_unused :
        all_ok = False
        for iunused, unused_data_words in enumerate( [unused_module_data_0, unused_module_data_1] ) :
            print("{} {}".format(indent, 40 * "-"))
            for iword, word in enumerate(unused_data_words) :
                word_fmt = { 0 : Fore.BLUE + "{: <20} {: ^20}".format(str(word), " ") + Fore.RESET
                            ,1 : Fore.BLUE + "{: ^20} {: <20}".format(" ", str(word)) + Fore.RESET } [iunused]
                description = Fore.BLUE + "headless" + Fore.RESET
                print("{} {} {}".format(indent, word_fmt, description))

    ##
    ## compare event footer words
    ##
    print("{} {}".format(indent, 40 * "-"))
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

        if np.any(np.array(diff)) :
            all_ok = False
    print("{} {}".format(indent, 40 * "-"))

    return all_ok

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
        diff_ok = compare_event(e0, e1, args)
        result_str = { True : "YES", False : Fore.RED + "NO" + Fore.RESET }[diff_ok]
        print("{: <10} EVENT OK? {}".format("", result_str))

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
