#! /bin/bash

# This file is speicfic to lxhiggs.hep.upenn.edu environment

foobar=/tape/mitch_sim/bjr/python27
export PATH=$foobar/bin:$PATH
export PATH=/cad/mentor/questa-10.7/questasim/bin:$PATH
export PATH=/cad/mentor/questa-10.7/questasim/linux_x86_64/mgls/bin:$PATH
export LD_LIBRARY_PATH=$foobar/lib:$LD_LIBRARY_PATH
export COCOTB=$(cocotb-config --share)
export LM_LICENSE_FILE=1717@jicama.seas.upenn.edu
export COCOTB_REDUCED_LOG_FMT=1
make 

