# Autogenerated file
onerror {
	quit -f -code 1
}
if [file exists work] {vdel -lib work -all}
vlib work
vmap -c
vmap work work
vlog -work work +define+COCOTB_SIM -sv -timescale 1ns/1ps -mfcu +acc=rmb  +incdir+/home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src +incdir+/home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/include +incdir+/home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/ip -L /home/dantrim/work/tdaq-htt-firmware/priya_stuff/xilinx/compiled_libraries/v2019.1/unisims_ver -L /home/dantrim/work/tdaq-htt-firmware/priya_stuff/xilinx/compiled_libraries/v2019.1/unisim /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/TopLevel.v /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src/SpyBuffer/SpyBuffer.v /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src/SpyBuffer/SpyController.v /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src/SpyBuffer/SpyMemory.v /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src/SpyBuffer/aFifo/aFifo.v /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src/SpyBuffer/aFifo/fifomem.v /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src/SpyBuffer/aFifo/rptr_empty.v /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src/SpyBuffer/aFifo/sync_r2w.v /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src/SpyBuffer/aFifo/sync_w2r.v /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src/SpyBuffer/aFifo/wptr_full.v /home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/ip/fifo_65/fifo_generator_0/fifo_generator_0_sim_netlist.v /home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/rtl/merge_event_handler.sv /home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/rtl/cluster_merge_engine.sv /home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/rtl/cluster_routing_engine.sv /home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/rtl/cluster_sync_engine.sv /home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/rtl/board2board_switching.sv
vsim -debugDB -voptargs="+acc" -onfinish exit +incdir+/home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/b2b_toplevel/../../src +incdir+/home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/include +incdir+/home/dantrim/work/tdaq-htt-firmware/priya_stuff/tp-fw/src/board2board_switching/ip -L /home/dantrim/work/tdaq-htt-firmware/priya_stuff/xilinx/compiled_libraries/v2019.1/unisims_ver -L /home/dantrim/work/tdaq-htt-firmware/priya_stuff/xilinx/compiled_libraries/v2019.1/unisim -L work TopLevel glbl -wlf test.wlf
set WildcardFilter "Variable Constant Generic Parameter SpecParam Assertion Cover Endpoint ScVariable CellInternal ImmediateAssert VHDLFile"
add wave -r /*
set StdArithNoWarnings 1
set NumericStdNoWarnings 1
log -recursive /*
onbreak resume
run -all
quit
