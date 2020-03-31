import cocotb
from cocotb.drivers import Driver
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge, Event, ReadOnly, NextTimeStep, Timer
from bitstring import BitArray, BitStream

class FifoWrapper :

    def __init__(self, block, clock, name, io_num) :

        self._fifo = block
        self._clock = clock
        self._name = name
        self._io_num = io_num
        self._io_type = None
        self._active = False

    @property
    def fifo(self) :
        return self._block

    @property
    def clock(self) :
        return self._clock

    @property
    def name(self) :
        return self._name

    @property
    def io_num(self) :
        return self._io_num


    @property
    def active(self) :
        return self._active

class B2BFifoDriver(FifoWrapper, Driver) :

    def __init__(self, block, clock, name, io_num, dump = False) :


        FifoWrapper.__init__(self, block, clock, name, io_num)
        Driver.__init__(self)
        self._active = True
        self._dump = dump

        self._ofilename = None
        self._ofile = None

        if dump :
            self._ofilename = "b2bfifo_driver_{}.evt".format(self.name.lower())
            self._ofile = open(self._ofilename, "wb")

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

        if self.dump :
            if self._ofile :
                if not self._ofile.closed :
                    self._ofile.close()

    def is_closed(self) :
        if self._ofile :
            return self._ofile.closed
        return True

    ##
    ## callbacks
    ##
    def write_word(self, transaction) :

        transaction = int(transaction)

        data_length = 9 * 8 # 9-bytes: 1-byte for meta-flag, 8-bytes for data
        ba = BitArray(uintle = transaction, length = data_length)
        meta_flag = ba.to_bytes()[0]
        data = ba[1:]

        bw = self._ofile.write(meta_flag)
        bw += self._ofile.write(data)
        self._ofile.flush()

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
            self.write_word(self, int(transaction))


class B2BFifoMonitor(FifoWrapper, Monitor) :

    def __init__(self, block, clock, name, io_num, expects_output, callbacks = []) :

        FifoWrapper.__init__(self, block, clock, name, io_num)
        self._active = expects_output

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
        cocotb.log.info("B2BFifoMonitor \"{}\" receives: {}".format(self.name, hex(transaction)))

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
