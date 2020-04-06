from bitstring import BitArray

import cocotb
from cocotb.triggers import Event, Combine, with_timeout, Timer

from tb_b2b import b2b_utils
from tb_utils import events, utils
#import event_parse

class Wrapper :

    def __init__(self, clock, name, n_input_ports, n_output_ports) :

        self._clock = clock
        self._name = name

        self._input_ports = tuple( [[None, None, False] for i in range(n_input_ports)] )
        self._output_ports = tuple( [ [None, None, False] for i in range(n_output_ports)] )

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

        inputs = BitArray( [x[2] for x in self._input_ports[::-1]] )
        outputs = BitArray( [x[2] for x in self._output_ports[::-1]] )
        return inputs, outputs

    def set_input_state(self, io_num, active) :

        if self._input_ports[io_num][0] :
            self._input_ports[io_num][2] = active
        else :
            self._input_ports[io_num][2] = False

    def set_output_state(self, io_num, active) :

        if self._output_ports[io_num][0] :
            self._output_ports[io_num][2] = active
        else :
            self._output_ports[io_num][2] = False

    def sort_ports(self) :

        self._input_ports = tuple(sorted(self._input_ports, key = lambda x : x[1].value))
        self._output_ports = tuple(sorted(self._output_ports, key = lambda x : x[1].value))

    def close(self) :

        """
        Re-implement in derived class.
        """

        pass

class B2BWrapper(Wrapper) :

    def __init__(self, clock, name) :
        super().__init__(clock, name, len(b2b_utils.B2BIO.Inputs), len(b2b_utils.B2BIO.Outputs))

    def add_input_driver(self, driver, IO) :

        io_num = IO.value
        if io_num > self.n_input_ports :
            raise ValueError("Provided input driver \"{}\" is registered for invalid IO port {}, B2B block only has {} input ports".format(driver.name, io_num, self.n_input_ports))

        self._input_ports[io_num][0] = driver
        self._input_ports[io_num][1] = IO
        self._input_ports[io_num][2] = driver.active

    def add_output_monitor(self, monitor, IO) :

        io_num = IO.value
        if io_num > self.n_output_ports :
            raise ValueError("Provided output monitor \"{}\" is registered for invalid IO port {}, B2B block only has {} output ports".format(monitor.name, io_num, self.n_output_ports))

        self._output_ports[io_num][0] = monitor
        self._output_ports[io_num][1] = IO
        self._output_ports[io_num][2] = monitor.active

    def close(self) :

        for input_port in self._input_ports :
            driver = input_port[0]
            if driver.dump :
                driver.close()

        for i in range(self.n_input_ports) :
            self.set_input_state(i, False)
        for i in range(self.n_output_ports) :
            self.set_output_state(i, False)

    def send_input_events(self, input_testvectors, n_to_send = -1, l0id_request = -1 ) :

        n_input_files = len(input_testvectors)
        if n_input_files != self.n_input_ports :
            raise ValueError("Number of input event tables (={}) is not equal to number of B2B input ports (={})".format(n_tables, self.n_input_ports))

        hooks = []
        for port_num, testvector_file in enumerate(input_testvectors) :

            driver, io, active = self.input_ports[port_num]

            input_events = events.load_events_from_file(filename = testvector_file, n_to_load = n_to_send, l0id_request = l0id_request)
            cocotb.log.info("Sending {} events to input (port_num, port_name) = ({}, {}) from testvector {}".format(len(input_events), io.value, io.name, testvector_file))

            hook = None
            for ievent, event in enumerate(input_events) :
                words = list(event)
                for iword, word in enumerate(words) :
                    hook = Event()
                    driver.append(word.get_binary(), event = hook)
            if hook :
                hooks.append(hook.wait())

        return hooks

    def compare_outputs(self, expected_output_events) :

        print(80 * "=")
        for port_num, exp_events in enumerate(expected_output_events) :
            print(40 * "- ")
            monitor, io, active = self.output_ports[port_num]
            if not active :
                exp_events = []

            received_words = monitor.observed_data_words
            obs_events = events.load_events(received_words, "little")

            port_str = "(port_num, port_name) = ({}, {})".format(io.value, io.name)

            n_events_expected = len(exp_events)
            n_events_observed = len(obs_events)
            print("Output {} : N_expected = {}, N_observed = {}".format(port_str, n_events_expected, n_events_observed))
            if n_events_expected != n_events_observed and active:
                print("\tNumber of observed and expected events differ for {}!".format(port_str))
                return

            print("Observed events:")
            for ievent, event in enumerate(obs_events) :
                l0id = event.l0id
                n_modules = event.n_modules
                n_words = len(event.words)
                print(" Event num {:03} : L0ID={}, N_words={}, N_modules={}".format(ievent, hex(l0id), n_words, n_modules))
                for i, h in enumerate(event.header_words) :
                    print("    Header[{:02}] = {}".format(i, h.hex()))
                for i, f in enumerate(event.footer_words) :
                    print("    Footer[{:02}] = {}".format(i, f.hex()))

            print("Expected events:")
            for ievent, event in enumerate(exp_events) :
                l0id = event.l0id
                n_modules = event.n_modules
                n_words = len(event.words)
                print(" Event num {:03} : L0ID={}, N_words={}, N_modules={}".format(ievent, hex(l0id), n_words, n_modules))
                print(" ==== HEADER ====")
                for i, h in enumerate(event.header_words) :
                    print("    Header[{:02}] = {}".format(i, h.hex()))
                print(" ==== FOOTER ====")
                for i, f in enumerate(event.footer_words) :
                    print("    Footer[{:02}] = {}".format(i, f.hex()))

            print("")
            for ievent in range(len(obs_events)) :
                obs_event = obs_events[ievent]
                exp_event = exp_events[ievent]

                ##
                ## header
                ##
                obs_header = obs_event.header_words
                exp_header = exp_event.header_words
                headers_ok = { True : "Y", False : "N" }[obs_header == exp_header]
                print("\t-> Event {:02} header ok? {}".format(ievent, headers_ok))

                ##
                ## modules
                ##
                obs_n_modules = obs_event.n_modules
                exp_n_modules = exp_event.n_modules
                n_modules_ok = { True : "Y", False : "N" }[obs_n_modules == exp_n_modules]
                print("\t-> Event {:02} N modules ok? {}".format(ievent, n_modules_ok))
                if n_modules_ok :
                    obs_module_data = obs_event.get_modules()
                    exp_module_data = exp_event.get_modules()
                    module_data_ok = True
                    for i in range(len(obs_module_data)) :
                        obs_data = obs_module_data[i]
                        exp_data = exp_module_data[i]

                        obs_module_header = [hex(x.value) for x in obs_data.header_words]
                        exp_module_header = [hex(x.value) for x in exp_data.header_words ]
                        mod_header_ok = obs_module_header == exp_module_header

                        obs_module_footer = [hex(x.value) for x in [obs_data.footer]]
                        exp_module_footer = [hex(x.value) for x in [exp_data.footer]]
                        mod_footer_ok = obs_module_footer == exp_module_footer

                        if not mod_header_ok :
                            module_data_ok = False
                        if not mod_footer_ok :
                            module_data_ok = False

                        mod_header_ok = { True : "Y", False : "N" }[mod_header_ok]
                        mod_footer_ok = { True : "Y", False : "N" }[mod_footer_ok]
                        print("\t\t\tModule {:02}: header ok? {}, footer ok? {}".format(i, mod_header_ok , mod_footer_ok))

                    module_data_ok = { True : "Y", False : "N" }[module_data_ok]
                    print("\t-> Event {:02} Module data ok? {}".format(ievent, module_data_ok))
                    

                ##
                ## footer
                ##
                obs_footer = obs_event.footer_words
                exp_footer = exp_event.footer_words
                footers_ok = { True : "Y", False : "N" }[obs_footer == exp_footer]
                print("\t-> Event {:02} footer ok? {}".format(ievent, footers_ok))



        print(80 * "=")
