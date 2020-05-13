
`timescale 1ns/1ps

module board2board_switching_wrapper #(
    parameter DATA_WIDTH=65,
    parameter TOTAL_CLUSTERS=4,
    parameter TOTAL_OUTPUT_BOARDS=14,
    parameter FIFO_DEPTH_BITS=6,
    parameter BOARD_ID=0
  ) 
   (
  b2b_clk,
  b2b_rst_n,
  b2b_srst_n,
  cluster_data,
  cluster_req,
  cluster_almost_full,
  cluster_empty,
  output_board_event,
  output_board_wren,
  output_board_almost_full
);

input wire b2b_clk;
  input wire b2b_rst_n;
input wire b2b_srst_n;
input wire [259 : 0] cluster_data;
wire  [64:0] cluster_data_unpacked [0:3];
assign {>>{cluster_data_unpacked}} = cluster_data;
output wire [0 : 3] cluster_req;
wire   cluster_req_unpacked [0:3];
assign {>>{cluster_req}} = cluster_req_unpacked;
input wire [0 : 3] cluster_almost_full;
wire   cluster_almost_full_unpacked [0:3];
assign {>>{cluster_almost_full_unpacked}} = cluster_almost_full;
input wire [0 : 3] cluster_empty;
wire   cluster_empty_unpacked [0:3];
assign {>>{cluster_empty_unpacked}} = cluster_empty;
output wire [909 : 0] output_board_event;
wire  [64:0] output_board_event_unpacked [0:13];
assign {>>{output_board_event}} = output_board_event_unpacked;
output wire [0 : 13] output_board_wren;
wire   output_board_wren_unpacked [0:13];
assign {>>{output_board_wren}} = output_board_wren_unpacked;
input wire [0 : 13] output_board_almost_full;
wire   output_board_almost_full_unpacked [0:13];
assign {>>{output_board_almost_full_unpacked}} = output_board_almost_full;

  board2board_switching #(
    .DATA_WIDTH(65),
    .TOTAL_CLUSTERS(4),
    .TOTAL_OUTPUT_BOARDS(14),
    .FIFO_DEPTH_BITS(6),
    .BOARD_ID(0)
  ) inst (
    .b2b_clk(b2b_clk),
    .b2b_rst_n(b2b_rst_n),
    .b2b_srst_n(b2b_srst_n),
    .cluster_data(cluster_data_unpacked),
    .cluster_req(cluster_req_unpacked),
    .cluster_almost_full(cluster_almost_full_unpacked),
    .cluster_empty(cluster_empty_unpacked),
    .output_board_event(output_board_event_unpacked),
    .output_board_wren(output_board_wren_unpacked),
    .output_board_almost_full(output_board_almost_full_unpacked)
  );
endmodule
