//Copyright 1986-2019 Xilinx, Inc. All Rights Reserved.
//--------------------------------------------------------------------------------
//Tool Version: Vivado v.2019.1.1 (lin64) Build 2580384 Sat Jun 29 08:04:45 MDT 2019
//Date        : Fri Mar  6 19:10:20 2020
//Host        : uciatlaslab.ps.uci.edu running 64-bit CentOS Linux release 7.7.1908 (Core)
//Command     : generate_target b2b_top.bd
//Design      : b2b_top
//Purpose     : IP block netlist
//--------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

module top_tp
   (FIFO_READ_empty,
    FIFO_READ_rd_data,
    FIFO_READ_rd_en,
    clk_in1,
    reset_rtl_0);
  (* X_INTERFACE_INFO = "xilinx.com:interface:fifo_read:1.0 FIFO_READ EMPTY" *) output FIFO_READ_empty;
  (* X_INTERFACE_INFO = "xilinx.com:interface:fifo_read:1.0 FIFO_READ RD_DATA" *) output [127:0]FIFO_READ_rd_data;
  (* X_INTERFACE_INFO = "xilinx.com:interface:fifo_read:1.0 FIFO_READ RD_EN" *) input FIFO_READ_rd_en;
  (* X_INTERFACE_INFO = "xilinx.com:signal:clock:1.0 CLK.CLK_IN1 CLK" *) (* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME CLK.CLK_IN1, CLK_DOMAIN b2b_top_clk_in1, FREQ_HZ 100000000, INSERT_VIP 0, PHASE 0.000" *) input clk_in1;
  (* X_INTERFACE_INFO = "xilinx.com:signal:reset:1.0 RST.RESET_RTL_0 RST" *) (* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME RST.RESET_RTL_0, INSERT_VIP 0, POLARITY ACTIVE_HIGH" *) input reset_rtl_0;
   parameter DATA_WIDTH = 65;
   parameter TOTAL_CLUSTERS = 4;
   
  wire FIFO_READ_1_EMPTY;
  wire [127:0]FIFO_READ_1_RD_DATA;
  wire FIFO_READ_1_RD_EN;
  wire [0:0]Net;
  wire [0:3]board2board_switching_0_cluster_req;
  wire [909:0]board2board_switching_0_output_board_event;
  wire [0:13]board2board_switching_0_output_board_wren;
  wire clk_in1_1;
  wire clk_wiz_clk_out1;
  wire fifo_generator_0_almost_full;
  wire [259:0]fifo_generator_1_dout;
  wire fifo_generator_1_empty;
  wire [0:0]proc_sys_reset_0_peripheral_reset;
  wire reset_rtl_0_1;
   

  assign FIFO_READ_1_RD_EN = FIFO_READ_rd_en;
  assign FIFO_READ_empty = FIFO_READ_1_EMPTY;
  assign FIFO_READ_rd_data[127:0] = FIFO_READ_1_RD_DATA;
  assign clk_in1_1 = clk_in1;
  assign reset_rtl_0_1 = reset_rtl_0;
   
   /*
    wire [DATA_WIDTH-1:0] cluster_data[TOTAL_CLUSTERS];
   assign cluster_data[0] = fifo_generator_1_dout[64:0];
   assign cluster_data[1] = fifo_generator_1_dout[129:65];
   assign cluster_data[2] = fifo_generator_1_dout[194:130];
   assign cluster_data[3] = fifo_generator_1_dout[259:195];
   */
   board2board_switching_wrapper #(
			 .DATA_WIDTH(DATA_WIDTH),
			 .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
			 .TOTAL_OUTPUT_BOARDS(14),
			 .FIFO_DEPTH_BITS(9),
			 .BOARD_ID(0)
			 )
     board2board_switching_0(.b2b_clk(clk_wiz_clk_out1),
			     .b2b_rst_n(Net),
			     .b2b_srst_n(Net),
			     .cluster_almost_full({1'b0,1'b0,1'b0,1'b0}),
			     .cluster_data(fifo_generator_1_dout),
			     .cluster_empty({fifo_generator_1_empty,fifo_generator_1_empty,fifo_generator_1_empty,fifo_generator_1_empty}),
			     .cluster_req(board2board_switching_0_cluster_req),
			     .output_board_almost_full({fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full,fifo_generator_0_almost_full}),
			     .output_board_event(board2board_switching_0_output_board_event),
			     .output_board_wren(board2board_switching_0_output_board_wren));
   

   
  b2b_top_clk_wiz_0 clk_wiz
       (.clk_in1(clk_in1_1),
        .clk_out1(clk_wiz_clk_out1),
        .reset(proc_sys_reset_0_peripheral_reset));

   
  b2b_top_fifo_generator_0_0 fifo_generator_0
       (.almost_full(fifo_generator_0_almost_full),
        .clk(clk_wiz_clk_out1),
        .din({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,board2board_switching_0_output_board_event}),
        .dout(FIFO_READ_1_RD_DATA),
        .empty(FIFO_READ_1_EMPTY),
        .rd_en(FIFO_READ_1_RD_EN),
        .srst(proc_sys_reset_0_peripheral_reset),
        .wr_en(board2board_switching_0_output_board_wren[13]));

   
  b2b_top_fifo_generator_1_0 fifo_generator_1
       (.clk(clk_wiz_clk_out1),
        .din({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .dout(fifo_getopnerator_1_dout),
        .empty(fifo_generator_1_empty),
        .rd_en(board2board_switching_0_cluster_req[3]),
        .srst(proc_sys_reset_0_peripheral_reset),
        .wr_en(1'b0));
  b2b_top_proc_sys_reset_0_0 proc_sys_reset_0
       (.aux_reset_in(1'b1),
        .dcm_locked(1'b1),
        .ext_reset_in(reset_rtl_0_1),
        .interconnect_aresetn(Net),
        .mb_debug_sys_rst(1'b0),
        .peripheral_reset(proc_sys_reset_0_peripheral_reset),
        .slowest_sync_clk(clk_wiz_clk_out1));
endmodule


module top_b2b_proj
   (FIFO_READ_empty,
    FIFO_READ_rd_data,
    FIFO_READ_rd_en,
    clk_in1,
    reset_rtl_0);
  output FIFO_READ_empty;
  output [127:0]FIFO_READ_rd_data;
  input FIFO_READ_rd_en;
  input clk_in1;
  input reset_rtl_0;

  wire FIFO_READ_empty;
  wire [127:0]FIFO_READ_rd_data;
  wire FIFO_READ_rd_en;
  wire clk_in1;
  wire reset_rtl_0;

  b2b_top b2b_top_i
       (.FIFO_READ_empty(FIFO_READ_empty),
        .FIFO_READ_rd_data(FIFO_READ_rd_data),
        .FIFO_READ_rd_en(FIFO_READ_rd_en),
        .clk_in1(clk_in1),
        .reset_rtl_0(reset_rtl_0));
endmodule
