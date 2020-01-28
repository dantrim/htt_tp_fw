# This module interfaces between cocotb and the dataflow code
# in the system-simulation repository, which knows about things like
# data formats.

import random
import os

from . import util

# Let's rewrite this class to use Elliot's BitField class.
from DataFormat import DataFormat, BitField

class DataWord(object):

    def __init__(self, contents, is_metadata=False, do_parse=True):
        self.contents = contents
        self.is_metadata = is_metadata

        # Flag. Only assigned if this is a metadata word.
        self.flag = None

        # in principle, this could be called by other routines.
        if do_parse:
            self._parse()

    def __str__(self):
        return str(self.get_binary())

    def __repr__(self):
        return str(self.get_binary())

    def _parse(self):
        """ Parses a data word from binary representation."""
        if self.is_metadata:
            genMetaValue = BitField.BitFieldWordValue(DataFormat.GenMetadata, self.contents)
            # assign self.flag only if this is a metadata word.
            self.flag = genMetaValue.getField("FLAG")

        # TODO: we could do other parsing here!
        # Collaborate with Elliot to decide if we want to extract more info.

    def get_binary(self, size=64):
        """ Returns binary value representation of this word, with is_metadata as the MSB."""
        full_value = util.BinaryValue(self.contents, n_bits=size+1)
        full_value[size] = int(self.is_metadata)
        return full_value

    # these are helper functions. They're not _strictly_ necessary but... useful?
    def is_start_of_event(self):
        """ Checks if the word is a start-of-event metadata word."""
        if self.flag == DataFormat.EVT_HDR1_FLAG.FLAG:
            return True
        return False

    def is_end_of_event(self):
        if self.flag == DataFormat.EVT_FTR1_FLAG.FLAG:
            return True
        return False

class DataEvent(object):

    # Does this class need to do anything else?
    # I'm not actually sure it does.

    def __init__(self, l0id):
        self.words = []
        self.l0id = l0id

    def add_word(self, word):
        self.words.append(word)

    def __str__(self):
        return "DataEvent (L0ID " + str(l0id) + "), " + str(len(self.words)) + " words"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.words)

    def __iter__(self):
        return iter(self.words)

def get_l0id_from_event(word):
    """ Helper function that uses the DataFormat package to get the L0ID from a word.
        If the word is not a start-of-event word, it returns -1."""
    if word.is_start_of_event():
        header = DataFormat.BitFieldWordValue(DataFormat.EVT_HDR1, word.contents)
        return header.getField("L0ID")
    return -1

# Adapted from event reader here:
# https://gitlab.cern.ch/atlas-tdaq-ph2upgrades/atlas-tdaq-htt/tdaq-htt-firmware/system-simulation/blob/master/DataFormat/DataFormat.py#L334
def read_events_from_file(filename, endian='little'):
    events = []
    with open(filename, 'rb') as file:

        current_event = None

        # TODO: actually test if file is EOF.
        while file_not_eof:

            # Read a word from binary file.
            is_metadata = bool(int.from_bytes(file.read(1), endian))
            contents = int.from_bytes(file.read(8), endian)

            # Create a word object.
            word = DataWord(contents, is_metadata)

            # if this is a start-of-event word, let's look up the ID?
            # Do some more parsing here in order to accomplish this.
            if word.is_start_of_event():
                header = DataFormat.BitFieldWordValue(DataFormat.EVT_HDR1, contents)
                current_event = DataEvent(header.getField("L0ID"))

            # Add the word to the current event we're reading.
            event.add_word(word)

            # Add the word to our event object
            if word.is_end_of_event():
                events.append(current_event)
    return events

def get_random_events(n_random, max_words=10):
    """ Generates random event objects for testing."""
    events = []

    # TODO: _improve_ this function. Events generated here are not really
    # generated in a sensible way. I just used random.randint() to get going.

    # Look up lengths.
    word_length = DataFormat.WORD_LENGTH
    l0id_size = DataFormat.EVT_HDR1.getFieldNBits("L0ID")
    flag_size = DataFormat.EVT_HDR1.getFieldNBits("FLAG")
    remaining_size = word_length - l0id_size - flag_size

    for i in range(n_random):

        # Generate initial word.
        flag = DataFormat.EVT_HDR1_FLAG.FLAG
        l0id = random.randint(0, 2**l0id_size - 1)
        remaining = random.randint(0, 2**remaining_size - 1)

        event = DataEvent(l0id)

        # This assumes (as does the entire function, really)
        # that a header word is always: [FLAG][STUFF][FOOTER]
        contents = (2**(word_length - flag_size) * flag) + (2**(l0id_size) * remaining) + l0id
        event.add_word(DataWord(contents, True))

        # Generate n random words.
        n_words = random.randint(0, max_words)
        for j in range(n_words):
            contents = random.randint(0, 2**word_length - 1)
            event.add_word(DataWord(contents, False))

        # Generate footer word.
        flag = DataFormat.EVT_FTR1_FLAG.FLAG
        remaining = random.randint(0, 2**(word_length - flag_size) - 1)
        contents = 2**(word_length - flag_size) * flag + remaining
        event.add_word(DataWord(contents, True))

        # Store generated event.
        events.append(event)

    return events
