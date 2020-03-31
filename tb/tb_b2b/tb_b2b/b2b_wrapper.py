import cocotb
from cocotb.triggers import Event, Combine, with_timeout, Timer

from tptest import events, util

from tb_b2b import b2b_utils
from bitstring import BitArray, BitStream
import event_parse

class Wrapper :

    def __init__(self, clock, name, n_input_ports, n_output_ports) :

        self._clock = clock
        self._name = name

        self._input_ports = tuple( [[None, False] for i in range(n_input_ports)] )
        self._output_ports = tuple( [ [None, False] for i in range(n_output_ports)] )

    @property
    def clock(self) :
        return self._clock

    @property
    def name(self) :
        return self._name

    @property
    def n_input_ports(self) :
        return len(self._input_ports)

    @property
    def n_output_ports(self) :
        return len(self._output_ports)

    @property
    def input_ports(self) :
        return self._input_ports

    @property
    def output_ports(self) :
        return self._output_ports


    def __str__(self) :
        return "Wrapper \"{}\": (IN,OUT)=({},{}) - ({}, {})".format(self.name, self.n_input_ports, self.n_output_ports, self._io_bitmask()[0].bin, self._io_bitmask()[1].bin)

    def __repr__(self) :
        return "Wrapper \"{}\": (IN,OUT)=({},{}) - ({}, {})".format(self.name, self.n_input_ports, self.n_output_ports, self._io_bitmask()[0].bin, self._io_bitmask()[1].bin)

    def _io_bitmask(self) :

        inputs = BitArray( [x[1] for x in self._input_ports] )
        outputs = BitArray( [x[1] for x in self._output_ports] )
        return inputs, outputs

    def set_input_state(self, io_num, active) :

        if self._input_ports[io_num][0] :
            self._input_ports[io_num][1] = active
        else :
            self._input_ports[io_num][1] = False

    def set_output_state(self, io_num, active) :

        if self._output_ports[io_num][0] :
            self._output_ports[io_num][1] = active
        else :
            self._output_ports[io_num][1] = False

    def close(self) :

        """
        Re-implement in derived class.
        """

        pass

class B2BWrapper(Wrapper) :

    def __init__(self, clock, name) :
        super().__init__(clock, name, len(b2b_utils.B2BIO.Inputs), len(b2b_utils.B2BIO.Outputs))

    def add_input_driver(self, driver) :

        io_num = driver.io_num
        if io_num > self.n_input_ports :
            raise ValueError("Provided input driver \"{}\" is registered for invalid IO port {}, B2B block only has {} input ports".format(driver.name, io_num, self.n_input_ports))
        self._input_ports[io_num][0] = driver
        self._input_ports[io_num][1] = driver.active

    def add_output_monitor(self, monitor) :

        io_num = monitor.io_num
        if io_num > self.n_output_ports :
            raise ValueError("Provided output monitor \"{}\" is registered for invalid IO port {}, B2B block only has {} output ports".format(monitor.name, io_num, self.n_output_ports))

        self._output_ports[io_num][0] = monitor
        self._output_ports[io_num][1] = monitor.active

    def close(self) :

        for input_port in self._input_ports :
            driver = input_port[0]
            if driver.dump :
                driver.close()

        for i in range(self.n_input_ports) :
            self.set_input_state(i, False)
        for i in range(self.n_output_ports) :
            self.set_output_state(i, False)
            

