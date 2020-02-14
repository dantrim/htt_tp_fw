
import cocotb
from cocotb.triggers import Event, Combine, with_timeout

from fifo_monitors import WordMonitor
from fifo_drivers import BasicFifoDriver

from tptest import events, util


class FifoWrapper(object) :

    def __init__(self, fifo, clock, name = "Fifo") :

        """
        A class to wrap the FIFO functionality of the
        SpyBuffer block

        args:
            fifo: the spybuffer block
            clock: the simulation clock
            name: name of this wrapper object
        """

        self.name = "FifoWrapper_{}".format(name)
        self.fifo = fifo
        self.clock = clock

        self._driver = None
        self._expected_output = []

        self._monitor = None
        self._observed_output = []

    def word_count(self) :
        return len(self._expected_output), len(self._observed_output)

    def input_word_monitor(self, transaction) :
        self._expected_output.append(transaction)

    def send_event(self, event, build_events = True) :

        input_callback = None
        if not build_events :
            input_callback = self.input_word_monitor
        else :
            raise Exception("We do not handle cases where we build events")

        words = list(event)
        for iword, word in enumerate(words[:-1]) :
            self._driver.append(word.get_binary(), callback = input_callback)
            self._monitor.expect(word)
        else :
            hook = Event()
            self._driver.append(words[-1].get_binary(), callback = input_callback, event = hook)
            self._monitor.expect(words[-1])
        return hook

    def send_data_from_file(self, filename = "", build_events = True, num_events = -1) :

        if not build_events :
            self._expected_output = []
            self._driver = BasicFifoDriver(name = "WordDriver", fifo = self.fifo, clock = self.clock)

            self._observed_output = []
            self._monitor = WordMonitor(fifo = self.fifo, clock = self.clock, observed_output = self._observed_output)
        else :
            raise Exception("We do not handle cases where we build events")

        input_events = events.read_events_from_file(filename)
        n_events = len(input_events)
        if num_events > 0 : n_events = num_events
        
        self.fifo._log.info("Sending {} events to fifo {}".format(n_events, self.name))
        if input_events :
            if num_events > 0 :
                if num_events >= len(input_events) :
                    pass
                else :
                    input_events = input_events[:num_events]

            for ievent, event in enumerate(input_events) :
                self.fifo._log.info("Sending event L0ID {}".format(util.hex(event.l0id)))
                hook = self.send_event(event, build_events = build_events)
            else :
                return hook
        return None

    @cocotb.coroutine
    def wait_for_events(self, timeout = -1, units = "ns") :

        done = True
        hooks = []
        output_monitor = self._monitor
        if output_monitor.has_remaining_events() :
            output_monitor.on_empty.clear()
            hooks.append(output_monitor.on_empty.wait())
            output_monitor.expect_empty = True
            done = False
        if not done :
            tr = Combine(*hooks)
            if timeout == -1 :
                yield tr
            else :
                yield with_timeout(tr, timeout, units)
            
