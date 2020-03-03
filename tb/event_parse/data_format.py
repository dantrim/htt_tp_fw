from __future__ import print_function
import sys
if sys.version_info[0] < 3 :
    from BitField import BitFieldWordDesc, BitFieldWordValue
else :
    from .BitField import BitFieldWordDesc, BitFieldWordValue
import DataFormat.headerwords as EVT_HEADER_WORDS
import DataFormat.footerwords as EVT_FOOTER_WORDS

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
    def l0id(self) :
        return self._l0id

    @l0id.setter
    def l0id(self, value) :
        # should not use setters, should just rely on stored data and retrieve
        self._l0id = value

class Module :

    """
    Store module data
    """

    def __init__(self) :

        # module header information (64-bit word + 32-bit word)
        self.header1 = BitFieldWordValue(DataFormat.M_HDR)
        self.header2 = BitFieldWordValue(DataFormat.M_HDR2)

        # module data
        self.words = [] # 16-bit (32-bit) wide words for strip (pixel)

        # footer information
        self.footer = None # footer only appears in clustered data, not raw

        # probably don't need data members, but the property's getters
        # should just parse the stored data words
        # meta
        self._type = None

    @property
    def module_type(self) :
        return self._type

    @module_type.setter
    def module_type(self, value) :
        # should really use the enums to check validity
        self._type = value
