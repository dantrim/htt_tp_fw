##############################################################################
#
# THE USER MUST NOT EDIT THESE LINES
#
##############################################################################

$(info *** SIM_BUILD=$(SIM_BUILD))
$(info *** TESTBENCH_TOPLEVEL=$(TESTBENCH_TOPLEVEL))
$(info *** TESTBENCH_TEST_MODULE=$(TESTBENCH_TEST_MODULE))
$(info *** COMPONENTS_LIB_DIR=$(COMPONENTS_LIB_DIR))

##############################################################################
#
# BELOW HERE THE USER CAN EDIT THE LINES
#
##############################################################################

# Default simulator; prefer QUESTA if not overridden.
SIM ?= questa

# Location of sources (and spy buffer sources).
SRCDIR = $(PWD)/../../../../../../src
SBDIR = $(SRCDIR)/SpyBuffer

# CocoTB configuration of our TopLevel and associated CocoTB test file
TOPLEVEL_LANG=verilog
TOPLEVEL=$(TESTBENCH_TOPLEVEL)
MODULE=$(TESTBENCH_TEST_MODULE)

# Verilog source files
VERILOG_SOURCES = \
    $(PWD)/$(TESTBENCH_TOPLEVEL).v \
    $(SBDIR)/SpyBuffer.v \
    $(SBDIR)/SpyController.v \
    $(SBDIR)/SpyMemory.v \
    $(SBDIR)/aFifo/aFifo.v \
    $(SBDIR)/aFifo/fifomem.v \
    $(SBDIR)/aFifo/rptr_empty.v \
    $(SBDIR)/aFifo/sync_r2w.v \
    $(SBDIR)/aFifo/sync_w2r.v \
    $(SBDIR)/aFifo/wptr_full.v

# HDL sources files
VHDL_SOURCES =

# Set the include path and compilation flags for CocoTB
EXTRA_ARGS += +incdir+$(SRCDIR)
VSIM_ARGS  += -debugDB -voptargs="+acc"

##############################################################################
#
# THE USER MUST NOT EDIT THE LINES BELOW
#
##############################################################################
include $(shell cocotb-config --makefiles)/Makefile.inc
include $(shell cocotb-config --makefiles)/Makefile.sim
