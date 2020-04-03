import cocotb
from cocotb.drivers import Driver
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge, Event, ReadOnly, NextTimeStep, Timer
from bitstring import BitArray, BitStream
import struct
from tb_utils import events, utils


class FifoWrapper :

    def __init__(self, block, clock, name, io_enum) :

        self._fifo = block
        self._clock = clock
        self._name = name
        self._io_enum = io_enum
        self._io_type = None
        self._active = False
        self._observed_words = []

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
    def io_num(self) :
        return self._io_enum.value


    @property
    def active(self) :
        return self._active

    @property
    def observed_data_words(self) :
        return self._observed_words

class B2BFifoDriver(FifoWrapper, Driver) :

    def __init__(self, block, clock, name, io_enum, dump = False) :


        FifoWrapper.__init__(self, block, clock, name, io_enum)
        Driver.__init__(self)
        self._active = True
        self._dump = dump

        self._ofilename = None
        self._first = True

        if dump :
            self._ofilename = "b2bfifo_driver_{}.evt".format(self.name.lower())
            #self._ofile = open(self._ofilename, "wb")

    @property
    def dump(self) :
        return self._dump

    def __str__(self) :
        return "B2BInputDriver \"{}\": io_num={}, active={}".format(self.name, self.io_num, self.active)

    def __repr__(self) :
        return "B2BInputDriver \"{}\": io_num={}, active={}".format(self.name, self.io_num, self.active)

    def __del__(self) :
        self.close()

    def close(self) :

        pass

    def is_closed(self) :
        return True

    ##
    ## callbacks
    ##
    def write_word(self, transaction) :

        transaction = int(transaction)

        data_length = 9 * 8 # 9-bytes: 1-byte for meta-flag, 8-bytes for data
        ba = BitArray(uintle = transaction, length = data_length)
        meta_flag = ba[:8] #.to_bytes()[0]
        data = ba[8:]

        fmt = { True : "wb", False : "ab" } [self._first]
        with open(self._ofilename, fmt) as ofile :
            bw = ofile.write(meta_flag.bytes)
            bw += ofile.write(data.bytes)
            self._first = False

    ##
    ## cocotb coroutines
    ##

    @cocotb.coroutine
    def _driver_send(self, transaction, sync = True, **kwargs) :

        if sync :
            yield RisingEdge(self.clock)
            self.fifo.write_enable <= 0

        while self.fifo.almost_full != 0 :
            yield RisingEdge(self.clock)

        self.fifo.write_data <= int(transaction)
        self.fifo.write_enable <= 1
        yield RisingEdge(self.clock)
        self.fifo.write_enable <= 0

        if self.dump :
            self.write_word(int(transaction))


class B2BFifoMonitor(FifoWrapper, Monitor) :

    def __init__(self, block, clock, name, io_enum, expects_output, callbacks = []) :

        FifoWrapper.__init__(self, block, clock, name, io_enum)
        self._active = expects_output
        self._first = True

        Monitor.__init__(self)

        self.add_callback(self.simple_callback)
        if callbacks :
            for cb in callbacks :
                self.add_callback(cb)
    ##
    ## callbacks
    ##

    def simple_callback(self, transaction) :

        transaction = int(transaction)

        # at this point "transaction" is a 65-bit word with the MSB the meta-flag,
        # and we want to store it in the same format as our testvector files which
        # have 9-bytes (72 bits) per data word and with the LSB the byte holding
        # the meta-data flag

        endian = "little"
        fmt = { "little" : "<Q?", "big" : ">Q?" }[endian]

        data = transaction.to_bytes(9, "little")
        contents, is_metadata = struct.unpack(fmt, data)
        word = events.DataWord(contents, is_metadata)

        self._observed_words.append(word)

        wfmt = { True : "wb" , False : "ab" }[self._first]
        with open("b2bfifo_output_{:02}_{}.evt".format(self.io_num, self.name), wfmt) as ofile :
            word.write_testvec_fmt(ofile, endian)
            self._first = False

    ##
    ## cocotb coroutines
    ##

    @cocotb.coroutine
    def _monitor_recv(self) :

        while True :

            yield RisingEdge(self.clock)
            yield ReadOnly()

            if self.fifo.empty.value == 0 :
                transaction = self.fifo.read_data.value
                yield NextTimeStep()
                self.fifo.read_enable <= 1
                self._recv(transaction)
            else :
                yield NextTimeStep()
                self.fifo.read_enable <= 0
