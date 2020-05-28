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
SRCDIR=$(PWD)/../../../../../../src
SBDIR=$(SRCDIR)/SpyBuffer
# evt_sync definition depends on b2b implementation
B2BDIR=$(SRCDIR)/board2board_switching
EVTSYNCDIR=$(SRCDIR)/evt_sync

#$(info *** SRCDIR = $(SRCDIR))
#$(info *** SBDIR = $(SBDIR))
#$(info *** EVTSYNCDIR = $(EVTSYNCDIR))

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
    $(SBDIR)/aFifo/wptr_full.v \
    $(B2BDIR)/ip/fifo_65/fifo_65_sim_netlist.v \
    $(B2BDIR)/rtl/find_idx.v \
    $(B2BDIR)/rtl/merge_event_handler.v \
    $(B2BDIR)/rtl/cluster_merge_engine.v \
    $(B2BDIR)/rtl/cluster_routing_engine.v \
    $(B2BDIR)/rtl/cluster_sync_engine.v \
    $(B2BDIR)/rtl/board2board_switching.v \
	$(EVTSYNCDIR)/rtl/evt_sync.v

$(info *** VERILOG_SOURCES=$(VERILOG_SOURCES))

# HDL sources files
VHDL_SOURCES =

# Set the include path and compilation flags for CocoTB
EXTRA_ARGS += +incdir+$(SRCDIR) +incdir+$(B2BDIR)/include +incdir+$(B2BDIR)/ip -L $(COMPONENTS_LIB_DIR)/unisims_ver -L $(COMPONENTS_LIB_DIR)/unisim
VSIM_ARGS  += glbl -debugDB -voptargs="+acc"

##############################################################################
#
# THE USER MUST NOT EDIT THE LINES BELOW
#
##############################################################################
include $(shell cocotb-config --makefiles)/Makefile.inc
include $(shell cocotb-config --makefiles)/Makefile.sim
