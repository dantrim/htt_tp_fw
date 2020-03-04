from __future__ import print_function
import sys
if sys.version_info[0] < 3 :
    from DataFormat.BitField import BitFieldWordDesc, BitFieldWordValue
    #from BitField import BitFieldWordDesc, BitFieldWordValue
else :
    from DataFormat.BitField import BitFieldWordDesc, BitFieldWordValue
    #from .BitField import BitFieldWordDesc, BitFieldWordValue
from DataFormat.DataFormatIO import SubwordUnpacker
from DataFormat import DataFormat

from data_format import Event, Module


class EventTable :

    """
    Read in cluster (track?) data and form
    and ordered table of events.
    """

    def __init__(self) :

        self._l0ids = []
        self._events = []

    @property
    def l0ids(self) :
        return self._l0ids

    @property
    def events(self) :
        return self._events

    def append(self, event) :
        self._events.append(event)
        # attach L0ID to _l0ids...

    def clear(self) :
        self._l0ids = []
        self._events = []

    # methods
    def load_from_file(self, filename, raw = None, verbose = False) :

        with open(filename, "rb") as input_file :

            current_event = None

            meta_flag = bool(int.from_bytes(input_file.read(1), DataFormat.ENDIAN)) # meta flag is 1 bit stored in a byte
            word = int.from_bytes(input_file.read(8), DataFormat.ENDIAN) # 64-bit word

            # initiate reading of the data
            while True :
                if not meta_flag :
                    if len(input_file.read(1)) == 0 :
                        # we are at EOF
                        print("End of stream")
                    else :
                        print("ERROR: expected metadata flag, word = {}".format(word))
                        #raise Exception("ERROR: Expected metadata flag")
                        break

                GenMetaValue = BitFieldWordValue(DataFormat.GenMetadata, word)
                flag = GenMetaValue.getField("FLAG")

                ##
                ## This is an event header
                ##

                if flag == DataFormat.EVT_HDR1_FLAG.FLAG :
                    if verbose :
                        print("{} {} {}".format(20 * "-", "Event Header", 20 * "-"))
                    current_event = Event()
                    self.append(current_event)

                    # iterate over the header words (each a 64-bit data word)
                    for header_word in current_event.headerwords :
                        header_word.value = word

                        # advance forward within the header data words
                        meta_flag = bool(int.from_bytes(input_file.read(1), DataFormat.ENDIAN))
                        word = int.from_bytes(input_file.read(8), DataFormat.ENDIAN)

                ##
                ## Module data
                ##

                elif flag == DataFormat.M_HDR_FLAG.FLAG :
                    if verbose :
                        print("{} {} {}".format(20 * "-", "Module", 20 * "-"))

                    module = Module()
                    current_event.modules.append(module)

                    module.header1.value = word

                    first = True
                    expectfooter = False

                    # iterate over the module data
                    while True :
                        meta_flag = bool(int.from_bytes(input_file.read(1), DataFormat.ENDIAN))
                        word = int.from_bytes(input_file.read(8), DataFormat.ENDIAN)

                        if meta_flag :
                            # no longer reading data (either a header or a footer has been reached)
                            break

                        # perform specific handling of each data type
                        data_type = module.header1.getField("TYPE")
                        data_raw = DataFormat.M_HDR_TYPE.RAW
                        data_clus = DataFormat.M_HDR_TYPE.CLUSTERED

                        det_type = module.header1.getField("DET")
                        det_pix = DataFormat.M_HDR_DET.PIXEL
                        det_strips = DataFormat.M_HDR_DET.STRIP

                        ##
                        ## RAW DATA -- PIXEL
                        ##
                        if data_type == data_raw and det_type == det_pix :
                            unpacker = SubwordUnpacker(word, DataFormat.WORD_LENGTH)
                            empty = False
                            if first :
                                val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                                module.header2.value = val
                            while not empty :
                                val, empty = unpacker.get(DataFormat.PIXEL_RAW_BITS)
                                module.words.append(val)

                        ##
                        ## RAW DATA -- STRIPS
                        ##
                        elif data_type == data_raw and det_type == det_strips :
                            unpacker = SubwordUnpacker(word, DataFormat.WORD_LENGTH)
                            empty = False
                            if first :
                                val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                                module.header2.value = val
                            while not empty :
                                val, empty = unpacker.get(DataFormat.HCC_CLUSTER.nbits)
                                module.words.append(val)

                        ##
                        ## CLUSTER DATA -- PIXEL
                        ##
                        elif data_type == data_clus and det_type == det_pix :
                            unpacker = SubwordUnpacker(word, DataFormat.WORD_LENGTH)
                            empty = False
                            if first :
                                val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                                module.header2.value = val
                            while not empty :
                                if not expectfooter :
                                    val, empty = unpacker.get(DataFormat.PIXEL_CLUSTER.nbits)
                                    cluster_val = BitFieldWordValue(DataFormat.PIXEL_CLUSTER, val)
                                    module.words.append(cluster_val)
                                    expectfooter = cluster_val.getField("LAST") == 1
                                else :
                                    val, empty = unpacker.get(DataFormat.PIXEL_CL_FTR.nbits)
                                    module.footer = BitFieldWordValue(DataFormat.PIXEL_CL_FTR, val)
                                    expectfooter = False

                        ##
                        ## CLUSTER DATA -- STRIPS
                        ##
                        elif data_type == data_clus and det_type == det_strips :
                            unpacker = SubwordUnpacker(word, DataFormat.WORD_LENGTH)
                            empty = False
                            if first :
                                val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                                module.header2.value = val
                            while not empty :
                                if not expectfooter :
                                    val, empty = unpacker.get(DataFormat.STRIP_CLUSTER.nbits)
                                    cluster_val = BitFieldWordValue(DataFormat.STRIP_CLUSTER, val)
                                    module.words.append(cluster_val)
                                    expectfooter = cluster_val.getField("LAST") == 1
                                else :
                                    val, empty = unpacker.get(DataFormat.STRIP_CL_FTR.nbits)
                                    module.footer = BitFieldWordValue(DataFormat.STRIP_CL_FTR, val)
                                    expectfooter = False

                        ##
                        ## WOOPS
                        ##
                        else :
                            raise Exception("ERROR Unhandled module type flag encountered: {}".format(module.header1.getField("TYPE")))

                elif flag == DataFormat.EVT_FTR1_FLAG.FLAG :
                    if verbose :
                        print("{} {} {}".format(20 * "-", "Event Footer", 20 * "-"))

                    for footer_word in current_event.footerwords :
                        footer_word.value = word
                        meta_flag = bool(int.from_bytes(input_file.read(1), DataFormat.ENDIAN))
                        word = int.from_bytes(input_file.read(8), DataFormat.ENDIAN)

                else :
                    print("ERROR: Unknown metadata flag {}", hex(meta_flag))
                    break
                    #raise Exception("ERROR Unknown metadata flag encountered: {}".format(hex(meta_flag)))
