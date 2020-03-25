import cocotb

from pathlib import Path

from DataFormat import DataFormat
from DataFormat import BitField

class OutputFileCallback :

    def __init__(self, name = "OutputFileCallback", filename = "output.evt") :

        self._name = name
        self._filename = filename
        self._file = None

        self.open_file(filename)

        self._current_l0id = -1

    @property
    def name(self) :
        return self._name

    @property
    def filename(self) :
        return self._filename

    @property
    def file(self) :
        return self._file

    def __del__(self) :

        self.close()

    def is_closed(self) :

        if self._file :
            return self._file.closed
        return True # sure

    def close(self) :

        cocotb.log.info("Callback {} closing output file {}".format(self.name, self.filename))
        if self._file :
            if not self._file.closed :
                self._file.close()
        

    def open_file(self, filename) :

        #cocotb.log.error("Callback {} failed to open file {} for writing".format(self.name, self.filename))
            

        self._file = open(filename, "wb")
        cocotb.log.info("Callback {} opened file {} for writing".format(self.name, self.filename))
        
    def callback(self, transaction) :

        if not self.is_closed() :
            #cocotb.log.info("Callback {} writing {} to file {}".format(self.name, hex(int(transaction)), self.filename))
            data = int(transaction)
            meta = (data >> 64) & 0xff
            word = (data & 0xffffffffffffffff)

            header = BitField.BitFieldWordValue(DataFormat.EVT_HDR1, word)
            if header.getField("FLAG") == DataFormat.EVT_HDR1_FLAG.FLAG :
                l0id = header.getField("L0ID")
                self._current_l0id = header.getField("L0ID")
            #cocotb.log.info(" --> {} RECEIVED DATA FOR L0ID = {}: {}".format(self.name, hex(self._current_l0id), hex(int(transaction))))

            #cocotb.log.info("  -> meta = {}, word = {}".format(hex(meta), hex(word)))
            bw = self.file.write(int(meta).to_bytes(1,'little'))
            bw += self.file.write(int(word).to_bytes(8,'little'))
#            bw = self.file.write(int(transaction).to_bytes(,'little'))
            #cocotb.log.info(" --> Wrote {} bytes".format(int(bw)))
            self.file.flush()
