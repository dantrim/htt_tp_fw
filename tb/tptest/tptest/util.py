from cocotb import binary

# This is not nice. But we want to get the builtin version
# of the hex() method so it can be overriden.
import sys
if sys.version_info.major <= 2:
    import __builtin__ as builtins
else:
    import builtins

# Utility class: this is just the cocotb binary value class,
# but with bigEndian = False by default...
class BinaryValue(binary.BinaryValue):

    def __init__(self, value=None, n_bits=None, bigEndian=False,
                 binaryRepresentation=binary.BinaryRepresentation.UNSIGNED, bits=None):
        # Just call the parent constructor but have bigendian default to false.
        super(BinaryValue, self).__init__(value, n_bits=n_bits, bigEndian=bigEndian,
                                      binaryRepresentation=binaryRepresentation, bits=bits)

def hex(value):
    """ Shadowed version of __builtins__.hex() that prunes longs.
        This is mildly evil, but I don't feel too bad about it.
        It's mostly used as util.hex anyway."""
    hex_value = builtins.hex(value)
    return hex_value.replace("L", '')
