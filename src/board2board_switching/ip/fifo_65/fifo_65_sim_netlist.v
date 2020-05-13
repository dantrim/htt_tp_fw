// Copyright 1986-2019 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2019.1.1 (lin64) Build 2580384 Sat Jun 29 08:04:45 MDT 2019
// Date        : Thu May  7 06:30:10 2020
// Host        : uciatlaslab.ps.uci.edu running 64-bit CentOS Linux release 7.7.1908 (Core)
// Command     : write_verilog -force -mode funcsim
//               /home/psundara/HTT/TP-FW/tp-fw/src/board2board_switching/Top/b2b/b2b.srcs/sources_1/ip/fifo_65/fifo_65_sim_netlist.v
// Design      : fifo_65
// Purpose     : This verilog netlist is a functional simulation representation of the design and should not be modified
//               or synthesized. This netlist cannot be used for SDF annotated simulation.
// Device      : xcvu37p-fsvh2892-3-e
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* CHECK_LICENSE_TYPE = "fifo_65,fifo_generator_v13_2_4,{}" *) (* downgradeipidentifiedwarnings = "yes" *) (* x_core_info = "fifo_generator_v13_2_4,Vivado 2019.1.1" *) 
(* NotValidForBitStream *)
module fifo_65
   (clk,
    srst,
    din,
    wr_en,
    rd_en,
    dout,
    full,
    empty,
    almost_empty,
    data_count,
    prog_full,
    prog_empty,
    wr_rst_busy,
    rd_rst_busy);
  (* x_interface_info = "xilinx.com:signal:clock:1.0 core_clk CLK" *) (* x_interface_parameter = "XIL_INTERFACENAME core_clk, FREQ_HZ 100000000, PHASE 0.000, INSERT_VIP 0" *) input clk;
  input srst;
  (* x_interface_info = "xilinx.com:interface:fifo_write:1.0 FIFO_WRITE WR_DATA" *) input [64:0]din;
  (* x_interface_info = "xilinx.com:interface:fifo_write:1.0 FIFO_WRITE WR_EN" *) input wr_en;
  (* x_interface_info = "xilinx.com:interface:fifo_read:1.0 FIFO_READ RD_EN" *) input rd_en;
  (* x_interface_info = "xilinx.com:interface:fifo_read:1.0 FIFO_READ RD_DATA" *) output [64:0]dout;
  (* x_interface_info = "xilinx.com:interface:fifo_write:1.0 FIFO_WRITE FULL" *) output full;
  (* x_interface_info = "xilinx.com:interface:fifo_read:1.0 FIFO_READ EMPTY" *) output empty;
  (* x_interface_info = "xilinx.com:interface:fifo_read:1.0 FIFO_READ ALMOST_EMPTY" *) output almost_empty;
  output [6:0]data_count;
  output prog_full;
  output prog_empty;
  output wr_rst_busy;
  output rd_rst_busy;

  wire almost_empty;
  wire clk;
  wire [6:0]data_count;
  wire [64:0]din;
  wire [64:0]dout;
  wire empty;
  wire full;
  wire prog_empty;
  wire prog_full;
  wire rd_en;
  wire rd_rst_busy;
  wire srst;
  wire wr_en;
  wire wr_rst_busy;
  wire NLW_U0_almost_full_UNCONNECTED;
  wire NLW_U0_axi_ar_dbiterr_UNCONNECTED;
  wire NLW_U0_axi_ar_overflow_UNCONNECTED;
  wire NLW_U0_axi_ar_prog_empty_UNCONNECTED;
  wire NLW_U0_axi_ar_prog_full_UNCONNECTED;
  wire NLW_U0_axi_ar_sbiterr_UNCONNECTED;
  wire NLW_U0_axi_ar_underflow_UNCONNECTED;
  wire NLW_U0_axi_aw_dbiterr_UNCONNECTED;
  wire NLW_U0_axi_aw_overflow_UNCONNECTED;
  wire NLW_U0_axi_aw_prog_empty_UNCONNECTED;
  wire NLW_U0_axi_aw_prog_full_UNCONNECTED;
  wire NLW_U0_axi_aw_sbiterr_UNCONNECTED;
  wire NLW_U0_axi_aw_underflow_UNCONNECTED;
  wire NLW_U0_axi_b_dbiterr_UNCONNECTED;
  wire NLW_U0_axi_b_overflow_UNCONNECTED;
  wire NLW_U0_axi_b_prog_empty_UNCONNECTED;
  wire NLW_U0_axi_b_prog_full_UNCONNECTED;
  wire NLW_U0_axi_b_sbiterr_UNCONNECTED;
  wire NLW_U0_axi_b_underflow_UNCONNECTED;
  wire NLW_U0_axi_r_dbiterr_UNCONNECTED;
  wire NLW_U0_axi_r_overflow_UNCONNECTED;
  wire NLW_U0_axi_r_prog_empty_UNCONNECTED;
  wire NLW_U0_axi_r_prog_full_UNCONNECTED;
  wire NLW_U0_axi_r_sbiterr_UNCONNECTED;
  wire NLW_U0_axi_r_underflow_UNCONNECTED;
  wire NLW_U0_axi_w_dbiterr_UNCONNECTED;
  wire NLW_U0_axi_w_overflow_UNCONNECTED;
  wire NLW_U0_axi_w_prog_empty_UNCONNECTED;
  wire NLW_U0_axi_w_prog_full_UNCONNECTED;
  wire NLW_U0_axi_w_sbiterr_UNCONNECTED;
  wire NLW_U0_axi_w_underflow_UNCONNECTED;
  wire NLW_U0_axis_dbiterr_UNCONNECTED;
  wire NLW_U0_axis_overflow_UNCONNECTED;
  wire NLW_U0_axis_prog_empty_UNCONNECTED;
  wire NLW_U0_axis_prog_full_UNCONNECTED;
  wire NLW_U0_axis_sbiterr_UNCONNECTED;
  wire NLW_U0_axis_underflow_UNCONNECTED;
  wire NLW_U0_dbiterr_UNCONNECTED;
  wire NLW_U0_m_axi_arvalid_UNCONNECTED;
  wire NLW_U0_m_axi_awvalid_UNCONNECTED;
  wire NLW_U0_m_axi_bready_UNCONNECTED;
  wire NLW_U0_m_axi_rready_UNCONNECTED;
  wire NLW_U0_m_axi_wlast_UNCONNECTED;
  wire NLW_U0_m_axi_wvalid_UNCONNECTED;
  wire NLW_U0_m_axis_tlast_UNCONNECTED;
  wire NLW_U0_m_axis_tvalid_UNCONNECTED;
  wire NLW_U0_overflow_UNCONNECTED;
  wire NLW_U0_s_axi_arready_UNCONNECTED;
  wire NLW_U0_s_axi_awready_UNCONNECTED;
  wire NLW_U0_s_axi_bvalid_UNCONNECTED;
  wire NLW_U0_s_axi_rlast_UNCONNECTED;
  wire NLW_U0_s_axi_rvalid_UNCONNECTED;
  wire NLW_U0_s_axi_wready_UNCONNECTED;
  wire NLW_U0_s_axis_tready_UNCONNECTED;
  wire NLW_U0_sbiterr_UNCONNECTED;
  wire NLW_U0_underflow_UNCONNECTED;
  wire NLW_U0_valid_UNCONNECTED;
  wire NLW_U0_wr_ack_UNCONNECTED;
  wire [4:0]NLW_U0_axi_ar_data_count_UNCONNECTED;
  wire [4:0]NLW_U0_axi_ar_rd_data_count_UNCONNECTED;
  wire [4:0]NLW_U0_axi_ar_wr_data_count_UNCONNECTED;
  wire [4:0]NLW_U0_axi_aw_data_count_UNCONNECTED;
  wire [4:0]NLW_U0_axi_aw_rd_data_count_UNCONNECTED;
  wire [4:0]NLW_U0_axi_aw_wr_data_count_UNCONNECTED;
  wire [4:0]NLW_U0_axi_b_data_count_UNCONNECTED;
  wire [4:0]NLW_U0_axi_b_rd_data_count_UNCONNECTED;
  wire [4:0]NLW_U0_axi_b_wr_data_count_UNCONNECTED;
  wire [10:0]NLW_U0_axi_r_data_count_UNCONNECTED;
  wire [10:0]NLW_U0_axi_r_rd_data_count_UNCONNECTED;
  wire [10:0]NLW_U0_axi_r_wr_data_count_UNCONNECTED;
  wire [10:0]NLW_U0_axi_w_data_count_UNCONNECTED;
  wire [10:0]NLW_U0_axi_w_rd_data_count_UNCONNECTED;
  wire [10:0]NLW_U0_axi_w_wr_data_count_UNCONNECTED;
  wire [10:0]NLW_U0_axis_data_count_UNCONNECTED;
  wire [10:0]NLW_U0_axis_rd_data_count_UNCONNECTED;
  wire [10:0]NLW_U0_axis_wr_data_count_UNCONNECTED;
  wire [31:0]NLW_U0_m_axi_araddr_UNCONNECTED;
  wire [1:0]NLW_U0_m_axi_arburst_UNCONNECTED;
  wire [3:0]NLW_U0_m_axi_arcache_UNCONNECTED;
  wire [0:0]NLW_U0_m_axi_arid_UNCONNECTED;
  wire [7:0]NLW_U0_m_axi_arlen_UNCONNECTED;
  wire [0:0]NLW_U0_m_axi_arlock_UNCONNECTED;
  wire [2:0]NLW_U0_m_axi_arprot_UNCONNECTED;
  wire [3:0]NLW_U0_m_axi_arqos_UNCONNECTED;
  wire [3:0]NLW_U0_m_axi_arregion_UNCONNECTED;
  wire [2:0]NLW_U0_m_axi_arsize_UNCONNECTED;
  wire [0:0]NLW_U0_m_axi_aruser_UNCONNECTED;
  wire [31:0]NLW_U0_m_axi_awaddr_UNCONNECTED;
  wire [1:0]NLW_U0_m_axi_awburst_UNCONNECTED;
  wire [3:0]NLW_U0_m_axi_awcache_UNCONNECTED;
  wire [0:0]NLW_U0_m_axi_awid_UNCONNECTED;
  wire [7:0]NLW_U0_m_axi_awlen_UNCONNECTED;
  wire [0:0]NLW_U0_m_axi_awlock_UNCONNECTED;
  wire [2:0]NLW_U0_m_axi_awprot_UNCONNECTED;
  wire [3:0]NLW_U0_m_axi_awqos_UNCONNECTED;
  wire [3:0]NLW_U0_m_axi_awregion_UNCONNECTED;
  wire [2:0]NLW_U0_m_axi_awsize_UNCONNECTED;
  wire [0:0]NLW_U0_m_axi_awuser_UNCONNECTED;
  wire [63:0]NLW_U0_m_axi_wdata_UNCONNECTED;
  wire [0:0]NLW_U0_m_axi_wid_UNCONNECTED;
  wire [7:0]NLW_U0_m_axi_wstrb_UNCONNECTED;
  wire [0:0]NLW_U0_m_axi_wuser_UNCONNECTED;
  wire [7:0]NLW_U0_m_axis_tdata_UNCONNECTED;
  wire [0:0]NLW_U0_m_axis_tdest_UNCONNECTED;
  wire [0:0]NLW_U0_m_axis_tid_UNCONNECTED;
  wire [0:0]NLW_U0_m_axis_tkeep_UNCONNECTED;
  wire [0:0]NLW_U0_m_axis_tstrb_UNCONNECTED;
  wire [3:0]NLW_U0_m_axis_tuser_UNCONNECTED;
  wire [6:0]NLW_U0_rd_data_count_UNCONNECTED;
  wire [0:0]NLW_U0_s_axi_bid_UNCONNECTED;
  wire [1:0]NLW_U0_s_axi_bresp_UNCONNECTED;
  wire [0:0]NLW_U0_s_axi_buser_UNCONNECTED;
  wire [63:0]NLW_U0_s_axi_rdata_UNCONNECTED;
  wire [0:0]NLW_U0_s_axi_rid_UNCONNECTED;
  wire [1:0]NLW_U0_s_axi_rresp_UNCONNECTED;
  wire [0:0]NLW_U0_s_axi_ruser_UNCONNECTED;
  wire [6:0]NLW_U0_wr_data_count_UNCONNECTED;

  (* C_ADD_NGC_CONSTRAINT = "0" *) 
  (* C_APPLICATION_TYPE_AXIS = "0" *) 
  (* C_APPLICATION_TYPE_RACH = "0" *) 
  (* C_APPLICATION_TYPE_RDCH = "0" *) 
  (* C_APPLICATION_TYPE_WACH = "0" *) 
  (* C_APPLICATION_TYPE_WDCH = "0" *) 
  (* C_APPLICATION_TYPE_WRCH = "0" *) 
  (* C_AXIS_TDATA_WIDTH = "8" *) 
  (* C_AXIS_TDEST_WIDTH = "1" *) 
  (* C_AXIS_TID_WIDTH = "1" *) 
  (* C_AXIS_TKEEP_WIDTH = "1" *) 
  (* C_AXIS_TSTRB_WIDTH = "1" *) 
  (* C_AXIS_TUSER_WIDTH = "4" *) 
  (* C_AXIS_TYPE = "0" *) 
  (* C_AXI_ADDR_WIDTH = "32" *) 
  (* C_AXI_ARUSER_WIDTH = "1" *) 
  (* C_AXI_AWUSER_WIDTH = "1" *) 
  (* C_AXI_BUSER_WIDTH = "1" *) 
  (* C_AXI_DATA_WIDTH = "64" *) 
  (* C_AXI_ID_WIDTH = "1" *) 
  (* C_AXI_LEN_WIDTH = "8" *) 
  (* C_AXI_LOCK_WIDTH = "1" *) 
  (* C_AXI_RUSER_WIDTH = "1" *) 
  (* C_AXI_TYPE = "1" *) 
  (* C_AXI_WUSER_WIDTH = "1" *) 
  (* C_COMMON_CLOCK = "1" *) 
  (* C_COUNT_TYPE = "0" *) 
  (* C_DATA_COUNT_WIDTH = "7" *) 
  (* C_DEFAULT_VALUE = "BlankString" *) 
  (* C_DIN_WIDTH = "65" *) 
  (* C_DIN_WIDTH_AXIS = "1" *) 
  (* C_DIN_WIDTH_RACH = "32" *) 
  (* C_DIN_WIDTH_RDCH = "64" *) 
  (* C_DIN_WIDTH_WACH = "1" *) 
  (* C_DIN_WIDTH_WDCH = "64" *) 
  (* C_DIN_WIDTH_WRCH = "2" *) 
  (* C_DOUT_RST_VAL = "0" *) 
  (* C_DOUT_WIDTH = "65" *) 
  (* C_ENABLE_RLOCS = "0" *) 
  (* C_ENABLE_RST_SYNC = "1" *) 
  (* C_EN_SAFETY_CKT = "0" *) 
  (* C_ERROR_INJECTION_TYPE = "0" *) 
  (* C_ERROR_INJECTION_TYPE_AXIS = "0" *) 
  (* C_ERROR_INJECTION_TYPE_RACH = "0" *) 
  (* C_ERROR_INJECTION_TYPE_RDCH = "0" *) 
  (* C_ERROR_INJECTION_TYPE_WACH = "0" *) 
  (* C_ERROR_INJECTION_TYPE_WDCH = "0" *) 
  (* C_ERROR_INJECTION_TYPE_WRCH = "0" *) 
  (* C_FAMILY = "virtexuplusHBM" *) 
  (* C_FULL_FLAGS_RST_VAL = "0" *) 
  (* C_HAS_ALMOST_EMPTY = "1" *) 
  (* C_HAS_ALMOST_FULL = "0" *) 
  (* C_HAS_AXIS_TDATA = "1" *) 
  (* C_HAS_AXIS_TDEST = "0" *) 
  (* C_HAS_AXIS_TID = "0" *) 
  (* C_HAS_AXIS_TKEEP = "0" *) 
  (* C_HAS_AXIS_TLAST = "0" *) 
  (* C_HAS_AXIS_TREADY = "1" *) 
  (* C_HAS_AXIS_TSTRB = "0" *) 
  (* C_HAS_AXIS_TUSER = "1" *) 
  (* C_HAS_AXI_ARUSER = "0" *) 
  (* C_HAS_AXI_AWUSER = "0" *) 
  (* C_HAS_AXI_BUSER = "0" *) 
  (* C_HAS_AXI_ID = "0" *) 
  (* C_HAS_AXI_RD_CHANNEL = "1" *) 
  (* C_HAS_AXI_RUSER = "0" *) 
  (* C_HAS_AXI_WR_CHANNEL = "1" *) 
  (* C_HAS_AXI_WUSER = "0" *) 
  (* C_HAS_BACKUP = "0" *) 
  (* C_HAS_DATA_COUNT = "1" *) 
  (* C_HAS_DATA_COUNTS_AXIS = "0" *) 
  (* C_HAS_DATA_COUNTS_RACH = "0" *) 
  (* C_HAS_DATA_COUNTS_RDCH = "0" *) 
  (* C_HAS_DATA_COUNTS_WACH = "0" *) 
  (* C_HAS_DATA_COUNTS_WDCH = "0" *) 
  (* C_HAS_DATA_COUNTS_WRCH = "0" *) 
  (* C_HAS_INT_CLK = "0" *) 
  (* C_HAS_MASTER_CE = "0" *) 
  (* C_HAS_MEMINIT_FILE = "0" *) 
  (* C_HAS_OVERFLOW = "0" *) 
  (* C_HAS_PROG_FLAGS_AXIS = "0" *) 
  (* C_HAS_PROG_FLAGS_RACH = "0" *) 
  (* C_HAS_PROG_FLAGS_RDCH = "0" *) 
  (* C_HAS_PROG_FLAGS_WACH = "0" *) 
  (* C_HAS_PROG_FLAGS_WDCH = "0" *) 
  (* C_HAS_PROG_FLAGS_WRCH = "0" *) 
  (* C_HAS_RD_DATA_COUNT = "0" *) 
  (* C_HAS_RD_RST = "0" *) 
  (* C_HAS_RST = "0" *) 
  (* C_HAS_SLAVE_CE = "0" *) 
  (* C_HAS_SRST = "1" *) 
  (* C_HAS_UNDERFLOW = "0" *) 
  (* C_HAS_VALID = "0" *) 
  (* C_HAS_WR_ACK = "0" *) 
  (* C_HAS_WR_DATA_COUNT = "0" *) 
  (* C_HAS_WR_RST = "0" *) 
  (* C_IMPLEMENTATION_TYPE = "0" *) 
  (* C_IMPLEMENTATION_TYPE_AXIS = "1" *) 
  (* C_IMPLEMENTATION_TYPE_RACH = "1" *) 
  (* C_IMPLEMENTATION_TYPE_RDCH = "1" *) 
  (* C_IMPLEMENTATION_TYPE_WACH = "1" *) 
  (* C_IMPLEMENTATION_TYPE_WDCH = "1" *) 
  (* C_IMPLEMENTATION_TYPE_WRCH = "1" *) 
  (* C_INIT_WR_PNTR_VAL = "0" *) 
  (* C_INTERFACE_TYPE = "0" *) 
  (* C_MEMORY_TYPE = "1" *) 
  (* C_MIF_FILE_NAME = "BlankString" *) 
  (* C_MSGON_VAL = "1" *) 
  (* C_OPTIMIZATION_MODE = "0" *) 
  (* C_OVERFLOW_LOW = "0" *) 
  (* C_POWER_SAVING_MODE = "0" *) 
  (* C_PRELOAD_LATENCY = "0" *) 
  (* C_PRELOAD_REGS = "1" *) 
  (* C_PRIM_FIFO_TYPE = "512x72" *) 
  (* C_PRIM_FIFO_TYPE_AXIS = "1kx18" *) 
  (* C_PRIM_FIFO_TYPE_RACH = "512x36" *) 
  (* C_PRIM_FIFO_TYPE_RDCH = "512x72" *) 
  (* C_PRIM_FIFO_TYPE_WACH = "512x36" *) 
  (* C_PRIM_FIFO_TYPE_WDCH = "512x72" *) 
  (* C_PRIM_FIFO_TYPE_WRCH = "512x36" *) 
  (* C_PROG_EMPTY_THRESH_ASSERT_VAL = "6" *) 
  (* C_PROG_EMPTY_THRESH_ASSERT_VAL_AXIS = "1022" *) 
  (* C_PROG_EMPTY_THRESH_ASSERT_VAL_RACH = "1022" *) 
  (* C_PROG_EMPTY_THRESH_ASSERT_VAL_RDCH = "1022" *) 
  (* C_PROG_EMPTY_THRESH_ASSERT_VAL_WACH = "1022" *) 
  (* C_PROG_EMPTY_THRESH_ASSERT_VAL_WDCH = "1022" *) 
  (* C_PROG_EMPTY_THRESH_ASSERT_VAL_WRCH = "1022" *) 
  (* C_PROG_EMPTY_THRESH_NEGATE_VAL = "7" *) 
  (* C_PROG_EMPTY_TYPE = "2" *) 
  (* C_PROG_EMPTY_TYPE_AXIS = "0" *) 
  (* C_PROG_EMPTY_TYPE_RACH = "0" *) 
  (* C_PROG_EMPTY_TYPE_RDCH = "0" *) 
  (* C_PROG_EMPTY_TYPE_WACH = "0" *) 
  (* C_PROG_EMPTY_TYPE_WDCH = "0" *) 
  (* C_PROG_EMPTY_TYPE_WRCH = "0" *) 
  (* C_PROG_FULL_THRESH_ASSERT_VAL = "59" *) 
  (* C_PROG_FULL_THRESH_ASSERT_VAL_AXIS = "1023" *) 
  (* C_PROG_FULL_THRESH_ASSERT_VAL_RACH = "1023" *) 
  (* C_PROG_FULL_THRESH_ASSERT_VAL_RDCH = "1023" *) 
  (* C_PROG_FULL_THRESH_ASSERT_VAL_WACH = "1023" *) 
  (* C_PROG_FULL_THRESH_ASSERT_VAL_WDCH = "1023" *) 
  (* C_PROG_FULL_THRESH_ASSERT_VAL_WRCH = "1023" *) 
  (* C_PROG_FULL_THRESH_NEGATE_VAL = "58" *) 
  (* C_PROG_FULL_TYPE = "1" *) 
  (* C_PROG_FULL_TYPE_AXIS = "0" *) 
  (* C_PROG_FULL_TYPE_RACH = "0" *) 
  (* C_PROG_FULL_TYPE_RDCH = "0" *) 
  (* C_PROG_FULL_TYPE_WACH = "0" *) 
  (* C_PROG_FULL_TYPE_WDCH = "0" *) 
  (* C_PROG_FULL_TYPE_WRCH = "0" *) 
  (* C_RACH_TYPE = "0" *) 
  (* C_RDCH_TYPE = "0" *) 
  (* C_RD_DATA_COUNT_WIDTH = "7" *) 
  (* C_RD_DEPTH = "64" *) 
  (* C_RD_FREQ = "1" *) 
  (* C_RD_PNTR_WIDTH = "6" *) 
  (* C_REG_SLICE_MODE_AXIS = "0" *) 
  (* C_REG_SLICE_MODE_RACH = "0" *) 
  (* C_REG_SLICE_MODE_RDCH = "0" *) 
  (* C_REG_SLICE_MODE_WACH = "0" *) 
  (* C_REG_SLICE_MODE_WDCH = "0" *) 
  (* C_REG_SLICE_MODE_WRCH = "0" *) 
  (* C_SELECT_XPM = "0" *) 
  (* C_SYNCHRONIZER_STAGE = "2" *) 
  (* C_UNDERFLOW_LOW = "0" *) 
  (* C_USE_COMMON_OVERFLOW = "0" *) 
  (* C_USE_COMMON_UNDERFLOW = "0" *) 
  (* C_USE_DEFAULT_SETTINGS = "0" *) 
  (* C_USE_DOUT_RST = "1" *) 
  (* C_USE_ECC = "0" *) 
  (* C_USE_ECC_AXIS = "0" *) 
  (* C_USE_ECC_RACH = "0" *) 
  (* C_USE_ECC_RDCH = "0" *) 
  (* C_USE_ECC_WACH = "0" *) 
  (* C_USE_ECC_WDCH = "0" *) 
  (* C_USE_ECC_WRCH = "0" *) 
  (* C_USE_EMBEDDED_REG = "1" *) 
  (* C_USE_FIFO16_FLAGS = "0" *) 
  (* C_USE_FWFT_DATA_COUNT = "1" *) 
  (* C_USE_PIPELINE_REG = "0" *) 
  (* C_VALID_LOW = "0" *) 
  (* C_WACH_TYPE = "0" *) 
  (* C_WDCH_TYPE = "0" *) 
  (* C_WRCH_TYPE = "0" *) 
  (* C_WR_ACK_LOW = "0" *) 
  (* C_WR_DATA_COUNT_WIDTH = "7" *) 
  (* C_WR_DEPTH = "64" *) 
  (* C_WR_DEPTH_AXIS = "1024" *) 
  (* C_WR_DEPTH_RACH = "16" *) 
  (* C_WR_DEPTH_RDCH = "1024" *) 
  (* C_WR_DEPTH_WACH = "16" *) 
  (* C_WR_DEPTH_WDCH = "1024" *) 
  (* C_WR_DEPTH_WRCH = "16" *) 
  (* C_WR_FREQ = "1" *) 
  (* C_WR_PNTR_WIDTH = "6" *) 
  (* C_WR_PNTR_WIDTH_AXIS = "10" *) 
  (* C_WR_PNTR_WIDTH_RACH = "4" *) 
  (* C_WR_PNTR_WIDTH_RDCH = "10" *) 
  (* C_WR_PNTR_WIDTH_WACH = "4" *) 
  (* C_WR_PNTR_WIDTH_WDCH = "10" *) 
  (* C_WR_PNTR_WIDTH_WRCH = "4" *) 
  (* C_WR_RESPONSE_LATENCY = "1" *) 
  fifo_65_fifo_generator_v13_2_4 U0
       (.almost_empty(almost_empty),
        .almost_full(NLW_U0_almost_full_UNCONNECTED),
        .axi_ar_data_count(NLW_U0_axi_ar_data_count_UNCONNECTED[4:0]),
        .axi_ar_dbiterr(NLW_U0_axi_ar_dbiterr_UNCONNECTED),
        .axi_ar_injectdbiterr(1'b0),
        .axi_ar_injectsbiterr(1'b0),
        .axi_ar_overflow(NLW_U0_axi_ar_overflow_UNCONNECTED),
        .axi_ar_prog_empty(NLW_U0_axi_ar_prog_empty_UNCONNECTED),
        .axi_ar_prog_empty_thresh({1'b0,1'b0,1'b0,1'b0}),
        .axi_ar_prog_full(NLW_U0_axi_ar_prog_full_UNCONNECTED),
        .axi_ar_prog_full_thresh({1'b0,1'b0,1'b0,1'b0}),
        .axi_ar_rd_data_count(NLW_U0_axi_ar_rd_data_count_UNCONNECTED[4:0]),
        .axi_ar_sbiterr(NLW_U0_axi_ar_sbiterr_UNCONNECTED),
        .axi_ar_underflow(NLW_U0_axi_ar_underflow_UNCONNECTED),
        .axi_ar_wr_data_count(NLW_U0_axi_ar_wr_data_count_UNCONNECTED[4:0]),
        .axi_aw_data_count(NLW_U0_axi_aw_data_count_UNCONNECTED[4:0]),
        .axi_aw_dbiterr(NLW_U0_axi_aw_dbiterr_UNCONNECTED),
        .axi_aw_injectdbiterr(1'b0),
        .axi_aw_injectsbiterr(1'b0),
        .axi_aw_overflow(NLW_U0_axi_aw_overflow_UNCONNECTED),
        .axi_aw_prog_empty(NLW_U0_axi_aw_prog_empty_UNCONNECTED),
        .axi_aw_prog_empty_thresh({1'b0,1'b0,1'b0,1'b0}),
        .axi_aw_prog_full(NLW_U0_axi_aw_prog_full_UNCONNECTED),
        .axi_aw_prog_full_thresh({1'b0,1'b0,1'b0,1'b0}),
        .axi_aw_rd_data_count(NLW_U0_axi_aw_rd_data_count_UNCONNECTED[4:0]),
        .axi_aw_sbiterr(NLW_U0_axi_aw_sbiterr_UNCONNECTED),
        .axi_aw_underflow(NLW_U0_axi_aw_underflow_UNCONNECTED),
        .axi_aw_wr_data_count(NLW_U0_axi_aw_wr_data_count_UNCONNECTED[4:0]),
        .axi_b_data_count(NLW_U0_axi_b_data_count_UNCONNECTED[4:0]),
        .axi_b_dbiterr(NLW_U0_axi_b_dbiterr_UNCONNECTED),
        .axi_b_injectdbiterr(1'b0),
        .axi_b_injectsbiterr(1'b0),
        .axi_b_overflow(NLW_U0_axi_b_overflow_UNCONNECTED),
        .axi_b_prog_empty(NLW_U0_axi_b_prog_empty_UNCONNECTED),
        .axi_b_prog_empty_thresh({1'b0,1'b0,1'b0,1'b0}),
        .axi_b_prog_full(NLW_U0_axi_b_prog_full_UNCONNECTED),
        .axi_b_prog_full_thresh({1'b0,1'b0,1'b0,1'b0}),
        .axi_b_rd_data_count(NLW_U0_axi_b_rd_data_count_UNCONNECTED[4:0]),
        .axi_b_sbiterr(NLW_U0_axi_b_sbiterr_UNCONNECTED),
        .axi_b_underflow(NLW_U0_axi_b_underflow_UNCONNECTED),
        .axi_b_wr_data_count(NLW_U0_axi_b_wr_data_count_UNCONNECTED[4:0]),
        .axi_r_data_count(NLW_U0_axi_r_data_count_UNCONNECTED[10:0]),
        .axi_r_dbiterr(NLW_U0_axi_r_dbiterr_UNCONNECTED),
        .axi_r_injectdbiterr(1'b0),
        .axi_r_injectsbiterr(1'b0),
        .axi_r_overflow(NLW_U0_axi_r_overflow_UNCONNECTED),
        .axi_r_prog_empty(NLW_U0_axi_r_prog_empty_UNCONNECTED),
        .axi_r_prog_empty_thresh({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .axi_r_prog_full(NLW_U0_axi_r_prog_full_UNCONNECTED),
        .axi_r_prog_full_thresh({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .axi_r_rd_data_count(NLW_U0_axi_r_rd_data_count_UNCONNECTED[10:0]),
        .axi_r_sbiterr(NLW_U0_axi_r_sbiterr_UNCONNECTED),
        .axi_r_underflow(NLW_U0_axi_r_underflow_UNCONNECTED),
        .axi_r_wr_data_count(NLW_U0_axi_r_wr_data_count_UNCONNECTED[10:0]),
        .axi_w_data_count(NLW_U0_axi_w_data_count_UNCONNECTED[10:0]),
        .axi_w_dbiterr(NLW_U0_axi_w_dbiterr_UNCONNECTED),
        .axi_w_injectdbiterr(1'b0),
        .axi_w_injectsbiterr(1'b0),
        .axi_w_overflow(NLW_U0_axi_w_overflow_UNCONNECTED),
        .axi_w_prog_empty(NLW_U0_axi_w_prog_empty_UNCONNECTED),
        .axi_w_prog_empty_thresh({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .axi_w_prog_full(NLW_U0_axi_w_prog_full_UNCONNECTED),
        .axi_w_prog_full_thresh({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .axi_w_rd_data_count(NLW_U0_axi_w_rd_data_count_UNCONNECTED[10:0]),
        .axi_w_sbiterr(NLW_U0_axi_w_sbiterr_UNCONNECTED),
        .axi_w_underflow(NLW_U0_axi_w_underflow_UNCONNECTED),
        .axi_w_wr_data_count(NLW_U0_axi_w_wr_data_count_UNCONNECTED[10:0]),
        .axis_data_count(NLW_U0_axis_data_count_UNCONNECTED[10:0]),
        .axis_dbiterr(NLW_U0_axis_dbiterr_UNCONNECTED),
        .axis_injectdbiterr(1'b0),
        .axis_injectsbiterr(1'b0),
        .axis_overflow(NLW_U0_axis_overflow_UNCONNECTED),
        .axis_prog_empty(NLW_U0_axis_prog_empty_UNCONNECTED),
        .axis_prog_empty_thresh({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .axis_prog_full(NLW_U0_axis_prog_full_UNCONNECTED),
        .axis_prog_full_thresh({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .axis_rd_data_count(NLW_U0_axis_rd_data_count_UNCONNECTED[10:0]),
        .axis_sbiterr(NLW_U0_axis_sbiterr_UNCONNECTED),
        .axis_underflow(NLW_U0_axis_underflow_UNCONNECTED),
        .axis_wr_data_count(NLW_U0_axis_wr_data_count_UNCONNECTED[10:0]),
        .backup(1'b0),
        .backup_marker(1'b0),
        .clk(clk),
        .data_count(data_count),
        .dbiterr(NLW_U0_dbiterr_UNCONNECTED),
        .din(din),
        .dout(dout),
        .empty(empty),
        .full(full),
        .injectdbiterr(1'b0),
        .injectsbiterr(1'b0),
        .int_clk(1'b0),
        .m_aclk(1'b0),
        .m_aclk_en(1'b0),
        .m_axi_araddr(NLW_U0_m_axi_araddr_UNCONNECTED[31:0]),
        .m_axi_arburst(NLW_U0_m_axi_arburst_UNCONNECTED[1:0]),
        .m_axi_arcache(NLW_U0_m_axi_arcache_UNCONNECTED[3:0]),
        .m_axi_arid(NLW_U0_m_axi_arid_UNCONNECTED[0]),
        .m_axi_arlen(NLW_U0_m_axi_arlen_UNCONNECTED[7:0]),
        .m_axi_arlock(NLW_U0_m_axi_arlock_UNCONNECTED[0]),
        .m_axi_arprot(NLW_U0_m_axi_arprot_UNCONNECTED[2:0]),
        .m_axi_arqos(NLW_U0_m_axi_arqos_UNCONNECTED[3:0]),
        .m_axi_arready(1'b0),
        .m_axi_arregion(NLW_U0_m_axi_arregion_UNCONNECTED[3:0]),
        .m_axi_arsize(NLW_U0_m_axi_arsize_UNCONNECTED[2:0]),
        .m_axi_aruser(NLW_U0_m_axi_aruser_UNCONNECTED[0]),
        .m_axi_arvalid(NLW_U0_m_axi_arvalid_UNCONNECTED),
        .m_axi_awaddr(NLW_U0_m_axi_awaddr_UNCONNECTED[31:0]),
        .m_axi_awburst(NLW_U0_m_axi_awburst_UNCONNECTED[1:0]),
        .m_axi_awcache(NLW_U0_m_axi_awcache_UNCONNECTED[3:0]),
        .m_axi_awid(NLW_U0_m_axi_awid_UNCONNECTED[0]),
        .m_axi_awlen(NLW_U0_m_axi_awlen_UNCONNECTED[7:0]),
        .m_axi_awlock(NLW_U0_m_axi_awlock_UNCONNECTED[0]),
        .m_axi_awprot(NLW_U0_m_axi_awprot_UNCONNECTED[2:0]),
        .m_axi_awqos(NLW_U0_m_axi_awqos_UNCONNECTED[3:0]),
        .m_axi_awready(1'b0),
        .m_axi_awregion(NLW_U0_m_axi_awregion_UNCONNECTED[3:0]),
        .m_axi_awsize(NLW_U0_m_axi_awsize_UNCONNECTED[2:0]),
        .m_axi_awuser(NLW_U0_m_axi_awuser_UNCONNECTED[0]),
        .m_axi_awvalid(NLW_U0_m_axi_awvalid_UNCONNECTED),
        .m_axi_bid(1'b0),
        .m_axi_bready(NLW_U0_m_axi_bready_UNCONNECTED),
        .m_axi_bresp({1'b0,1'b0}),
        .m_axi_buser(1'b0),
        .m_axi_bvalid(1'b0),
        .m_axi_rdata({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .m_axi_rid(1'b0),
        .m_axi_rlast(1'b0),
        .m_axi_rready(NLW_U0_m_axi_rready_UNCONNECTED),
        .m_axi_rresp({1'b0,1'b0}),
        .m_axi_ruser(1'b0),
        .m_axi_rvalid(1'b0),
        .m_axi_wdata(NLW_U0_m_axi_wdata_UNCONNECTED[63:0]),
        .m_axi_wid(NLW_U0_m_axi_wid_UNCONNECTED[0]),
        .m_axi_wlast(NLW_U0_m_axi_wlast_UNCONNECTED),
        .m_axi_wready(1'b0),
        .m_axi_wstrb(NLW_U0_m_axi_wstrb_UNCONNECTED[7:0]),
        .m_axi_wuser(NLW_U0_m_axi_wuser_UNCONNECTED[0]),
        .m_axi_wvalid(NLW_U0_m_axi_wvalid_UNCONNECTED),
        .m_axis_tdata(NLW_U0_m_axis_tdata_UNCONNECTED[7:0]),
        .m_axis_tdest(NLW_U0_m_axis_tdest_UNCONNECTED[0]),
        .m_axis_tid(NLW_U0_m_axis_tid_UNCONNECTED[0]),
        .m_axis_tkeep(NLW_U0_m_axis_tkeep_UNCONNECTED[0]),
        .m_axis_tlast(NLW_U0_m_axis_tlast_UNCONNECTED),
        .m_axis_tready(1'b0),
        .m_axis_tstrb(NLW_U0_m_axis_tstrb_UNCONNECTED[0]),
        .m_axis_tuser(NLW_U0_m_axis_tuser_UNCONNECTED[3:0]),
        .m_axis_tvalid(NLW_U0_m_axis_tvalid_UNCONNECTED),
        .overflow(NLW_U0_overflow_UNCONNECTED),
        .prog_empty(prog_empty),
        .prog_empty_thresh({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .prog_empty_thresh_assert({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .prog_empty_thresh_negate({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .prog_full(prog_full),
        .prog_full_thresh({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .prog_full_thresh_assert({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .prog_full_thresh_negate({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .rd_clk(1'b0),
        .rd_data_count(NLW_U0_rd_data_count_UNCONNECTED[6:0]),
        .rd_en(rd_en),
        .rd_rst(1'b0),
        .rd_rst_busy(rd_rst_busy),
        .rst(1'b0),
        .s_aclk(1'b0),
        .s_aclk_en(1'b0),
        .s_aresetn(1'b0),
        .s_axi_araddr({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .s_axi_arburst({1'b0,1'b0}),
        .s_axi_arcache({1'b0,1'b0,1'b0,1'b0}),
        .s_axi_arid(1'b0),
        .s_axi_arlen({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .s_axi_arlock(1'b0),
        .s_axi_arprot({1'b0,1'b0,1'b0}),
        .s_axi_arqos({1'b0,1'b0,1'b0,1'b0}),
        .s_axi_arready(NLW_U0_s_axi_arready_UNCONNECTED),
        .s_axi_arregion({1'b0,1'b0,1'b0,1'b0}),
        .s_axi_arsize({1'b0,1'b0,1'b0}),
        .s_axi_aruser(1'b0),
        .s_axi_arvalid(1'b0),
        .s_axi_awaddr({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .s_axi_awburst({1'b0,1'b0}),
        .s_axi_awcache({1'b0,1'b0,1'b0,1'b0}),
        .s_axi_awid(1'b0),
        .s_axi_awlen({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .s_axi_awlock(1'b0),
        .s_axi_awprot({1'b0,1'b0,1'b0}),
        .s_axi_awqos({1'b0,1'b0,1'b0,1'b0}),
        .s_axi_awready(NLW_U0_s_axi_awready_UNCONNECTED),
        .s_axi_awregion({1'b0,1'b0,1'b0,1'b0}),
        .s_axi_awsize({1'b0,1'b0,1'b0}),
        .s_axi_awuser(1'b0),
        .s_axi_awvalid(1'b0),
        .s_axi_bid(NLW_U0_s_axi_bid_UNCONNECTED[0]),
        .s_axi_bready(1'b0),
        .s_axi_bresp(NLW_U0_s_axi_bresp_UNCONNECTED[1:0]),
        .s_axi_buser(NLW_U0_s_axi_buser_UNCONNECTED[0]),
        .s_axi_bvalid(NLW_U0_s_axi_bvalid_UNCONNECTED),
        .s_axi_rdata(NLW_U0_s_axi_rdata_UNCONNECTED[63:0]),
        .s_axi_rid(NLW_U0_s_axi_rid_UNCONNECTED[0]),
        .s_axi_rlast(NLW_U0_s_axi_rlast_UNCONNECTED),
        .s_axi_rready(1'b0),
        .s_axi_rresp(NLW_U0_s_axi_rresp_UNCONNECTED[1:0]),
        .s_axi_ruser(NLW_U0_s_axi_ruser_UNCONNECTED[0]),
        .s_axi_rvalid(NLW_U0_s_axi_rvalid_UNCONNECTED),
        .s_axi_wdata({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .s_axi_wid(1'b0),
        .s_axi_wlast(1'b0),
        .s_axi_wready(NLW_U0_s_axi_wready_UNCONNECTED),
        .s_axi_wstrb({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .s_axi_wuser(1'b0),
        .s_axi_wvalid(1'b0),
        .s_axis_tdata({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .s_axis_tdest(1'b0),
        .s_axis_tid(1'b0),
        .s_axis_tkeep(1'b0),
        .s_axis_tlast(1'b0),
        .s_axis_tready(NLW_U0_s_axis_tready_UNCONNECTED),
        .s_axis_tstrb(1'b0),
        .s_axis_tuser({1'b0,1'b0,1'b0,1'b0}),
        .s_axis_tvalid(1'b0),
        .sbiterr(NLW_U0_sbiterr_UNCONNECTED),
        .sleep(1'b0),
        .srst(srst),
        .underflow(NLW_U0_underflow_UNCONNECTED),
        .valid(NLW_U0_valid_UNCONNECTED),
        .wr_ack(NLW_U0_wr_ack_UNCONNECTED),
        .wr_clk(1'b0),
        .wr_data_count(NLW_U0_wr_data_count_UNCONNECTED[6:0]),
        .wr_en(wr_en),
        .wr_rst(1'b0),
        .wr_rst_busy(wr_rst_busy));
endmodule

(* ORIG_REF_NAME = "blk_mem_gen_generic_cstr" *) 
module fifo_65_blk_mem_gen_generic_cstr
   (dout,
    clk,
    tmp_ram_rd_en,
    p_17_out,
    tmp_ram_regout_en,
    srst_full_ff_i,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ,
    din);
  output [64:0]dout;
  input clk;
  input tmp_ram_rd_en;
  input p_17_out;
  input tmp_ram_regout_en;
  input srst_full_ff_i;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  input [64:0]din;

  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  wire clk;
  wire [64:0]din;
  wire [64:0]dout;
  wire p_17_out;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;

  fifo_65_blk_mem_gen_prim_width \ramloop[0].ram.r 
       (.\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ),
        .\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .clk(clk),
        .din(din),
        .dout(dout),
        .p_17_out(p_17_out),
        .srst_full_ff_i(srst_full_ff_i),
        .tmp_ram_rd_en(tmp_ram_rd_en),
        .tmp_ram_regout_en(tmp_ram_regout_en));
endmodule

(* ORIG_REF_NAME = "blk_mem_gen_prim_width" *) 
module fifo_65_blk_mem_gen_prim_width
   (dout,
    clk,
    tmp_ram_rd_en,
    p_17_out,
    tmp_ram_regout_en,
    srst_full_ff_i,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ,
    din);
  output [64:0]dout;
  input clk;
  input tmp_ram_rd_en;
  input p_17_out;
  input tmp_ram_regout_en;
  input srst_full_ff_i;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  input [64:0]din;

  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  wire clk;
  wire [64:0]din;
  wire [64:0]dout;
  wire p_17_out;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;

  fifo_65_blk_mem_gen_prim_wrapper \prim_noinit.ram 
       (.\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ),
        .\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_1 (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .clk(clk),
        .din(din),
        .dout(dout),
        .p_17_out(p_17_out),
        .srst_full_ff_i(srst_full_ff_i),
        .tmp_ram_rd_en(tmp_ram_rd_en),
        .tmp_ram_regout_en(tmp_ram_regout_en));
endmodule

(* ORIG_REF_NAME = "blk_mem_gen_prim_wrapper" *) 
module fifo_65_blk_mem_gen_prim_wrapper
   (dout,
    clk,
    tmp_ram_rd_en,
    p_17_out,
    tmp_ram_regout_en,
    srst_full_ff_i,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_1 ,
    din);
  output [64:0]dout;
  input clk;
  input tmp_ram_rd_en;
  input p_17_out;
  input tmp_ram_regout_en;
  input srst_full_ff_i;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_1 ;
  input [64:0]din;

  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_1 ;
  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_140 ;
  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_141 ;
  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_142 ;
  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_144 ;
  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_145 ;
  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_146 ;
  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_147 ;
  wire clk;
  wire [64:0]din;
  wire [64:0]dout;
  wire p_17_out;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;
  wire \NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASOUTDBITERR_UNCONNECTED ;
  wire \NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASOUTSBITERR_UNCONNECTED ;
  wire \NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_DBITERR_UNCONNECTED ;
  wire \NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_SBITERR_UNCONNECTED ;
  wire [31:0]\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASDOUTA_UNCONNECTED ;
  wire [31:0]\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASDOUTB_UNCONNECTED ;
  wire [3:0]\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASDOUTPA_UNCONNECTED ;
  wire [3:0]\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASDOUTPB_UNCONNECTED ;
  wire [7:0]\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_ECCPARITY_UNCONNECTED ;
  wire [8:0]\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_RDADDRECC_UNCONNECTED ;

  (* box_type = "PRIMITIVE" *) 
  RAMB36E2 #(
    .CASCADE_ORDER_A("NONE"),
    .CASCADE_ORDER_B("NONE"),
    .CLOCK_DOMAINS("COMMON"),
    .DOA_REG(1),
    .DOB_REG(1),
    .ENADDRENA("FALSE"),
    .ENADDRENB("FALSE"),
    .EN_ECC_PIPE("FALSE"),
    .EN_ECC_READ("FALSE"),
    .EN_ECC_WRITE("FALSE"),
    .INITP_00(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_01(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_02(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_03(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_04(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_05(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_06(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_07(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_08(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_09(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_0A(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_0B(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_0C(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_0D(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_0E(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INITP_0F(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_00(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_01(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_02(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_03(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_04(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_05(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_06(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_07(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_08(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_09(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_0A(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_0B(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_0C(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_0D(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_0E(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_0F(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_10(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_11(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_12(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_13(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_14(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_15(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_16(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_17(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_18(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_19(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_1A(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_1B(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_1C(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_1D(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_1E(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_1F(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_20(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_21(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_22(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_23(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_24(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_25(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_26(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_27(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_28(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_29(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_2A(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_2B(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_2C(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_2D(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_2E(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_2F(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_30(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_31(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_32(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_33(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_34(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_35(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_36(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_37(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_38(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_39(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_3A(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_3B(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_3C(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_3D(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_3E(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_3F(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_40(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_41(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_42(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_43(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_44(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_45(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_46(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_47(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_48(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_49(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_4A(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_4B(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_4C(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_4D(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_4E(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_4F(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_50(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_51(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_52(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_53(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_54(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_55(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_56(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_57(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_58(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_59(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_5A(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_5B(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_5C(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_5D(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_5E(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_5F(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_60(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_61(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_62(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_63(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_64(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_65(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_66(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_67(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_68(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_69(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_6A(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_6B(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_6C(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_6D(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_6E(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_6F(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_70(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_71(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_72(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_73(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_74(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_75(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_76(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_77(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_78(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_79(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_7A(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_7B(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_7C(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_7D(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_7E(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_7F(256'h0000000000000000000000000000000000000000000000000000000000000000),
    .INIT_A(36'h000000000),
    .INIT_B(36'h000000000),
    .INIT_FILE("NONE"),
    .IS_CLKARDCLK_INVERTED(1'b0),
    .IS_CLKBWRCLK_INVERTED(1'b0),
    .IS_ENARDEN_INVERTED(1'b0),
    .IS_ENBWREN_INVERTED(1'b0),
    .IS_RSTRAMARSTRAM_INVERTED(1'b0),
    .IS_RSTRAMB_INVERTED(1'b0),
    .IS_RSTREGARSTREG_INVERTED(1'b0),
    .IS_RSTREGB_INVERTED(1'b0),
    .RDADDRCHANGEA("FALSE"),
    .RDADDRCHANGEB("FALSE"),
    .READ_WIDTH_A(72),
    .READ_WIDTH_B(0),
    .RSTREG_PRIORITY_A("REGCE"),
    .RSTREG_PRIORITY_B("REGCE"),
    .SIM_COLLISION_CHECK("ALL"),
    .SLEEP_ASYNC("FALSE"),
    .SRVAL_A(36'h000000000),
    .SRVAL_B(36'h000000000),
    .WRITE_MODE_A("WRITE_FIRST"),
    .WRITE_MODE_B("WRITE_FIRST"),
    .WRITE_WIDTH_A(0),
    .WRITE_WIDTH_B(72)) 
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram 
       (.ADDRARDADDR({1'b0,1'b0,1'b0,\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .ADDRBWRADDR({1'b0,1'b0,1'b0,\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_1 ,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .ADDRENA(1'b0),
        .ADDRENB(1'b0),
        .CASDIMUXA(1'b0),
        .CASDIMUXB(1'b0),
        .CASDINA({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .CASDINB({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .CASDINPA({1'b0,1'b0,1'b0,1'b0}),
        .CASDINPB({1'b0,1'b0,1'b0,1'b0}),
        .CASDOMUXA(1'b0),
        .CASDOMUXB(1'b0),
        .CASDOMUXEN_A(1'b0),
        .CASDOMUXEN_B(1'b0),
        .CASDOUTA(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASDOUTA_UNCONNECTED [31:0]),
        .CASDOUTB(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASDOUTB_UNCONNECTED [31:0]),
        .CASDOUTPA(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASDOUTPA_UNCONNECTED [3:0]),
        .CASDOUTPB(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASDOUTPB_UNCONNECTED [3:0]),
        .CASINDBITERR(1'b0),
        .CASINSBITERR(1'b0),
        .CASOREGIMUXA(1'b0),
        .CASOREGIMUXB(1'b0),
        .CASOREGIMUXEN_A(1'b0),
        .CASOREGIMUXEN_B(1'b0),
        .CASOUTDBITERR(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASOUTDBITERR_UNCONNECTED ),
        .CASOUTSBITERR(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_CASOUTSBITERR_UNCONNECTED ),
        .CLKARDCLK(clk),
        .CLKBWRCLK(clk),
        .DBITERR(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_DBITERR_UNCONNECTED ),
        .DINADIN({din[32:9],din[7:0]}),
        .DINBDIN(din[64:33]),
        .DINPADINP({1'b0,1'b0,1'b0,din[8]}),
        .DINPBDINP({1'b0,1'b0,1'b0,1'b0}),
        .DOUTADOUT({dout[32:9],dout[7:0]}),
        .DOUTBDOUT(dout[64:33]),
        .DOUTPADOUTP({\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_140 ,\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_141 ,\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_142 ,dout[8]}),
        .DOUTPBDOUTP({\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_144 ,\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_145 ,\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_146 ,\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_n_147 }),
        .ECCPARITY(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_ECCPARITY_UNCONNECTED [7:0]),
        .ECCPIPECE(1'b0),
        .ENARDEN(tmp_ram_rd_en),
        .ENBWREN(p_17_out),
        .INJECTDBITERR(1'b0),
        .INJECTSBITERR(1'b0),
        .RDADDRECC(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_RDADDRECC_UNCONNECTED [8:0]),
        .REGCEAREGCE(tmp_ram_regout_en),
        .REGCEB(1'b0),
        .RSTRAMARSTRAM(1'b0),
        .RSTRAMB(1'b0),
        .RSTREGARSTREG(srst_full_ff_i),
        .RSTREGB(1'b0),
        .SBITERR(\NLW_DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_SBITERR_UNCONNECTED ),
        .SLEEP(1'b0),
        .WEA({1'b0,1'b0,1'b0,1'b0}),
        .WEBWE({p_17_out,p_17_out,p_17_out,p_17_out,p_17_out,p_17_out,p_17_out,p_17_out}));
endmodule

(* ORIG_REF_NAME = "blk_mem_gen_top" *) 
module fifo_65_blk_mem_gen_top
   (dout,
    clk,
    tmp_ram_rd_en,
    p_17_out,
    tmp_ram_regout_en,
    srst_full_ff_i,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ,
    din);
  output [64:0]dout;
  input clk;
  input tmp_ram_rd_en;
  input p_17_out;
  input tmp_ram_regout_en;
  input srst_full_ff_i;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  input [64:0]din;

  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  wire clk;
  wire [64:0]din;
  wire [64:0]dout;
  wire p_17_out;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;

  fifo_65_blk_mem_gen_generic_cstr \valid.cstr 
       (.\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ),
        .\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .clk(clk),
        .din(din),
        .dout(dout),
        .p_17_out(p_17_out),
        .srst_full_ff_i(srst_full_ff_i),
        .tmp_ram_rd_en(tmp_ram_rd_en),
        .tmp_ram_regout_en(tmp_ram_regout_en));
endmodule

(* ORIG_REF_NAME = "blk_mem_gen_v8_4_3" *) 
module fifo_65_blk_mem_gen_v8_4_3
   (dout,
    clk,
    tmp_ram_rd_en,
    p_17_out,
    tmp_ram_regout_en,
    srst_full_ff_i,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ,
    din);
  output [64:0]dout;
  input clk;
  input tmp_ram_rd_en;
  input p_17_out;
  input tmp_ram_regout_en;
  input srst_full_ff_i;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  input [64:0]din;

  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  wire clk;
  wire [64:0]din;
  wire [64:0]dout;
  wire p_17_out;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;

  fifo_65_blk_mem_gen_v8_4_3_synth inst_blk_mem_gen
       (.\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ),
        .\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .clk(clk),
        .din(din),
        .dout(dout),
        .p_17_out(p_17_out),
        .srst_full_ff_i(srst_full_ff_i),
        .tmp_ram_rd_en(tmp_ram_rd_en),
        .tmp_ram_regout_en(tmp_ram_regout_en));
endmodule

(* ORIG_REF_NAME = "blk_mem_gen_v8_4_3_synth" *) 
module fifo_65_blk_mem_gen_v8_4_3_synth
   (dout,
    clk,
    tmp_ram_rd_en,
    p_17_out,
    tmp_ram_regout_en,
    srst_full_ff_i,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ,
    din);
  output [64:0]dout;
  input clk;
  input tmp_ram_rd_en;
  input p_17_out;
  input tmp_ram_regout_en;
  input srst_full_ff_i;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  input [64:0]din;

  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  wire clk;
  wire [64:0]din;
  wire [64:0]dout;
  wire p_17_out;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;

  fifo_65_blk_mem_gen_top \gnbram.gnativebmg.native_blk_mem_gen 
       (.\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ),
        .\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .clk(clk),
        .din(din),
        .dout(dout),
        .p_17_out(p_17_out),
        .srst_full_ff_i(srst_full_ff_i),
        .tmp_ram_rd_en(tmp_ram_rd_en),
        .tmp_ram_regout_en(tmp_ram_regout_en));
endmodule

(* ORIG_REF_NAME = "bram_fifo_rstlogic" *) 
module fifo_65_bram_fifo_rstlogic
   (wr_rst_reg_reg_0,
    srst_full_ff_i,
    srst,
    clk);
  output wr_rst_reg_reg_0;
  output srst_full_ff_i;
  input srst;
  input clk;

  wire clk;
  (* async_reg = "true" *) wire d_asreg;
  (* async_reg = "true" *) wire rd_rst_reg;
  (* async_reg = "true" *) wire rdrst_q1;
  (* async_reg = "true" *) wire rdrst_q2;
  (* async_reg = "true" *) wire rdrst_q3;
  (* async_reg = "true" *) wire rst_d1;
  (* async_reg = "true" *) wire rst_d2;
  wire srst;
  wire srst_full_ff_i;
  wire wr_rst_reg_i_1_n_0;
  wire wr_rst_reg_reg_0;
  (* async_reg = "true" *) wire wrrst_q1;
  (* async_reg = "true" *) wire wrrst_q2;
  (* async_reg = "true" *) wire wrrst_q3;

  LUT2 #(
    .INIT(4'hE)) 
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_i_4 
       (.I0(srst),
        .I1(wr_rst_reg_reg_0),
        .O(srst_full_ff_i));
  LUT1 #(
    .INIT(2'h2)) 
    i_0
       (.I0(1'b0),
        .O(d_asreg));
  LUT1 #(
    .INIT(2'h2)) 
    i_1
       (.I0(1'b0),
        .O(rd_rst_reg));
  LUT1 #(
    .INIT(2'h2)) 
    i_2
       (.I0(1'b0),
        .O(wrrst_q1));
  LUT1 #(
    .INIT(2'h2)) 
    i_3
       (.I0(1'b0),
        .O(wrrst_q2));
  LUT1 #(
    .INIT(2'h2)) 
    i_4
       (.I0(1'b0),
        .O(wrrst_q3));
  LUT1 #(
    .INIT(2'h2)) 
    i_5
       (.I0(1'b0),
        .O(rdrst_q1));
  LUT1 #(
    .INIT(2'h2)) 
    i_6
       (.I0(1'b0),
        .O(rdrst_q2));
  LUT1 #(
    .INIT(2'h2)) 
    i_7
       (.I0(1'b0),
        .O(rdrst_q3));
  (* ASYNC_REG *) 
  (* KEEP = "yes" *) 
  FDRE #(
    .INIT(1'b1)) 
    rst_d1_reg
       (.C(clk),
        .CE(1'b1),
        .D(srst),
        .Q(rst_d1),
        .R(1'b0));
  (* ASYNC_REG *) 
  (* KEEP = "yes" *) 
  FDRE #(
    .INIT(1'b1)) 
    rst_d2_reg
       (.C(clk),
        .CE(1'b1),
        .D(rst_d1),
        .Q(rst_d2),
        .R(1'b0));
  LUT2 #(
    .INIT(4'h2)) 
    wr_rst_reg_i_1
       (.I0(srst),
        .I1(wr_rst_reg_reg_0),
        .O(wr_rst_reg_i_1_n_0));
  FDRE #(
    .INIT(1'b0)) 
    wr_rst_reg_reg
       (.C(clk),
        .CE(1'b1),
        .D(wr_rst_reg_i_1_n_0),
        .Q(wr_rst_reg_reg_0),
        .R(1'b0));
endmodule

(* ORIG_REF_NAME = "dc_ss_fwft" *) 
module fifo_65_dc_ss_fwft
   (Q,
    out,
    rd_en,
    srst_full_ff_i,
    E,
    clk);
  output [6:0]Q;
  input out;
  input rd_en;
  input srst_full_ff_i;
  input [0:0]E;
  input clk;

  wire [0:0]E;
  wire [6:0]Q;
  wire clk;
  wire out;
  wire rd_en;
  wire srst_full_ff_i;

  fifo_65_updn_cntr dc
       (.E(E),
        .Q(Q),
        .clk(clk),
        .out(out),
        .rd_en(rd_en),
        .srst_full_ff_i(srst_full_ff_i));
endmodule

(* ORIG_REF_NAME = "fifo_generator_ramfifo" *) 
module fifo_65_fifo_generator_ramfifo
   (data_count,
    dout,
    almost_empty,
    empty,
    full,
    prog_empty,
    wr_rst_reg_reg,
    prog_full,
    rd_en,
    srst,
    clk,
    din,
    wr_en);
  output [6:0]data_count;
  output [64:0]dout;
  output almost_empty;
  output empty;
  output full;
  output prog_empty;
  output wr_rst_reg_reg;
  output prog_full;
  input rd_en;
  input srst;
  input clk;
  input [64:0]din;
  input wr_en;

  wire almost_empty;
  wire clk;
  wire [6:0]data_count;
  wire [64:0]din;
  wire [64:0]dout;
  wire empty;
  wire full;
  wire \gntv_or_sync_fifo.gl0.rd_n_21 ;
  wire \gntv_or_sync_fifo.gl0.rd_n_23 ;
  wire \gntv_or_sync_fifo.gl0.rd_n_24 ;
  wire \gntv_or_sync_fifo.gl0.rd_n_25 ;
  wire \gntv_or_sync_fifo.gl0.rd_n_26 ;
  wire \gntv_or_sync_fifo.gl0.rd_n_27 ;
  wire \gntv_or_sync_fifo.gl0.wr_n_0 ;
  wire \gr1.gdcf.dc/cntr_en ;
  wire [0:0]\grss.gpe.rdpe/rd_pntr_inv_pad ;
  wire \gwss.gpf.wrpf/eqOp__4 ;
  wire \gwss.gpf.wrpf/p_1_out__0 ;
  wire \gwss.wsts/comp0 ;
  wire [5:0]p_0_out;
  wire [5:0]p_11_out;
  wire [5:0]p_12_out;
  wire p_17_out;
  wire p_3_out;
  wire p_7_out;
  wire [6:1]plusOp;
  wire prog_empty;
  wire prog_full;
  wire rd_en;
  wire srst;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;
  wire wr_en;
  wire wr_rst_reg_reg;

  fifo_65_rd_logic \gntv_or_sync_fifo.gl0.rd 
       (.D({plusOp[6:4],plusOp[2:1]}),
        .\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram (wr_rst_reg_reg),
        .E(\gr1.gdcf.dc/cntr_en ),
        .Q(data_count),
        .almost_empty(almost_empty),
        .clk(clk),
        .comp0(\gwss.wsts/comp0 ),
        .empty(empty),
        .eqOp__4(\gwss.gpf.wrpf/eqOp__4 ),
        .\gc1.count_d2_reg[0] (\gntv_or_sync_fifo.gl0.rd_n_23 ),
        .\gc1.count_d2_reg[0]_0 (\gntv_or_sync_fifo.gl0.rd_n_24 ),
        .\gc1.count_d2_reg[4] (\gntv_or_sync_fifo.gl0.rd_n_25 ),
        .\gc1.count_d2_reg[4]_0 (\gntv_or_sync_fifo.gl0.rd_n_26 ),
        .\gc1.count_d2_reg[5] (p_0_out),
        .\gcc0.gc0.count_reg[2] (\gntv_or_sync_fifo.gl0.rd_n_21 ),
        .\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ({p_12_out[5:4],p_12_out[2:0]}),
        .\greg.gpcry_sym.diff_pntr_pad_reg[6] (p_11_out),
        .\greg.ram_rd_en_i_reg (\gntv_or_sync_fifo.gl0.rd_n_27 ),
        .out(p_3_out),
        .p_17_out(p_17_out),
        .p_1_out__0(\gwss.gpf.wrpf/p_1_out__0 ),
        .p_7_out(p_7_out),
        .prog_empty(prog_empty),
        .prog_full(prog_full),
        .ram_empty_fb_i_reg(\gntv_or_sync_fifo.gl0.wr_n_0 ),
        .rd_en(rd_en),
        .rd_pntr_inv_pad(\grss.gpe.rdpe/rd_pntr_inv_pad ),
        .srst(srst),
        .srst_full_ff_i(srst_full_ff_i),
        .tmp_ram_rd_en(tmp_ram_rd_en),
        .tmp_ram_regout_en(tmp_ram_regout_en),
        .wr_en(wr_en));
  fifo_65_wr_logic \gntv_or_sync_fifo.gl0.wr 
       (.D({plusOp[6:4],plusOp[2:1]}),
        .E(\gr1.gdcf.dc/cntr_en ),
        .Q({p_12_out[5:4],p_12_out[2:0]}),
        .clk(clk),
        .comp0(\gwss.wsts/comp0 ),
        .\count_reg[6] (p_3_out),
        .eqOp__4(\gwss.gpf.wrpf/eqOp__4 ),
        .full(full),
        .\gcc0.gc0.count_d1_reg[5] (p_11_out),
        .\gdiff.gcry_1_sym.diff_pntr_pad_reg[3] (\gntv_or_sync_fifo.gl0.rd_n_21 ),
        .\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] (\gntv_or_sync_fifo.gl0.rd_n_26 ),
        .\gpfs.prog_full_i_reg (\gntv_or_sync_fifo.gl0.rd_n_27 ),
        .\greg.gpcry_sym.diff_pntr_pad_reg[6] (\gntv_or_sync_fifo.gl0.rd_n_25 ),
        .out(\gntv_or_sync_fifo.gl0.wr_n_0 ),
        .p_17_out(p_17_out),
        .p_1_out__0(\gwss.gpf.wrpf/p_1_out__0 ),
        .p_7_out(p_7_out),
        .prog_full(prog_full),
        .ram_full_fb_i_reg(p_0_out),
        .ram_full_fb_i_reg_0(\gntv_or_sync_fifo.gl0.rd_n_24 ),
        .ram_full_fb_i_reg_1(\gntv_or_sync_fifo.gl0.rd_n_23 ),
        .rd_en(rd_en),
        .rd_pntr_inv_pad(\grss.gpe.rdpe/rd_pntr_inv_pad ),
        .srst_full_ff_i(srst_full_ff_i),
        .wr_en(wr_en));
  fifo_65_memory \gntv_or_sync_fifo.mem 
       (.\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram (p_0_out),
        .\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 (p_11_out),
        .clk(clk),
        .din(din),
        .dout(dout),
        .p_17_out(p_17_out),
        .srst_full_ff_i(srst_full_ff_i),
        .tmp_ram_rd_en(tmp_ram_rd_en),
        .tmp_ram_regout_en(tmp_ram_regout_en));
  fifo_65_reset_blk_ramfifo rstblk
       (.clk(clk),
        .srst(srst),
        .srst_full_ff_i(srst_full_ff_i),
        .wr_rst_reg_reg(wr_rst_reg_reg));
endmodule

(* ORIG_REF_NAME = "fifo_generator_top" *) 
module fifo_65_fifo_generator_top
   (DATA_COUNT,
    dout,
    almost_empty,
    empty,
    full,
    prog_empty,
    wr_rst_reg_reg,
    prog_full,
    rd_en,
    srst,
    clk,
    din,
    wr_en);
  output [6:0]DATA_COUNT;
  output [64:0]dout;
  output almost_empty;
  output empty;
  output full;
  output prog_empty;
  output wr_rst_reg_reg;
  output prog_full;
  input rd_en;
  input srst;
  input clk;
  input [64:0]din;
  input wr_en;

  wire [6:0]DATA_COUNT;
  wire almost_empty;
  wire clk;
  wire [64:0]din;
  wire [64:0]dout;
  wire empty;
  wire full;
  wire prog_empty;
  wire prog_full;
  wire rd_en;
  wire srst;
  wire wr_en;
  wire wr_rst_reg_reg;

  fifo_65_fifo_generator_ramfifo \grf.rf 
       (.almost_empty(almost_empty),
        .clk(clk),
        .data_count(DATA_COUNT),
        .din(din),
        .dout(dout),
        .empty(empty),
        .full(full),
        .prog_empty(prog_empty),
        .prog_full(prog_full),
        .rd_en(rd_en),
        .srst(srst),
        .wr_en(wr_en),
        .wr_rst_reg_reg(wr_rst_reg_reg));
endmodule

(* C_ADD_NGC_CONSTRAINT = "0" *) (* C_APPLICATION_TYPE_AXIS = "0" *) (* C_APPLICATION_TYPE_RACH = "0" *) 
(* C_APPLICATION_TYPE_RDCH = "0" *) (* C_APPLICATION_TYPE_WACH = "0" *) (* C_APPLICATION_TYPE_WDCH = "0" *) 
(* C_APPLICATION_TYPE_WRCH = "0" *) (* C_AXIS_TDATA_WIDTH = "8" *) (* C_AXIS_TDEST_WIDTH = "1" *) 
(* C_AXIS_TID_WIDTH = "1" *) (* C_AXIS_TKEEP_WIDTH = "1" *) (* C_AXIS_TSTRB_WIDTH = "1" *) 
(* C_AXIS_TUSER_WIDTH = "4" *) (* C_AXIS_TYPE = "0" *) (* C_AXI_ADDR_WIDTH = "32" *) 
(* C_AXI_ARUSER_WIDTH = "1" *) (* C_AXI_AWUSER_WIDTH = "1" *) (* C_AXI_BUSER_WIDTH = "1" *) 
(* C_AXI_DATA_WIDTH = "64" *) (* C_AXI_ID_WIDTH = "1" *) (* C_AXI_LEN_WIDTH = "8" *) 
(* C_AXI_LOCK_WIDTH = "1" *) (* C_AXI_RUSER_WIDTH = "1" *) (* C_AXI_TYPE = "1" *) 
(* C_AXI_WUSER_WIDTH = "1" *) (* C_COMMON_CLOCK = "1" *) (* C_COUNT_TYPE = "0" *) 
(* C_DATA_COUNT_WIDTH = "7" *) (* C_DEFAULT_VALUE = "BlankString" *) (* C_DIN_WIDTH = "65" *) 
(* C_DIN_WIDTH_AXIS = "1" *) (* C_DIN_WIDTH_RACH = "32" *) (* C_DIN_WIDTH_RDCH = "64" *) 
(* C_DIN_WIDTH_WACH = "1" *) (* C_DIN_WIDTH_WDCH = "64" *) (* C_DIN_WIDTH_WRCH = "2" *) 
(* C_DOUT_RST_VAL = "0" *) (* C_DOUT_WIDTH = "65" *) (* C_ENABLE_RLOCS = "0" *) 
(* C_ENABLE_RST_SYNC = "1" *) (* C_EN_SAFETY_CKT = "0" *) (* C_ERROR_INJECTION_TYPE = "0" *) 
(* C_ERROR_INJECTION_TYPE_AXIS = "0" *) (* C_ERROR_INJECTION_TYPE_RACH = "0" *) (* C_ERROR_INJECTION_TYPE_RDCH = "0" *) 
(* C_ERROR_INJECTION_TYPE_WACH = "0" *) (* C_ERROR_INJECTION_TYPE_WDCH = "0" *) (* C_ERROR_INJECTION_TYPE_WRCH = "0" *) 
(* C_FAMILY = "virtexuplusHBM" *) (* C_FULL_FLAGS_RST_VAL = "0" *) (* C_HAS_ALMOST_EMPTY = "1" *) 
(* C_HAS_ALMOST_FULL = "0" *) (* C_HAS_AXIS_TDATA = "1" *) (* C_HAS_AXIS_TDEST = "0" *) 
(* C_HAS_AXIS_TID = "0" *) (* C_HAS_AXIS_TKEEP = "0" *) (* C_HAS_AXIS_TLAST = "0" *) 
(* C_HAS_AXIS_TREADY = "1" *) (* C_HAS_AXIS_TSTRB = "0" *) (* C_HAS_AXIS_TUSER = "1" *) 
(* C_HAS_AXI_ARUSER = "0" *) (* C_HAS_AXI_AWUSER = "0" *) (* C_HAS_AXI_BUSER = "0" *) 
(* C_HAS_AXI_ID = "0" *) (* C_HAS_AXI_RD_CHANNEL = "1" *) (* C_HAS_AXI_RUSER = "0" *) 
(* C_HAS_AXI_WR_CHANNEL = "1" *) (* C_HAS_AXI_WUSER = "0" *) (* C_HAS_BACKUP = "0" *) 
(* C_HAS_DATA_COUNT = "1" *) (* C_HAS_DATA_COUNTS_AXIS = "0" *) (* C_HAS_DATA_COUNTS_RACH = "0" *) 
(* C_HAS_DATA_COUNTS_RDCH = "0" *) (* C_HAS_DATA_COUNTS_WACH = "0" *) (* C_HAS_DATA_COUNTS_WDCH = "0" *) 
(* C_HAS_DATA_COUNTS_WRCH = "0" *) (* C_HAS_INT_CLK = "0" *) (* C_HAS_MASTER_CE = "0" *) 
(* C_HAS_MEMINIT_FILE = "0" *) (* C_HAS_OVERFLOW = "0" *) (* C_HAS_PROG_FLAGS_AXIS = "0" *) 
(* C_HAS_PROG_FLAGS_RACH = "0" *) (* C_HAS_PROG_FLAGS_RDCH = "0" *) (* C_HAS_PROG_FLAGS_WACH = "0" *) 
(* C_HAS_PROG_FLAGS_WDCH = "0" *) (* C_HAS_PROG_FLAGS_WRCH = "0" *) (* C_HAS_RD_DATA_COUNT = "0" *) 
(* C_HAS_RD_RST = "0" *) (* C_HAS_RST = "0" *) (* C_HAS_SLAVE_CE = "0" *) 
(* C_HAS_SRST = "1" *) (* C_HAS_UNDERFLOW = "0" *) (* C_HAS_VALID = "0" *) 
(* C_HAS_WR_ACK = "0" *) (* C_HAS_WR_DATA_COUNT = "0" *) (* C_HAS_WR_RST = "0" *) 
(* C_IMPLEMENTATION_TYPE = "0" *) (* C_IMPLEMENTATION_TYPE_AXIS = "1" *) (* C_IMPLEMENTATION_TYPE_RACH = "1" *) 
(* C_IMPLEMENTATION_TYPE_RDCH = "1" *) (* C_IMPLEMENTATION_TYPE_WACH = "1" *) (* C_IMPLEMENTATION_TYPE_WDCH = "1" *) 
(* C_IMPLEMENTATION_TYPE_WRCH = "1" *) (* C_INIT_WR_PNTR_VAL = "0" *) (* C_INTERFACE_TYPE = "0" *) 
(* C_MEMORY_TYPE = "1" *) (* C_MIF_FILE_NAME = "BlankString" *) (* C_MSGON_VAL = "1" *) 
(* C_OPTIMIZATION_MODE = "0" *) (* C_OVERFLOW_LOW = "0" *) (* C_POWER_SAVING_MODE = "0" *) 
(* C_PRELOAD_LATENCY = "0" *) (* C_PRELOAD_REGS = "1" *) (* C_PRIM_FIFO_TYPE = "512x72" *) 
(* C_PRIM_FIFO_TYPE_AXIS = "1kx18" *) (* C_PRIM_FIFO_TYPE_RACH = "512x36" *) (* C_PRIM_FIFO_TYPE_RDCH = "512x72" *) 
(* C_PRIM_FIFO_TYPE_WACH = "512x36" *) (* C_PRIM_FIFO_TYPE_WDCH = "512x72" *) (* C_PRIM_FIFO_TYPE_WRCH = "512x36" *) 
(* C_PROG_EMPTY_THRESH_ASSERT_VAL = "6" *) (* C_PROG_EMPTY_THRESH_ASSERT_VAL_AXIS = "1022" *) (* C_PROG_EMPTY_THRESH_ASSERT_VAL_RACH = "1022" *) 
(* C_PROG_EMPTY_THRESH_ASSERT_VAL_RDCH = "1022" *) (* C_PROG_EMPTY_THRESH_ASSERT_VAL_WACH = "1022" *) (* C_PROG_EMPTY_THRESH_ASSERT_VAL_WDCH = "1022" *) 
(* C_PROG_EMPTY_THRESH_ASSERT_VAL_WRCH = "1022" *) (* C_PROG_EMPTY_THRESH_NEGATE_VAL = "7" *) (* C_PROG_EMPTY_TYPE = "2" *) 
(* C_PROG_EMPTY_TYPE_AXIS = "0" *) (* C_PROG_EMPTY_TYPE_RACH = "0" *) (* C_PROG_EMPTY_TYPE_RDCH = "0" *) 
(* C_PROG_EMPTY_TYPE_WACH = "0" *) (* C_PROG_EMPTY_TYPE_WDCH = "0" *) (* C_PROG_EMPTY_TYPE_WRCH = "0" *) 
(* C_PROG_FULL_THRESH_ASSERT_VAL = "59" *) (* C_PROG_FULL_THRESH_ASSERT_VAL_AXIS = "1023" *) (* C_PROG_FULL_THRESH_ASSERT_VAL_RACH = "1023" *) 
(* C_PROG_FULL_THRESH_ASSERT_VAL_RDCH = "1023" *) (* C_PROG_FULL_THRESH_ASSERT_VAL_WACH = "1023" *) (* C_PROG_FULL_THRESH_ASSERT_VAL_WDCH = "1023" *) 
(* C_PROG_FULL_THRESH_ASSERT_VAL_WRCH = "1023" *) (* C_PROG_FULL_THRESH_NEGATE_VAL = "58" *) (* C_PROG_FULL_TYPE = "1" *) 
(* C_PROG_FULL_TYPE_AXIS = "0" *) (* C_PROG_FULL_TYPE_RACH = "0" *) (* C_PROG_FULL_TYPE_RDCH = "0" *) 
(* C_PROG_FULL_TYPE_WACH = "0" *) (* C_PROG_FULL_TYPE_WDCH = "0" *) (* C_PROG_FULL_TYPE_WRCH = "0" *) 
(* C_RACH_TYPE = "0" *) (* C_RDCH_TYPE = "0" *) (* C_RD_DATA_COUNT_WIDTH = "7" *) 
(* C_RD_DEPTH = "64" *) (* C_RD_FREQ = "1" *) (* C_RD_PNTR_WIDTH = "6" *) 
(* C_REG_SLICE_MODE_AXIS = "0" *) (* C_REG_SLICE_MODE_RACH = "0" *) (* C_REG_SLICE_MODE_RDCH = "0" *) 
(* C_REG_SLICE_MODE_WACH = "0" *) (* C_REG_SLICE_MODE_WDCH = "0" *) (* C_REG_SLICE_MODE_WRCH = "0" *) 
(* C_SELECT_XPM = "0" *) (* C_SYNCHRONIZER_STAGE = "2" *) (* C_UNDERFLOW_LOW = "0" *) 
(* C_USE_COMMON_OVERFLOW = "0" *) (* C_USE_COMMON_UNDERFLOW = "0" *) (* C_USE_DEFAULT_SETTINGS = "0" *) 
(* C_USE_DOUT_RST = "1" *) (* C_USE_ECC = "0" *) (* C_USE_ECC_AXIS = "0" *) 
(* C_USE_ECC_RACH = "0" *) (* C_USE_ECC_RDCH = "0" *) (* C_USE_ECC_WACH = "0" *) 
(* C_USE_ECC_WDCH = "0" *) (* C_USE_ECC_WRCH = "0" *) (* C_USE_EMBEDDED_REG = "1" *) 
(* C_USE_FIFO16_FLAGS = "0" *) (* C_USE_FWFT_DATA_COUNT = "1" *) (* C_USE_PIPELINE_REG = "0" *) 
(* C_VALID_LOW = "0" *) (* C_WACH_TYPE = "0" *) (* C_WDCH_TYPE = "0" *) 
(* C_WRCH_TYPE = "0" *) (* C_WR_ACK_LOW = "0" *) (* C_WR_DATA_COUNT_WIDTH = "7" *) 
(* C_WR_DEPTH = "64" *) (* C_WR_DEPTH_AXIS = "1024" *) (* C_WR_DEPTH_RACH = "16" *) 
(* C_WR_DEPTH_RDCH = "1024" *) (* C_WR_DEPTH_WACH = "16" *) (* C_WR_DEPTH_WDCH = "1024" *) 
(* C_WR_DEPTH_WRCH = "16" *) (* C_WR_FREQ = "1" *) (* C_WR_PNTR_WIDTH = "6" *) 
(* C_WR_PNTR_WIDTH_AXIS = "10" *) (* C_WR_PNTR_WIDTH_RACH = "4" *) (* C_WR_PNTR_WIDTH_RDCH = "10" *) 
(* C_WR_PNTR_WIDTH_WACH = "4" *) (* C_WR_PNTR_WIDTH_WDCH = "10" *) (* C_WR_PNTR_WIDTH_WRCH = "4" *) 
(* C_WR_RESPONSE_LATENCY = "1" *) (* ORIG_REF_NAME = "fifo_generator_v13_2_4" *) 
module fifo_65_fifo_generator_v13_2_4
   (backup,
    backup_marker,
    clk,
    rst,
    srst,
    wr_clk,
    wr_rst,
    rd_clk,
    rd_rst,
    din,
    wr_en,
    rd_en,
    prog_empty_thresh,
    prog_empty_thresh_assert,
    prog_empty_thresh_negate,
    prog_full_thresh,
    prog_full_thresh_assert,
    prog_full_thresh_negate,
    int_clk,
    injectdbiterr,
    injectsbiterr,
    sleep,
    dout,
    full,
    almost_full,
    wr_ack,
    overflow,
    empty,
    almost_empty,
    valid,
    underflow,
    data_count,
    rd_data_count,
    wr_data_count,
    prog_full,
    prog_empty,
    sbiterr,
    dbiterr,
    wr_rst_busy,
    rd_rst_busy,
    m_aclk,
    s_aclk,
    s_aresetn,
    m_aclk_en,
    s_aclk_en,
    s_axi_awid,
    s_axi_awaddr,
    s_axi_awlen,
    s_axi_awsize,
    s_axi_awburst,
    s_axi_awlock,
    s_axi_awcache,
    s_axi_awprot,
    s_axi_awqos,
    s_axi_awregion,
    s_axi_awuser,
    s_axi_awvalid,
    s_axi_awready,
    s_axi_wid,
    s_axi_wdata,
    s_axi_wstrb,
    s_axi_wlast,
    s_axi_wuser,
    s_axi_wvalid,
    s_axi_wready,
    s_axi_bid,
    s_axi_bresp,
    s_axi_buser,
    s_axi_bvalid,
    s_axi_bready,
    m_axi_awid,
    m_axi_awaddr,
    m_axi_awlen,
    m_axi_awsize,
    m_axi_awburst,
    m_axi_awlock,
    m_axi_awcache,
    m_axi_awprot,
    m_axi_awqos,
    m_axi_awregion,
    m_axi_awuser,
    m_axi_awvalid,
    m_axi_awready,
    m_axi_wid,
    m_axi_wdata,
    m_axi_wstrb,
    m_axi_wlast,
    m_axi_wuser,
    m_axi_wvalid,
    m_axi_wready,
    m_axi_bid,
    m_axi_bresp,
    m_axi_buser,
    m_axi_bvalid,
    m_axi_bready,
    s_axi_arid,
    s_axi_araddr,
    s_axi_arlen,
    s_axi_arsize,
    s_axi_arburst,
    s_axi_arlock,
    s_axi_arcache,
    s_axi_arprot,
    s_axi_arqos,
    s_axi_arregion,
    s_axi_aruser,
    s_axi_arvalid,
    s_axi_arready,
    s_axi_rid,
    s_axi_rdata,
    s_axi_rresp,
    s_axi_rlast,
    s_axi_ruser,
    s_axi_rvalid,
    s_axi_rready,
    m_axi_arid,
    m_axi_araddr,
    m_axi_arlen,
    m_axi_arsize,
    m_axi_arburst,
    m_axi_arlock,
    m_axi_arcache,
    m_axi_arprot,
    m_axi_arqos,
    m_axi_arregion,
    m_axi_aruser,
    m_axi_arvalid,
    m_axi_arready,
    m_axi_rid,
    m_axi_rdata,
    m_axi_rresp,
    m_axi_rlast,
    m_axi_ruser,
    m_axi_rvalid,
    m_axi_rready,
    s_axis_tvalid,
    s_axis_tready,
    s_axis_tdata,
    s_axis_tstrb,
    s_axis_tkeep,
    s_axis_tlast,
    s_axis_tid,
    s_axis_tdest,
    s_axis_tuser,
    m_axis_tvalid,
    m_axis_tready,
    m_axis_tdata,
    m_axis_tstrb,
    m_axis_tkeep,
    m_axis_tlast,
    m_axis_tid,
    m_axis_tdest,
    m_axis_tuser,
    axi_aw_injectsbiterr,
    axi_aw_injectdbiterr,
    axi_aw_prog_full_thresh,
    axi_aw_prog_empty_thresh,
    axi_aw_data_count,
    axi_aw_wr_data_count,
    axi_aw_rd_data_count,
    axi_aw_sbiterr,
    axi_aw_dbiterr,
    axi_aw_overflow,
    axi_aw_underflow,
    axi_aw_prog_full,
    axi_aw_prog_empty,
    axi_w_injectsbiterr,
    axi_w_injectdbiterr,
    axi_w_prog_full_thresh,
    axi_w_prog_empty_thresh,
    axi_w_data_count,
    axi_w_wr_data_count,
    axi_w_rd_data_count,
    axi_w_sbiterr,
    axi_w_dbiterr,
    axi_w_overflow,
    axi_w_underflow,
    axi_w_prog_full,
    axi_w_prog_empty,
    axi_b_injectsbiterr,
    axi_b_injectdbiterr,
    axi_b_prog_full_thresh,
    axi_b_prog_empty_thresh,
    axi_b_data_count,
    axi_b_wr_data_count,
    axi_b_rd_data_count,
    axi_b_sbiterr,
    axi_b_dbiterr,
    axi_b_overflow,
    axi_b_underflow,
    axi_b_prog_full,
    axi_b_prog_empty,
    axi_ar_injectsbiterr,
    axi_ar_injectdbiterr,
    axi_ar_prog_full_thresh,
    axi_ar_prog_empty_thresh,
    axi_ar_data_count,
    axi_ar_wr_data_count,
    axi_ar_rd_data_count,
    axi_ar_sbiterr,
    axi_ar_dbiterr,
    axi_ar_overflow,
    axi_ar_underflow,
    axi_ar_prog_full,
    axi_ar_prog_empty,
    axi_r_injectsbiterr,
    axi_r_injectdbiterr,
    axi_r_prog_full_thresh,
    axi_r_prog_empty_thresh,
    axi_r_data_count,
    axi_r_wr_data_count,
    axi_r_rd_data_count,
    axi_r_sbiterr,
    axi_r_dbiterr,
    axi_r_overflow,
    axi_r_underflow,
    axi_r_prog_full,
    axi_r_prog_empty,
    axis_injectsbiterr,
    axis_injectdbiterr,
    axis_prog_full_thresh,
    axis_prog_empty_thresh,
    axis_data_count,
    axis_wr_data_count,
    axis_rd_data_count,
    axis_sbiterr,
    axis_dbiterr,
    axis_overflow,
    axis_underflow,
    axis_prog_full,
    axis_prog_empty);
  input backup;
  input backup_marker;
  input clk;
  input rst;
  input srst;
  input wr_clk;
  input wr_rst;
  input rd_clk;
  input rd_rst;
  input [64:0]din;
  input wr_en;
  input rd_en;
  input [5:0]prog_empty_thresh;
  input [5:0]prog_empty_thresh_assert;
  input [5:0]prog_empty_thresh_negate;
  input [5:0]prog_full_thresh;
  input [5:0]prog_full_thresh_assert;
  input [5:0]prog_full_thresh_negate;
  input int_clk;
  input injectdbiterr;
  input injectsbiterr;
  input sleep;
  output [64:0]dout;
  output full;
  output almost_full;
  output wr_ack;
  output overflow;
  output empty;
  output almost_empty;
  output valid;
  output underflow;
  output [6:0]data_count;
  output [6:0]rd_data_count;
  output [6:0]wr_data_count;
  output prog_full;
  output prog_empty;
  output sbiterr;
  output dbiterr;
  output wr_rst_busy;
  output rd_rst_busy;
  input m_aclk;
  input s_aclk;
  input s_aresetn;
  input m_aclk_en;
  input s_aclk_en;
  input [0:0]s_axi_awid;
  input [31:0]s_axi_awaddr;
  input [7:0]s_axi_awlen;
  input [2:0]s_axi_awsize;
  input [1:0]s_axi_awburst;
  input [0:0]s_axi_awlock;
  input [3:0]s_axi_awcache;
  input [2:0]s_axi_awprot;
  input [3:0]s_axi_awqos;
  input [3:0]s_axi_awregion;
  input [0:0]s_axi_awuser;
  input s_axi_awvalid;
  output s_axi_awready;
  input [0:0]s_axi_wid;
  input [63:0]s_axi_wdata;
  input [7:0]s_axi_wstrb;
  input s_axi_wlast;
  input [0:0]s_axi_wuser;
  input s_axi_wvalid;
  output s_axi_wready;
  output [0:0]s_axi_bid;
  output [1:0]s_axi_bresp;
  output [0:0]s_axi_buser;
  output s_axi_bvalid;
  input s_axi_bready;
  output [0:0]m_axi_awid;
  output [31:0]m_axi_awaddr;
  output [7:0]m_axi_awlen;
  output [2:0]m_axi_awsize;
  output [1:0]m_axi_awburst;
  output [0:0]m_axi_awlock;
  output [3:0]m_axi_awcache;
  output [2:0]m_axi_awprot;
  output [3:0]m_axi_awqos;
  output [3:0]m_axi_awregion;
  output [0:0]m_axi_awuser;
  output m_axi_awvalid;
  input m_axi_awready;
  output [0:0]m_axi_wid;
  output [63:0]m_axi_wdata;
  output [7:0]m_axi_wstrb;
  output m_axi_wlast;
  output [0:0]m_axi_wuser;
  output m_axi_wvalid;
  input m_axi_wready;
  input [0:0]m_axi_bid;
  input [1:0]m_axi_bresp;
  input [0:0]m_axi_buser;
  input m_axi_bvalid;
  output m_axi_bready;
  input [0:0]s_axi_arid;
  input [31:0]s_axi_araddr;
  input [7:0]s_axi_arlen;
  input [2:0]s_axi_arsize;
  input [1:0]s_axi_arburst;
  input [0:0]s_axi_arlock;
  input [3:0]s_axi_arcache;
  input [2:0]s_axi_arprot;
  input [3:0]s_axi_arqos;
  input [3:0]s_axi_arregion;
  input [0:0]s_axi_aruser;
  input s_axi_arvalid;
  output s_axi_arready;
  output [0:0]s_axi_rid;
  output [63:0]s_axi_rdata;
  output [1:0]s_axi_rresp;
  output s_axi_rlast;
  output [0:0]s_axi_ruser;
  output s_axi_rvalid;
  input s_axi_rready;
  output [0:0]m_axi_arid;
  output [31:0]m_axi_araddr;
  output [7:0]m_axi_arlen;
  output [2:0]m_axi_arsize;
  output [1:0]m_axi_arburst;
  output [0:0]m_axi_arlock;
  output [3:0]m_axi_arcache;
  output [2:0]m_axi_arprot;
  output [3:0]m_axi_arqos;
  output [3:0]m_axi_arregion;
  output [0:0]m_axi_aruser;
  output m_axi_arvalid;
  input m_axi_arready;
  input [0:0]m_axi_rid;
  input [63:0]m_axi_rdata;
  input [1:0]m_axi_rresp;
  input m_axi_rlast;
  input [0:0]m_axi_ruser;
  input m_axi_rvalid;
  output m_axi_rready;
  input s_axis_tvalid;
  output s_axis_tready;
  input [7:0]s_axis_tdata;
  input [0:0]s_axis_tstrb;
  input [0:0]s_axis_tkeep;
  input s_axis_tlast;
  input [0:0]s_axis_tid;
  input [0:0]s_axis_tdest;
  input [3:0]s_axis_tuser;
  output m_axis_tvalid;
  input m_axis_tready;
  output [7:0]m_axis_tdata;
  output [0:0]m_axis_tstrb;
  output [0:0]m_axis_tkeep;
  output m_axis_tlast;
  output [0:0]m_axis_tid;
  output [0:0]m_axis_tdest;
  output [3:0]m_axis_tuser;
  input axi_aw_injectsbiterr;
  input axi_aw_injectdbiterr;
  input [3:0]axi_aw_prog_full_thresh;
  input [3:0]axi_aw_prog_empty_thresh;
  output [4:0]axi_aw_data_count;
  output [4:0]axi_aw_wr_data_count;
  output [4:0]axi_aw_rd_data_count;
  output axi_aw_sbiterr;
  output axi_aw_dbiterr;
  output axi_aw_overflow;
  output axi_aw_underflow;
  output axi_aw_prog_full;
  output axi_aw_prog_empty;
  input axi_w_injectsbiterr;
  input axi_w_injectdbiterr;
  input [9:0]axi_w_prog_full_thresh;
  input [9:0]axi_w_prog_empty_thresh;
  output [10:0]axi_w_data_count;
  output [10:0]axi_w_wr_data_count;
  output [10:0]axi_w_rd_data_count;
  output axi_w_sbiterr;
  output axi_w_dbiterr;
  output axi_w_overflow;
  output axi_w_underflow;
  output axi_w_prog_full;
  output axi_w_prog_empty;
  input axi_b_injectsbiterr;
  input axi_b_injectdbiterr;
  input [3:0]axi_b_prog_full_thresh;
  input [3:0]axi_b_prog_empty_thresh;
  output [4:0]axi_b_data_count;
  output [4:0]axi_b_wr_data_count;
  output [4:0]axi_b_rd_data_count;
  output axi_b_sbiterr;
  output axi_b_dbiterr;
  output axi_b_overflow;
  output axi_b_underflow;
  output axi_b_prog_full;
  output axi_b_prog_empty;
  input axi_ar_injectsbiterr;
  input axi_ar_injectdbiterr;
  input [3:0]axi_ar_prog_full_thresh;
  input [3:0]axi_ar_prog_empty_thresh;
  output [4:0]axi_ar_data_count;
  output [4:0]axi_ar_wr_data_count;
  output [4:0]axi_ar_rd_data_count;
  output axi_ar_sbiterr;
  output axi_ar_dbiterr;
  output axi_ar_overflow;
  output axi_ar_underflow;
  output axi_ar_prog_full;
  output axi_ar_prog_empty;
  input axi_r_injectsbiterr;
  input axi_r_injectdbiterr;
  input [9:0]axi_r_prog_full_thresh;
  input [9:0]axi_r_prog_empty_thresh;
  output [10:0]axi_r_data_count;
  output [10:0]axi_r_wr_data_count;
  output [10:0]axi_r_rd_data_count;
  output axi_r_sbiterr;
  output axi_r_dbiterr;
  output axi_r_overflow;
  output axi_r_underflow;
  output axi_r_prog_full;
  output axi_r_prog_empty;
  input axis_injectsbiterr;
  input axis_injectdbiterr;
  input [9:0]axis_prog_full_thresh;
  input [9:0]axis_prog_empty_thresh;
  output [10:0]axis_data_count;
  output [10:0]axis_wr_data_count;
  output [10:0]axis_rd_data_count;
  output axis_sbiterr;
  output axis_dbiterr;
  output axis_overflow;
  output axis_underflow;
  output axis_prog_full;
  output axis_prog_empty;

  wire \<const0> ;
  wire \<const1> ;
  wire almost_empty;
  wire clk;
  wire [6:0]data_count;
  wire [64:0]din;
  wire [64:0]dout;
  wire empty;
  wire full;
  wire prog_empty;
  wire prog_full;
  wire rd_en;
  wire srst;
  wire wr_en;
  wire wr_rst_busy;

  assign almost_full = \<const0> ;
  assign axi_ar_data_count[4] = \<const0> ;
  assign axi_ar_data_count[3] = \<const0> ;
  assign axi_ar_data_count[2] = \<const0> ;
  assign axi_ar_data_count[1] = \<const0> ;
  assign axi_ar_data_count[0] = \<const0> ;
  assign axi_ar_dbiterr = \<const0> ;
  assign axi_ar_overflow = \<const0> ;
  assign axi_ar_prog_empty = \<const1> ;
  assign axi_ar_prog_full = \<const0> ;
  assign axi_ar_rd_data_count[4] = \<const0> ;
  assign axi_ar_rd_data_count[3] = \<const0> ;
  assign axi_ar_rd_data_count[2] = \<const0> ;
  assign axi_ar_rd_data_count[1] = \<const0> ;
  assign axi_ar_rd_data_count[0] = \<const0> ;
  assign axi_ar_sbiterr = \<const0> ;
  assign axi_ar_underflow = \<const0> ;
  assign axi_ar_wr_data_count[4] = \<const0> ;
  assign axi_ar_wr_data_count[3] = \<const0> ;
  assign axi_ar_wr_data_count[2] = \<const0> ;
  assign axi_ar_wr_data_count[1] = \<const0> ;
  assign axi_ar_wr_data_count[0] = \<const0> ;
  assign axi_aw_data_count[4] = \<const0> ;
  assign axi_aw_data_count[3] = \<const0> ;
  assign axi_aw_data_count[2] = \<const0> ;
  assign axi_aw_data_count[1] = \<const0> ;
  assign axi_aw_data_count[0] = \<const0> ;
  assign axi_aw_dbiterr = \<const0> ;
  assign axi_aw_overflow = \<const0> ;
  assign axi_aw_prog_empty = \<const1> ;
  assign axi_aw_prog_full = \<const0> ;
  assign axi_aw_rd_data_count[4] = \<const0> ;
  assign axi_aw_rd_data_count[3] = \<const0> ;
  assign axi_aw_rd_data_count[2] = \<const0> ;
  assign axi_aw_rd_data_count[1] = \<const0> ;
  assign axi_aw_rd_data_count[0] = \<const0> ;
  assign axi_aw_sbiterr = \<const0> ;
  assign axi_aw_underflow = \<const0> ;
  assign axi_aw_wr_data_count[4] = \<const0> ;
  assign axi_aw_wr_data_count[3] = \<const0> ;
  assign axi_aw_wr_data_count[2] = \<const0> ;
  assign axi_aw_wr_data_count[1] = \<const0> ;
  assign axi_aw_wr_data_count[0] = \<const0> ;
  assign axi_b_data_count[4] = \<const0> ;
  assign axi_b_data_count[3] = \<const0> ;
  assign axi_b_data_count[2] = \<const0> ;
  assign axi_b_data_count[1] = \<const0> ;
  assign axi_b_data_count[0] = \<const0> ;
  assign axi_b_dbiterr = \<const0> ;
  assign axi_b_overflow = \<const0> ;
  assign axi_b_prog_empty = \<const1> ;
  assign axi_b_prog_full = \<const0> ;
  assign axi_b_rd_data_count[4] = \<const0> ;
  assign axi_b_rd_data_count[3] = \<const0> ;
  assign axi_b_rd_data_count[2] = \<const0> ;
  assign axi_b_rd_data_count[1] = \<const0> ;
  assign axi_b_rd_data_count[0] = \<const0> ;
  assign axi_b_sbiterr = \<const0> ;
  assign axi_b_underflow = \<const0> ;
  assign axi_b_wr_data_count[4] = \<const0> ;
  assign axi_b_wr_data_count[3] = \<const0> ;
  assign axi_b_wr_data_count[2] = \<const0> ;
  assign axi_b_wr_data_count[1] = \<const0> ;
  assign axi_b_wr_data_count[0] = \<const0> ;
  assign axi_r_data_count[10] = \<const0> ;
  assign axi_r_data_count[9] = \<const0> ;
  assign axi_r_data_count[8] = \<const0> ;
  assign axi_r_data_count[7] = \<const0> ;
  assign axi_r_data_count[6] = \<const0> ;
  assign axi_r_data_count[5] = \<const0> ;
  assign axi_r_data_count[4] = \<const0> ;
  assign axi_r_data_count[3] = \<const0> ;
  assign axi_r_data_count[2] = \<const0> ;
  assign axi_r_data_count[1] = \<const0> ;
  assign axi_r_data_count[0] = \<const0> ;
  assign axi_r_dbiterr = \<const0> ;
  assign axi_r_overflow = \<const0> ;
  assign axi_r_prog_empty = \<const1> ;
  assign axi_r_prog_full = \<const0> ;
  assign axi_r_rd_data_count[10] = \<const0> ;
  assign axi_r_rd_data_count[9] = \<const0> ;
  assign axi_r_rd_data_count[8] = \<const0> ;
  assign axi_r_rd_data_count[7] = \<const0> ;
  assign axi_r_rd_data_count[6] = \<const0> ;
  assign axi_r_rd_data_count[5] = \<const0> ;
  assign axi_r_rd_data_count[4] = \<const0> ;
  assign axi_r_rd_data_count[3] = \<const0> ;
  assign axi_r_rd_data_count[2] = \<const0> ;
  assign axi_r_rd_data_count[1] = \<const0> ;
  assign axi_r_rd_data_count[0] = \<const0> ;
  assign axi_r_sbiterr = \<const0> ;
  assign axi_r_underflow = \<const0> ;
  assign axi_r_wr_data_count[10] = \<const0> ;
  assign axi_r_wr_data_count[9] = \<const0> ;
  assign axi_r_wr_data_count[8] = \<const0> ;
  assign axi_r_wr_data_count[7] = \<const0> ;
  assign axi_r_wr_data_count[6] = \<const0> ;
  assign axi_r_wr_data_count[5] = \<const0> ;
  assign axi_r_wr_data_count[4] = \<const0> ;
  assign axi_r_wr_data_count[3] = \<const0> ;
  assign axi_r_wr_data_count[2] = \<const0> ;
  assign axi_r_wr_data_count[1] = \<const0> ;
  assign axi_r_wr_data_count[0] = \<const0> ;
  assign axi_w_data_count[10] = \<const0> ;
  assign axi_w_data_count[9] = \<const0> ;
  assign axi_w_data_count[8] = \<const0> ;
  assign axi_w_data_count[7] = \<const0> ;
  assign axi_w_data_count[6] = \<const0> ;
  assign axi_w_data_count[5] = \<const0> ;
  assign axi_w_data_count[4] = \<const0> ;
  assign axi_w_data_count[3] = \<const0> ;
  assign axi_w_data_count[2] = \<const0> ;
  assign axi_w_data_count[1] = \<const0> ;
  assign axi_w_data_count[0] = \<const0> ;
  assign axi_w_dbiterr = \<const0> ;
  assign axi_w_overflow = \<const0> ;
  assign axi_w_prog_empty = \<const1> ;
  assign axi_w_prog_full = \<const0> ;
  assign axi_w_rd_data_count[10] = \<const0> ;
  assign axi_w_rd_data_count[9] = \<const0> ;
  assign axi_w_rd_data_count[8] = \<const0> ;
  assign axi_w_rd_data_count[7] = \<const0> ;
  assign axi_w_rd_data_count[6] = \<const0> ;
  assign axi_w_rd_data_count[5] = \<const0> ;
  assign axi_w_rd_data_count[4] = \<const0> ;
  assign axi_w_rd_data_count[3] = \<const0> ;
  assign axi_w_rd_data_count[2] = \<const0> ;
  assign axi_w_rd_data_count[1] = \<const0> ;
  assign axi_w_rd_data_count[0] = \<const0> ;
  assign axi_w_sbiterr = \<const0> ;
  assign axi_w_underflow = \<const0> ;
  assign axi_w_wr_data_count[10] = \<const0> ;
  assign axi_w_wr_data_count[9] = \<const0> ;
  assign axi_w_wr_data_count[8] = \<const0> ;
  assign axi_w_wr_data_count[7] = \<const0> ;
  assign axi_w_wr_data_count[6] = \<const0> ;
  assign axi_w_wr_data_count[5] = \<const0> ;
  assign axi_w_wr_data_count[4] = \<const0> ;
  assign axi_w_wr_data_count[3] = \<const0> ;
  assign axi_w_wr_data_count[2] = \<const0> ;
  assign axi_w_wr_data_count[1] = \<const0> ;
  assign axi_w_wr_data_count[0] = \<const0> ;
  assign axis_data_count[10] = \<const0> ;
  assign axis_data_count[9] = \<const0> ;
  assign axis_data_count[8] = \<const0> ;
  assign axis_data_count[7] = \<const0> ;
  assign axis_data_count[6] = \<const0> ;
  assign axis_data_count[5] = \<const0> ;
  assign axis_data_count[4] = \<const0> ;
  assign axis_data_count[3] = \<const0> ;
  assign axis_data_count[2] = \<const0> ;
  assign axis_data_count[1] = \<const0> ;
  assign axis_data_count[0] = \<const0> ;
  assign axis_dbiterr = \<const0> ;
  assign axis_overflow = \<const0> ;
  assign axis_prog_empty = \<const1> ;
  assign axis_prog_full = \<const0> ;
  assign axis_rd_data_count[10] = \<const0> ;
  assign axis_rd_data_count[9] = \<const0> ;
  assign axis_rd_data_count[8] = \<const0> ;
  assign axis_rd_data_count[7] = \<const0> ;
  assign axis_rd_data_count[6] = \<const0> ;
  assign axis_rd_data_count[5] = \<const0> ;
  assign axis_rd_data_count[4] = \<const0> ;
  assign axis_rd_data_count[3] = \<const0> ;
  assign axis_rd_data_count[2] = \<const0> ;
  assign axis_rd_data_count[1] = \<const0> ;
  assign axis_rd_data_count[0] = \<const0> ;
  assign axis_sbiterr = \<const0> ;
  assign axis_underflow = \<const0> ;
  assign axis_wr_data_count[10] = \<const0> ;
  assign axis_wr_data_count[9] = \<const0> ;
  assign axis_wr_data_count[8] = \<const0> ;
  assign axis_wr_data_count[7] = \<const0> ;
  assign axis_wr_data_count[6] = \<const0> ;
  assign axis_wr_data_count[5] = \<const0> ;
  assign axis_wr_data_count[4] = \<const0> ;
  assign axis_wr_data_count[3] = \<const0> ;
  assign axis_wr_data_count[2] = \<const0> ;
  assign axis_wr_data_count[1] = \<const0> ;
  assign axis_wr_data_count[0] = \<const0> ;
  assign dbiterr = \<const0> ;
  assign m_axi_araddr[31] = \<const0> ;
  assign m_axi_araddr[30] = \<const0> ;
  assign m_axi_araddr[29] = \<const0> ;
  assign m_axi_araddr[28] = \<const0> ;
  assign m_axi_araddr[27] = \<const0> ;
  assign m_axi_araddr[26] = \<const0> ;
  assign m_axi_araddr[25] = \<const0> ;
  assign m_axi_araddr[24] = \<const0> ;
  assign m_axi_araddr[23] = \<const0> ;
  assign m_axi_araddr[22] = \<const0> ;
  assign m_axi_araddr[21] = \<const0> ;
  assign m_axi_araddr[20] = \<const0> ;
  assign m_axi_araddr[19] = \<const0> ;
  assign m_axi_araddr[18] = \<const0> ;
  assign m_axi_araddr[17] = \<const0> ;
  assign m_axi_araddr[16] = \<const0> ;
  assign m_axi_araddr[15] = \<const0> ;
  assign m_axi_araddr[14] = \<const0> ;
  assign m_axi_araddr[13] = \<const0> ;
  assign m_axi_araddr[12] = \<const0> ;
  assign m_axi_araddr[11] = \<const0> ;
  assign m_axi_araddr[10] = \<const0> ;
  assign m_axi_araddr[9] = \<const0> ;
  assign m_axi_araddr[8] = \<const0> ;
  assign m_axi_araddr[7] = \<const0> ;
  assign m_axi_araddr[6] = \<const0> ;
  assign m_axi_araddr[5] = \<const0> ;
  assign m_axi_araddr[4] = \<const0> ;
  assign m_axi_araddr[3] = \<const0> ;
  assign m_axi_araddr[2] = \<const0> ;
  assign m_axi_araddr[1] = \<const0> ;
  assign m_axi_araddr[0] = \<const0> ;
  assign m_axi_arburst[1] = \<const0> ;
  assign m_axi_arburst[0] = \<const0> ;
  assign m_axi_arcache[3] = \<const0> ;
  assign m_axi_arcache[2] = \<const0> ;
  assign m_axi_arcache[1] = \<const0> ;
  assign m_axi_arcache[0] = \<const0> ;
  assign m_axi_arid[0] = \<const0> ;
  assign m_axi_arlen[7] = \<const0> ;
  assign m_axi_arlen[6] = \<const0> ;
  assign m_axi_arlen[5] = \<const0> ;
  assign m_axi_arlen[4] = \<const0> ;
  assign m_axi_arlen[3] = \<const0> ;
  assign m_axi_arlen[2] = \<const0> ;
  assign m_axi_arlen[1] = \<const0> ;
  assign m_axi_arlen[0] = \<const0> ;
  assign m_axi_arlock[0] = \<const0> ;
  assign m_axi_arprot[2] = \<const0> ;
  assign m_axi_arprot[1] = \<const0> ;
  assign m_axi_arprot[0] = \<const0> ;
  assign m_axi_arqos[3] = \<const0> ;
  assign m_axi_arqos[2] = \<const0> ;
  assign m_axi_arqos[1] = \<const0> ;
  assign m_axi_arqos[0] = \<const0> ;
  assign m_axi_arregion[3] = \<const0> ;
  assign m_axi_arregion[2] = \<const0> ;
  assign m_axi_arregion[1] = \<const0> ;
  assign m_axi_arregion[0] = \<const0> ;
  assign m_axi_arsize[2] = \<const0> ;
  assign m_axi_arsize[1] = \<const0> ;
  assign m_axi_arsize[0] = \<const0> ;
  assign m_axi_aruser[0] = \<const0> ;
  assign m_axi_arvalid = \<const0> ;
  assign m_axi_awaddr[31] = \<const0> ;
  assign m_axi_awaddr[30] = \<const0> ;
  assign m_axi_awaddr[29] = \<const0> ;
  assign m_axi_awaddr[28] = \<const0> ;
  assign m_axi_awaddr[27] = \<const0> ;
  assign m_axi_awaddr[26] = \<const0> ;
  assign m_axi_awaddr[25] = \<const0> ;
  assign m_axi_awaddr[24] = \<const0> ;
  assign m_axi_awaddr[23] = \<const0> ;
  assign m_axi_awaddr[22] = \<const0> ;
  assign m_axi_awaddr[21] = \<const0> ;
  assign m_axi_awaddr[20] = \<const0> ;
  assign m_axi_awaddr[19] = \<const0> ;
  assign m_axi_awaddr[18] = \<const0> ;
  assign m_axi_awaddr[17] = \<const0> ;
  assign m_axi_awaddr[16] = \<const0> ;
  assign m_axi_awaddr[15] = \<const0> ;
  assign m_axi_awaddr[14] = \<const0> ;
  assign m_axi_awaddr[13] = \<const0> ;
  assign m_axi_awaddr[12] = \<const0> ;
  assign m_axi_awaddr[11] = \<const0> ;
  assign m_axi_awaddr[10] = \<const0> ;
  assign m_axi_awaddr[9] = \<const0> ;
  assign m_axi_awaddr[8] = \<const0> ;
  assign m_axi_awaddr[7] = \<const0> ;
  assign m_axi_awaddr[6] = \<const0> ;
  assign m_axi_awaddr[5] = \<const0> ;
  assign m_axi_awaddr[4] = \<const0> ;
  assign m_axi_awaddr[3] = \<const0> ;
  assign m_axi_awaddr[2] = \<const0> ;
  assign m_axi_awaddr[1] = \<const0> ;
  assign m_axi_awaddr[0] = \<const0> ;
  assign m_axi_awburst[1] = \<const0> ;
  assign m_axi_awburst[0] = \<const0> ;
  assign m_axi_awcache[3] = \<const0> ;
  assign m_axi_awcache[2] = \<const0> ;
  assign m_axi_awcache[1] = \<const0> ;
  assign m_axi_awcache[0] = \<const0> ;
  assign m_axi_awid[0] = \<const0> ;
  assign m_axi_awlen[7] = \<const0> ;
  assign m_axi_awlen[6] = \<const0> ;
  assign m_axi_awlen[5] = \<const0> ;
  assign m_axi_awlen[4] = \<const0> ;
  assign m_axi_awlen[3] = \<const0> ;
  assign m_axi_awlen[2] = \<const0> ;
  assign m_axi_awlen[1] = \<const0> ;
  assign m_axi_awlen[0] = \<const0> ;
  assign m_axi_awlock[0] = \<const0> ;
  assign m_axi_awprot[2] = \<const0> ;
  assign m_axi_awprot[1] = \<const0> ;
  assign m_axi_awprot[0] = \<const0> ;
  assign m_axi_awqos[3] = \<const0> ;
  assign m_axi_awqos[2] = \<const0> ;
  assign m_axi_awqos[1] = \<const0> ;
  assign m_axi_awqos[0] = \<const0> ;
  assign m_axi_awregion[3] = \<const0> ;
  assign m_axi_awregion[2] = \<const0> ;
  assign m_axi_awregion[1] = \<const0> ;
  assign m_axi_awregion[0] = \<const0> ;
  assign m_axi_awsize[2] = \<const0> ;
  assign m_axi_awsize[1] = \<const0> ;
  assign m_axi_awsize[0] = \<const0> ;
  assign m_axi_awuser[0] = \<const0> ;
  assign m_axi_awvalid = \<const0> ;
  assign m_axi_bready = \<const0> ;
  assign m_axi_rready = \<const0> ;
  assign m_axi_wdata[63] = \<const0> ;
  assign m_axi_wdata[62] = \<const0> ;
  assign m_axi_wdata[61] = \<const0> ;
  assign m_axi_wdata[60] = \<const0> ;
  assign m_axi_wdata[59] = \<const0> ;
  assign m_axi_wdata[58] = \<const0> ;
  assign m_axi_wdata[57] = \<const0> ;
  assign m_axi_wdata[56] = \<const0> ;
  assign m_axi_wdata[55] = \<const0> ;
  assign m_axi_wdata[54] = \<const0> ;
  assign m_axi_wdata[53] = \<const0> ;
  assign m_axi_wdata[52] = \<const0> ;
  assign m_axi_wdata[51] = \<const0> ;
  assign m_axi_wdata[50] = \<const0> ;
  assign m_axi_wdata[49] = \<const0> ;
  assign m_axi_wdata[48] = \<const0> ;
  assign m_axi_wdata[47] = \<const0> ;
  assign m_axi_wdata[46] = \<const0> ;
  assign m_axi_wdata[45] = \<const0> ;
  assign m_axi_wdata[44] = \<const0> ;
  assign m_axi_wdata[43] = \<const0> ;
  assign m_axi_wdata[42] = \<const0> ;
  assign m_axi_wdata[41] = \<const0> ;
  assign m_axi_wdata[40] = \<const0> ;
  assign m_axi_wdata[39] = \<const0> ;
  assign m_axi_wdata[38] = \<const0> ;
  assign m_axi_wdata[37] = \<const0> ;
  assign m_axi_wdata[36] = \<const0> ;
  assign m_axi_wdata[35] = \<const0> ;
  assign m_axi_wdata[34] = \<const0> ;
  assign m_axi_wdata[33] = \<const0> ;
  assign m_axi_wdata[32] = \<const0> ;
  assign m_axi_wdata[31] = \<const0> ;
  assign m_axi_wdata[30] = \<const0> ;
  assign m_axi_wdata[29] = \<const0> ;
  assign m_axi_wdata[28] = \<const0> ;
  assign m_axi_wdata[27] = \<const0> ;
  assign m_axi_wdata[26] = \<const0> ;
  assign m_axi_wdata[25] = \<const0> ;
  assign m_axi_wdata[24] = \<const0> ;
  assign m_axi_wdata[23] = \<const0> ;
  assign m_axi_wdata[22] = \<const0> ;
  assign m_axi_wdata[21] = \<const0> ;
  assign m_axi_wdata[20] = \<const0> ;
  assign m_axi_wdata[19] = \<const0> ;
  assign m_axi_wdata[18] = \<const0> ;
  assign m_axi_wdata[17] = \<const0> ;
  assign m_axi_wdata[16] = \<const0> ;
  assign m_axi_wdata[15] = \<const0> ;
  assign m_axi_wdata[14] = \<const0> ;
  assign m_axi_wdata[13] = \<const0> ;
  assign m_axi_wdata[12] = \<const0> ;
  assign m_axi_wdata[11] = \<const0> ;
  assign m_axi_wdata[10] = \<const0> ;
  assign m_axi_wdata[9] = \<const0> ;
  assign m_axi_wdata[8] = \<const0> ;
  assign m_axi_wdata[7] = \<const0> ;
  assign m_axi_wdata[6] = \<const0> ;
  assign m_axi_wdata[5] = \<const0> ;
  assign m_axi_wdata[4] = \<const0> ;
  assign m_axi_wdata[3] = \<const0> ;
  assign m_axi_wdata[2] = \<const0> ;
  assign m_axi_wdata[1] = \<const0> ;
  assign m_axi_wdata[0] = \<const0> ;
  assign m_axi_wid[0] = \<const0> ;
  assign m_axi_wlast = \<const0> ;
  assign m_axi_wstrb[7] = \<const0> ;
  assign m_axi_wstrb[6] = \<const0> ;
  assign m_axi_wstrb[5] = \<const0> ;
  assign m_axi_wstrb[4] = \<const0> ;
  assign m_axi_wstrb[3] = \<const0> ;
  assign m_axi_wstrb[2] = \<const0> ;
  assign m_axi_wstrb[1] = \<const0> ;
  assign m_axi_wstrb[0] = \<const0> ;
  assign m_axi_wuser[0] = \<const0> ;
  assign m_axi_wvalid = \<const0> ;
  assign m_axis_tdata[7] = \<const0> ;
  assign m_axis_tdata[6] = \<const0> ;
  assign m_axis_tdata[5] = \<const0> ;
  assign m_axis_tdata[4] = \<const0> ;
  assign m_axis_tdata[3] = \<const0> ;
  assign m_axis_tdata[2] = \<const0> ;
  assign m_axis_tdata[1] = \<const0> ;
  assign m_axis_tdata[0] = \<const0> ;
  assign m_axis_tdest[0] = \<const0> ;
  assign m_axis_tid[0] = \<const0> ;
  assign m_axis_tkeep[0] = \<const0> ;
  assign m_axis_tlast = \<const0> ;
  assign m_axis_tstrb[0] = \<const0> ;
  assign m_axis_tuser[3] = \<const0> ;
  assign m_axis_tuser[2] = \<const0> ;
  assign m_axis_tuser[1] = \<const0> ;
  assign m_axis_tuser[0] = \<const0> ;
  assign m_axis_tvalid = \<const0> ;
  assign overflow = \<const0> ;
  assign rd_data_count[6] = \<const0> ;
  assign rd_data_count[5] = \<const0> ;
  assign rd_data_count[4] = \<const0> ;
  assign rd_data_count[3] = \<const0> ;
  assign rd_data_count[2] = \<const0> ;
  assign rd_data_count[1] = \<const0> ;
  assign rd_data_count[0] = \<const0> ;
  assign rd_rst_busy = wr_rst_busy;
  assign s_axi_arready = \<const0> ;
  assign s_axi_awready = \<const0> ;
  assign s_axi_bid[0] = \<const0> ;
  assign s_axi_bresp[1] = \<const0> ;
  assign s_axi_bresp[0] = \<const0> ;
  assign s_axi_buser[0] = \<const0> ;
  assign s_axi_bvalid = \<const0> ;
  assign s_axi_rdata[63] = \<const0> ;
  assign s_axi_rdata[62] = \<const0> ;
  assign s_axi_rdata[61] = \<const0> ;
  assign s_axi_rdata[60] = \<const0> ;
  assign s_axi_rdata[59] = \<const0> ;
  assign s_axi_rdata[58] = \<const0> ;
  assign s_axi_rdata[57] = \<const0> ;
  assign s_axi_rdata[56] = \<const0> ;
  assign s_axi_rdata[55] = \<const0> ;
  assign s_axi_rdata[54] = \<const0> ;
  assign s_axi_rdata[53] = \<const0> ;
  assign s_axi_rdata[52] = \<const0> ;
  assign s_axi_rdata[51] = \<const0> ;
  assign s_axi_rdata[50] = \<const0> ;
  assign s_axi_rdata[49] = \<const0> ;
  assign s_axi_rdata[48] = \<const0> ;
  assign s_axi_rdata[47] = \<const0> ;
  assign s_axi_rdata[46] = \<const0> ;
  assign s_axi_rdata[45] = \<const0> ;
  assign s_axi_rdata[44] = \<const0> ;
  assign s_axi_rdata[43] = \<const0> ;
  assign s_axi_rdata[42] = \<const0> ;
  assign s_axi_rdata[41] = \<const0> ;
  assign s_axi_rdata[40] = \<const0> ;
  assign s_axi_rdata[39] = \<const0> ;
  assign s_axi_rdata[38] = \<const0> ;
  assign s_axi_rdata[37] = \<const0> ;
  assign s_axi_rdata[36] = \<const0> ;
  assign s_axi_rdata[35] = \<const0> ;
  assign s_axi_rdata[34] = \<const0> ;
  assign s_axi_rdata[33] = \<const0> ;
  assign s_axi_rdata[32] = \<const0> ;
  assign s_axi_rdata[31] = \<const0> ;
  assign s_axi_rdata[30] = \<const0> ;
  assign s_axi_rdata[29] = \<const0> ;
  assign s_axi_rdata[28] = \<const0> ;
  assign s_axi_rdata[27] = \<const0> ;
  assign s_axi_rdata[26] = \<const0> ;
  assign s_axi_rdata[25] = \<const0> ;
  assign s_axi_rdata[24] = \<const0> ;
  assign s_axi_rdata[23] = \<const0> ;
  assign s_axi_rdata[22] = \<const0> ;
  assign s_axi_rdata[21] = \<const0> ;
  assign s_axi_rdata[20] = \<const0> ;
  assign s_axi_rdata[19] = \<const0> ;
  assign s_axi_rdata[18] = \<const0> ;
  assign s_axi_rdata[17] = \<const0> ;
  assign s_axi_rdata[16] = \<const0> ;
  assign s_axi_rdata[15] = \<const0> ;
  assign s_axi_rdata[14] = \<const0> ;
  assign s_axi_rdata[13] = \<const0> ;
  assign s_axi_rdata[12] = \<const0> ;
  assign s_axi_rdata[11] = \<const0> ;
  assign s_axi_rdata[10] = \<const0> ;
  assign s_axi_rdata[9] = \<const0> ;
  assign s_axi_rdata[8] = \<const0> ;
  assign s_axi_rdata[7] = \<const0> ;
  assign s_axi_rdata[6] = \<const0> ;
  assign s_axi_rdata[5] = \<const0> ;
  assign s_axi_rdata[4] = \<const0> ;
  assign s_axi_rdata[3] = \<const0> ;
  assign s_axi_rdata[2] = \<const0> ;
  assign s_axi_rdata[1] = \<const0> ;
  assign s_axi_rdata[0] = \<const0> ;
  assign s_axi_rid[0] = \<const0> ;
  assign s_axi_rlast = \<const0> ;
  assign s_axi_rresp[1] = \<const0> ;
  assign s_axi_rresp[0] = \<const0> ;
  assign s_axi_ruser[0] = \<const0> ;
  assign s_axi_rvalid = \<const0> ;
  assign s_axi_wready = \<const0> ;
  assign s_axis_tready = \<const0> ;
  assign sbiterr = \<const0> ;
  assign underflow = \<const0> ;
  assign valid = \<const0> ;
  assign wr_ack = \<const0> ;
  assign wr_data_count[6] = \<const0> ;
  assign wr_data_count[5] = \<const0> ;
  assign wr_data_count[4] = \<const0> ;
  assign wr_data_count[3] = \<const0> ;
  assign wr_data_count[2] = \<const0> ;
  assign wr_data_count[1] = \<const0> ;
  assign wr_data_count[0] = \<const0> ;
  GND GND
       (.G(\<const0> ));
  VCC VCC
       (.P(\<const1> ));
  fifo_65_fifo_generator_v13_2_4_synth inst_fifo_gen
       (.almost_empty(almost_empty),
        .clk(clk),
        .data_count(data_count),
        .din(din),
        .dout(dout),
        .empty(empty),
        .full(full),
        .prog_empty(prog_empty),
        .prog_full(prog_full),
        .rd_en(rd_en),
        .srst(srst),
        .wr_en(wr_en),
        .wr_rst_reg_reg(wr_rst_busy));
endmodule

(* ORIG_REF_NAME = "fifo_generator_v13_2_4_synth" *) 
module fifo_65_fifo_generator_v13_2_4_synth
   (data_count,
    dout,
    almost_empty,
    empty,
    full,
    prog_empty,
    wr_rst_reg_reg,
    prog_full,
    rd_en,
    srst,
    clk,
    din,
    wr_en);
  output [6:0]data_count;
  output [64:0]dout;
  output almost_empty;
  output empty;
  output full;
  output prog_empty;
  output wr_rst_reg_reg;
  output prog_full;
  input rd_en;
  input srst;
  input clk;
  input [64:0]din;
  input wr_en;

  wire almost_empty;
  wire clk;
  wire [6:0]data_count;
  wire [64:0]din;
  wire [64:0]dout;
  wire empty;
  wire full;
  wire prog_empty;
  wire prog_full;
  wire rd_en;
  wire srst;
  wire wr_en;
  wire wr_rst_reg_reg;

  fifo_65_fifo_generator_top \gconvfifo.rf 
       (.DATA_COUNT(data_count),
        .almost_empty(almost_empty),
        .clk(clk),
        .din(din),
        .dout(dout),
        .empty(empty),
        .full(full),
        .prog_empty(prog_empty),
        .prog_full(prog_full),
        .rd_en(rd_en),
        .srst(srst),
        .wr_en(wr_en),
        .wr_rst_reg_reg(wr_rst_reg_reg));
endmodule

(* ORIG_REF_NAME = "memory" *) 
module fifo_65_memory
   (dout,
    clk,
    tmp_ram_rd_en,
    p_17_out,
    tmp_ram_regout_en,
    srst_full_ff_i,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ,
    din);
  output [64:0]dout;
  input clk;
  input tmp_ram_rd_en;
  input p_17_out;
  input tmp_ram_regout_en;
  input srst_full_ff_i;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  input [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  input [64:0]din;

  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  wire [5:0]\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  wire clk;
  wire [64:0]din;
  wire [64:0]dout;
  wire p_17_out;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;

  fifo_65_blk_mem_gen_v8_4_3 \gbm.gbmg.gbmgb.ngecc.bmg 
       (.\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ),
        .\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .clk(clk),
        .din(din),
        .dout(dout),
        .p_17_out(p_17_out),
        .srst_full_ff_i(srst_full_ff_i),
        .tmp_ram_rd_en(tmp_ram_rd_en),
        .tmp_ram_regout_en(tmp_ram_regout_en));
endmodule

(* ORIG_REF_NAME = "rd_bin_cntr" *) 
module fifo_65_rd_bin_cntr
   (D,
    \gc1.count_d2_reg[5]_0 ,
    \gcc0.gc0.count_reg[2] ,
    \gc1.count_d2_reg[0]_0 ,
    comp1,
    \gc1.count_d2_reg[0]_1 ,
    \gc1.count_d2_reg[4]_0 ,
    \gc1.count_d2_reg[4]_1 ,
    \greg.gpcry_sym.diff_pntr_pad_reg[6] ,
    p_17_out,
    E,
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ,
    srst_full_ff_i,
    clk);
  output [0:0]D;
  output [5:0]\gc1.count_d2_reg[5]_0 ;
  output [0:0]\gcc0.gc0.count_reg[2] ;
  output \gc1.count_d2_reg[0]_0 ;
  output comp1;
  output \gc1.count_d2_reg[0]_1 ;
  output \gc1.count_d2_reg[4]_0 ;
  output \gc1.count_d2_reg[4]_1 ;
  input [5:0]\greg.gpcry_sym.diff_pntr_pad_reg[6] ;
  input p_17_out;
  input [0:0]E;
  input [4:0]\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ;
  input srst_full_ff_i;
  input clk;

  wire [0:0]D;
  wire [0:0]E;
  wire clk;
  wire comp1;
  wire \gc1.count_d2_reg[0]_0 ;
  wire \gc1.count_d2_reg[0]_1 ;
  wire \gc1.count_d2_reg[4]_0 ;
  wire \gc1.count_d2_reg[4]_1 ;
  wire [5:0]\gc1.count_d2_reg[5]_0 ;
  wire [0:0]\gcc0.gc0.count_reg[2] ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad[3]_i_2_n_0 ;
  wire [4:0]\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ;
  wire \greg.gpcry_sym.diff_pntr_pad[3]_i_2_n_0 ;
  wire [5:0]\greg.gpcry_sym.diff_pntr_pad_reg[6] ;
  wire p_17_out;
  wire [5:0]plusOp__0;
  wire ram_empty_fb_i_i_3_n_0;
  wire ram_empty_fb_i_i_4_n_0;
  wire [5:0]rd_pntr_plus1;
  wire [5:0]rd_pntr_plus2;
  wire srst_full_ff_i;

  (* SOFT_HLUTNM = "soft_lutpair1" *) 
  LUT1 #(
    .INIT(2'h1)) 
    \gc1.count[0]_i_1 
       (.I0(rd_pntr_plus2[0]),
        .O(plusOp__0[0]));
  LUT2 #(
    .INIT(4'h6)) 
    \gc1.count[1]_i_1 
       (.I0(rd_pntr_plus2[0]),
        .I1(rd_pntr_plus2[1]),
        .O(plusOp__0[1]));
  (* SOFT_HLUTNM = "soft_lutpair1" *) 
  LUT3 #(
    .INIT(8'h78)) 
    \gc1.count[2]_i_1 
       (.I0(rd_pntr_plus2[0]),
        .I1(rd_pntr_plus2[1]),
        .I2(rd_pntr_plus2[2]),
        .O(plusOp__0[2]));
  (* SOFT_HLUTNM = "soft_lutpair0" *) 
  LUT4 #(
    .INIT(16'h7F80)) 
    \gc1.count[3]_i_1 
       (.I0(rd_pntr_plus2[1]),
        .I1(rd_pntr_plus2[0]),
        .I2(rd_pntr_plus2[2]),
        .I3(rd_pntr_plus2[3]),
        .O(plusOp__0[3]));
  (* SOFT_HLUTNM = "soft_lutpair0" *) 
  LUT5 #(
    .INIT(32'h7FFF8000)) 
    \gc1.count[4]_i_1 
       (.I0(rd_pntr_plus2[2]),
        .I1(rd_pntr_plus2[0]),
        .I2(rd_pntr_plus2[1]),
        .I3(rd_pntr_plus2[3]),
        .I4(rd_pntr_plus2[4]),
        .O(plusOp__0[4]));
  LUT6 #(
    .INIT(64'h7FFFFFFF80000000)) 
    \gc1.count[5]_i_1 
       (.I0(rd_pntr_plus2[3]),
        .I1(rd_pntr_plus2[1]),
        .I2(rd_pntr_plus2[0]),
        .I3(rd_pntr_plus2[2]),
        .I4(rd_pntr_plus2[4]),
        .I5(rd_pntr_plus2[5]),
        .O(plusOp__0[5]));
  FDSE #(
    .INIT(1'b1)) 
    \gc1.count_d1_reg[0] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus2[0]),
        .Q(rd_pntr_plus1[0]),
        .S(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d1_reg[1] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus2[1]),
        .Q(rd_pntr_plus1[1]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d1_reg[2] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus2[2]),
        .Q(rd_pntr_plus1[2]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d1_reg[3] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus2[3]),
        .Q(rd_pntr_plus1[3]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d1_reg[4] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus2[4]),
        .Q(rd_pntr_plus1[4]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d1_reg[5] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus2[5]),
        .Q(rd_pntr_plus1[5]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d2_reg[0] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus1[0]),
        .Q(\gc1.count_d2_reg[5]_0 [0]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d2_reg[1] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus1[1]),
        .Q(\gc1.count_d2_reg[5]_0 [1]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d2_reg[2] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus1[2]),
        .Q(\gc1.count_d2_reg[5]_0 [2]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d2_reg[3] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus1[3]),
        .Q(\gc1.count_d2_reg[5]_0 [3]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d2_reg[4] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus1[4]),
        .Q(\gc1.count_d2_reg[5]_0 [4]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_d2_reg[5] 
       (.C(clk),
        .CE(E),
        .D(rd_pntr_plus1[5]),
        .Q(\gc1.count_d2_reg[5]_0 [5]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_reg[0] 
       (.C(clk),
        .CE(E),
        .D(plusOp__0[0]),
        .Q(rd_pntr_plus2[0]),
        .R(srst_full_ff_i));
  FDSE #(
    .INIT(1'b1)) 
    \gc1.count_reg[1] 
       (.C(clk),
        .CE(E),
        .D(plusOp__0[1]),
        .Q(rd_pntr_plus2[1]),
        .S(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_reg[2] 
       (.C(clk),
        .CE(E),
        .D(plusOp__0[2]),
        .Q(rd_pntr_plus2[2]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_reg[3] 
       (.C(clk),
        .CE(E),
        .D(plusOp__0[3]),
        .Q(rd_pntr_plus2[3]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_reg[4] 
       (.C(clk),
        .CE(E),
        .D(plusOp__0[4]),
        .Q(rd_pntr_plus2[4]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gc1.count_reg[5] 
       (.C(clk),
        .CE(E),
        .D(plusOp__0[5]),
        .Q(rd_pntr_plus2[5]),
        .R(srst_full_ff_i));
  LUT5 #(
    .INIT(32'h69699669)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[3]_i_1 
       (.I0(\gdiff.gcry_1_sym.diff_pntr_pad[3]_i_2_n_0 ),
        .I1(\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] [2]),
        .I2(\gc1.count_d2_reg[5]_0 [2]),
        .I3(\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] [1]),
        .I4(\gc1.count_d2_reg[5]_0 [1]),
        .O(\gcc0.gc0.count_reg[2] ));
  LUT6 #(
    .INIT(64'h0000900090909990)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[3]_i_2 
       (.I0(\gc1.count_d2_reg[5]_0 [1]),
        .I1(\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] [1]),
        .I2(\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] [0]),
        .I3(p_17_out),
        .I4(E),
        .I5(\gc1.count_d2_reg[5]_0 [0]),
        .O(\gdiff.gcry_1_sym.diff_pntr_pad[3]_i_2_n_0 ));
  LUT4 #(
    .INIT(16'hB44B)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_5 
       (.I0(\gc1.count_d2_reg[5]_0 [4]),
        .I1(\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] [3]),
        .I2(\gc1.count_d2_reg[5]_0 [5]),
        .I3(\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] [4]),
        .O(\gc1.count_d2_reg[4]_1 ));
  LUT5 #(
    .INIT(32'h69699669)) 
    \greg.gpcry_sym.diff_pntr_pad[3]_i_1 
       (.I0(\greg.gpcry_sym.diff_pntr_pad[3]_i_2_n_0 ),
        .I1(\greg.gpcry_sym.diff_pntr_pad_reg[6] [2]),
        .I2(\gc1.count_d2_reg[5]_0 [2]),
        .I3(\greg.gpcry_sym.diff_pntr_pad_reg[6] [1]),
        .I4(\gc1.count_d2_reg[5]_0 [1]),
        .O(D));
  LUT6 #(
    .INIT(64'h9000909099909999)) 
    \greg.gpcry_sym.diff_pntr_pad[3]_i_2 
       (.I0(\gc1.count_d2_reg[5]_0 [1]),
        .I1(\greg.gpcry_sym.diff_pntr_pad_reg[6] [1]),
        .I2(\greg.gpcry_sym.diff_pntr_pad_reg[6] [0]),
        .I3(p_17_out),
        .I4(E),
        .I5(\gc1.count_d2_reg[5]_0 [0]),
        .O(\greg.gpcry_sym.diff_pntr_pad[3]_i_2_n_0 ));
  LUT4 #(
    .INIT(16'hB44B)) 
    \greg.gpcry_sym.diff_pntr_pad[6]_i_5 
       (.I0(\gc1.count_d2_reg[5]_0 [4]),
        .I1(\greg.gpcry_sym.diff_pntr_pad_reg[6] [4]),
        .I2(\gc1.count_d2_reg[5]_0 [5]),
        .I3(\greg.gpcry_sym.diff_pntr_pad_reg[6] [5]),
        .O(\gc1.count_d2_reg[4]_0 ));
  LUT6 #(
    .INIT(64'h9009000000000000)) 
    ram_empty_fb_i_i_2
       (.I0(\greg.gpcry_sym.diff_pntr_pad_reg[6] [1]),
        .I1(rd_pntr_plus1[1]),
        .I2(\greg.gpcry_sym.diff_pntr_pad_reg[6] [0]),
        .I3(rd_pntr_plus1[0]),
        .I4(ram_empty_fb_i_i_3_n_0),
        .I5(ram_empty_fb_i_i_4_n_0),
        .O(comp1));
  LUT4 #(
    .INIT(16'h9009)) 
    ram_empty_fb_i_i_3
       (.I0(rd_pntr_plus1[4]),
        .I1(\greg.gpcry_sym.diff_pntr_pad_reg[6] [4]),
        .I2(rd_pntr_plus1[5]),
        .I3(\greg.gpcry_sym.diff_pntr_pad_reg[6] [5]),
        .O(ram_empty_fb_i_i_3_n_0));
  LUT4 #(
    .INIT(16'h9009)) 
    ram_empty_fb_i_i_4
       (.I0(rd_pntr_plus1[2]),
        .I1(\greg.gpcry_sym.diff_pntr_pad_reg[6] [2]),
        .I2(rd_pntr_plus1[3]),
        .I3(\greg.gpcry_sym.diff_pntr_pad_reg[6] [3]),
        .O(ram_empty_fb_i_i_4_n_0));
  LUT4 #(
    .INIT(16'h9009)) 
    ram_full_fb_i_i_2
       (.I0(\gc1.count_d2_reg[5]_0 [0]),
        .I1(\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] [0]),
        .I2(\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] [1]),
        .I3(\gc1.count_d2_reg[5]_0 [1]),
        .O(\gc1.count_d2_reg[0]_1 ));
  LUT4 #(
    .INIT(16'h9009)) 
    ram_full_fb_i_i_6
       (.I0(\gc1.count_d2_reg[5]_0 [0]),
        .I1(\greg.gpcry_sym.diff_pntr_pad_reg[6] [0]),
        .I2(\greg.gpcry_sym.diff_pntr_pad_reg[6] [1]),
        .I3(\gc1.count_d2_reg[5]_0 [1]),
        .O(\gc1.count_d2_reg[0]_0 ));
endmodule

(* ORIG_REF_NAME = "rd_fwft" *) 
module fifo_65_rd_fwft
   (almost_empty,
    empty,
    out,
    tmp_ram_regout_en,
    tmp_ram_rd_en,
    ram_empty_i0__3,
    E,
    rd_pntr_inv_pad,
    p_1_out__0,
    srst_full_ff_i,
    clk,
    rd_en,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ,
    srst,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ,
    comp1,
    comp0,
    ram_empty_fb_i_reg,
    wr_en);
  output almost_empty;
  output empty;
  output out;
  output tmp_ram_regout_en;
  output tmp_ram_rd_en;
  output ram_empty_i0__3;
  output [0:0]E;
  output [0:0]rd_pntr_inv_pad;
  output p_1_out__0;
  input srst_full_ff_i;
  input clk;
  input rd_en;
  input \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  input srst;
  input \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  input comp1;
  input comp0;
  input ram_empty_fb_i_reg;
  input wr_en;

  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ;
  wire [0:0]E;
  (* DONT_TOUCH *) wire aempty_fwft_fb_i;
  (* DONT_TOUCH *) wire aempty_fwft_i;
  wire aempty_fwft_i0__1;
  wire clk;
  wire comp0;
  wire comp1;
  (* DONT_TOUCH *) wire [1:0]curr_fwft_state;
  (* DONT_TOUCH *) wire empty_fwft_fb_i;
  (* DONT_TOUCH *) wire empty_fwft_fb_o_i;
  wire empty_fwft_fb_o_i_reg0;
  (* DONT_TOUCH *) wire empty_fwft_i;
  wire empty_fwft_i0__1;
  wire [1:0]next_fwft_state;
  wire p_1_out__0;
  wire ram_empty_fb_i_reg;
  wire ram_empty_i0__3;
  wire rd_en;
  wire [0:0]rd_pntr_inv_pad;
  wire srst;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;
  (* DONT_TOUCH *) wire user_valid;
  wire wr_en;

  assign almost_empty = aempty_fwft_i;
  assign empty = empty_fwft_i;
  assign out = user_valid;
  LUT6 #(
    .INIT(64'hFFFFFFFFFFFF4555)) 
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_i_1 
       (.I0(\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .I1(rd_en),
        .I2(curr_fwft_state[1]),
        .I3(curr_fwft_state[0]),
        .I4(\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ),
        .I5(srst),
        .O(tmp_ram_rd_en));
  LUT5 #(
    .INIT(32'hFFFFFFB0)) 
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_i_3 
       (.I0(rd_en),
        .I1(curr_fwft_state[0]),
        .I2(curr_fwft_state[1]),
        .I3(\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ),
        .I4(srst),
        .O(tmp_ram_regout_en));
  LUT5 #(
    .INIT(32'hFFCB8000)) 
    aempty_fwft_fb_i_i_1
       (.I0(rd_en),
        .I1(curr_fwft_state[0]),
        .I2(curr_fwft_state[1]),
        .I3(\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .I4(aempty_fwft_fb_i),
        .O(aempty_fwft_i0__1));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDSE #(
    .INIT(1'b1)) 
    aempty_fwft_fb_i_reg
       (.C(clk),
        .CE(1'b1),
        .D(aempty_fwft_i0__1),
        .Q(aempty_fwft_fb_i),
        .S(srst_full_ff_i));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDSE #(
    .INIT(1'b1)) 
    aempty_fwft_i_reg
       (.C(clk),
        .CE(1'b1),
        .D(aempty_fwft_i0__1),
        .Q(aempty_fwft_i),
        .S(srst_full_ff_i));
  LUT4 #(
    .INIT(16'hF320)) 
    empty_fwft_fb_i_i_1
       (.I0(rd_en),
        .I1(curr_fwft_state[1]),
        .I2(curr_fwft_state[0]),
        .I3(empty_fwft_fb_i),
        .O(empty_fwft_i0__1));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDSE #(
    .INIT(1'b1)) 
    empty_fwft_fb_i_reg
       (.C(clk),
        .CE(1'b1),
        .D(empty_fwft_i0__1),
        .Q(empty_fwft_fb_i),
        .S(srst_full_ff_i));
  LUT4 #(
    .INIT(16'hF320)) 
    empty_fwft_fb_o_i_i_1
       (.I0(rd_en),
        .I1(curr_fwft_state[1]),
        .I2(curr_fwft_state[0]),
        .I3(empty_fwft_fb_o_i),
        .O(empty_fwft_fb_o_i_reg0));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDSE #(
    .INIT(1'b1)) 
    empty_fwft_fb_o_i_reg
       (.C(clk),
        .CE(1'b1),
        .D(empty_fwft_fb_o_i_reg0),
        .Q(empty_fwft_fb_o_i),
        .S(srst_full_ff_i));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDSE #(
    .INIT(1'b1)) 
    empty_fwft_i_reg
       (.C(clk),
        .CE(1'b1),
        .D(empty_fwft_i0__1),
        .Q(empty_fwft_i),
        .S(srst_full_ff_i));
  LUT6 #(
    .INIT(64'h4444444400004000)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_7 
       (.I0(ram_empty_fb_i_reg),
        .I1(wr_en),
        .I2(curr_fwft_state[0]),
        .I3(curr_fwft_state[1]),
        .I4(rd_en),
        .I5(\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .O(p_1_out__0));
  LUT3 #(
    .INIT(8'hBA)) 
    \gpregsm1.curr_fwft_state[0]_i_1 
       (.I0(curr_fwft_state[1]),
        .I1(rd_en),
        .I2(curr_fwft_state[0]),
        .O(next_fwft_state[0]));
  LUT4 #(
    .INIT(16'h20FF)) 
    \gpregsm1.curr_fwft_state[1]_i_1 
       (.I0(curr_fwft_state[1]),
        .I1(rd_en),
        .I2(curr_fwft_state[0]),
        .I3(\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .O(next_fwft_state[1]));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDRE #(
    .INIT(1'b0)) 
    \gpregsm1.curr_fwft_state_reg[0] 
       (.C(clk),
        .CE(1'b1),
        .D(next_fwft_state[0]),
        .Q(curr_fwft_state[0]),
        .R(srst_full_ff_i));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDRE #(
    .INIT(1'b0)) 
    \gpregsm1.curr_fwft_state_reg[1] 
       (.C(clk),
        .CE(1'b1),
        .D(next_fwft_state[1]),
        .Q(curr_fwft_state[1]),
        .R(srst_full_ff_i));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDRE #(
    .INIT(1'b0)) 
    \gpregsm1.user_valid_reg 
       (.C(clk),
        .CE(1'b1),
        .D(next_fwft_state[0]),
        .Q(user_valid),
        .R(srst_full_ff_i));
  LUT6 #(
    .INIT(64'hFFFFFFFF4444F444)) 
    \greg.gpcry_sym.diff_pntr_pad[6]_i_7 
       (.I0(ram_empty_fb_i_reg),
        .I1(wr_en),
        .I2(curr_fwft_state[0]),
        .I3(curr_fwft_state[1]),
        .I4(rd_en),
        .I5(\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .O(rd_pntr_inv_pad));
  LUT4 #(
    .INIT(16'h4555)) 
    \greg.ram_rd_en_i_i_1 
       (.I0(\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .I1(rd_en),
        .I2(curr_fwft_state[1]),
        .I3(curr_fwft_state[0]),
        .O(E));
  LUT6 #(
    .INIT(64'hFF0FFFFF88008888)) 
    ram_empty_fb_i_i_1
       (.I0(E),
        .I1(comp1),
        .I2(comp0),
        .I3(ram_empty_fb_i_reg),
        .I4(wr_en),
        .I5(\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 ),
        .O(ram_empty_i0__3));
endmodule

(* ORIG_REF_NAME = "rd_logic" *) 
module fifo_65_rd_logic
   (almost_empty,
    empty,
    out,
    p_7_out,
    prog_empty,
    Q,
    tmp_ram_regout_en,
    tmp_ram_rd_en,
    \gc1.count_d2_reg[5] ,
    rd_pntr_inv_pad,
    \gcc0.gc0.count_reg[2] ,
    p_1_out__0,
    \gc1.count_d2_reg[0] ,
    \gc1.count_d2_reg[0]_0 ,
    \gc1.count_d2_reg[4] ,
    \gc1.count_d2_reg[4]_0 ,
    \greg.ram_rd_en_i_reg ,
    srst_full_ff_i,
    clk,
    p_17_out,
    rd_en,
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ,
    srst,
    D,
    \greg.gpcry_sym.diff_pntr_pad_reg[6] ,
    comp0,
    ram_empty_fb_i_reg,
    wr_en,
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ,
    eqOp__4,
    prog_full,
    E);
  output almost_empty;
  output empty;
  output out;
  output p_7_out;
  output prog_empty;
  output [6:0]Q;
  output tmp_ram_regout_en;
  output tmp_ram_rd_en;
  output [5:0]\gc1.count_d2_reg[5] ;
  output [0:0]rd_pntr_inv_pad;
  output [0:0]\gcc0.gc0.count_reg[2] ;
  output p_1_out__0;
  output \gc1.count_d2_reg[0] ;
  output \gc1.count_d2_reg[0]_0 ;
  output \gc1.count_d2_reg[4] ;
  output \gc1.count_d2_reg[4]_0 ;
  output \greg.ram_rd_en_i_reg ;
  input srst_full_ff_i;
  input clk;
  input p_17_out;
  input rd_en;
  input \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  input srst;
  input [4:0]D;
  input [5:0]\greg.gpcry_sym.diff_pntr_pad_reg[6] ;
  input comp0;
  input ram_empty_fb_i_reg;
  input wr_en;
  input [4:0]\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ;
  input eqOp__4;
  input prog_full;
  input [0:0]E;

  wire [4:0]D;
  wire \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ;
  wire [0:0]E;
  wire [6:0]Q;
  wire almost_empty;
  wire clk;
  wire comp0;
  wire comp1;
  wire empty;
  wire eqOp__4;
  wire \gc1.count_d2_reg[0] ;
  wire \gc1.count_d2_reg[0]_0 ;
  wire \gc1.count_d2_reg[4] ;
  wire \gc1.count_d2_reg[4]_0 ;
  wire [5:0]\gc1.count_d2_reg[5] ;
  wire [0:0]\gcc0.gc0.count_reg[2] ;
  wire [4:0]\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ;
  wire [5:0]\greg.gpcry_sym.diff_pntr_pad_reg[6] ;
  wire \greg.ram_rd_en_i_reg ;
  wire out;
  wire p_17_out;
  wire p_1_out__0;
  wire p_2_out;
  wire p_7_out;
  wire [3:3]plusOp;
  wire prog_empty;
  wire prog_full;
  wire ram_empty_fb_i_reg;
  wire ram_empty_i0__3;
  wire rd_en;
  wire [0:0]rd_pntr_inv_pad;
  wire srst;
  wire srst_full_ff_i;
  wire tmp_ram_rd_en;
  wire tmp_ram_regout_en;
  wire wr_en;

  fifo_65_dc_ss_fwft \gr1.gdcf.dc 
       (.E(E),
        .Q(Q),
        .clk(clk),
        .out(out),
        .rd_en(rd_en),
        .srst_full_ff_i(srst_full_ff_i));
  fifo_65_rd_fwft \gr1.gr1_int.rfwft 
       (.\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram (\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram ),
        .\DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_0 (p_2_out),
        .E(p_7_out),
        .almost_empty(almost_empty),
        .clk(clk),
        .comp0(comp0),
        .comp1(comp1),
        .empty(empty),
        .out(out),
        .p_1_out__0(p_1_out__0),
        .ram_empty_fb_i_reg(ram_empty_fb_i_reg),
        .ram_empty_i0__3(ram_empty_i0__3),
        .rd_en(rd_en),
        .rd_pntr_inv_pad(rd_pntr_inv_pad),
        .srst(srst),
        .srst_full_ff_i(srst_full_ff_i),
        .tmp_ram_rd_en(tmp_ram_rd_en),
        .tmp_ram_regout_en(tmp_ram_regout_en),
        .wr_en(wr_en));
  fifo_65_rd_pe_ss \grss.gpe.rdpe 
       (.D({D[4:2],plusOp,D[1:0]}),
        .E(p_7_out),
        .clk(clk),
        .eqOp__4(eqOp__4),
        .\greg.ram_rd_en_i_reg_0 (\greg.ram_rd_en_i_reg ),
        .p_17_out(p_17_out),
        .prog_empty(prog_empty),
        .prog_full(prog_full),
        .srst_full_ff_i(srst_full_ff_i));
  fifo_65_rd_status_flags_ss \grss.rsts 
       (.clk(clk),
        .out(p_2_out),
        .ram_empty_i0__3(ram_empty_i0__3),
        .srst_full_ff_i(srst_full_ff_i));
  fifo_65_rd_bin_cntr rpntr
       (.D(plusOp),
        .E(p_7_out),
        .clk(clk),
        .comp1(comp1),
        .\gc1.count_d2_reg[0]_0 (\gc1.count_d2_reg[0] ),
        .\gc1.count_d2_reg[0]_1 (\gc1.count_d2_reg[0]_0 ),
        .\gc1.count_d2_reg[4]_0 (\gc1.count_d2_reg[4] ),
        .\gc1.count_d2_reg[4]_1 (\gc1.count_d2_reg[4]_0 ),
        .\gc1.count_d2_reg[5]_0 (\gc1.count_d2_reg[5] ),
        .\gcc0.gc0.count_reg[2] (\gcc0.gc0.count_reg[2] ),
        .\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] (\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ),
        .\greg.gpcry_sym.diff_pntr_pad_reg[6] (\greg.gpcry_sym.diff_pntr_pad_reg[6] ),
        .p_17_out(p_17_out),
        .srst_full_ff_i(srst_full_ff_i));
endmodule

(* ORIG_REF_NAME = "rd_pe_ss" *) 
module fifo_65_rd_pe_ss
   (prog_empty,
    \greg.ram_rd_en_i_reg_0 ,
    srst_full_ff_i,
    E,
    clk,
    p_17_out,
    eqOp__4,
    prog_full,
    D);
  output prog_empty;
  output \greg.ram_rd_en_i_reg_0 ;
  input srst_full_ff_i;
  input [0:0]E;
  input clk;
  input p_17_out;
  input eqOp__4;
  input prog_full;
  input [5:0]D;

  wire [5:0]D;
  wire [0:0]E;
  wire clk;
  wire [6:1]diff_pntr_pad;
  wire eqOp;
  wire eqOp5_in;
  wire eqOp__4;
  wire \gntv_or_sync_fifo.gl0.wr/gwss.gpf.wrpf/ram_rd_en_i ;
  wire \gntv_or_sync_fifo.gl0.wr/gwss.gpf.wrpf/ram_wr_en_i ;
  wire \gpe2.prog_empty_i_i_1_n_0 ;
  wire \greg.ram_rd_en_i_reg_0 ;
  wire p_17_out;
  wire prog_empty;
  wire prog_full;
  wire srst_full_ff_i;

  LUT6 #(
    .INIT(64'hFFFFFFFFCCFC44CC)) 
    \gpe2.prog_empty_i_i_1 
       (.I0(eqOp),
        .I1(prog_empty),
        .I2(eqOp5_in),
        .I3(\gntv_or_sync_fifo.gl0.wr/gwss.gpf.wrpf/ram_wr_en_i ),
        .I4(\gntv_or_sync_fifo.gl0.wr/gwss.gpf.wrpf/ram_rd_en_i ),
        .I5(srst_full_ff_i),
        .O(\gpe2.prog_empty_i_i_1_n_0 ));
  LUT6 #(
    .INIT(64'h0000000000001000)) 
    \gpe2.prog_empty_i_i_2 
       (.I0(diff_pntr_pad[6]),
        .I1(diff_pntr_pad[5]),
        .I2(diff_pntr_pad[3]),
        .I3(diff_pntr_pad[1]),
        .I4(diff_pntr_pad[4]),
        .I5(diff_pntr_pad[2]),
        .O(eqOp));
  LUT6 #(
    .INIT(64'h0000000000000100)) 
    \gpe2.prog_empty_i_i_3 
       (.I0(diff_pntr_pad[6]),
        .I1(diff_pntr_pad[5]),
        .I2(diff_pntr_pad[2]),
        .I3(diff_pntr_pad[3]),
        .I4(diff_pntr_pad[4]),
        .I5(diff_pntr_pad[1]),
        .O(eqOp5_in));
  FDRE #(
    .INIT(1'b1)) 
    \gpe2.prog_empty_i_reg 
       (.C(clk),
        .CE(1'b1),
        .D(\gpe2.prog_empty_i_i_1_n_0 ),
        .Q(prog_empty),
        .R(1'b0));
  LUT4 #(
    .INIT(16'hDF40)) 
    \gpfs.prog_full_i_i_1 
       (.I0(\gntv_or_sync_fifo.gl0.wr/gwss.gpf.wrpf/ram_rd_en_i ),
        .I1(\gntv_or_sync_fifo.gl0.wr/gwss.gpf.wrpf/ram_wr_en_i ),
        .I2(eqOp__4),
        .I3(prog_full),
        .O(\greg.ram_rd_en_i_reg_0 ));
  FDRE #(
    .INIT(1'b0)) 
    \greg.gpcry_sym.diff_pntr_pad_reg[1] 
       (.C(clk),
        .CE(1'b1),
        .D(D[0]),
        .Q(diff_pntr_pad[1]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \greg.gpcry_sym.diff_pntr_pad_reg[2] 
       (.C(clk),
        .CE(1'b1),
        .D(D[1]),
        .Q(diff_pntr_pad[2]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \greg.gpcry_sym.diff_pntr_pad_reg[3] 
       (.C(clk),
        .CE(1'b1),
        .D(D[2]),
        .Q(diff_pntr_pad[3]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \greg.gpcry_sym.diff_pntr_pad_reg[4] 
       (.C(clk),
        .CE(1'b1),
        .D(D[3]),
        .Q(diff_pntr_pad[4]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \greg.gpcry_sym.diff_pntr_pad_reg[5] 
       (.C(clk),
        .CE(1'b1),
        .D(D[4]),
        .Q(diff_pntr_pad[5]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \greg.gpcry_sym.diff_pntr_pad_reg[6] 
       (.C(clk),
        .CE(1'b1),
        .D(D[5]),
        .Q(diff_pntr_pad[6]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \greg.ram_rd_en_i_reg 
       (.C(clk),
        .CE(1'b1),
        .D(E),
        .Q(\gntv_or_sync_fifo.gl0.wr/gwss.gpf.wrpf/ram_rd_en_i ),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \greg.ram_wr_en_i_reg 
       (.C(clk),
        .CE(1'b1),
        .D(p_17_out),
        .Q(\gntv_or_sync_fifo.gl0.wr/gwss.gpf.wrpf/ram_wr_en_i ),
        .R(srst_full_ff_i));
endmodule

(* ORIG_REF_NAME = "rd_status_flags_ss" *) 
module fifo_65_rd_status_flags_ss
   (out,
    srst_full_ff_i,
    ram_empty_i0__3,
    clk);
  output out;
  input srst_full_ff_i;
  input ram_empty_i0__3;
  input clk;

  wire clk;
  (* DONT_TOUCH *) wire ram_empty_fb_i;
  (* DONT_TOUCH *) wire ram_empty_i;
  wire ram_empty_i0__3;
  wire srst_full_ff_i;

  assign out = ram_empty_fb_i;
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDSE #(
    .INIT(1'b1)) 
    ram_empty_fb_i_reg
       (.C(clk),
        .CE(1'b1),
        .D(ram_empty_i0__3),
        .Q(ram_empty_fb_i),
        .S(srst_full_ff_i));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDSE #(
    .INIT(1'b1)) 
    ram_empty_i_reg
       (.C(clk),
        .CE(1'b1),
        .D(ram_empty_i0__3),
        .Q(ram_empty_i),
        .S(srst_full_ff_i));
endmodule

(* ORIG_REF_NAME = "reset_blk_ramfifo" *) 
module fifo_65_reset_blk_ramfifo
   (wr_rst_reg_reg,
    srst_full_ff_i,
    srst,
    clk);
  output wr_rst_reg_reg;
  output srst_full_ff_i;
  input srst;
  input clk;

  wire clk;
  wire srst;
  wire srst_full_ff_i;
  wire wr_rst_reg_reg;

  fifo_65_bram_fifo_rstlogic \g8serrst.usrst_inst 
       (.clk(clk),
        .srst(srst),
        .srst_full_ff_i(srst_full_ff_i),
        .wr_rst_reg_reg_0(wr_rst_reg_reg));
endmodule

(* ORIG_REF_NAME = "updn_cntr" *) 
module fifo_65_updn_cntr
   (Q,
    out,
    rd_en,
    srst_full_ff_i,
    E,
    clk);
  output [6:0]Q;
  input out;
  input rd_en;
  input srst_full_ff_i;
  input [0:0]E;
  input clk;

  wire [0:0]E;
  wire [6:0]Q;
  wire clk;
  wire \count[0]_i_1_n_0 ;
  wire \count[6]_i_3_n_0 ;
  wire \count[6]_i_4_n_0 ;
  wire \count[6]_i_5_n_0 ;
  wire \count[6]_i_6_n_0 ;
  wire \count[6]_i_7_n_0 ;
  wire \count[6]_i_8_n_0 ;
  wire \count[6]_i_9_n_0 ;
  wire \count_reg[6]_i_2_n_10 ;
  wire \count_reg[6]_i_2_n_11 ;
  wire \count_reg[6]_i_2_n_12 ;
  wire \count_reg[6]_i_2_n_13 ;
  wire \count_reg[6]_i_2_n_14 ;
  wire \count_reg[6]_i_2_n_15 ;
  wire \count_reg[6]_i_2_n_3 ;
  wire \count_reg[6]_i_2_n_4 ;
  wire \count_reg[6]_i_2_n_5 ;
  wire \count_reg[6]_i_2_n_6 ;
  wire \count_reg[6]_i_2_n_7 ;
  wire out;
  wire rd_en;
  wire srst_full_ff_i;
  wire [7:5]\NLW_count_reg[6]_i_2_CO_UNCONNECTED ;
  wire [7:6]\NLW_count_reg[6]_i_2_O_UNCONNECTED ;

  LUT1 #(
    .INIT(2'h1)) 
    \count[0]_i_1 
       (.I0(Q[0]),
        .O(\count[0]_i_1_n_0 ));
  LUT1 #(
    .INIT(2'h1)) 
    \count[6]_i_3 
       (.I0(Q[1]),
        .O(\count[6]_i_3_n_0 ));
  LUT2 #(
    .INIT(4'h9)) 
    \count[6]_i_4 
       (.I0(Q[5]),
        .I1(Q[6]),
        .O(\count[6]_i_4_n_0 ));
  LUT2 #(
    .INIT(4'h9)) 
    \count[6]_i_5 
       (.I0(Q[4]),
        .I1(Q[5]),
        .O(\count[6]_i_5_n_0 ));
  LUT2 #(
    .INIT(4'h9)) 
    \count[6]_i_6 
       (.I0(Q[3]),
        .I1(Q[4]),
        .O(\count[6]_i_6_n_0 ));
  LUT2 #(
    .INIT(4'h9)) 
    \count[6]_i_7 
       (.I0(Q[2]),
        .I1(Q[3]),
        .O(\count[6]_i_7_n_0 ));
  LUT2 #(
    .INIT(4'h9)) 
    \count[6]_i_8 
       (.I0(Q[1]),
        .I1(Q[2]),
        .O(\count[6]_i_8_n_0 ));
  LUT3 #(
    .INIT(8'h6A)) 
    \count[6]_i_9 
       (.I0(Q[1]),
        .I1(out),
        .I2(rd_en),
        .O(\count[6]_i_9_n_0 ));
  FDRE #(
    .INIT(1'b0)) 
    \count_reg[0] 
       (.C(clk),
        .CE(E),
        .D(\count[0]_i_1_n_0 ),
        .Q(Q[0]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \count_reg[1] 
       (.C(clk),
        .CE(E),
        .D(\count_reg[6]_i_2_n_15 ),
        .Q(Q[1]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \count_reg[2] 
       (.C(clk),
        .CE(E),
        .D(\count_reg[6]_i_2_n_14 ),
        .Q(Q[2]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \count_reg[3] 
       (.C(clk),
        .CE(E),
        .D(\count_reg[6]_i_2_n_13 ),
        .Q(Q[3]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \count_reg[4] 
       (.C(clk),
        .CE(E),
        .D(\count_reg[6]_i_2_n_12 ),
        .Q(Q[4]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \count_reg[5] 
       (.C(clk),
        .CE(E),
        .D(\count_reg[6]_i_2_n_11 ),
        .Q(Q[5]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \count_reg[6] 
       (.C(clk),
        .CE(E),
        .D(\count_reg[6]_i_2_n_10 ),
        .Q(Q[6]),
        .R(srst_full_ff_i));
  (* METHODOLOGY_DRC_VIOS = "{SYNTH-8 {cell *THIS*}}" *) 
  CARRY8 \count_reg[6]_i_2 
       (.CI(Q[0]),
        .CI_TOP(1'b0),
        .CO({\NLW_count_reg[6]_i_2_CO_UNCONNECTED [7:5],\count_reg[6]_i_2_n_3 ,\count_reg[6]_i_2_n_4 ,\count_reg[6]_i_2_n_5 ,\count_reg[6]_i_2_n_6 ,\count_reg[6]_i_2_n_7 }),
        .DI({1'b0,1'b0,1'b0,Q[4:1],\count[6]_i_3_n_0 }),
        .O({\NLW_count_reg[6]_i_2_O_UNCONNECTED [7:6],\count_reg[6]_i_2_n_10 ,\count_reg[6]_i_2_n_11 ,\count_reg[6]_i_2_n_12 ,\count_reg[6]_i_2_n_13 ,\count_reg[6]_i_2_n_14 ,\count_reg[6]_i_2_n_15 }),
        .S({1'b0,1'b0,\count[6]_i_4_n_0 ,\count[6]_i_5_n_0 ,\count[6]_i_6_n_0 ,\count[6]_i_7_n_0 ,\count[6]_i_8_n_0 ,\count[6]_i_9_n_0 }));
endmodule

(* ORIG_REF_NAME = "wr_bin_cntr" *) 
module fifo_65_wr_bin_cntr
   (Q,
    \gcc0.gc0.count_d1_reg[5]_0 ,
    D,
    \gcc0.gc0.count_reg[3]_0 ,
    ram_full_comb,
    comp0,
    ram_full_fb_i_reg,
    \greg.gpcry_sym.diff_pntr_pad_reg[6] ,
    rd_pntr_inv_pad,
    E,
    p_7_out,
    out,
    wr_en,
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ,
    p_1_out__0,
    ram_full_fb_i_reg_0,
    ram_full_fb_i_reg_1,
    srst_full_ff_i,
    clk);
  output [4:0]Q;
  output [5:0]\gcc0.gc0.count_d1_reg[5]_0 ;
  output [4:0]D;
  output [4:0]\gcc0.gc0.count_reg[3]_0 ;
  output ram_full_comb;
  output comp0;
  input [5:0]ram_full_fb_i_reg;
  input \greg.gpcry_sym.diff_pntr_pad_reg[6] ;
  input [0:0]rd_pntr_inv_pad;
  input [0:0]E;
  input p_7_out;
  input out;
  input wr_en;
  input \gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ;
  input p_1_out__0;
  input ram_full_fb_i_reg_0;
  input ram_full_fb_i_reg_1;
  input srst_full_ff_i;
  input clk;

  wire [4:0]D;
  wire [0:0]E;
  wire [4:0]Q;
  wire clk;
  wire comp0;
  wire [5:0]\gcc0.gc0.count_d1_reg[5]_0 ;
  wire [4:0]\gcc0.gc0.count_reg[3]_0 ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_2_n_0 ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_3_n_0 ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_4_n_0 ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_6_n_0 ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ;
  wire \greg.gpcry_sym.diff_pntr_pad[6]_i_2_n_0 ;
  wire \greg.gpcry_sym.diff_pntr_pad[6]_i_3_n_0 ;
  wire \greg.gpcry_sym.diff_pntr_pad[6]_i_4_n_0 ;
  wire \greg.gpcry_sym.diff_pntr_pad[6]_i_6_n_0 ;
  wire \greg.gpcry_sym.diff_pntr_pad_reg[6] ;
  wire out;
  wire [3:3]p_12_out;
  wire p_1_out__0;
  wire p_7_out;
  wire [5:0]plusOp__1;
  wire ram_full_comb;
  wire ram_full_fb_i_i_3_n_0;
  wire ram_full_fb_i_i_5_n_0;
  wire ram_full_fb_i_i_7_n_0;
  wire [5:0]ram_full_fb_i_reg;
  wire ram_full_fb_i_reg_0;
  wire ram_full_fb_i_reg_1;
  wire [0:0]rd_pntr_inv_pad;
  wire srst_full_ff_i;
  wire wr_en;

  (* SOFT_HLUTNM = "soft_lutpair4" *) 
  LUT1 #(
    .INIT(2'h1)) 
    \gcc0.gc0.count[0]_i_1 
       (.I0(Q[0]),
        .O(plusOp__1[0]));
  (* SOFT_HLUTNM = "soft_lutpair6" *) 
  LUT2 #(
    .INIT(4'h6)) 
    \gcc0.gc0.count[1]_i_1 
       (.I0(Q[0]),
        .I1(Q[1]),
        .O(plusOp__1[1]));
  (* SOFT_HLUTNM = "soft_lutpair6" *) 
  LUT3 #(
    .INIT(8'h78)) 
    \gcc0.gc0.count[2]_i_1 
       (.I0(Q[0]),
        .I1(Q[1]),
        .I2(Q[2]),
        .O(plusOp__1[2]));
  (* SOFT_HLUTNM = "soft_lutpair3" *) 
  LUT4 #(
    .INIT(16'h7F80)) 
    \gcc0.gc0.count[3]_i_1 
       (.I0(Q[1]),
        .I1(Q[0]),
        .I2(Q[2]),
        .I3(p_12_out),
        .O(plusOp__1[3]));
  (* SOFT_HLUTNM = "soft_lutpair3" *) 
  LUT5 #(
    .INIT(32'h7FFF8000)) 
    \gcc0.gc0.count[4]_i_1 
       (.I0(Q[2]),
        .I1(Q[0]),
        .I2(Q[1]),
        .I3(p_12_out),
        .I4(Q[3]),
        .O(plusOp__1[4]));
  LUT6 #(
    .INIT(64'h7FFFFFFF80000000)) 
    \gcc0.gc0.count[5]_i_1 
       (.I0(p_12_out),
        .I1(Q[1]),
        .I2(Q[0]),
        .I3(Q[2]),
        .I4(Q[3]),
        .I5(Q[4]),
        .O(plusOp__1[5]));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_d1_reg[0] 
       (.C(clk),
        .CE(E),
        .D(Q[0]),
        .Q(\gcc0.gc0.count_d1_reg[5]_0 [0]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_d1_reg[1] 
       (.C(clk),
        .CE(E),
        .D(Q[1]),
        .Q(\gcc0.gc0.count_d1_reg[5]_0 [1]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_d1_reg[2] 
       (.C(clk),
        .CE(E),
        .D(Q[2]),
        .Q(\gcc0.gc0.count_d1_reg[5]_0 [2]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_d1_reg[3] 
       (.C(clk),
        .CE(E),
        .D(p_12_out),
        .Q(\gcc0.gc0.count_d1_reg[5]_0 [3]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_d1_reg[4] 
       (.C(clk),
        .CE(E),
        .D(Q[3]),
        .Q(\gcc0.gc0.count_d1_reg[5]_0 [4]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_d1_reg[5] 
       (.C(clk),
        .CE(E),
        .D(Q[4]),
        .Q(\gcc0.gc0.count_d1_reg[5]_0 [5]),
        .R(srst_full_ff_i));
  FDSE #(
    .INIT(1'b1)) 
    \gcc0.gc0.count_reg[0] 
       (.C(clk),
        .CE(E),
        .D(plusOp__1[0]),
        .Q(Q[0]),
        .S(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_reg[1] 
       (.C(clk),
        .CE(E),
        .D(plusOp__1[1]),
        .Q(Q[1]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_reg[2] 
       (.C(clk),
        .CE(E),
        .D(plusOp__1[2]),
        .Q(Q[2]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_reg[3] 
       (.C(clk),
        .CE(E),
        .D(plusOp__1[3]),
        .Q(p_12_out),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_reg[4] 
       (.C(clk),
        .CE(E),
        .D(plusOp__1[4]),
        .Q(Q[3]),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gcc0.gc0.count_reg[5] 
       (.C(clk),
        .CE(E),
        .D(plusOp__1[5]),
        .Q(Q[4]),
        .R(srst_full_ff_i));
  (* SOFT_HLUTNM = "soft_lutpair4" *) 
  LUT5 #(
    .INIT(32'h99999699)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[1]_i_1 
       (.I0(Q[0]),
        .I1(ram_full_fb_i_reg[0]),
        .I2(out),
        .I3(wr_en),
        .I4(p_7_out),
        .O(\gcc0.gc0.count_reg[3]_0 [0]));
  LUT6 #(
    .INIT(64'hF75108AE08AEF751)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[2]_i_1 
       (.I0(Q[0]),
        .I1(E),
        .I2(p_7_out),
        .I3(ram_full_fb_i_reg[0]),
        .I4(ram_full_fb_i_reg[1]),
        .I5(Q[1]),
        .O(\gcc0.gc0.count_reg[3]_0 [1]));
  (* SOFT_HLUTNM = "soft_lutpair5" *) 
  LUT5 #(
    .INIT(32'h69699669)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[4]_i_1 
       (.I0(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_3_n_0 ),
        .I1(p_12_out),
        .I2(ram_full_fb_i_reg[3]),
        .I3(Q[2]),
        .I4(ram_full_fb_i_reg[2]),
        .O(\gcc0.gc0.count_reg[3]_0 [2]));
  LUT6 #(
    .INIT(64'h51AEF70808F751AE)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[5]_i_1 
       (.I0(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_3_n_0 ),
        .I1(Q[2]),
        .I2(ram_full_fb_i_reg[2]),
        .I3(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_4_n_0 ),
        .I4(p_12_out),
        .I5(ram_full_fb_i_reg[3]),
        .O(\gcc0.gc0.count_reg[3]_0 [3]));
  LUT6 #(
    .INIT(64'h1701FF7FE8FE0080)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_1 
       (.I0(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_2_n_0 ),
        .I1(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_3_n_0 ),
        .I2(p_12_out),
        .I3(ram_full_fb_i_reg[3]),
        .I4(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_4_n_0 ),
        .I5(\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ),
        .O(\gcc0.gc0.count_reg[3]_0 [4]));
  (* SOFT_HLUTNM = "soft_lutpair9" *) 
  LUT2 #(
    .INIT(4'h2)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_2 
       (.I0(Q[2]),
        .I1(ram_full_fb_i_reg[2]),
        .O(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_2_n_0 ));
  LUT6 #(
    .INIT(64'hA2A220A220A22020)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_3 
       (.I0(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_6_n_0 ),
        .I1(ram_full_fb_i_reg[1]),
        .I2(Q[1]),
        .I3(ram_full_fb_i_reg[0]),
        .I4(p_1_out__0),
        .I5(Q[0]),
        .O(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_3_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair7" *) 
  LUT2 #(
    .INIT(4'h9)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_4 
       (.I0(Q[3]),
        .I1(ram_full_fb_i_reg[4]),
        .O(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_4_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair9" *) 
  LUT2 #(
    .INIT(4'h9)) 
    \gdiff.gcry_1_sym.diff_pntr_pad[6]_i_6 
       (.I0(Q[2]),
        .I1(ram_full_fb_i_reg[2]),
        .O(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_6_n_0 ));
  LUT5 #(
    .INIT(32'h96996666)) 
    \greg.gpcry_sym.diff_pntr_pad[1]_i_1 
       (.I0(\gcc0.gc0.count_d1_reg[5]_0 [0]),
        .I1(ram_full_fb_i_reg[0]),
        .I2(out),
        .I3(wr_en),
        .I4(p_7_out),
        .O(D[0]));
  LUT6 #(
    .INIT(64'h75108AEF8AEF7510)) 
    \greg.gpcry_sym.diff_pntr_pad[2]_i_1 
       (.I0(\gcc0.gc0.count_d1_reg[5]_0 [0]),
        .I1(E),
        .I2(p_7_out),
        .I3(ram_full_fb_i_reg[0]),
        .I4(ram_full_fb_i_reg[1]),
        .I5(\gcc0.gc0.count_d1_reg[5]_0 [1]),
        .O(D[1]));
  (* SOFT_HLUTNM = "soft_lutpair2" *) 
  LUT5 #(
    .INIT(32'h69699669)) 
    \greg.gpcry_sym.diff_pntr_pad[4]_i_1 
       (.I0(\greg.gpcry_sym.diff_pntr_pad[6]_i_3_n_0 ),
        .I1(\gcc0.gc0.count_d1_reg[5]_0 [3]),
        .I2(ram_full_fb_i_reg[3]),
        .I3(\gcc0.gc0.count_d1_reg[5]_0 [2]),
        .I4(ram_full_fb_i_reg[2]),
        .O(D[2]));
  LUT6 #(
    .INIT(64'h51AEF70808F751AE)) 
    \greg.gpcry_sym.diff_pntr_pad[5]_i_1 
       (.I0(\greg.gpcry_sym.diff_pntr_pad[6]_i_3_n_0 ),
        .I1(\gcc0.gc0.count_d1_reg[5]_0 [2]),
        .I2(ram_full_fb_i_reg[2]),
        .I3(\greg.gpcry_sym.diff_pntr_pad[6]_i_4_n_0 ),
        .I4(\gcc0.gc0.count_d1_reg[5]_0 [3]),
        .I5(ram_full_fb_i_reg[3]),
        .O(D[3]));
  LUT6 #(
    .INIT(64'h1701FF7FE8FE0080)) 
    \greg.gpcry_sym.diff_pntr_pad[6]_i_1 
       (.I0(\greg.gpcry_sym.diff_pntr_pad[6]_i_2_n_0 ),
        .I1(\greg.gpcry_sym.diff_pntr_pad[6]_i_3_n_0 ),
        .I2(\gcc0.gc0.count_d1_reg[5]_0 [3]),
        .I3(ram_full_fb_i_reg[3]),
        .I4(\greg.gpcry_sym.diff_pntr_pad[6]_i_4_n_0 ),
        .I5(\greg.gpcry_sym.diff_pntr_pad_reg[6] ),
        .O(D[4]));
  (* SOFT_HLUTNM = "soft_lutpair8" *) 
  LUT2 #(
    .INIT(4'h2)) 
    \greg.gpcry_sym.diff_pntr_pad[6]_i_2 
       (.I0(\gcc0.gc0.count_d1_reg[5]_0 [2]),
        .I1(ram_full_fb_i_reg[2]),
        .O(\greg.gpcry_sym.diff_pntr_pad[6]_i_2_n_0 ));
  LUT6 #(
    .INIT(64'hA2A220A220A22020)) 
    \greg.gpcry_sym.diff_pntr_pad[6]_i_3 
       (.I0(\greg.gpcry_sym.diff_pntr_pad[6]_i_6_n_0 ),
        .I1(ram_full_fb_i_reg[1]),
        .I2(\gcc0.gc0.count_d1_reg[5]_0 [1]),
        .I3(ram_full_fb_i_reg[0]),
        .I4(rd_pntr_inv_pad),
        .I5(\gcc0.gc0.count_d1_reg[5]_0 [0]),
        .O(\greg.gpcry_sym.diff_pntr_pad[6]_i_3_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair7" *) 
  LUT2 #(
    .INIT(4'h9)) 
    \greg.gpcry_sym.diff_pntr_pad[6]_i_4 
       (.I0(\gcc0.gc0.count_d1_reg[5]_0 [4]),
        .I1(ram_full_fb_i_reg[4]),
        .O(\greg.gpcry_sym.diff_pntr_pad[6]_i_4_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair8" *) 
  LUT2 #(
    .INIT(4'h9)) 
    \greg.gpcry_sym.diff_pntr_pad[6]_i_6 
       (.I0(\gcc0.gc0.count_d1_reg[5]_0 [2]),
        .I1(ram_full_fb_i_reg[2]),
        .O(\greg.gpcry_sym.diff_pntr_pad[6]_i_6_n_0 ));
  LUT6 #(
    .INIT(64'h00FFFFFF00008080)) 
    ram_full_fb_i_i_1
       (.I0(wr_en),
        .I1(ram_full_fb_i_reg_0),
        .I2(ram_full_fb_i_i_3_n_0),
        .I3(comp0),
        .I4(p_7_out),
        .I5(out),
        .O(ram_full_comb));
  LUT6 #(
    .INIT(64'h8200008200000000)) 
    ram_full_fb_i_i_3
       (.I0(ram_full_fb_i_i_5_n_0),
        .I1(ram_full_fb_i_reg[2]),
        .I2(Q[2]),
        .I3(ram_full_fb_i_reg[5]),
        .I4(Q[4]),
        .I5(\gdiff.gcry_1_sym.diff_pntr_pad[6]_i_4_n_0 ),
        .O(ram_full_fb_i_i_3_n_0));
  LUT6 #(
    .INIT(64'h8008000000000000)) 
    ram_full_fb_i_i_4
       (.I0(ram_full_fb_i_reg_1),
        .I1(\greg.gpcry_sym.diff_pntr_pad[6]_i_4_n_0 ),
        .I2(\gcc0.gc0.count_d1_reg[5]_0 [5]),
        .I3(ram_full_fb_i_reg[5]),
        .I4(\greg.gpcry_sym.diff_pntr_pad[6]_i_6_n_0 ),
        .I5(ram_full_fb_i_i_7_n_0),
        .O(comp0));
  (* SOFT_HLUTNM = "soft_lutpair5" *) 
  LUT2 #(
    .INIT(4'h9)) 
    ram_full_fb_i_i_5
       (.I0(p_12_out),
        .I1(ram_full_fb_i_reg[3]),
        .O(ram_full_fb_i_i_5_n_0));
  (* SOFT_HLUTNM = "soft_lutpair2" *) 
  LUT2 #(
    .INIT(4'h9)) 
    ram_full_fb_i_i_7
       (.I0(\gcc0.gc0.count_d1_reg[5]_0 [3]),
        .I1(ram_full_fb_i_reg[3]),
        .O(ram_full_fb_i_i_7_n_0));
endmodule

(* ORIG_REF_NAME = "wr_logic" *) 
module fifo_65_wr_logic
   (out,
    full,
    prog_full,
    Q,
    \gcc0.gc0.count_d1_reg[5] ,
    D,
    p_17_out,
    E,
    comp0,
    eqOp__4,
    srst_full_ff_i,
    clk,
    \gpfs.prog_full_i_reg ,
    ram_full_fb_i_reg,
    \greg.gpcry_sym.diff_pntr_pad_reg[6] ,
    rd_pntr_inv_pad,
    p_7_out,
    wr_en,
    \count_reg[6] ,
    rd_en,
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ,
    p_1_out__0,
    ram_full_fb_i_reg_0,
    ram_full_fb_i_reg_1,
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[3] );
  output out;
  output full;
  output prog_full;
  output [4:0]Q;
  output [5:0]\gcc0.gc0.count_d1_reg[5] ;
  output [4:0]D;
  output p_17_out;
  output [0:0]E;
  output comp0;
  output eqOp__4;
  input srst_full_ff_i;
  input clk;
  input \gpfs.prog_full_i_reg ;
  input [5:0]ram_full_fb_i_reg;
  input \greg.gpcry_sym.diff_pntr_pad_reg[6] ;
  input [0:0]rd_pntr_inv_pad;
  input p_7_out;
  input wr_en;
  input \count_reg[6] ;
  input rd_en;
  input \gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ;
  input p_1_out__0;
  input ram_full_fb_i_reg_0;
  input ram_full_fb_i_reg_1;
  input [0:0]\gdiff.gcry_1_sym.diff_pntr_pad_reg[3] ;

  wire [4:0]D;
  wire [0:0]E;
  wire [4:0]Q;
  wire clk;
  wire comp0;
  wire \count_reg[6] ;
  wire eqOp__4;
  wire full;
  wire [5:0]\gcc0.gc0.count_d1_reg[5] ;
  wire [0:0]\gdiff.gcry_1_sym.diff_pntr_pad_reg[3] ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ;
  wire \gpfs.prog_full_i_reg ;
  wire \greg.gpcry_sym.diff_pntr_pad_reg[6] ;
  wire out;
  wire p_17_out;
  wire p_1_out__0;
  wire p_7_out;
  wire prog_full;
  wire ram_full_comb;
  wire [5:0]ram_full_fb_i_reg;
  wire ram_full_fb_i_reg_0;
  wire ram_full_fb_i_reg_1;
  wire rd_en;
  wire [0:0]rd_pntr_inv_pad;
  wire srst_full_ff_i;
  wire wpntr_n_16;
  wire wpntr_n_17;
  wire wpntr_n_18;
  wire wpntr_n_19;
  wire wpntr_n_20;
  wire wr_en;

  fifo_65_wr_pf_ss \gwss.gpf.wrpf 
       (.D({wpntr_n_16,wpntr_n_17,wpntr_n_18,\gdiff.gcry_1_sym.diff_pntr_pad_reg[3] ,wpntr_n_19,wpntr_n_20}),
        .clk(clk),
        .eqOp__4(eqOp__4),
        .\gpfs.prog_full_i_reg_0 (\gpfs.prog_full_i_reg ),
        .prog_full(prog_full),
        .srst_full_ff_i(srst_full_ff_i));
  fifo_65_wr_status_flags_ss \gwss.wsts 
       (.E(E),
        .clk(clk),
        .\count_reg[6] (\count_reg[6] ),
        .full(full),
        .out(out),
        .ram_full_comb(ram_full_comb),
        .rd_en(rd_en),
        .srst_full_ff_i(srst_full_ff_i),
        .wr_en(wr_en),
        .wr_en_0(p_17_out));
  fifo_65_wr_bin_cntr wpntr
       (.D(D),
        .E(p_17_out),
        .Q(Q),
        .clk(clk),
        .comp0(comp0),
        .\gcc0.gc0.count_d1_reg[5]_0 (\gcc0.gc0.count_d1_reg[5] ),
        .\gcc0.gc0.count_reg[3]_0 ({wpntr_n_16,wpntr_n_17,wpntr_n_18,wpntr_n_19,wpntr_n_20}),
        .\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] (\gdiff.gcry_1_sym.diff_pntr_pad_reg[6] ),
        .\greg.gpcry_sym.diff_pntr_pad_reg[6] (\greg.gpcry_sym.diff_pntr_pad_reg[6] ),
        .out(out),
        .p_1_out__0(p_1_out__0),
        .p_7_out(p_7_out),
        .ram_full_comb(ram_full_comb),
        .ram_full_fb_i_reg(ram_full_fb_i_reg),
        .ram_full_fb_i_reg_0(ram_full_fb_i_reg_0),
        .ram_full_fb_i_reg_1(ram_full_fb_i_reg_1),
        .rd_pntr_inv_pad(rd_pntr_inv_pad),
        .srst_full_ff_i(srst_full_ff_i),
        .wr_en(wr_en));
endmodule

(* ORIG_REF_NAME = "wr_pf_ss" *) 
module fifo_65_wr_pf_ss
   (prog_full,
    eqOp__4,
    srst_full_ff_i,
    \gpfs.prog_full_i_reg_0 ,
    clk,
    D);
  output prog_full;
  output eqOp__4;
  input srst_full_ff_i;
  input \gpfs.prog_full_i_reg_0 ;
  input clk;
  input [5:0]D;

  wire [5:0]D;
  wire clk;
  wire eqOp__4;
  wire \gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[1] ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[2] ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[3] ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[4] ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[5] ;
  wire \gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[6] ;
  wire \gpfs.prog_full_i_reg_0 ;
  wire prog_full;
  wire srst_full_ff_i;

  FDRE #(
    .INIT(1'b0)) 
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[1] 
       (.C(clk),
        .CE(1'b1),
        .D(D[0]),
        .Q(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[1] ),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[2] 
       (.C(clk),
        .CE(1'b1),
        .D(D[1]),
        .Q(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[2] ),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[3] 
       (.C(clk),
        .CE(1'b1),
        .D(D[2]),
        .Q(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[3] ),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[4] 
       (.C(clk),
        .CE(1'b1),
        .D(D[3]),
        .Q(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[4] ),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[5] 
       (.C(clk),
        .CE(1'b1),
        .D(D[4]),
        .Q(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[5] ),
        .R(srst_full_ff_i));
  FDRE #(
    .INIT(1'b0)) 
    \gdiff.gcry_1_sym.diff_pntr_pad_reg[6] 
       (.C(clk),
        .CE(1'b1),
        .D(D[5]),
        .Q(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[6] ),
        .R(srst_full_ff_i));
  LUT6 #(
    .INIT(64'h0008000000000000)) 
    \gpfs.prog_full_i_i_2 
       (.I0(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[1] ),
        .I1(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[6] ),
        .I2(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[3] ),
        .I3(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[2] ),
        .I4(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[5] ),
        .I5(\gdiff.gcry_1_sym.diff_pntr_pad_reg_n_0_[4] ),
        .O(eqOp__4));
  FDRE #(
    .INIT(1'b0)) 
    \gpfs.prog_full_i_reg 
       (.C(clk),
        .CE(1'b1),
        .D(\gpfs.prog_full_i_reg_0 ),
        .Q(prog_full),
        .R(srst_full_ff_i));
endmodule

(* ORIG_REF_NAME = "wr_status_flags_ss" *) 
module fifo_65_wr_status_flags_ss
   (out,
    full,
    E,
    wr_en_0,
    srst_full_ff_i,
    ram_full_comb,
    clk,
    wr_en,
    \count_reg[6] ,
    rd_en);
  output out;
  output full;
  output [0:0]E;
  output [0:0]wr_en_0;
  input srst_full_ff_i;
  input ram_full_comb;
  input clk;
  input wr_en;
  input \count_reg[6] ;
  input rd_en;

  wire [0:0]E;
  wire clk;
  wire \count_reg[6] ;
  (* DONT_TOUCH *) wire ram_afull_fb;
  (* DONT_TOUCH *) wire ram_afull_i;
  wire ram_full_comb;
  (* DONT_TOUCH *) wire ram_full_fb_i;
  (* DONT_TOUCH *) wire ram_full_i;
  wire rd_en;
  wire srst_full_ff_i;
  wire wr_en;
  wire [0:0]wr_en_0;

  assign full = ram_full_i;
  assign out = ram_full_fb_i;
  LUT2 #(
    .INIT(4'h2)) 
    \DEVICE_8SERIES.NO_BMM_INFO.SDP.WIDE_PRIM36_NO_ECC.ram_i_2 
       (.I0(wr_en),
        .I1(ram_full_fb_i),
        .O(wr_en_0));
  LUT4 #(
    .INIT(16'hB444)) 
    \count[6]_i_1 
       (.I0(ram_full_fb_i),
        .I1(wr_en),
        .I2(\count_reg[6] ),
        .I3(rd_en),
        .O(E));
  LUT1 #(
    .INIT(2'h2)) 
    i_0
       (.I0(1'b0),
        .O(ram_afull_i));
  LUT1 #(
    .INIT(2'h2)) 
    i_1
       (.I0(1'b0),
        .O(ram_afull_fb));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDRE #(
    .INIT(1'b0)) 
    ram_full_fb_i_reg
       (.C(clk),
        .CE(1'b1),
        .D(ram_full_comb),
        .Q(ram_full_fb_i),
        .R(srst_full_ff_i));
  (* DONT_TOUCH *) 
  (* KEEP = "yes" *) 
  (* equivalent_register_removal = "no" *) 
  FDRE #(
    .INIT(1'b0)) 
    ram_full_i_reg
       (.C(clk),
        .CE(1'b1),
        .D(ram_full_comb),
        .Q(ram_full_i),
        .R(srst_full_ff_i));
endmodule
`ifndef GLBL
`define GLBL
`timescale  1 ps / 1 ps

module glbl ();

    parameter ROC_WIDTH = 100000;
    parameter TOC_WIDTH = 0;

//--------   STARTUP Globals --------------
    wire GSR;
    wire GTS;
    wire GWE;
    wire PRLD;
    tri1 p_up_tmp;
    tri (weak1, strong0) PLL_LOCKG = p_up_tmp;

    wire PROGB_GLBL;
    wire CCLKO_GLBL;
    wire FCSBO_GLBL;
    wire [3:0] DO_GLBL;
    wire [3:0] DI_GLBL;
   
    reg GSR_int;
    reg GTS_int;
    reg PRLD_int;

//--------   JTAG Globals --------------
    wire JTAG_TDO_GLBL;
    wire JTAG_TCK_GLBL;
    wire JTAG_TDI_GLBL;
    wire JTAG_TMS_GLBL;
    wire JTAG_TRST_GLBL;

    reg JTAG_CAPTURE_GLBL;
    reg JTAG_RESET_GLBL;
    reg JTAG_SHIFT_GLBL;
    reg JTAG_UPDATE_GLBL;
    reg JTAG_RUNTEST_GLBL;

    reg JTAG_SEL1_GLBL = 0;
    reg JTAG_SEL2_GLBL = 0 ;
    reg JTAG_SEL3_GLBL = 0;
    reg JTAG_SEL4_GLBL = 0;

    reg JTAG_USER_TDO1_GLBL = 1'bz;
    reg JTAG_USER_TDO2_GLBL = 1'bz;
    reg JTAG_USER_TDO3_GLBL = 1'bz;
    reg JTAG_USER_TDO4_GLBL = 1'bz;

    assign (strong1, weak0) GSR = GSR_int;
    assign (strong1, weak0) GTS = GTS_int;
    assign (weak1, weak0) PRLD = PRLD_int;

    initial begin
	GSR_int = 1'b1;
	PRLD_int = 1'b1;
	#(ROC_WIDTH)
	GSR_int = 1'b0;
	PRLD_int = 1'b0;
    end

    initial begin
	GTS_int = 1'b1;
	#(TOC_WIDTH)
	GTS_int = 1'b0;
    end

endmodule
`endif
