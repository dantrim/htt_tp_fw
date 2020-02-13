# Default simulator; prefer QUESTA if not overridden.
SIM ?= questa

# Location of sources (and spy buffer sources).
SRCDIR = $(PWD)/../../src
SBDIR = $(SRCDIR)/SpyBuffer

# All Verilog source files.
VERILOG_SOURCES = \
	$(PWD)/TopLevel.v \
    $(SBDIR)/SpyBuffer.v \
    $(SBDIR)/SpyController.v \
    $(SBDIR)/SpyMemory.v \
    $(SBDIR)/aFifo/aFifo.v \
    $(SBDIR)/aFifo/fifomem.v \
    $(SBDIR)/aFifo/rptr_empty.v \
    $(SBDIR)/aFifo/sync_r2w.v \
    $(SBDIR)/aFifo/sync_w2r.v \
    $(SBDIR)/aFifo/wptr_full.v

# Any VHDL sources.
VHDL_SOURCES =

# Toplevel (RTL) and module (Python) for tests.
TOPLEVEL=TopLevel
TOPLEVEL_LANG=verilog
MODULE=DantrimTests2

# We need to set the include path appropriately!
EXTRA_ARGS += +incdir+$(SRCDIR)

# Boilerplate includes.
include $(shell cocotb-config --makefiles)/Makefile.inc
include $(shell cocotb-config --makefiles)/Makefile.sim

