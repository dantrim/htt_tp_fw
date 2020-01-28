from cocotb import binary

# Utility class: this is just the cocotb binary value class,
# but with bigEndian = False by default...
class BinaryValue(binary.BinaryValue):

    def __init__(self, value=None, n_bits=None, bigEndian=False,
                 binaryRepresentation=binary.BinaryRepresentation.UNSIGNED, bits=None):
        # Just call the parent constructor but have bigendian default to false.
        super(BinaryValue, self).__init__(value, n_bits=n_bits, bigEndian=bigEndian,
                                      binaryRepresentation=binaryRepresentation, bits=bits)
