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

        self._file = open(filename, "wb")
        cocotb.log.info("Callback {} opened file {} for writing".format(self.name, self.filename))
        
    def callback(self, transaction) :

        if not self.is_closed() :
            data = int(transaction)
            meta = (data >> 64) & 0xff
            word = (data & 0xffffffffffffffff)
            bw = self.file.write(int(meta).to_bytes(1,'little'))
            bw += self.file.write(int(word).to_bytes(8,'little'))
            self.file.flush()
