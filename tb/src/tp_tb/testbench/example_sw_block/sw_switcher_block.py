from tp_tb.utils import software_block


class SWSwitcherBlock(software_block.SoftwareBlock):
    def __init__(self, name):
        super().__init__(name)

        for i in range(2):
            self._input_callbacks.append(self.callback_gen(i))

    def callback_gen(self, input_num):
        if input_num == 0:
            return self._port_0_handle_input_data
        elif input_num == 1:
            return self._port_1_handle_input_data

    def _port_0_handle_input_data(self, transaction):
        print(f"Input[0] handle input: {hex(int(transaction))}")
        self.output_fifos[1].append(transaction)

    def _port_1_handle_input_data(self, transaction):
        print(f"Input[1] handle input: {hex(int(transaction))}")
        self.output_fifos[0].append(transaction)
