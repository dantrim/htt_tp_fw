from cocotb import binary


# taken from: https://gitlab.cern.ch/atlas-tdaq-p2-firmware/tdaq-htt-firmware/tp-fw/-/blob/master/tb/tptest/tptest/util.py
class BinaryValue(binary.BinaryValue):
    def __init__(
        self,
        value=None,
        n_bits=None,
        bigEndian=False,
        binaryRepresentation=binary.BinaryRepresentation.UNSIGNED,
        bits=None,
    ):
        super().__init__(
            value,
            n_bits=n_bits,
            bigEndian=bigEndian,
            binaryRepresentation=binaryRepresentation,
            bits=bits,
        )
