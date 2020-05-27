import cocotb
from cocotb.triggers import Event, Combine, with_timeout, Timer

from tp_tb.testbench.evt_sync import evt_sync_utils

from tp_tb.utils import events
from tp_tb.utils import block_wrapper


class EvtSyncWrapper(block_wrapper.BlockWrapper):
    def __init__(self, clock, name):
        super().__init__(
            clock,
            name,
            len(evt_sync_utils.EvtSyncIO.Inputs),
            len(evt_sync_utils.EvtSyncIO.Outputs),
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
                    # if word.is_start_of_event():
                    #    flow_kwargs.update(
                    #        b2b_flow.event_rate_delay(
                    #            io, event, pass_through=not event_delays
                    #        )
                    #    )
                    hook = (
                        Event()
                    )  # used to tell outside world that all events have been queued to be sent into the fifos
                    driver.append(word.get_binary(), event=hook, **flow_kwargs)
            if hook:
                hooks.append(hook.wait())

        return hooks

    # def send_input_events(self, input_testvectors, n_to_send=-1, l0id_request=-1):
    #    n_input_files = len(input_testvectors)
    #    if n_input_files != self.n_input_ports:
    #        raise ValueError(f"Number of input event tables (={n_input_files}) is not equal to number of EventSync input ports (={self.n_input_ports})")
    #    hooks = []
    #    n_sent_total = 0
    #    for port_num, testvector_file in enumerate(input_testvectors):
    #        driver, io, active = self.input_ports[port_num]
    #        input_events = events.load_events_from_file(filename = testvector_file, n_to_load = n_to_send, l0id_request = l0id_request)
    #        hook = None
    #        n_sent = 0
    #        for ievent, event in enumerate(input_events):
    #            words = list(event)
    #            for iword, word in enumerate(words):
    #                flow_kwargs = {}
    #                hook = Event()
    #                driver.append(word.get_binary(), event = hook, **flow_kwargs)
    #                n_sent += 1
    #        if hook:
    #            hooks.append(hook.wait())
    #        cocotb.log.info(60 * "-")
    #        cocotb.log.info(f"Sent {n_sent} words to input (port_num, port_name) = ({io.value}, {io.name}) from testvector {testvector_file}")
    #        n_sent_total += n_sent

    #    cocotb.log.info(f"Sent {n_sent_total} events in total")
    #    return hooks
