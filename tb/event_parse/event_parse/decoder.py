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
        return header_words, footer_words, module_data

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

        self.headerwords = []
        self.footerwords = []
        self.modules = []

        header_data, footer_data, module_data = event_data.head_foot_mod()

        for iword, word_desc in enumerate(EVT_HEADER_WORDS) :
            val = header_data[iword]
            self.headerwords.append(BitFieldWordValue(word_desc, value = val))

        for iword, word_desc in enumerate(EVT_FOOTER_WORDS) :
            val = footer_data[iword]
            self.footerwords.append(BitFieldWordValue(word_desc, value = val))

        for imod, mod_data in enumerate(module_data) :
            m = Module(mod_data)
            self.modules.append(m)
        

class Module :

    def __init__(self, module_data = []) :

        self.header1 = BitFieldWordValue(DataFormat.M_HDR, value = module_data[0])
        self.header2 = BitFieldWordValue(DataFormat.M_HDR2)
        self.data = []
        self.footer = None

        ##
        ## parse
        ##

        data_type = self.header1.getField("TYPE")
        data_type_raw = DataFormat.M_HDR_TYPE.RAW
        data_type_clus = DataFormat.M_HDR_TYPE.CLUSTERED

        det_type = self.header1.getField("DET")
        det_type_pix = DataFormat.M_HDR_DET.PIXEL
        det_type_strip = DataFormat.M_HDR_DET.STRIP

        first = True
        expectfooter = False

        for word in module_data[1:] :

            ##
            ## RAW
            ##

            if data_type == data_type_raw :

                raw_word_length = {
                    det_type_pix : DataFormat.PIXEL_RAW_BITS
                    ,det_type_strips : DataFormat.HCC_CLUSTER.nbits
                } [det_type]

                unpacker = SubwordUnpacker(word, DataFormat.WORD_LENGTH)
                empty = False
                if first :
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

                unpacker = SubwordUnpacker(word, DataFormat.WORD_LENGTH)
                empty = False

                if first :
                    val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                    self.header2.value = val
                while not empty :
                    if not expectfooter :
                        val, empty = unpacker.get(clus_word_length)
                        cluster_val = BitFieldWordValue(clus_word_format, val)
                        self.data.append(cluster_val)
                        expectfooter = cluster_val.getField("LAST") == 1
                    else :
                        val, empty = unpacker.get(clus_footer_length)
                        self.footer = BitFieldWordValue(clus_footer_format, val)
                        expectfooter = False
            


