
SIM ?= questa

TBDIR = $(PWD)
SRCDIR = $(PWD)/../src
SBDIR = $(PWD)/../src/SpyBuffer
VERILOG_SOURCES = $(TBDIR)/tp_tb.v \
  $(SRCDIR)/tp.v \
  $(SBDIR)/SpyBuffer.v \
  $(SBDIR)/SpyController.v \
  $(SBDIR)/SpyMemory.v \
  $(SBDIR)/aFifo/aFifo.v \
  $(SBDIR)/aFifo/fifomem.v \
  $(SBDIR)/aFifo/rptr_empty.v \
  $(SBDIR)/aFifo/sync_r2w.v \
  $(SBDIR)/aFifo/sync_w2r.v \
  $(SBDIR)/aFifo/wptr_full.v

TOPLEVEL = tp_tb
TOPLEVEL_LANG = verilog

MODULE = tp_tb

EXTRA_ARGS += +incdir+$(SRCDIR)

include $(shell cocotb-config --makefiles)/Makefile.inc
include $(shell cocotb-config --makefiles)/Makefile.sim

