
from pathlib import Path

import cocotb
from cocotb.triggers import Event, Combine, with_timeout

from tptest import events, util
from .b2b_utils import B2BIO


class B2BInputDriver :

    """
    A class to handle the input signals to the board-to-board block
    """

    def __init__(self, input_fifo_blocks, clock, base_tp) :

        if type(base_tp) != B2BIO.B2BOutputs :
            raise Exception("ERROR B2BInputDriver base_tp must be of type {}".format(type(B2BIO.B2BOutputs)))

        self._input_fifos = input_fifo_blocks
        self._clock = clock
        self._name = "B2BInputDriver_{}".format(base_tp.name)
        self._base_tp = base_tp

    ##
    ## properties
    ##

    @property
    def input_fifos(self) :
        return self._input_fifos

    @property
    def clock(self) :
        return self._clock

    @property
    def name(self) :
        return self._name

    @property
    def base_tp(self) :
        return self._base_tp

    ##
    ## methods
    ##
