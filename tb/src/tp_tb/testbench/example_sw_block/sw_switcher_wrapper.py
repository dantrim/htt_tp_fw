from bitstring import BitArray

import cocotb
from cocotb.triggers import Event, Combine, with_timeout, Timer

from tp_tb.testbench.example_sw_block.sw_switcher_ports import SWSwitcherPorts

from tp_tb.utils import events
from tp_tb.utils import block_wrapper


class SWSwitcherWrapper(block_wrapper.BlockWrapper):
    def __init__(self, clock, name):
        super().__init__(
            clock, name, len(SWSwitcherPorts.Inputs), len(SWSwitcherPorts.Outputs),
        )

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
