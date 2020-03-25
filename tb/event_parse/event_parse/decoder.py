#!/bin/env python3

from __future__ import print_function
import sys
if sys.version_info[0] < 3 :
    from DataFormat.BitField import BitFieldWordDesc, BitFieldWordValue
else :
    from DataFormat.BitField import BitFieldWordDesc, BitFieldWordValue
from DataFormat.DataFormatIO import SubwordUnpacker
from DataFormat import DataFormat
EVT_HEADER_WORDS = DataFormat.headerwords
EVT_FOOTER_WORDS = DataFormat.footerwords

from b2b_test.blocks import b2b_utils

def padded_hex(i, l):
    given_int = i
    given_len = l

    hex_result = hex(given_int)[2:] # remove '0x' from beginning of str
    num_hex_chars = len(hex_result)
    extra_zeros = '0' * (given_len - num_hex_chars) # may not get used..

    return ('0x' + hex_result if num_hex_chars == given_len else
            '?' * given_len if num_hex_chars > given_len else
            '0x' + extra_zeros + hex_result if num_hex_chars < given_len else
            None)

def get_flag(word) :

    h = BitFieldWordValue(DataFormat.GenMetadata, word)
    return h.getField("FLAG")    

def is_start_of_event(flag) :

    return flag == DataFormat.EVT_HDR1_FLAG.FLAG

def is_start_of_event_footer(flag) :

    return flag == DataFormat.EVT_FTR1_FLAG.FLAG

def is_start_of_module(flag) :

    return flag == DataFormat.M_HDR_FLAG.FLAG

def is_valid_flag(flag) :

    return flag == DataFormat.EVT_HDR1_FLAG.FLAG \
            or flag == DataFormat.M_HDR_FLAG.FLAG \
            or flag == DataFormat.EVT_FTR1_FLAG.FLAG

def next_word(input_file) :

    meta_flag = bool(int.from_bytes(input_file.read(1), DataFormat.ENDIAN))
    data = int.from_bytes(input_file.read(8), DataFormat.ENDIAN)

    return meta_flag, data

def decode_events_from_file(input_file, verbose = False, n_events = -1) :

    meta_flag, data_word = next_word(input_file)

    events = []
    event = EventData()
    footer_count = 0
    in_footer = False

    while True :

        if not meta_flag :
            if len(input_file.read(1)) == 0 :
                if verbose :
                    print("End of Stream")
                pass
            else :
                print("ERROR: expected meta_flag, word = {}".format(data_word))
            break

        flag = get_flag(data_word)

        if is_start_of_event(flag) :
            if verbose :
                print("---- HEADER ----")
            for i in range(6) :
                if verbose :
                    print(hex(data_word))
                event.words.append(data_word)
                meta_flag, data_word = next_word(input_file)

        elif is_start_of_module(flag) :
            if verbose :
                print("---- MODULE ---- (meta = {})".format(meta_flag))
                print(hex(data_word))
            start_idx = len(event.words)
            event.words.append(data_word)
            event.n_modules += 1
            while True :
                meta_flag, data_word = next_word(input_file)
                if meta_flag :
                    break
                if verbose :
                    print("{} (meta = {})".format(hex(data_word), meta_flag))
                event.words.append(data_word)
            end_idx = len(event.words)
            event.module_bounds.append( (start_idx, end_idx) )

        elif is_start_of_event_footer(flag) :
            if verbose :
                print("---- FOOTER ----")
            for i in range(3) :
                if verbose :
                    print(hex(data_word))
                event.words.append(data_word)
                meta_flag, data_word = next_word(input_file)

            events.append(Event(event))
            if n_events > 0 and len(events) >= n_events :
                break
            event.clear()
        else :
            print("WHOOPS")

    return events

class EventData :

    def __init__(self) :

        self.words = []
        self.header_words = []
        self.footer_words = []
        self.data_words = []

        self.n_modules = 0
        self.module_bounds = []

    def clear(self) :
        self.words = []
        self.header_words = []
        self.footer_words = []
        self.data_words = []

        self.n_modules = 0
        self.module_bounds = []

    def add_header_data(self, data) :

        self.words.append(data)
        self.header_words.append(data)

    def head_foot_mod(self) :

        header_words = self.words[:6]
        footer_words = self.words[-3:]
        module_data = []
        for ib, mod_bounds in enumerate(self.module_bounds) :
            mod_data = self.words[mod_bounds[0]:mod_bounds[1]]
            module_data.append(mod_data)
        return header_words, footer_words, module_data, len(self.words)

    def print(self) :

        header_words, footer_words, module_data = self.head_foot_mod()

        sep = 55 * "="
        print(sep)
        print(" **************** PRINT EVENT DATA [START] ********************* ")
        print(" --------------- HEADER --------------------")
        for hw in header_words :
            print(hex(hw))
        for imod, mod in enumerate(module_data) :
            print(" -------------- MODULE [{}] -----------------".format(imod))
            for mw in mod :
                print(hex(mw))
        print(" --------------------- FOOTER ---------------------")
        for fw in footer_words :
            print(hex(fw))
        print(" **************** PRINT EVENT DATA [END] ********************* ")

class Event :

    def __init__(self, event_data = None) :

        # this isn't the safest rn, I assume everything is filled

        self._headerwords = []
        self._footerwords = []
        self._modules = []
        self._n_words_total = 0

        header_data, footer_data, module_data, n_words_total = event_data.head_foot_mod()

        for iword, word_desc in enumerate(EVT_HEADER_WORDS) :
            val = header_data[iword]
            self._headerwords.append(BitFieldWordValue(word_desc, value = val))

        for iword, word_desc in enumerate(EVT_FOOTER_WORDS) :
            val = footer_data[iword]
            self._footerwords.append(BitFieldWordValue(word_desc, value = val))

        for imod, mod_data in enumerate(module_data) :
            m = Module(mod_data)
            self._modules.append(m)

        self._n_words_total = n_words_total

    @property
    def n_words_total(self) :
        return self._n_words_total

    @property
    def header(self) :
        return self._headerwords

    @property
    def header_l0id(self) :
        return self._headerwords[0].getField("L0ID")

    @property
    def header_trk_type(self) :
        return self._headerwords[0].getField("TRK_TYPE")

    @property
    def header_flag(self) :
        return self._headerwords[0].getField("FLAG")

    @property
    def header_bcid(self) :
        return self._headerwords[1].getField("BCID")

    @property
    def header_runnumber(self) :
        return self._headerwords[1].getField("RUNNUMBER")

    @property
    def header_status(self) :
        return self._headerwords[5].getField("STATUS")

    @property
    def header_crc(self) :
        return self._headerwords[5].getField("CRC")

    @property
    def footer(self) :
        return self._footerwords

    @property
    def footer_flag(self) :
        return self._footerwords[0].getField("FLAG")

    @property
    def footer_meta_count(self) :
        return self._footerwords[0].getField("META_COUNT")

    @property
    def footer_hdr_crc(self) :
        return self._footerwords[0].getField("HDR_CRC")

    @property
    def footer_error_flags(self) :
        return self._footerwords[1].getField("ERROR_FLAGS")

    @property
    def footer_word_count(self) :
        return self._footerwords[2].getField("WORD_COUNT")

    @property
    def footer_crc(self) :
        return self._footerwords[2].getField("CRC")

    @property
    def modules(self) :
        return self._modules

    @property
    def empty(self) :
        return self.n_words_total == (len(self.header) + len(self.footer))

    def word_dump(self) :

        print("EVENT DUMP: L0ID={}, EMPTY={}, N_MODULES={}".format(hex(self.header_l0id), self.empty, len(self.modules))) 
        for word in self.header :
            print("EVENT DUMP: HEADER      {}".format(padded_hex(word.value, 16)))
        for imod, module in enumerate(self.modules) :
            for data in module.raw_data :
                print("EVENT DUMP: MODULE[{:03}] {}".format(imod, padded_hex(data, 16)))
        for word in self.footer :
            print("EVENT DUMP: FOOTER      {}".format(padded_hex(word.value, 16)))

class Module :

    def __init__(self, module_data = []) :

        self.header1 = BitFieldWordValue(DataFormat.M_HDR, value = module_data[0])
        self.header2 = BitFieldWordValue(DataFormat.M_HDR2)
        self.data = []
        self.footer = None
        self.n_words_total = len(module_data)

        self.raw_data = module_data

        ##
        ## parse
        ##

        data_type = self.header1.getField("TYPE")
        data_type_raw = DataFormat.M_HDR_TYPE.RAW
        data_type_clus = DataFormat.M_HDR_TYPE.CLUSTERED

        det_type = self.header1.getField("DET")
        det_type_pix = DataFormat.M_HDR_DET.PIXEL
        det_type_strip = DataFormat.M_HDR_DET.STRIP

        is_pix = (det_type == det_type_pix)
        is_strip = (det_type == det_type_strip)

        expectfooter = False

        for iword, word in enumerate(module_data[1:]) :

            ##
            ## RAW
            ##
            unpacker = SubwordUnpacker(word, DataFormat.WORD_LENGTH)
            empty = False

            if data_type == data_type_raw :

                raw_word_length = {
                    det_type_pix : DataFormat.PIXEL_RAW_BITS
                    ,det_type_strips : DataFormat.HCC_CLUSTER.nbits
                } [det_type]

                if iword == 0 :
                    val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                    self.header2.value = val
                while not empty :
                    val, empty = unpacker.get(raw_word_length)
                    self.data.append(val)

            ##
            ## CLUSTER
            ##

            elif data_type == data_type_clus :

                clus_word_format = {
                    det_type_pix : DataFormat.PIXEL_CLUSTER
                    ,det_type_strip : DataFormat.STRIP_CLUSTER
                } [det_type]
                clus_word_length = clus_word_format.nbits

                clus_footer_format = {
                    det_type_pix : DataFormat.PIXEL_CL_FTR
                    ,det_type_strip : DataFormat.STRIP_CL_FTR
                } [det_type]
                clus_footer_length = clus_footer_format.nbits

                if iword == 0 :
                    val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                    self.header2.value = val

                # test for empty module
                if len(module_data[1:]) == 1 : #and det_type == det_type_strip :
                    tmp_words = []
                    while not empty :
                        val, empty = unpacker.get(clus_word_length)
                        tmp_words.append(val)
                    for tw in tmp_words :
                        flag = (tw >> (clus_word_length - 8)) & 0xff
                        if flag == DataFormat.CL_FTR_FLAG.FLAG :
                            self.footer = BitFieldWordValue(clus_footer_format, tw)
                        else :
                            self.data.append( BitFieldWordValue(clus_word_format, tw) )
                else :
                    while not empty :

                        if not expectfooter and self.footer == None :
                            val, empty = unpacker.get(clus_word_length)
                            cluster_val = BitFieldWordValue(clus_word_format, val)
                            self.data.append(cluster_val)
                            expectfooter = cluster_val.getField("LAST") == 1
                        else :
                            val, empty = unpacker.get(clus_footer_length)
                            if not self.footer :
                                self.footer = BitFieldWordValue(clus_footer_format, val)
                                break
                            expectfooter = False

        if data_type == data_type_clus and (self.footer == None  or self.footer == 0x0) :
            raise Exception("ERROR Failed to find FOOTER for clustered data")

    @property
    def header_flag(self) :
        return self.header1.getField("FLAG")

    @property
    def header_type(self) :
        return self.header1.getField("TYPE")

    @property
    def header_det(self) :
        return self.header1.getField("DET")

    @property
    def header_routing(self) :
        return self.header1.getField("ROUTING")

    @property
    def header_modid(self) :
        return self.header2.getField("MODID")

    @property
    def header_modtype(self) :
        return self.header2.getField("MODTYPE")

    @property
    def header_orientation(self) :
        return self.header2.getField("ORIENTATION")

    @property
    def footer_flag(self) :
        if self.footer is None : return 0x0
        return self.footer.getField("FLAG")

    @property
    def footer_count(self) :
        if self.footer is None : return 0x0
        return self.footer.getField("COUNT")

    @property
    def n_clusters(self) :
        return self.footer_count

    @property
    def footer_error(self) :
        if self.footer is None : return 0x0
        return self.footer.getField("ERROR")

    def routing_dest(self) :

        """
        Parse the module routing flags and determine B2B output
        """

        dest_list = set()
        routing_flags = self.header_routing
        for output in b2b_utils.B2BIO.B2BOutputs :
            is_amtp = "amtp" in output.name.lower()
            tp_num = int(output.name.split("_")[-1])
            idx = int(output.value)

            routing_index = {
                True : 4
                ,False : 2
            } [is_amtp]

            tp_offset = {
                True : 0
                ,False : 48
            } [is_amtp]

            mask = {
                True : 0xf
                ,False : 0x3
            } [is_amtp]

            offset = tp_offset + (tp_num * routing_index)
            mask = (mask << offset)
            routed = (routing_flags & mask) != 0
            if routed :
                dest_list.add(idx)

        return dest_list

    def module_type_str(self) :

        det_type = self.header_det
        out_type = None
        if det_type == DataFormat.M_HDR_DET.PIXEL :
            out_type = "PIXEL"
        elif det_type == DataFormat.M_HDR_DET.STRIP :
            out_type = "STRIP"
        return out_type

    @property
    def cluster_data(self) :
        return self.data
