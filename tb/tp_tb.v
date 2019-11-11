/*
 * top-level verilog test bench for initial toy version of
 * TP main fpga
 * 
 * begun 2019-11-11
 * 
 */

`timescale 1ns / 1ps
`default_nettype none

module tp_tb;
   reg clk = 1'b0;
   localparam clkperiod = 5.0;  // 200 MHz for now
   initial begin
      forever begin
	 clk = 1'b0;
	 #(clkperiod/2);
	 clk = 1'b1;
	 #(clkperiod/2);
      end
   end
   reg rst = 1'b0;
   localparam W = 65;  // inclusive of metadata flag (bit 64)
   reg [W-1:0] din = 1'b0;
   reg din_valid = 1'b0;
   wire [W-1:0] dout;
   wire dout_valid;
   tp dut
     (.clk(clk),
      .rst(rst),
      .din(din),
      .din_valid(din_valid),
      .dout(dout),
      .dout_valid(dout_valid));
endmodule // tp_tb


`default_nettype wire
