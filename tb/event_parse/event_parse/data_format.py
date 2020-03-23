from __future__ import print_function
import sys
if sys.version_info[0] < 3 :
    from DataFormat.BitField import BitFieldWordDesc, BitFieldWordValue
else :
    from DataFormat.BitField import BitFieldWordDesc, BitFieldWordValue
from DataFormat import DataFormat
EVT_HEADER_WORDS = DataFormat.headerwords
EVT_FOOTER_WORDS = DataFormat.footerwords

from b2b_test.blocks import b2b_utils

class Event :

    """
    Store a given event's data
    """

    def __init__(self) :

        # the event header information
        self.headerwords = []
        for word in EVT_HEADER_WORDS :
            self.headerwords.append(BitFieldWordValue(word))

        # module data
        self.modules = []

        # the event footer information
        self.footerwords = []
        for word in EVT_FOOTER_WORDS :
            self.footerwords.append(BitFieldWordValue(word))

        # probably don't need data members, but the property's getters
        # should just parse the stored data words
        # meta
        self._l0id = 0x0

    @property
    def header_l0id(self) :
        return self.headerwords[0].getField("L0ID")

    @property
    def header_trk_type(self) :
        return self.headerwords[0].getField("TRK_TYPE")

    @property
    def header_flag(self) :
        return self.headerwords[0].getField("FLAG")

    @property
    def header_bcid(self) :
        return self.headerwords[1].getField("BCID")

    @property
    def header_runnumber(self) :
        return self.headerwords[1].getField("RUNNUMBER")

    @property
    def header_status(self) :
        return self.headerwords[5].getField("STATUS")

    @property
    def header_crc(self) :
        return self.headerwords[5].getField("CRC")

    @property
    def footer_flag(self) :
        return self.footerwords[0].getField("FLAG")

    @property
    def footer_meta_count(self) :
        return self.footerwords[0].getField("META_COUNT")

    @property
    def footer_hdr_crc(self) :
        return self.footerwords[0].getField("HDR_CRC")

    @property
    def footer_error_flags(self) :
        return self.footerwords[1].getField("ERROR_FLAGS")

    @property
    def footer_word_count(self) :
        return self.footerwords[2].getField("WORD_COUNT")

    @property
    def footer_crc(self) :
        return self.footerwords[2].getField("CRC")


class Module :

    """
    Store module data
    """

    def __init__(self) :

        # module header information (64-bit word + 32-bit word)
        self.header1 = BitFieldWordValue(DataFormat.M_HDR)
        self.header2 = BitFieldWordValue(DataFormat.M_HDR2)

        # module data
        # somewhere these should be absorbed into separate classes (e.g. Cluster or Raw?)
        self.words = [] # 16-bit (32-bit) wide words for strip (pixel)

        # footer information
        self.footer = None # footer only appears in clustered data, not raw

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
    def footer_error(self) :
        if self.footer is None : return 0x0
        return self.footer.getField("ERROR")

    ##
    ## methods
    ##

    def n_words(self) :
        return len(self.words)

    def routing_dest(self) :
    
        """
        Parses a module's routing flags and determines to which B2B outputs
        this module should be routed.
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
