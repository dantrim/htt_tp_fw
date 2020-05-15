from bitstring import BitArray
from columnar import columnar

import cocotb
from cocotb.triggers import Event, Combine, with_timeout, Timer

from tb_b2b import b2b_utils
from tb_b2b import b2b_flow
from tb_utils import events

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

class bcolors:
    #HEADER = '\033[95m'
    #OKBLUE = '\033[94m'
    #OKGREEN = '\033[92m'
    #WARNING = '\033[93m'
    #FAIL = '\033[91m'
    #ENDC = '\033[0m'
    #BOLD = '\033[1m'
    #UNDERLINE = '\033[4m'
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''

class B2BWrapper(Wrapper) :

    def __init__(self, clock, name) :
        super().__init__(clock, name, len(b2b_utils.B2BIO.Inputs), len(b2b_utils.B2BIO.Outputs))


    def add_input_driver(self, driver, IO, active = True) :

        io_num = IO.value
        if io_num > self.n_input_ports :
            raise ValueError("Provided input driver \"{}\" is registered for invalid IO port {}, B2B block only has {} input ports".format(driver.name, io_num, self.n_input_ports))

        self._input_ports[io_num][0] = driver
        self._input_ports[io_num][1] = IO
        self._input_ports[io_num][2] = active

    def add_output_monitor(self, monitor, IO, active = True) :

        io_num = IO.value
        if io_num > self.n_output_ports :
            raise ValueError("Provided output monitor \"{}\" is registered for invalid IO port {}, B2B block only has {} output ports".format(monitor.name, io_num, self.n_output_ports))

        self._output_ports[io_num][0] = monitor
        self._output_ports[io_num][1] = IO
        self._output_ports[io_num][2] = active

    def close(self) :

        for input_port in self._input_ports :
            driver = input_port[0]
            if driver.dump :
                driver.close()

        for i in range(self.n_input_ports) :
            self.set_input_state(i, False)
        for i in range(self.n_output_ports) :
            self.set_output_state(i, False)

    def send_input_events(self, input_testvectors, n_to_send = -1, l0id_request = -1, event_delays = False) :

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
                    flow_kwargs = {}

                    # delays are entered at event boundaries
                    if word.is_start_of_event() :
                        flow_kwargs.update( b2b_flow.event_rate_delay(io, event, pass_through = not event_delays) )
                    hook = Event() # used to tell outside world that all events have been queued to be sent into the fifos
                    driver.append(word.get_binary(), event = hook, **flow_kwargs)
            if hook :
                hooks.append(hook.wait())

        return hooks

    def compare_port_with_expected(self, port_num, expected_events) :

        fifo, io, is_active = self.output_ports[port_num]
        #port_str = "(port_num, port_name) = ({}, {})".format(io.value, io.name)
        port_str = "({}, {})".format(io.value, io.name)

        test_n_events = True
        test_l0ids = True
        test_l0ids_order = True
        test_event_headers = True
        test_event_footers = True
        test_n_modules = True
        test_n_words_module = True
        test_module_headers = True
        test_module_footers = True

        ##
        ## for ports marked as not active, we do not expect to have any data
        ## but there may still be testvectors defined for them, so we avoid
        ## this case by returning here
        ##
        if not is_active :
            return True

        log = cocotb.log

        observed_data_words = fifo.observed_words
        observed_events = events.load_events(observed_data_words, "little")

        ##
        ## number of events as expected
        ##
        n_expected = len(expected_events)
        n_observed = len(observed_events)
        if n_expected != n_observed :
            test_n_events = False

        ##
        ## received L0IDs the same
        ##
        l0ids_expected = [x.l0id for x in expected_events]
        l0ids_observed = [x.l0id for x in observed_events]
        test_l0ids = set(l0ids_expected) == set(l0ids_observed)

        if not test_l0ids :
            #log.error("TEST {} Observed and expected L0IDs are different for {}".format(port_str, port_str))
            exp_set = set(l0ids_expected)
            obs_set = set(l0ids_observed)

            common_l0ids = sorted(list(exp_set.intersection(obs_set)))
            in_exp_not_obs = sorted(list(exp_set - obs_set))
            in_obs_not_exp = sorted(list(obs_set - exp_set))

            n_common, n_exp_not_obs, n_obs_not_exp = len(common_l0ids), len(in_exp_not_obs), len(in_obs_not_exp)
            n_rows = max([n_common, n_exp_not_obs, n_obs_not_exp])
            for l in [ common_l0ids, in_exp_not_obs, in_obs_not_exp ] :
                while len(l) != n_rows :
                    l.append(-1)

            header = ["{}TEST ERROR {}{}".format(bcolors.FAIL,port_str,bcolors.ENDC), "Expected L0IDs not observed", "Observed L0IDs not expected"]
            data = []
            eo = []
            oe = []
            for i in range(n_rows) :
                if in_exp_not_obs[i] >= 0 :
                    eo.append(hex(in_exp_not_obs[i]))
                if in_obs_not_exp[i] >= 0 :
                    oe.append(hex(in_obs_not_exp[i]))
            data.append(["", "\n".join(eo), "\n".join(oe)])
            table = columnar(data, header, no_borders = False)
            log.info(table)

        ##
        ## observed L0IDs are in the same order
        ##

        l0id_event_fails = []
        if not test_l0ids :
            test_l0ids_order = False # just set this false if set of L0IDs differ 
        else : 
            for iexpected, expected_l0id in enumerate(l0ids_expected) :
                observed_l0id = l0ids_observed[iexpected]
                if observed_l0id != expected_l0id :
                    l0id_event_fails.append(iexpected)
        test_l0ids_order = not len(l0id_event_fails)
        first_expected_l0id_fail = None 
        first_observed_l0id_fail = None 
        if not test_l0ids_order :
            #log.info("TEST {} Observed L0IDs appear in different order than expected!".format(port_str))
            first_expected_l0id_fail_idx = l0id_event_fails[0]
            first_expected_l0id_fail = l0ids_expected[first_expected_l0id_fail_idx]
            first_observed_l0id_fail = l0ids_observed[first_expected_l0id_fail_idx]
            #log.info("TEST {} First out of order L0ID appears at expected event number {}, with Expected L0ID={} and Observed L0ID={}"
            #            .format(port_str, first_expected_l0id_fail_idx, hex(first_expected_l0id_fail), hex(first_observed_l0id_fail)))

        ##
        ## event-by-event checks
        ##
        test_n_events = True
        test_l0ids = True
        test_l0ids_order = True
        test_continue = test_n_events and test_l0ids
        if not test_continue :
            return False

        # here we sort the events by l0id
        expected_events_sorted = sorted(expected_events, key = lambda x : x.l0id)
        observed_events_sorted = sorted(observed_events, key = lambda x : x.l0id)

        l0id_header_fails = []
        l0id_footer_fails = []
        l0id_n_module_fails = []
        l0id_module_len_fails = {}

        failed_footer_fields = set()
        failed_header_fields = set()


        for ievent in range(len(expected_events_sorted)) :
            expected_event = expected_events_sorted[ievent]
            observed_event = observed_events_sorted[ievent]
            l0id = expected_event.l0id

            ##
            ## event header
            ##
            event_header_words_expected = expected_event.header_words
            event_header_words_observed = observed_event.header_words
            headers_equal = event_header_words_expected == event_header_words_observed # this does word-by-word comparison

            if not headers_equal :
                l0id_header_fails.append(l0id)

                # only print detailed information if there is a failure
                header_field_names = observed_event.header_field_names()
                table_header = ["{}TEST ERROR {}\nL0ID={}{}".format(bcolors.FAIL,port_str, hex(l0id),bcolors.ENDC), "HEADER FIELD", "OBSERVED", "EXPECTED", "ERROR"]
                err_str = { True : "PASS", False : "{}FAIL{}".format(bcolors.FAIL, bcolors.ENDC) }
                data = []
                for header_row in header_field_names :
                    for field in header_row :
                        obs = observed_event.header_field(field)
                        exp = expected_event.header_field(field)
                        data.append( ["", field, hex(obs), hex(exp), err_str[obs==exp]] )
                        if not obs==exp :
                            failed_header_fields.add(field)
                table = columnar(data, table_header, no_borders = False)
                log.info(table)
                


            ##
            ## event footer
            ##
            event_footer_words_expected = expected_event.footer_words
            event_footer_words_observed = observed_event.footer_words
            footers_equal = event_footer_words_expected == event_footer_words_observed # this does word-by-word comparison

            if not footers_equal :
                l0id_footer_fails.append(l0id)

                # only print detailed information if there is a failure
                footer_field_names = observed_event.footer_field_names()
                table_header = ["{}TEST ERROR {}\nL0ID={}{}".format(bcolors.FAIL,port_str,hex(l0id),bcolors.ENDC), "FOOTER FIELD", "OBSERVED", "EXPECTED", "ERROR"]
                err_str = { True : "PASS", False : "{}FAIL{}".format(bcolors.FAIL, bcolors.ENDC) }
                data = []
                for footer_row in footer_field_names :
                    for field in footer_row :
                        obs = observed_event.footer_field(field)
                        exp = expected_event.footer_field(field)
                        data.append( ["", field, hex(obs), hex(exp), err_str[obs==exp]] )
                        if not obs==exp :
                            failed_footer_fields.add(field)
                table = columnar(data, table_header, no_borders = False)
                log.info(table)

            ##
            ## modules
            ##
            n_modules_expected = expected_event.n_modules
            n_modules_observed = observed_event.n_modules
            n_modules_equal = n_modules_expected == n_modules_observed
            if not n_modules_equal :
                l0id_n_module_fails.append(l0id)

            ##
            ## each module has the same number of data words
            ##
            module_len_fails = {}
            if n_modules_equal :
                expected_modules = expected_event.get_modules()
                observed_modules = observed_event.get_modules()
                for imod in range(n_modules_expected) :
                    expected_module = expected_modules[imod]
                    observed_module = observed_modules[imod]

                    n_mod_dwords_expected = len(expected_module)
                    n_mod_dwords_observed = len(observed_module)

                    n_mod_dwords_equal = n_mod_dwords_expected == n_mod_dwords_observed
                    if not n_mod_dwords_equal :
                        module_len_fails[imod] = { "expected" : n_mod_dwords_expected, "observed" : n_mod_dwords_observed }
            l0id_module_len_fails[hex(l0id)] = module_len_fails

        n_h, n_f, n_m = len(l0id_header_fails), len(l0id_footer_fails), len(l0id_n_module_fails)
        n_mod_len_fail = False
        for l0id, faildict in l0id_module_len_fails.items() :
            if faildict :
                n_mod_len_fail = True
                break
        if n_h or n_f or n_m or n_mod_len_fail :
            #log.info("{}TEST ERROR{} {} Unexected event header/footer/number of modules:".format(port_str))
            #log.info("TEST {} Unexpected event headers (failed in {} events), event footers (failed in {} events), number of modules (failed in {} events)"
            #    .format(port_str, n_h, n_f, n_m))
            n_rows = max([n_h, n_f, n_m])
            for l in [l0id_header_fails, l0id_footer_fails, l0id_n_module_fails] :
                while len(l) != n_rows :
                    l.append(-1)
            r0 = "TEST {}".format(port_str)
            #headers = [r0, "Event Header Failures", "Event Footer Failures", "Module Count Failures"]
            headers = ["{}TEST ERROR {} {}".format(bcolors.FAIL, port_str, bcolors.ENDC), "L0ID w/ Occurrences", "Info"]
            data = []
            hf_fails = []
            ff_fails = []
            mf_fails = []
            #log.info(header)
            for i in range(n_rows) :
                if l0id_header_fails[i] >= 0 :
                    hf_fails.append(hex(l0id_header_fails[i]))
                if l0id_footer_fails[i] >= 0 :
                    ff_fails.append(hex(l0id_footer_fails[i]))           
                if l0id_n_module_fails[i] >= 0 :
                    mf_fails.append(hex(l0id_n_module_fails[i]))
#                hf = hex(l0id_header_fails[i]) if l0id_header_fails[i] >= 0 else ""
#                ff = hex(l0id_footer_fails[i]) if l0id_footer_fails[i] >= 0 else ""
#                mf = hex(l0id_n_module_fails[i]) if l0id_n_module_fails[i] >= 0 else ""
#                data.append( ["", hf, ff, mf] )
                #line = "TEST {} {}\t{}\t{}".format(port_str, hf, ff, mf)
                #log.info(line)

            data = [
                ["Event Header Errors", ", ".join(hf_fails), ""]
                ,["Event Footer Errors", ", ".join(ff_fails), ""]
                ,["Module Count Errors", ", ".join(mf_fails), ""]
            ]

            if n_mod_len_fail :
                test_n_words_module = False
                l0ids = list(l0id_module_len_fails.keys())
                l0id_str = ", ".join(l0ids)
                info_str = {}
                for l0 in l0ids :
                    event_fails = []
                    for module_num, faildict in l0id_module_len_fails[l0].items() :
                        fail_str = "Module # {:03} (obs: {}, exp: {})".format(module_num, faildict["observed"], faildict["expected"])
                        event_fails.append(fail_str)
                    info = ["L0ID: {}".format(l0)]
                    event_fails = "\n".join(event_fails)
                    info_str[l0] = event_fails
                
                is_first = True
                for il0, l0 in enumerate(l0ids) :
                    if l0id_module_len_fails[l0] :
                        if is_first :
                            data.append( ["Module Length Errors", l0, "{}".format(info_str[l0])] )
                            is_first = False
                        else :
                            data.append( ["", l0, "{}".format(info_str[l0])] )
            else :
                data.append( ["Module Length Errors", "", ""] )
            table = columnar(data, headers, no_borders = False)
            log.info(table)

        test_event_headers = n_h == 0
        test_event_footers = n_f == 0
        test_n_modules = n_m == 0 

        result_str = { True : "PASS", False : "{}FAIL{}".format(bcolors.FAIL,bcolors.ENDC) }
        n_x = 80
        log.info(n_x * "*")
        table_header = ["TEST SUMMARY {}\nSub-test".format(port_str), "Result", "Notes"]
        data = [
            ["Correct Number of Events", result_str[test_n_events], "# events\n(exp., obs.) = ({},{})".format(n_expected, n_observed)]
            ,["Correct L0IDs received", result_str[test_l0ids], ""]
            ,["L0IDs received in correct order", result_str[test_l0ids_order], "First bad L0ID event:\n(exp., obs.)=({},{})".format(first_expected_l0id_fail, first_observed_l0id_fail)]
            ,["Event headers correct", result_str[test_event_headers], "Bad event header fields:\n{}".format(", ".join(failed_header_fields))]
            ,["Event footers correct", result_str[test_event_footers], "Bad event footer fields:\n{}".format(", ".join(failed_footer_fields))]
            ,["Correct # of modules/event", result_str[test_n_modules], ""]
            ,["Module lengths correct", result_str[test_n_words_module], ""]
            ,["Correct module headers/event", "NOT TESTED (YET)", ""]
            ,["Correct module footers/event", "NOT TESTED (YET)", ""]
        ]
        table = columnar(data, table_header, no_borders = False)
        log.info(table)
        log.info(n_x * "*")

        return (test_n_events
                and test_l0ids
                and test_l0ids_order
                and test_n_modules
                and test_event_headers
                and test_event_footers
                and test_module_headers
                and test_module_footers
            )

    def compare_outputs_with_expected(self, expected_output_events) :

        log = cocotb.log

        test_passed = True
        result_str = { True : "PASS", False : "FAIL" }
        results = []
        for port_num, exp_events in enumerate(expected_output_events) :

            fifo, io, is_active = self.output_ports[port_num]
            port_str = "({}, {})".format(io.value, io.name)
            port_passed = self.compare_port_with_expected(port_num, exp_events)
            if not port_passed :
                test_passed = False

            results.append( (port_str, test_passed) )

        header = ["B2B TEST RESULTS SUMMARY\nOUTPUT PORT", "RESULT"]
        data = []
        for r in results :
            port_str, res = r
            data.append( [port_str, result_str[res]] )
        data.append([10 * "*" for _ in header])
        data.append(["{}FINAL B2B RESULT{}".format(bcolors.OKBLUE,bcolors.ENDC), result_str[test_passed]])
        table = columnar(data, header, no_borders = False)
        log.info(table)

        return test_passed
