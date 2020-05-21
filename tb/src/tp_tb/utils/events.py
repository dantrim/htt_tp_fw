import os
import struct
from pathlib import Path

from . import utils
from DataFormat import DataFormat, BitField  # , BitFieldWordValue
from DataFormat.DataFormatIO import SubwordUnpacker


class DataWord:
    def __init__(
        self, contents, is_metadata=False, timestamp=None, timestamp_units=None
    ):

        self._contents = contents
        self._is_metadata = is_metadata
        self._flag = None
        self._timestamp = timestamp
        self._timestamp_units = timestamp_units

        if is_metadata:
            gen = DataFormat.BitFieldWordValue(DataFormat.GenMetadata, contents)
            self._flag = gen.getField("FLAG")

    @property
    def contents(self):
        return self._contents

    @property
    def is_metadata(self):
        return self._is_metadata

    @property
    def flag(self):
        return self._flag

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def timestamp_units(self):
        return self._timestamp_units

    def __str__(self):
        return self.hex()

    def __repr__(self):
        return self.hex()

    def __eq__(self, other):
        return self.get_binary() == other.get_binary()

    def _up_to_8(self, n):

        return (int(n) + 7) & (-8)

    def _padded_hex(self, l0id_value, l0id_str_len):

        """
        Make equal-spaced hex strings to make visual inspection simpler.
        """
        # from https://stackoverflow.com/questions/12638408/decorating-hex-function-to-pad-zeros

        given_int = l0id_value
        given_len = l0id_str_len

        hex_result = hex(given_int)[2:]  # remove '0x' from beginning of str
        num_hex_chars = len(hex_result)
        extra_zeros = "0" * (given_len - num_hex_chars)  # may not get used..

        return (
            "0x" + hex_result
            if num_hex_chars == given_len
            else "?" * given_len
            if num_hex_chars > given_len
            else "0x" + extra_zeros + hex_result
            if num_hex_chars < given_len
            else None
        )

    def set_timestamp(self, time, units):
        self._timestamp = float(time)
        self._timestamp_units = str(units)

    def get_binary(self, size=64):

        """
        Returns binary value representation of this word, with the
        metadata flag as MSB.
        """

        full_word = utils.BinaryValue(self.contents, n_bits=size + 1)
        full_word[size] = int(self.is_metadata)
        return full_word

    def hex(self):

        word = self.get_binary()
        length_8 = self._up_to_8(len(word))
        n_bytes = int(length_8 / 8 * 2 - 1)
        return self._padded_hex(int(word), n_bytes)

    def is_start_of_event(self):
        return self.is_event_header_start()

    def is_event_header_start(self):

        return self.flag == DataFormat.EVT_HDR1_FLAG.FLAG

    def is_event_footer_start(self):

        return self.flag == DataFormat.EVT_FTR1_FLAG.FLAG

    def is_module_header_start(self):

        return self.flag == DataFormat.M_HDR_FLAG.FLAG

    def write(self, ofd, endian="little"):

        """
        Saves this DataWord to a write-able output descriptor (e.g. file) as binary.
        """

        fmt = {"little": "<", "big": ">"}[endian]
        fmt += "?Q"
        return ofd.write(struct.pack(fmt, self.is_metadata, self.contents))

    def write_testvec_fmt(self, ofd, endian="little"):

        fmt = {"little": "<", "big": ">"}[endian]
        fmt += "?Q"
        return ofd.write(struct.pack(fmt, self.is_metadata, self.contents))


class ModuleData:
    def __init__(self, data_words=[], l0id=None):

        if not data_words[0].is_module_header_start():
            raise ValueError(
                f"ModuleData first word (={data_words[0]}) is not a module header!"
            )

        self._data_words = data_words
        self._l0id = l0id
        self._header = []
        self._cluster_data = []
        self._footer = None
        self._header_field_map = {}
        self._parse(data_words)
        self._is_dummy = False

    @staticmethod
    def header_field_names():
        header_words = [
            ["FLAG", "TYPE", "DET", "ROUTING"],  # ,"SPARE"]
            ["MODID", "MODTYPE", "ORIENTATION"],  # ,"SPARE"]
        ]
        return header_words

    @staticmethod
    def footer_field_names():
        footer_words = [["FLAG", "COUNT", "ERROR"]]
        return footer_words

    def header_field(self, field_name=""):
        idx = self._header_field_map[field_name]
        return self._header[idx].getField(field_name)

    def footer_field(self, field_name=""):
        if self._footer is None:
            return 0x0
        return self._footer.getField(field_name)

    @property
    def data_words(self):
        return self._data_words

    @property
    def header_words(self):
        return self._header

    @property
    def footer(self):
        return self._footer

    @property
    def cluster_data(self):
        return self._cluster_data

    def __len__(self):
        return len(self._data_words)

    def __eq__(self, other):
        lengths_equal = len(self._data_words) == len(other)
        if lengths_equal:
            h0, h1 = hex(self.header_words[0].value), hex(self.header_words[1].value)
            h0_other, h1_other = (
                hex(other.header_words[0].value),
                hex(other.header_words[1].value),
            )
            headers_equal = (h0 == h0_other) and (h1 == h1_other)

            footers_equal = hex(self.footer.value) == hex(other.footer.value)

            data_equal = headers_equal and footers_equal
        mod_eq = lengths_equal and data_equal
        return mod_eq

    def header_description_strings(self):

        out = []
        header_words = self.header_field_names()
        for hw in header_words:
            fieldvals = [hex(self.header_field(x)) for x in hw]
            fieldvals = zip(hw, fieldvals)
            out.append(", ".join([f"{x}:{y}" for x, y in list(fieldvals)]))
        return out

    def footer_description_strings(self):

        out = []

        footer_words = self.footer_field_names()
        for fw in footer_words:
            fieldvals = [hex(self.footer_field(x)) for x in fw]
            if self._footer is None:
                fieldvals = [hex(0xDEADBEEF) for _ in fieldvals]
            fieldvals = zip(fw, fieldvals)
            out.append(", ".join([f"{x}:{y}" for x, y in list(fieldvals)]))
        return out

    #    def routing_dest(self) :
    #
    #        """
    #        Parse the module routing flags and determine B2B output
    #        """
    #
    #        dest_list = set()
    #        routing_flags = self.header_routing
    #        for output in b2b_utils.B2BIO.B2BOutputs :
    #            is_amtp = "amtp" in output.name.lower()
    #            tp_num = int(output.name.split("_")[-1])
    #            idx = int(output.value)
    #
    #            routing_index = {
    #                True : 4
    #                ,False : 2
    #            } [is_amtp]
    #
    #            tp_offset = {
    #                True : 0
    #                ,False : 48
    #            } [is_amtp]
    #
    #            mask = {
    #                True : 0xf
    #                ,False : 0x3
    #            } [is_amtp]
    #
    #            offset = tp_offset + (tp_num * routing_index)
    #            mask = (mask << offset)
    #            routed = (routing_flags & mask) != 0
    #            if routed :
    #                dest_list.add(idx)
    #
    #        return dest_list

    def is_pixel(self):
        return self.module_type_str().lower() == "pixel"

    def is_strip(self):
        return self.module_type_str().lower() == "strip"

    def module_type_str(self):

        det_type = self.header_field("DET")
        out_type = None
        if det_type == DataFormat.M_HDR_DET.PIXEL:
            out_type = "PIXEL"
        elif det_type == DataFormat.M_HDR_DET.STRIP:
            out_type = "STRIP"
        return out_type

    def _parse(self, words):

        h0 = DataFormat.BitFieldWordValue(DataFormat.M_HDR, value=words[0].contents)
        h1 = DataFormat.BitFieldWordValue(DataFormat.M_HDR2)
        self._header = [h0, h1]

        data_type = self._header[0].getField("TYPE")
        data_type_raw = DataFormat.M_HDR_TYPE.RAW
        data_type_clus = DataFormat.M_HDR_TYPE.CLUSTERED

        det_type = self._header[0].getField("DET")
        det_type_pix = DataFormat.M_HDR_DET.PIXEL
        det_type_strip = DataFormat.M_HDR_DET.STRIP

        expectfooter = False

        for iword, word in enumerate(words[1:]):

            unpacker = SubwordUnpacker(word.contents, DataFormat.WORD_LENGTH)
            empty = False

            ##
            ## raw
            ##

            if data_type == data_type_raw:
                raw_length = {
                    det_type_pix: DataFormat.PIXEL_RAW_BITS,
                    det_type_strip: DataFormat.HCC_CLUSTER.nbits,
                }[det_type]

                if iword == 0:
                    val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                    h1.value = val
                while not empty:
                    val, empty = unpacker.get(raw_length)
                    self._cluster_data.append(val)

            ##
            ## clustered data
            ##

            if data_type == data_type_clus:

                clus_word_format = {
                    det_type_pix: DataFormat.PIXEL_CLUSTER,
                    det_type_strip: DataFormat.STRIP_CLUSTER,
                }[det_type]
                clus_word_length = clus_word_format.nbits

                clus_footer_format = {
                    det_type_pix: DataFormat.PIXEL_CL_FTR,
                    det_type_strip: DataFormat.STRIP_CL_FTR,
                }[det_type]
                clus_footer_length = clus_footer_format.nbits

                if iword == 0:
                    val, empty = unpacker.get(DataFormat.M_HDR2.nbits)
                    h1.value = val

                ##
                ## here we handle mis-shapened words
                ##
                # test for empty module
                if len(words[1:]) == 1:
                    tmp_words = []
                    while not empty:
                        val, empty = unpacker.get(clus_word_length)
                        tmp_words.append(val)
                    for tw in tmp_words:
                        flag = (tw >> (clus_word_length - 8)) & 0xFF
                        if flag == DataFormat.CL_FTR_FLAG.FLAG:
                            self._footer = DataFormat.BitFieldWordValue(
                                clus_footer_format, tw
                            )
                        else:
                            self._cluster_data.append(
                                DataFormat.BitFieldWordValue(clus_word_format, tw)
                            )
                else:
                    while not empty:
                        if (not expectfooter) and (self.footer is None):
                            val, empty = unpacker.get(clus_word_length)
                            cluster_val = DataFormat.BitFieldWordValue(
                                clus_word_format, val
                            )
                            self._cluster_data.append(cluster_val)
                            expectfooter = cluster_val.getField("LAST") == 1
                        else:
                            val, empty = unpacker.get(clus_footer_length)
                            expectfooter = False
                            if self._footer is None:
                                self._footer = DataFormat.BitFieldWordValue(
                                    clus_footer_format, val
                                )
                                break

                ##
                ## if not doing mis-shapened word handling, uncomment this
                ##
                # while not empty :
                #    if (not expectfooter) and (self.footer == None) :
                #        val, empty = unpacker.get(clus_word_length)
                #        cluster_val = DataFormat.BitFieldWordValue(clus_word_format, val)
                #        self._cluster_data.append(cluster_val)
                #        expectfooter = cluster_val.getField("LAST") == 1
                #    else :
                #        val, empty = unpacker.get(clus_footer_length)
                #        expectfooter = False
                #        if not self._footer :
                #            self._footer = DataFormat.BitFieldWordValue(clus_footer_format, val)
                #            break

        if data_type == data_type_clus and (
            self._footer is None or self._footer == 0x0
        ):
            print("WARNING Failed to find MODULE FOOTER for clustered data")

        self._parse_header()

    def _parse_header(self):

        header_descriptors = [DataFormat.M_HDR, DataFormat.M_HDR2]

        if len(self._header) != len(header_descriptors):
            raise ValueError(
                "ERROR Cannot parse module header if module data has not been loaded!"
            )
        for i, descriptor in enumerate(header_descriptors):
            bitfield = self._header[i]
            # bitfield = DataFormat.BitFieldWordValue(descriptor, data_word.contents)
            # self._header_fields.append(bitfield)

            field_names = bitfield.classobj.fields
            for fn in field_names:
                self._header_field_map[fn.name] = i


class DataEvent:
    def __init__(self, l0id):
        self._words = []
        self._l0id = l0id
        self._pos = 0

        self._header_idx = []
        self._footer_idx = []
        self._module_idx = []

        ##
        ## parsed fields
        ##

        self._header_field_map = {}
        self._footer_field_map = {}

        self._header_fields = []
        self._footer_fields = []

    @staticmethod
    def header_field_names():
        header_words = [
            ["FLAG", "TRK_TYPE", "SPARE", "L0ID"],
            ["BCID", "SPARE", "RUNNUMBER"],
            ["ROI"],
            ["EFPU_ID", "EFPU_PID", "TIME"],
            ["Connection_ID", "Transaction_ID"],
            ["STATUS", "CRC"],
        ]
        return header_words

    @staticmethod
    def footer_field_names():
        footer_words = [
            ["FLAG", "SPARE", "META_COUNT", "HDR_CRC"],
            ["ERROR_FLAGS"],
            ["WORD_COUNT", "CRC"],
        ]
        return footer_words

    def parse(self):
        self._parse_header()
        self._parse_footer()

    def header_field(self, field_name=""):
        idx = self._header_field_map[field_name]
        return self._header_fields[idx].getField(field_name)

    def footer_field(self, field_name=""):
        idx = self._footer_field_map[field_name]
        return self._footer_fields[idx].getField(field_name)

    def _parse_header(self):

        header_descriptors = [
            DataFormat.EVT_HDR1,
            DataFormat.EVT_HDR2,
            DataFormat.EVT_HDR3,
            DataFormat.EVT_HDR4,
            DataFormat.EVT_HDR5,
            DataFormat.EVT_HDR6,
        ]

        if len(self.header_words) != len(header_descriptors):
            raise ValueError(
                "ERROR Cannot parse header if event data has not been loaded!"
            )

        for i, descriptor in enumerate(header_descriptors):
            data_word = self.header_words[i]
            bitfield = DataFormat.BitFieldWordValue(descriptor, data_word.contents)
            self._header_fields.append(bitfield)

            field_names = bitfield.classobj.fields
            for fn in field_names:
                self._header_field_map[fn.name] = i

    def _parse_footer(self):

        footer_descriptors = [
            DataFormat.EVT_FTR1,
            DataFormat.EVT_FTR2,
            DataFormat.EVT_FTR3,
        ]

        if len(self.footer_words) != len(footer_descriptors):
            raise ValueError(
                "ERROR Cannot parse footer if event data has not been loaded!"
            )

        for i, descriptor in enumerate(footer_descriptors):
            data_word = self.footer_words[i]
            bitfield = DataFormat.BitFieldWordValue(descriptor, data_word.contents)
            self._footer_fields.append(bitfield)

            field_names = bitfield.classobj.fields
            for fn in field_names:
                self._footer_field_map[fn.name] = i

    @property
    def words(self):
        return self._words

    @property
    def l0id(self):
        return self._l0id

    @property
    def header_words(self):
        return self.words[self._header_idx[0] : self._header_idx[1]]

    @property
    def footer_words(self):
        return self.words[self._footer_idx[0] : self._footer_idx[1]]

    @property
    def module_words(self):

        if len(self._module_idx) == 0:
            return []
        modules = []
        for imod, mod in enumerate(self._module_idx):
            start, stop = mod
            modules.append(self._words[start:stop])
        return modules

    @property
    def n_modules(self):
        return len(self._module_idx)

    def get_modules(self):
        out_mods = []
        for module_data in self.module_words:
            module = ModuleData(module_data, l0id=self.l0id)
            out_mods.append(module)
        return out_mods

    def _pending_module(self):

        return len(self._module_idx) > 0 and self._module_idx[-1][1] < 0

    def add_word(self, word):
        self._words.append(word)

        if word.is_metadata:
            if word.is_event_header_start():
                self._header_idx = [self._pos, self._pos + 6]

            elif word.is_event_footer_start() or word.is_module_header_start():

                if self._pending_module():
                    self._module_idx[-1][1] = self._pos

                if word.is_event_footer_start():
                    self._footer_idx = [self._pos, self._pos + 3]

                elif word.is_module_header_start():
                    mod_idx = [self._pos, -1]
                    self._module_idx.append(mod_idx)
        self._pos += 1

    def unmatched_data_words(self):

        ##
        ## first gather the indices of the datawords that are accounted for
        ##
        used_idx = list(range(self._header_idx[0], self._header_idx[1], 1))
        used_idx.extend(list(range(self._footer_idx[0], self._footer_idx[1], 1)))
        for imod, mod in enumerate(self._module_idx):
            mod_idx_0, mod_idx_1 = mod
            used_idx.extend(range(mod_idx_0, mod_idx_1, 1))
        used_idx = sorted(used_idx)

        ##
        ## find unaccounted for indices
        ##
        expected_indices = range(
            0, len(self._words), 1
        )  # if every word was accounted for
        unused_idx = sorted(list(set(expected_indices) - set(used_idx)))

        unused_data_words = []
        for idx in unused_idx:
            unused_data_words.append(self._words[idx])
        return unused_data_words

    def write(self, ofd, endian="little"):
        for word in self.words:
            word.write(ofd, endian)

    def __str__(self):
        return f"DataEvent (L0ID={hex(self.l0id)}, N-words={len(self.words)}, N-modules={self.n_modules})"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.words)

    def __iter__(self):
        return iter(self.words)

    def header_field_strings(self):
        output = []
        for iheader_word_num, field_names in enumerate(self.header_field_names()):
            field_list = [self.header_field(x) for x in field_names]
            output.append(field_list)
        return output

    def footer_field_strings(self):
        output = []
        for ifooter_word_num, field_names in enumerate(self.footer_field_names()):
            field_list = [self.footer_field(x) for x in field_names]
            output.append(field_list)
        return output

    def header_description_strings(self):

        out = []
        header_words = self.header_field_names()
        for hw in header_words:
            fieldvals = [hex(self.header_field(x)) for x in hw]
            fieldvals = zip(hw, fieldvals)
            out.append(", ".join([f"{x}:{y}" for x, y in list(fieldvals)]))
        return out

    def footer_description_strings(self):

        out = []
        footer_words = self.footer_field_names()
        for fw in footer_words:
            fieldvals = [hex(self.footer_field(x)) for x in fw]
            fieldvals = zip(fw, fieldvals)
            out.append(", ".join([f"{x}:{y}" for x, y in list(fieldvals)]))
        return out


def load_events(data_words=[], endian="little", n_to_load=-1, l0id_request=-1):

    """
    Load data from a list of DataWord objects
    and fill events.
    """

    current_event = None
    events = []
    l0ids_loaded = set()
    for word in data_words:

        if word.is_event_header_start():
            if n_to_load > 0 and len(events) >= n_to_load:
                break
            if l0id_request > 0 and int(l0id_request) in l0ids_loaded:
                break
            header = DataFormat.BitFieldWordValue(DataFormat.EVT_HDR1, word.contents)
            current_event = DataEvent(header.getField("L0ID"))
            l0ids_loaded.add(int(current_event.l0id))

        if current_event is not None:
            current_event.add_word(word)

        if word.is_event_footer_start():
            events.append(current_event)

    if int(l0id_request) > 0 and len(events) > 0:
        tmp = []
        for event in events:
            if int(event.l0id) == int(l0id_request):
                tmp.append(event)
                break
        events = tmp

    for event in events:
        event.parse()

    return events


def timing_file_from_data_filename(data_file):

    path = Path(data_file)
    filedir = path.parents[0]
    timing_filename = data_file.split("/")[-1].replace(
        ".evt", "_timing.txt"
    )  # NOTE this is an expected naming convention
    timing_file = Path(filedir) / timing_filename

    ok = timing_file.exists() and timing_file.is_file()
    if not ok:
        raise Exception(f"ERROR Timing information file (={timing_file}) not found")
    return str(timing_file)


def timing_info_gen(filename):

    timing_filename = timing_file_from_data_filename(filename)
    with open(timing_filename, "r") as ifile:
        for iline, line in enumerate(ifile):
            line = line.strip()
            if "info" in line.lower():
                if "data_file" in line.lower():
                    corresponding_data_file = line.strip().split(":")[-1]
                    data_match = corresponding_data_file.replace(".evt", "")
                    time_match = timing_filename.split("/")[-1].replace(
                        "_timing.txt", ""
                    )
                    if data_match != time_match:
                        raise Exception(
                            f"ERROR Timing file (={timing_filename}) does not match with expected corresponding data file (={corresponding_data_file})"
                        )
                if "time_unit" in line.lower():
                    time_unit = line.strip().split(":")[-1]
                    yield time_unit
                continue
            yield line


def file_event_generator(filename, endian="little", n_to_load=-1):

    path = Path(filename)
    ok = path.exists() and path.is_file()
    if not ok:
        raise Exception(f"Cannot find provided file {filename}")

    at_event_end = False
    n_events_loaded = 0
    with open(filename, "rb") as ifile:
        current_event = None
        filesize = os.stat(filename).st_size
        for _ in range(0, filesize, 9):
            data = ifile.read(9)
            if len(data) != 9:
                raise Exception(f"Malformed event data file {filename}")

            fmt = {"little": "<?Q", "big": ">?Q"}[endian]
            is_metadata, contents = struct.unpack(fmt, data)
            word = DataWord(contents, is_metadata)

            if word.is_event_header_start():

                if at_event_end and current_event is not None:
                    current_event.parse()
                    yield current_event
                    n_events_loaded += 1

                if n_to_load > 0 and n_events_loaded >= n_to_load:
                    break

                header = DataFormat.BitFieldWordValue(DataFormat.EVT_HDR1, contents)
                current_event = DataEvent(header.getField("L0ID"))

            if current_event is not None:
                current_event.add_word(word)

            if word.is_event_footer_start():
                at_event_end = True


def load_events_from_file(
    filename, endian="little", n_to_load=-1, l0id_request=-1, load_timing_info=False
):

    path = Path(filename)
    ok = path.exists() and path.is_file()
    if not ok:
        raise Exception(f"Cannot find provided file {filename}")

    if n_to_load > 0 and l0id_request > 0:
        raise Exception(
            "ERROR Cannot request specific number of events AND a specific L0ID at the same time"
        )

    timing_gen = None
    time_units = None
    if load_timing_info:
        timing_gen = timing_info_gen(filename)
        time_units = next(timing_gen)  # first one returned is the time unit (str)

    events = []
    l0ids_loaded = set()
    with open(filename, "rb") as ifile:
        current_event = None
        filesize = os.stat(filename).st_size
        for _ in range(0, filesize, 9):
            data = ifile.read(9)
            if len(data) != 9:
                raise Exception(f"Malformed event data file {filename}")

            fmt = {"little": "<?Q", "big": ">?Q"}[endian]
            is_metadata, contents = struct.unpack(fmt, data)
            word = DataWord(contents, is_metadata)

            ##
            ## timestamp
            ##
            if timing_gen:
                try:
                    word.set_timestamp(next(timing_gen), units=time_units)
                except StopIteration:
                    raise Exception(
                        f"ERROR Timing file for loaded data file (={filename}) has incorrect number of words in it!"
                    )

            if word.is_event_header_start():
                if n_to_load > 0 and len(events) >= n_to_load:
                    break
                if l0id_request > 0 and int(l0id_request) in l0ids_loaded:
                    break
                header = DataFormat.BitFieldWordValue(DataFormat.EVT_HDR1, contents)
                current_event = DataEvent(header.getField("L0ID"))
                l0ids_loaded.add(int(current_event.l0id))

            if current_event is not None:
                current_event.add_word(word)

            if word.is_event_footer_start():
                events.append(current_event)

    if int(l0id_request) > 0 and len(events) > 0:
        tmp = []
        for event in events:
            if int(event.l0id) == int(l0id_request):
                tmp.append(event)
                break
        events = tmp

    for event in events:
        event.parse()

    return events
