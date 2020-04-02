import os, struct
import tb_utils
from tb_utils import utils
from tb_b2b import b2b_utils
from pathlib import Path

from DataFormat import DataFormat, BitField
from DataFormat.DataFormatIO import SubwordUnpacker

class DataWord :

    def __init__(self, contents, is_metadata = False) :

        self._contents = contents
        self._is_metadata = is_metadata
        self._flag = None

        if is_metadata :
            gen = DataFormat.BitFieldWordValue(DataFormat.GenMetadata, contents)
            self._flag = gen.getField("FLAG")

    @property
    def contents(self) :
        return self._contents

    @property
    def is_metadata(self) :
        return self._is_metadata

    @property
    def flag(self) :
        return self._flag

    def __str__(self) :
        return str(self.get_binary())

    def __repr__(self) :
        return str(self.get_binary())

    def _up_to_8(self, n) :

        return ((int(n)+7) & (-8))

    def _padded_hex(self, i, l):

        given_int = i
        given_len = l
    
        hex_result = hex(given_int)[2:] # remove '0x' from beginning of str
        num_hex_chars = len(hex_result)
        extra_zeros = '0' * (given_len - num_hex_chars) # may not get used..
    
        return ('0x' + hex_result if num_hex_chars == given_len else
                '?' * given_len if num_hex_chars > given_len else
                '0x' + extra_zeros + hex_result if num_hex_chars < given_len else
                None)

    def get_binary(self, size = 64) :

        """
        Returns binary value representation of this word, with the
        metadata flag as MSB.
        """

        full_word = utils.BinaryValue(self.contents, n_bits = size + 1)
        full_word[size] = int(self.is_metadata)
        return full_word

    def hex(self) :

        word = self.get_binary()
        length_8 = self._up_to_8(len(word))
        n_bytes = int(length_8 / 8 * 2 - 1)
        return self._padded_hex(int(word),  n_bytes)

    def is_event_header_start(self) :

        return self.flag == DataFormat.EVT_HDR1_FLAG.FLAG

    def is_event_footer_start(self) :

        return self.flag == DataFormat.EVT_FTR1_FLAG.FLAG

    def is_module_header_start(self) :

        return self.flag == DataFormat.M_HDR_FLAG.FLAG

    def write(self, ofd, endian = "little") :

        """
        Saves this DataWord to a write-able output descriptor (e.g. file) as binary.
        """

        fmt = { "little" : "<", "big" : ">" }[endian]
        fmt += "?Q"
        return ofd.write(struct.pack(fmt, self.is_metadata, self.contents))

class ModuleData :

    def __init__(self, data_words = []) :

        if not data_words[0].is_module_header_start() :
            raise ValueError("ModuleData first word (={}) is not a module header!".format(data_words[0]))

        self._header = []
        self._cluster_data = []
        self._footer = None

        self._parse(data_words)

    @property
    def header_words(self) :
        return self._header

    @property
    def footer(self) :
        return self._footer

    @property
    def cluster_data(self) :
        return self._cluster_data

    @property
    def header_flag(self) :
        return self._header[0].getField("FLAG")

    @property
    def header_type(self) :
        return self._header[0].getField("TYPE")

    @property
    def header_det(self) :
        return self._header[0].getField("DET")

    @property
    def header_routing(self) :
        return self._header[0].getField("ROUTING")

    @property
    def header_modid(self) :
        return self._header[1].getField("MODID")

    @property
    def header_modtype(self) :
        return self._header[1].getField("MODTYPE")

    @property
    def header_orientation(self) :
        return self._header[1].getField("ORIENTATION")

    @property
    def footer_flag(self) :
        if self._footer is None : return 0x0
        return self._footer.getField("FLAG")

    @property
    def footer_count(self) :
        if self._footer is None : return 0x0
        return self._footer.getField("COUNT")

    @property
    def n_clusters(self) :
        return self.footer_count

    @property
    def footer_error(self) :
        if self._footer is None : return 0x0
        return self._footer.getField("ERROR")

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

    def cluster_data(self) :
        return self._cluster_data

    def _parse(self, words) :

        h0 = DataFormat.BitFieldWordValue(DataFormat.M_HDR, value = words[0])
        h1 = DataFormat.BitFieldWordValue(DataFormat.M_HDR2)
        self._header = [h0, h1]

        data_type = self.header1.getField("TYPE")
        data_type_raw = DataFormat.M_HDR_TYPE.RAW
        data_type_clus = DataFormat.M_HDR_TYPE.CLUSTERED

        det_type = self.header1.getField("DET")
        det_type_pix = DataFormat.M_HDR_DET.PIXEL
        det_type_strip = DataFormat.M_HDR_DET.STRIP

        is_pix = (det_type == det_type_pix)
        is_strip = (det_type == det_type_strip)

        expectfooter = False

        for iword, word in enumerate(words) :

            unpacker = SubwordUnpacker(word, DataFormat.WORD_LENGTH)
            empty = False

            ##
            ## raw
            ##

            if data_type == data_type_raw :
                raw_length = {
                    det_type_pix : DataFormat.PIXEL_RAW_BITS
                    ,det_type_strips : DataFormat.HCC_CLUSTER.nbits
                }[det_type]

                if iword == 0 :
                    val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                    h1.value = val
                while not empty :
                    val, empty = unpacker.get(raw_length)
                    self._cluster_data.append(val)

            ##
            ## clustered data
            ##

            if data_type == data_type_clus :

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
                    h1.value = val

                # test for empty module
                if len(words[1:]) == 1 :
                    tmp_words = []
                    while not empty :
                        val, empty = unpacker.get(clus_word_length)
                        tmp_words.append(val)
                    for tw in tmp_words :
                        flag = (tw >> (clus_word_length - 8)) & 0xff
                        if flag == DataFormat.CL_FTR_FLAG.FLAG :
                            self._footer = DataFormat.BitFieldWordValue(clus_footer_format, tw)
                        else :
                            self._cluster_data.append( DataFormat.BitFieldWordValue(clus_word_format, tw))
                else :
                    while not empty :
                        if not expectfooter and self.footer == None :
                            val, empty = unpacker.get(clus_word_length)
                            cluster_val = DataFormat.BitFieldWordValue(clus_word_format, val)
                            self._cluster_data.append(cluster_val)
                            expectfooter = cluster_val.getField("LAST") == 1
                        else :
                            val, empty = unpacker.get(clus_footer_length)
                            if not self._footer :
                                self._footer = DataFormat.BitFieldWordValue(clus_footer_format, val)
                                break
                            expectfooter = False

        if data_type == data_type_clus and (self._footer == None or self._footer == 0x0) :
            raise Exception("ERROR Faield to find FOOTER for clustered data")

class DataEvent :

    def __init__(self, l0id) :
        self._words = []
        self._l0id = l0id
        self._pos = 0

        self._header_idx = []
        self._footer_idx = []
        self._module_idx = []

    @property
    def words(self) :
        return self._words

    @property
    def l0id(self) :
        return self._l0id

    @property
    def header_words(self) :
        return self.words[ self._header_idx[0] : self._header_idx[1] ]

    @property
    def footer_words(self) :

        return self.words[ self._footer_idx[0] : self._footer_idx[1] ]

    @property
    def module_words(self) :

        if len(self._module_idx) == 0 :
            return []
        modules = []
        for imod, mod in enumerate(self._module_idx) :
            start, stop = mod
            modules.append( self._words[start : stop] )
        return modules

    @property
    def n_modules(self) :
        return len(self._module_idx)

    def modules(self) :
        out_mods = []
        for module_data in self.module_words :
            module = ModuleData(module_data)
            out_mods.append(module)
        return out_mods

    def _pending_module(self) :

        return len(self._module_idx) > 0 and self._module_idx[-1][1] < 0

    def add_word(self, word) :
        self._words.append(word)
        
        if word.is_metadata :
            if word.is_event_header_start() :
                self._header_idx = [self._pos, self._pos + 6]

            elif word.is_event_footer_start() or word.is_module_header_start() :

                if self._pending_module() :
                    self._module_idx[-1][1] = self._pos

                if word.is_event_footer_start() :
                    self._footer_idx = [self._pos, self._pos + 3]
                elif word.is_module_header_start() :
                    mod_idx = [self._pos, -1]
                    self._module_idx.append(mod_idx)
        self._pos += 1

    def write(self, ofd, endian = "little") :
        for word in self.words :
            word.write(ofd, endian)

    def __str__(self) :
        return "DataEvent (L0ID={}, N-words={}, N-modules={})".format(hex(self.l0id), len(self.words), self.n_modules)

    def __repr__(self) :
        return self.__str__()

    def __len__(self) :
        return len(self.words)

    def __iter__(self) :
        return iter(self.words)

def load_events(data_words = [], endian = "little", n_to_load = -1) :

    """
    Load data from a list of DataWord objects
    and fill events.
    """

    current_event = None
    events = []
    for word in data_words :

        if word.is_event_header_start() :
            if n_to_load > 0 and len(events) >= n_to_load :
                break
            header = DataFormat.BitFieldWordValue(DataFormat.EVT_HDR1, word.contents)
            current_event = DataEvent(header.getField("L0ID"))
        
        if current_event is not None :
            current_event.add_word(word)
        
        if word.is_event_footer_start() :
            events.append(current_event)
    return events

def load_events_from_file(filename, endian = "little", n_to_load = -1) :

    path = Path(filename)
    ok = path.exists() and path.is_file()
    if not ok :
        raise Exception("Cannot find provided file {}".format(filename))

    events = []
    with open(filename, "rb") as ifile :
        current_event = None
        filesize = os.stat(filename).st_size
        for _ in range(0, filesize, 9) :
            data = ifile.read(9)
            if len(data) != 9 :
                raise Exception("Malformed event data file {}".format(filename))

            fmt = { "little" : "<?Q", "big" : ">?Q" }[endian]
            is_metadata, contents = struct.unpack(fmt, data)
            word = DataWord(contents, is_metadata)

            if word.is_event_header_start() :
                if n_to_load > 0 and len(events) >= n_to_load :
                    break
                header = DataFormat.BitFieldWordValue(DataFormat.EVT_HDR1, contents)
                current_event = DataEvent(header.getField("L0ID"))

            if current_event is not None :
                current_event.add_word(word)

            if word.is_event_footer_start() :
                events.append(current_event)
    return events
