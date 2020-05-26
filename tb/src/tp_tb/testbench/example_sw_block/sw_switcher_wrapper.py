from bitstring import BitArray

import cocotb
from cocotb.triggers import Event, Combine, with_timeout, Timer

from . import sw_switcher_utils

from tp_tb.utils import events


class Wrapper:
    def __init__(self, clock, name, n_input_ports, n_output_ports):

        self._clock = clock
        self._name = name

        self._input_ports = tuple([[None, None, False] for i in range(n_input_ports)])
        self._output_ports = tuple([[None, None, False] for i in range(n_output_ports)])

    @property
    def clock(self):
        return self._clock

    @property
    def name(self):
        return self._name

    @property
    def n_input_ports(self):
        return len(self._input_ports)

    @property
    def n_output_ports(self):
        return len(self._output_ports)

    @property
    def input_ports(self):
        return self._input_ports

    @property
    def output_ports(self):
        return self._output_ports

    def __str__(self):
        return f'Wrapper "{self.name}": (IN,OUT)=({self.n_input_ports},{self.n_output_ports}) = ({self._io_bitmask()[0].bin}, {self._io_bitmask()[1].bin})'

    def __repr__(self):
        return f'Wrapper "{self.name}": (IN,OUT)=({self.n_input_ports},{self.n_output_ports}) = ({self._io_bitmask()[0].bin}, {self._io_bitmask()[1].bin})'

    def _io_bitmask(self):

        inputs = BitArray([x[2] for x in self._input_ports[::-1]])
        outputs = BitArray([x[2] for x in self._output_ports[::-1]])
        return inputs, outputs

    def set_input_state(self, io_num, active):

        if self._input_ports[io_num][0]:
            self._input_ports[io_num][2] = active
        else:
            self._input_ports[io_num][2] = False

    def set_output_state(self, io_num, active):

        if self._output_ports[io_num][0]:
            self._output_ports[io_num][2] = active
        else:
            self._output_ports[io_num][2] = False

    def sort_ports(self):

        self._input_ports = tuple(sorted(self._input_ports, key=lambda x: x[1].value))
        self._output_ports = tuple(sorted(self._output_ports, key=lambda x: x[1].value))

    def close(self):

        """
        Re-implement in derived class.
        """

        pass


class SWSwitcherWrapper(Wrapper):
    def __init__(self, clock, name):
        super().__init__(
            clock,
            name,
            len(sw_switcher_utils.SWSwitcherIO.Inputs),
            len(sw_switcher_utils.SWSwitcherIO.Outputs),
        )

    def add_input_driver(self, driver, IO, active=True):

        io_num = IO.value
        if io_num > self.n_input_ports:
            raise ValueError(
                f'Provided input driver "{driver.name}" is registered for invalid IO port {io_num}, B2B block only has {self.n_input_ports} input ports'
            )

        self._input_ports[io_num][0] = driver
        self._input_ports[io_num][1] = IO
        self._input_ports[io_num][2] = active

    def add_output_monitor(self, monitor, IO, active=True):

        io_num = IO.value
        if io_num > self.n_output_ports:
            raise ValueError(
                f'Provided output monitor "{monitor.name}" is registered for invalid IO port {io_num}, B2B block only has {self.n_output_ports} output ports'
            )

        self._output_ports[io_num][0] = monitor
        self._output_ports[io_num][1] = IO
        self._output_ports[io_num][2] = active

    def close(self):

        for input_port in self._input_ports:
            driver = input_port[0]
            if driver.dump:
                driver.close()

        for i in range(self.n_input_ports):
            self.set_input_state(i, False)
        for i in range(self.n_output_ports):
            self.set_output_state(i, False)

    def send_input_events(
        self, input_testvectors, n_to_send=-1, l0id_request=-1, event_delays=False
    ):

        n_input_files = len(input_testvectors)
        if n_input_files != self.n_input_ports:
            raise ValueError(
                f"Number of input event tables (={n_input_files}) is not equal to number of B2B input ports (={self.n_input_ports})"
            )

        hooks = []
        for port_num, testvector_file in enumerate(input_testvectors):

            driver, io, active = self.input_ports[port_num]

            input_events = events.load_events_from_file(
                filename=testvector_file, n_to_load=n_to_send, l0id_request=l0id_request
            )
            cocotb.log.info(
                f"Sending {len(input_events)} events to input (port_num, port_name) = ({io.value}, {io.name}) from testvector {testvector_file}"
            )

            hook = None
            for ievent, event in enumerate(input_events):
                words = list(event)
                for iword, word in enumerate(words):
                    flow_kwargs = {}

                    # delays are entered at event boundaries
                    hook = (
                        Event()
                    )  # used to tell outside world that all events have been queued to be sent into the fifos
                    driver.append(word.get_binary(), event=hook, **flow_kwargs)
            if hook:
                hooks.append(hook.wait())

        return hooks
