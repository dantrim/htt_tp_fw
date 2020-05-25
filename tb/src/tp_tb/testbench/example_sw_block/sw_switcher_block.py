from tp_tb.utils import software_block


class SWSwitcherBlock(software_block.SoftwareBlock):
    def __init__(self, clock, name):
        super().__init__(clock, name)

        self._dummy_delay_0 = 50
        self._dummy_delay_1 = 50
        self._dummy_delay_unit_str = "ns"

        for i in range(2):
            self._input_callbacks.append(self.callback_gen(i))

    def callback_gen(self, input_num):
        if input_num == 0:
            return self._port_0_handle_input_data
        elif input_num == 1:
            return self._port_1_handle_input_data

    def _port_0_handle_input_data(self, transaction):
        data, timestamp = transaction

        # add dummy delay mimicking some work being done
        # in reality we would probably try syncing up all the outputs,
        # but in principle the outputs could be uncorrelated with each other
        flow_kwargs = {
            "delay": self._dummy_delay_0,
            "delay_unit": self._dummy_delay_unit_str,
        }
        self.output_fifos[1].append(data, **flow_kwargs)

    def _port_1_handle_input_data(self, transaction):
        data, timestamp = transaction

        # add dummy delay mimicking some work being done
        # in reality we would probably try syncing up all the outputs,
        # but in principle the outputs could be uncorrelated with each other
        flow_kwargs = {
            "delay": self._dummy_delay_1,
            "delay_unit": self._dummy_delay_unit_str,
        }
        self.output_fifos[0].append(data, **flow_kwargs)
