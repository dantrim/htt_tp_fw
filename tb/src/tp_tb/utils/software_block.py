import cocotb

from .utils import fifo_wrapper


class SoftwareBlock:
    def __init__(self, clock, name):
        self._clock = clock
        self._input_fifos = []
        self._output_fifos = []
        self._input_callbacks = []
        self._name = name

    @property
    def clock(self):
        return self._clock

    @property
    def input_fifos(self):
        return self._input_fifos

    @property
    def output_fifos(self):
        return self._output_fifos

    @property
    def input_callbacks(self):
        return self._input_callbacks

    @property
    def name(self):
        return self._name

    def add_fifo(self, fifo_block, clock, name, io_enum, callback, direction="in"):

        if direction.lower() == "in":
            callback = self.input_callbacks[io_enum.value]
            wrapper = fifo_wrapper.FifoMonitor(
                fifo_block, clock, name, io_enum, callbacks=[callback], write_out=False
            )
            self._input_fifos.append(wrapper)
        elif direction.lower() == "out":
            wrapper = fifo_wrapper.FifoDriver(
                fifo_block, clock, name, io_enum, write_out=False
            )
            self._output_fifos.append(wrapper)
