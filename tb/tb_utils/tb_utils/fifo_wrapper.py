
from pathlib import Path
import struct

import cocotb
from cocotb.drivers import Driver
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge, Event, ReadOnly, NextTimeStep, Timer

import tb_utils

class FifoWrapper :

    def __init__(self, fifo_block, clock, block_name, io_enum, write_out = True, out_dir = "") :

        self._fifo = fifo_block
        self._clock = clock
        self._block_name = block_name
        self._io_enum = io_enum
        self._io_type = None
        self._is_active = False
        self._observed_words = []

        self._write_out = write_out
        self._output_directory = out_dir
        self._output_filename = ""
        self._first_write = True

        if self.write_out :
            if self.output_directory == "" :
                out_path = Path("./")
            else :
                out_path = Path(out_dir)
            if not out_path.is_dir() :
                cocotb.log.info("WARNING Requested output directory (={}) not valid, setting to \"./\"".format(out_dir))
                out_path = Path("./")

            # construct full output filename
            out_path = out_path / "{}_{}_{}_{:02}.evt".format(str(type(self).__name__.lower()), self.block_name, io_enum.name.replace("_",""), int(io_enum.value))
            self._output_filename = str(out_path)

    @property
    def fifo(self) :
        return self._fifo

    @property
    def clock(self) :
        return self._clock

    @property
    def block_name(self) :
        return self._block_name

    @property
    def io_port_num(self) :
        return int(self._io_enum.value)

    @property
    def is_active(self) :
        return self._is_active
    @is_active.setter
    def is_active(self, val) :
        self._is_active = bool(val)

    @property
    def observed_words(self) :
        return self._observed_words

    @property
    def write_out(self) :
        return self._write_out

    @property
    def output_directory(self) :
        return self._output_directory

    @property
    def output_filename(self) :
        return self._output_filename

    def __str__(self) :
        return "{} {} (port_num={}, active={})".format(type(self).__name__, self.block_name, self.io_port_num, self.is_actice)

    def __repr__(self) :
        return "{} {} (port_num={}, active={})".format(type(self).__name__, self.block_name, self.io_port_num, self.is_actice)

    ##
    ## callbacks/methods
    ##

    def transaction_to_data_word(self, transaction) :

        # at this point "transaction" is a 65-bit word with the MSB the meta-flag,
        # and we want to store it in the same format as our testvector files which
        # have 9-bytes (72-bits) per data word and with the LSB the byte holding the
        # meta-data flag

        transaction = int(transaction)

        endian = "little" # hard-code, not sure this is ever going to change
        fmt = { "little" : "<Q?", "big" : ">?Q" }[endian]
        data = transaction.to_bytes(9, endian)
        contents, is_metadata = struct.unpack(fmt, data)
        word = tb_utils.events.DataWord(contents, is_metadata)
        return word

    def store_word(self, transaction_tuple) :

        transaction, time_ns = transaction_tuple

        dword = self.transaction_to_data_word(transaction)
        self._observed_words.append(dword)

    def write_word(self, transaction_tuple) :

        transaction, time_ns = transaction_tuple

        word = self.transaction_to_data_word(transaction)
        wfmt = { True : "wb", False : "ab" }[self._first_write]
        with open(self.output_filename, wfmt) as ofile :
            word.write_testvec_fmt(ofile)
            self._first_write = False

class FifoDriver(FifoWrapper, Driver) :

    def __init__(self, fifo_block, clock, block_name, io_enum, write_out = True, out_dir = "") :

        FifoWrapper.__init__(self, fifo_block, clock, block_name, io_enum, write_out, out_dir)
        Driver.__init__(self)

    ##
    ## cocotb coroutine implementation
    ##
    @cocotb.coroutine
    def _driver_send(self, transaction, sync = True, **kwargs) :

        if sync :
            yield RisingEdge(self.clock)
            self.fifo.write_enable <= 0

        time = cocotb.utils.get_sim_time(units = "ns") # keep track of the simulation time (this time should coincide with what appears in the waveforms)
        cocotb.log.info("FOO {} DRIVER WAIT START {}".format(self.io_port_num, time))

        #yield RisingEdge(self.clock)
        timer = Timer(10, units = "ns")
        yield timer
        time = cocotb.utils.get_sim_time(units = "ns") # keep track of the simulation time (this time should coincide with what appears in the waveforms)
        cocotb.log.info("FOO {} DRIVER WAIT STOP {}".format(self.io_port_num, time))

        # wait until there is space in the fifo
        while self.fifo.almost_full != 0 :
            yield RisingEdge(self.clock)

        self.fifo.write_data <= int(transaction)
        self.fifo.write_enable <= 1
        time = cocotb.utils.get_sim_time(units = "ns") # keep track of the simulation time (this time should coincide with what appears in the waveforms)

        yield RisingEdge(self.clock) # latch
        self.fifo.write_enable <= 0 # end the write enable strobe

        if self.write_out :
            self.write_word((int(transaction), time))
        

class FifoMonitor(FifoWrapper, Monitor) :

    def __init__(self, fifo_block, clock, block_name, io_enum, callbacks = [], write_out = True, out_dir = "") :
        FifoWrapper.__init__(self, fifo_block, clock, block_name, io_enum, write_out, out_dir)
        Monitor.__init__(self)

        self.add_callback(self.store_word)
        if write_out :
            self.add_callback(self.write_word)
        if callbacks :
            for cb in callbacks :
                self.add_callback(cb)

    ##
    ## cocotb coroutine implementation
    ##
    @cocotb.coroutine
    def _monitor_recv(self) :

        while True :

            yield RisingEdge(self.clock)
            yield ReadOnly()

            if self.fifo.empty.value == 0 :
                transaction = self.fifo.read_data.value
                time = cocotb.utils.get_sim_time(units = "ns") # keep track of the simulation time (this time should coincide with what appears in the waveforms)
                yield NextTimeStep()
                self.fifo.read_enable <= 1 # strobe the read-enable only if there is data available
                self._recv((transaction, time))
            else :
                yield NextTimeStep()
                self.fifo.read_enable <= 0
