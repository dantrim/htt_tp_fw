
from pathlib import Path

import cocotb
from cocotb.triggers import Timer

from tptest import events, util

from .b2b_utils import B2BIO, get_testvector_files
from b2b_test.fifo_output_monitor import WordMonitor

class B2BOutputMonitor :

    """
    A class to monitor and process the data received on the output
    FIFOs of the B2B block.
    """

    def __init__(self, dut, base_tp, n_words_expected = 0) :

        if type(base_tp) != B2BIO.B2BOutputs :
            raise Exception("ERROR B2BOutputDriver base_tp must be of type {}".format(type(B2BIO.B2BOutputs)))

        self._output_fifos = [x.output_buffer for x in dut.output_cluster_SpyBuffer] # expect the FIFO order to match indices designated in B2BIO.B2BOutputs
        self._clock = dut.clock
        self._name = "B2BOutputMonitor_{}".format(base_tp.name)
        self._base_tp = base_tp
        self._log = dut._log

        self._log.info("B2BOutputMonitor (name={}) initialized with {} FIFOs".format(self.name, len(self.output_fifos)))

        self._monitors = []
        self._testvecs_expected = []
        self._n_words_expected = n_words_expected
        self._n_words_recvd = 0

    ##
    ## properties
    ##

    @property
    def output_fifos(self) :
        return self._output_fifos

    @property
    def clock(self) :
        return self._clock

    @property
    def name(self) :
        return self._name

    @property
    def base_tp(self) :
        return self._base_tp

    @property
    def n_words_expected(self) :
        """
        The total number of words that should be observed at the output
        of the B2B block
        """
        return self._n_words_expected

    @property
    def n_words_received(self) :
        return self._n_words_recvd


    ##
    ## methods
    ##

    def configure_monitors(self, testvecdir = "") :

        testvec_expected = get_testvector_files(self.base_tp, testvecdir, "output")
        self._log.info("Establing output FIFO monitors")

        for fifo in B2BIO.B2BOutputs :

            input_num = int(fifo.value)
            testvec = testvec_expected[input_num]
            self._log.info(" -> Output {} ({}) : Expected = {}".format(input_num, fifo.name, testvec))

            monitor = WordMonitor(self.output_fifos[input_num], self.clock,
                        "OutputFIFOMonitor_{}".format(input_num))
            self._monitors.append(monitor)
            self._testvecs_expected.append(testvec)

    
    @cocotb.coroutine
    def wait_for_events(self, timeout = -1, units = "ns") :

        done = True
        hooks = []

        for i, mon in enumerate(self._monitors) :
            cocotb.log.info(" -> OUTPUT FIFO {} RECVD {} WORDS".format(mon.name, mon.n_words_received()))
            self._n_words_recvd += mon.n_words_received()
        cocotb.log.info("  ==> OUTPUT N WORDS RECVD: {}".format(self._n_words_recvd))
        all_recvd = self._n_words_recvd == self.n_words_expected

        if not all_recvd :
            yield Timer(timeout, units) # just use a Timeout, until settling on a more robust method for filling expected/routed event numbers
