import cocotb
from cocotb.drivers import Driver
from cocotb.triggers import RisingEdge, Event, ReadOnly, NextTimeStep, Timer

from . import fifo_wrapper


class SoftwareBlock:
    def __init__(self, clock, name):
        self._clock = clock
        self._input_fifos = []
        self._output_fifos = []
        self._raw_output_fifos = []
        self._output_drivers = []
        self._name = name

    @property
    def clock(self):
        return self._clock

    @property
    def name(self):
        return self._name

    @property
    def input_fifos(self):
        return self._input_fifos

    @property
    def raw_output_fifos(self):
        return self._raw_output_fifos

    @property
    def output_drivers(self):
        return self._output_drivers

    def output_handler_gen(self, output_num, name=""):
        raise NotImplementedError(
            "Sub-classes of SoftwareBlock should define a "
            '"output_handler_gen" function'
        )

    def input_callback_gen(self, input_num):
        raise NotImplementedError(
            "Sub-classes of SoftwareBlock should define a "
            '"input_callback_gen" function'
        )

    class OutputDriver(Driver):
        def __init__(self, clock, fifo_block, output_num, handler):
            super().__init__()
            self._output_num = output_num
            self._clock = clock
            self._fifo = fifo_block
            self._handler = handler

        @property
        def clock(self):
            return self._clock

        @property
        def fifo(self):
            return self._fifo

        @property
        def output_num(self):
            return self._output_num

        @property
        def handler(self):
            return self._handler

        @cocotb.coroutine
        def _driver_send(self, transaction, sync=True, **kwargs):
            yield self.handler(transaction)

        @cocotb.coroutine
        def write_to_fifo(self, data, sync=True):
            if sync:
                yield RisingEdge(self.clock)
                self.fifo.write_enable <= 0
            while self.fifo.almost_full != 0:
                yield RisingEdge(self.clock)

            self.fifo.write_enable <= 1
            self.fifo.write_data <= int(data)
            yield RisingEdge(self.clock)
            self.fifo.write_enable <= 0

    def add_fifo(self, fifo_block, clock, name, io_enum, direction="in"):

        if direction.lower() == "in":
            callback = self.input_callback_gen(io_enum.value)
            wrapper = fifo_wrapper.FifoMonitor(
                fifo_block, clock, name, io_enum, callbacks=[callback], write_out=False
            )
            self._input_fifos.append(wrapper)
        elif direction.lower() == "out":
            self._raw_output_fifos.append(fifo_block)

    def start(self):
        for i, output_fifo_block in enumerate(self._raw_output_fifos):
            handler = self.output_handler_gen(i)
            output_driver = self.OutputDriver(self.clock, output_fifo_block, i, handler)
            self._output_drivers.append(output_driver)
