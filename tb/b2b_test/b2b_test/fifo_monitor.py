import cocotb
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge, ReadOnly, NextTimeStep

class IOMonitor(Monitor) :

    """
    Justs inspects words driven onto or out of a given
    Spy FIFO. Does not drive any signals.
    """

    def __init__(self, fifo_block, clock, name, input_or_output = "input") :

        self._fifo = fifo_block
        self._clock = clock
        self._name = name
        self._io = ""

        if "in" in input_or_output.lower() or "input" in input_or_output.lower() :
            self._io = "input"
        else :
            self._io = "output"

        if not self._io :
            raise Exception("ERROR IOMonitor could not be initialized \
                    unknown \"input_or_output\" parameter provided = {}".
                        format(input_or_output))

        super().__init__(callback = self.io_monitor)
        #super().__init__()

        self.fifo._log.info("Created IOMonitor {} for {}".format(self.name, self.io_type))

        self._ofilename = "{}_{}.evt".format(self.name, input_or_output.lower())
        self._ofile = None
        self.open_file(self._ofilename)

    ##
    ## properties
    ##

    @property
    def fifo(self) :
        return self._fifo

    @property
    def clock(self) :
        return self._clock

    @property
    def name(self) :
        return self._name

    @property
    def io_type(self) :
        return self._io

    ##
    ## methods
    ##

    def __del__(self) :
        self.close()

    def close(self) :

        if self._ofile :
            if not self._ofile.closed :
                self._ofile.close()

    def is_closed(self) :

        if self._ofile :
            return self._ofile.closed
        return True

    def open_file(self, filename = "io_mon.evt") : 
        self._ofile = open(filename, "wb")

    def write_word(self, word) :

        word = int(word)
        meta = (word >> 64) & 0xff
        data = (word & 0xffffffffffffffff)

        bw = self._ofile.write(int(meta).to_bytes(1, "little"))
        bw += self._ofile.write(int(data).to_bytes(8, "little"))
        self._ofile.flush()

    ##
    ## cocotb coroutines
    ##

    @cocotb.coroutine
    def _monitor_recv(self) :

        while True :

            yield RisingEdge(self.clock)
            yield ReadOnly()

            strobe, bus, reset = {
                "input" : (self.fifo.write_enable, self.fifo.write_data, self.fifo.wreset)
                ,"output" : (self.fifo.read_enable, self.fifo.read_data, self.fifo.rreset)
            } [ self.io_type ]

            if strobe.value == 1 : #and reset.value == 1 : # reset active LOW 
                try :
                    transaction = int(bus.value)
                except ValueError :
                    continue
                self._recv(transaction)

    def io_monitor(self, transaction) :

        self.write_word(transaction)
