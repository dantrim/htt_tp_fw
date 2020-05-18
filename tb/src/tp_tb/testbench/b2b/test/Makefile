# Default simulator; prefer QUESTA if not overridden.
SIM ?= questa
#COMPLIB_DIR = /home/psundara/xilinx/compiled_libraries/v2019.1
COMPLIB_DIR = /home/dantrim/work/tdaq-htt-firmware/priya_stuff/xilinx/compiled_libraries/v2019.1
export TESTVECDIR=/home/dantrim/work/tdaq-htt-firmware/testvecs/20200410/

# Location of sources (and spy buffer sources).
#SRCDIR = $(PWD)/../../../../src
SRCDIR = $(PWD)/../../../../../../src
SBDIR = $(SRCDIR)/SpyBuffer
#B2BDIR= $(SRCDIR)/board2board_switching
B2BDIR = /home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching

# Toplevel (RTL) and module (Python) for tests.
#COCOTB_RESULTS_FILE=$(PWD)/results.xml
#TESTBENCH_TOPLEVEL ?= TopLevel_b2b
#TESTBENCH_TEST_MODULE ?= test_b2b

# All Verilog source files.
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
	$(B2BDIR)/rtl/find_idx.sv \
	$(B2BDIR)/ip/fifo_65/fifo_65_sim_netlist.v \
    $(B2BDIR)/rtl/merge_event_handler.sv \
    $(B2BDIR)/rtl/cluster_merge_engine.sv \
    $(B2BDIR)/rtl/cluster_routing_engine.sv \
    $(B2BDIR)/rtl/cluster_sync_engine.sv \
    $(B2BDIR)/rtl/board2board_switching.sv

# Any VHDL sources.
VHDL_SOURCES =
TOPLEVEL=$(TESTBENCH_TOPLEVEL)
TOPLEVEL_LANG=verilog
MODULE=$(TESTBENCH_TEST_MODULE)


# We need to set the include path appropriately!
EXTRA_ARGS += +incdir+$(SRCDIR) +incdir+$(B2BDIR)/include +incdir+$(B2BDIR)/ip -L $(COMPLIB_DIR)/unisims_ver -L $(COMPLIB_DIR)/unisim
VSIM_ARGS  += glbl -debugDB -voptargs="+acc"
HTT_TEST=1

# Boilerplate includes.
include $(shell cocotb-config --makefiles)/Makefile.inc
include $(shell cocotb-config --makefiles)/Makefile.sim
