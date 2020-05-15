import os
import struct

from .events import DataWord, timing_info_gen

from DataFormat import DataFormat

N_BYTES_PER_WORD = 9
N_WORDS_FOR_EVENT_HEADER = 6
N_WORDS_FOR_MODULE_HEADER = 2
N_WORDS_FOR_EVENT_FOOTER = 3
DATA_ENDIAN = "little"

def dump_evt_file(input_filename, n_events = 0, l0id_to_load = []
            ,do_boundary = False
            ,do_parse = False
            ,do_timestamp = False
            ,do_total_word_count = False
            ,do_event_word_count = False
            ,list_l0id = False
):
    """
    Loads the events from the input file "input_filename" and dumps the
    data words to standard out.
    """

    # just to be sure that the list contains type int
    l0id_to_load = [int(l) for l in l0id_to_load]

    s_in_event_header = False
    s_in_module = False
    s_in_event_footer = False

    module_type = ""
    expect_module_footer = False
    n_events_loaded = 0
    n_footer_count = 0
    n_module_count = 0
    dump_word = True
    n_word_read_total = -1
    n_word_read_event = -1
    l0ids_loaded = []

    header_word_start_idx = 0
    footer_word_start_idx = 0
    module_word_start_idx = 0

    ##
    ## timing
    ##
    timing_gen = None
    time_units = None
    if do_timestamp :
        timing_gen = timing_info_gen(input_filename)
        time_units = next(timing_gen)

    filesize = os.stat(input_filename).st_size
    with open(input_filename, "rb") as input_file :
        for _ in range(0, filesize, N_BYTES_PER_WORD) :
            data = input_file.read(N_BYTES_PER_WORD)
            if len(data) != N_BYTES_PER_WORD :
                raise Exception(f"ERROR Malformed event data file {input_filename}")
            fmt = { "little" : "<?Q", "big" : ">?Q" }[DATA_ENDIAN]
            is_metadata, contents = struct.unpack(fmt, data)
            data_word = DataWord(contents, is_metadata)
            dump_word = True

            n_word_read_total += 1
            n_word_read_event += 1

            if n_word_read_total == 0 and not data_word.is_start_of_event() :
                raise Exception(f"ERROR Malformed event data file (={input_Filename}): first word is not start of event!")

            if timing_gen :
                try :
                    data_word.set_timestamp(next(timing_gen), units = time_units)
                except StopIteration :
                    raise Exception(f"ERROR Timing file for loaded data file (={input_filename}) has incorrect number of words in it!")

            ##
            ## TRANSITION TO EVENT (HEADER) STATE
            ##
            if data_word.is_start_of_event() :
                header_word_start_idx = n_word_read_total
                footer_word_start_idx = -1
                module_word_start_idx = -1
                module_type = ""

                n_word_read_event = 0
                if s_in_event_footer and n_footer_count >= 3 :
                    n_events_loaded += 1
                    if n_footer_count > 3 :
                        print(f"WARNING Length of EVENT_FOOTER appears to be large (expect: {N_WORDS_FOR_EVENT_FOOTER} words, got: {n_footer_count} words)")
                if n_events and n_events_loaded >= n_events :
                    break
                s_in_event_header = True
                s_in_module = False
                s_in_event_footer = False
                n_footer_count = 0
                n_module_count = 0
                n_word_read_event = 0

            ##
            ## TRANSITION TO MODULE STATE
            ##
            if data_word.is_metadata and (not data_word.is_start_of_event()) and (not data_word.is_event_footer_start()) :
                s_in_event_header = False
                s_in_module = True
                s_in_event_footer = False

                seen_last_cluster = False
                module_footer = None

                expect_module_footer = False
                module_word = DataFormat.BitFieldWordValue(DataFormat.M_HDR, data_word.contents) 
                module_type = {0:"pix",1:"strip"}[module_word.getField("DET")]
                module_word_start_idx = n_word_read_total

            ##
            ## TRANSITION TO EVENT FOOTER STATE
            ##
            if data_word.is_event_footer_start() :
                s_in_event_header = False
                s_in_module = False
                s_in_event_footer = True
                footer_word_start_idx = n_word_read_total

            ##
            ## keep count of long (many words) we have been in the header
            ## so that we know when we are finished with the current
            ## event (the footer is a fixed number of words)
            ##
            if s_in_event_footer :
                n_footer_count += 1

            ##
            ## get the current event's L0ID from the event header
            ##
            if data_word.is_start_of_event() :
                header = DataFormat.BitFieldWordValue(DataFormat.EVT_HDR1, data_word.contents)
                current_l0id = header.getField("L0ID")
                l0ids_loaded.append(current_l0id)

            ##
            ## determine if we need to dump the current word based on some
            ## input arguments
            ##
            if len(l0id_to_load) :
                if int(current_l0id) not in l0id_to_load :
                    dump_word = False
                else :
                    dump_word = True
            if list_l0id :
                dump_word = False

            ##
            ## dump the word (this gets messy due to the different options of detail in the printout)
            ##
            if dump_word :
                extra_before = ""
                extra_after = ""
                boundary_string = ""
                
                ##
                ## print event boundary markers/separators
                ## (event header, module header, event footer)
                ##
                if do_boundary :
                    is_module = data_word.is_metadata and not (data_word.is_start_of_event() or data_word.is_event_footer_start())
                    word_width = len(str(data_word))
                    d_string = ""

                    if do_total_word_count :
                        word_width += 11

                    if do_event_word_count :
                        word_width += 7

                    if do_timestamp :
                        word_width += 15

                    if do_parse :
                        word_width += 55

                    sep = ""
                    if data_word.is_start_of_event() :
                        sep = "="
                        b_string = word_width * sep
                        d_string = f"[EVENT {n_events_loaded:03}]"
                        boundary_string = f"{b_string} {d_string}"
                    elif is_module :
                        sep = "-"
                        b_string = word_width * sep
                        d_string = f"[MODULE {n_events_loaded:03}/{n_module_count:03}]"
                        boundary_string += f"{b_string} {d_string}"
                        n_module_count = 1
                    elif data_word.is_event_footer_start() :
                        sep = "-"
                        b_string = word_width * sep
                        d_string = f"[FOOTER {n_events_loaded:03}]"
                        boundary_string = f"{b_string} {d_string}"

                    if boundary_string :
                        print(boundary_string)

                ##
                ## construct the string to print in front of (to the left of)
                ## the printed hex-formatted data word
                ##
                if do_total_word_count :
                    extra_before += f"{n_word_read_total:<9}"
                if do_timestamp :
                    extra_before += f"{data_word.timestamp:<13}" + " "

                ##
                ## construct the string to print after (to the right of) the
                ## printed hex-formatted data word
                ##

                ## this part gets kind of messy due to the decoding of the data words
                ## on the fly, especially for finding the module last cluster and footer
                field_str = ""
                if do_parse :
                    if header_word_start_idx >= 0 :
                        header_idx = (n_word_read_total - header_word_start_idx)
                        if header_idx < N_WORDS_FOR_EVENT_HEADER :
                            header_field_desc = [DataFormat.EVT_HDR1, DataFormat.EVT_HDR2, DataFormat.EVT_HDR3, DataFormat.EVT_HDR4, DataFormat.EVT_HDR5, DataFormat.EVT_HDR6][header_idx]
                            header_word = DataFormat.BitFieldWordValue(header_field_desc, data_word.contents)
                            field_str = []
                            for field in header_field_desc.fields :
                                if field.name.lower() == "spare" : continue
                                field_str.append(f"{field.name.upper()}: {hex(header_word.getField(field.name))}")
                            field_str = ", ".join(field_str)
                        else :
                            header_word_start_idx = -1
    
                    if module_word_start_idx >= 0 :
                        module_idx = (n_word_read_total - module_word_start_idx)
                        if module_idx < N_WORDS_FOR_MODULE_HEADER :
                            module_field_desc = [DataFormat.M_HDR, DataFormat.M_HDR2][module_idx] # DataFormat breaks its own naming conventions
                            module_data = data_word.contents
                            if module_idx == 1 :
                                module_data = 0xffffffff & (module_data >> 32)
                            module_word = DataFormat.BitFieldWordValue(module_field_desc, module_data)
                            field_str = []
                            for field in module_field_desc.fields :
                                if field.name.lower() == "spare" : continue
                                field_str.append(f"{field.name.upper()}: {hex(module_word.getField(field.name))}")
                            field_str = ", ".join(field_str)
                        else :
                            module_word_start_idx = -1
    
                    if s_in_module and (module_word_start_idx<0) :
                        word_desc = {"pix":DataFormat.PIXEL_CLUSTER,"strip":DataFormat.STRIP_CLUSTER}[module_type]
                        cluster_data_str = str(data_word).replace("0x","")[1:] # remove '0x' string and skip metadata flag
                        cluster_words = []
                        if module_type == "pix" :
                            cluster_words.append( int(cluster_data_str[:8],16) )
                            cluster_words.append( int(cluster_data_str[8:],16) )
                        elif module_type == "strip" :
                            cluster_words.append( int(cluster_data_str[:4],16) )
                            cluster_words.append( int(cluster_data_str[4:8], 16) )
                            cluster_words.append( int(cluster_data_str[8:12], 16) )
                            cluster_words.append( int(cluster_data_str[12:16], 16) )
                        cluster_words = [DataFormat.BitFieldWordValue(word_desc, x) for x in cluster_words]
    
                        last_cluster_idx = -1
                        last_cluster_in_word_idx = len(cluster_words)-1
    
                        if not seen_last_cluster and module_footer == None :
                            for i, clw in enumerate(cluster_words) :
                                is_last = clw.getField("LAST") == 1
                                if is_last :
                                    seen_last_cluster = True
                                    continue # skip to next
                                if seen_last_cluster :
                                    module_footer = cluster_words[i]
                                    break
                                else :
                                    module_footer = None
                        elif seen_last_cluster and module_footer == None :
                            module_footer = cluster_words[0]
                        else :
                            raise Exception("ERROR Failed to parse module footer properly")
    
                        if seen_last_cluster and module_footer :
                            field_str = []
                            footer_desc = {"pix":DataFormat.PIXEL_CL_FTR, "strip":DataFormat.STRIP_CL_FTR}[module_type]
                            module_footer = DataFormat.BitFieldWordValue(footer_desc, module_footer.value)
                            if module_footer.getField("FLAG") == 0x77 :
                                for field in module_footer.classobj.fields :
                                    if field.name.lower() == "spare" : continue
                                    field_str.append(f"{field.name.upper()}: {hex(module_footer.getField(field.name))}")
                                field_str = ", ".join(field_str)
    
                    if footer_word_start_idx >= 0 :
                        module_type = ""
                        footer_idx = (n_word_read_total - footer_word_start_idx)
                        if footer_idx < N_WORDS_FOR_EVENT_FOOTER :
                            footer_field_desc = [DataFormat.EVT_FTR1, DataFormat.EVT_FTR2, DataFormat.EVT_FTR3][footer_idx]
                            footer_word = DataFormat.BitFieldWordValue(footer_field_desc, data_word.contents)
                            field_str = []
                            for field in footer_field_desc.fields :
                                if field.name.lower() == "spare" : continue
                                field_str.append(f"{field.name.upper()}: {hex(footer_word.getField(field.name))}")
                            field_str = ", ".join(field_str)
                        else :
                            footer_word_start_idx = -1

                ##
                ## build the final strings to pre-pend (append) to the left (right) of the
                ## hex-string formatted data word
                ##
                if do_event_word_count :
                    if len(extra_after) : extra_after += "  "
                    extra_after += f"{n_word_read_event:<4}"

                if field_str :
                    if len(extra_after) : extra_after += "  "
                    extra_after += f"{field_str}"

                if extra_before :
                    extra_before += " "
                if extra_after :
                    extra_after = 3 * " " + extra_after

                ##
                ## now print it
                ##
                word_string = f"{extra_before}{data_word}{extra_after}"
                print(word_string)

    if list_l0id :
        print(20 * "-")
        print(f"Loaded {len(l0ids_loaded)} events:")
        for i, l in enumerate(l0ids_loaded) :
            l_str = hex(l)
            print(f" {i:<4}: {l_str}")
        print(20 * "-")

    
