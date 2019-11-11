/*
 * tp.v
 *
 * toy version of top-level Track Processor main FPGA
 * 
 * begun 2019-11-11
 * 
 */

`timescale 1ns / 1ps
`default_nettype none

module tp #(
  parameter W = 65  // inclusive of metadata flag (bit 64)
) ( input  wire         clk,        // main TP clock, nominally 200 MHz
    input  wire         rst,        // do we need a reset?
    input  wire [W-1:0] din,        // eventually we will have serial inputs
    input  wire         din_valid,
    output wire [W-1:0] dout,       // eventually we will have serial outputs
    output wire         dout_valid
    );
   // Instantiate an input spy buffer
   reg sb1_ren = 0;  // to be driven by python code
   wire [W-1:0] sb1_dout;
   wire sb1_afull, sb1_empty;
   SpyBuffer 
     #(.DATA_WIDTH(W-1))  // exclusive of metadata flag bit
   sb1
     (.rclock(clk), .wclock(clk), .rreset(rst), .wreset(rst),
      .write_data(din), .write_enable(din_valid),
      .read_enable(sb1_ren),
      .read_data(sb1_dout),
      .almost_full(sb1_afull),
      .empty(sb1_empty),
      // The following should not be needed until one actually wants
      // to use the spy-buffer functionality, whereas for now we just
      // want to use the fifo functionality.
      .freeze(1'b0),
      .spy_read_enable(1'b0), .spy_meta_read_enable(1'b0),
      .spy_read_addr(1'b0), .spy_meta_read_addr(1'b0),
      .spy_write_addr(), .spy_meta_write_addr(),
      .spy_data(), .spy_meta_read_data());
   

   // Instantiate an output spy buffer
   reg [W-1:0] sb2_din = 1'b0;   // to be driven by python code
   reg sb2_dvin = 1'b0;  // python
   wire sb2_empty;
   wire sb2_ren = !sb2_empty;
   wire sb2_afull;
   SpyBuffer 
     #(.DATA_WIDTH(W-1))  // exclusive of metadata flag bit
   sb2
     (.rclock(clk), .wclock(clk), .rreset(rst), .wreset(rst),
      .write_data(sb2_din), .write_enable(sb2_dvin),
      .read_enable(sb2_ren),
      .read_data(dout),
      .almost_full(sb2_afull),
      .empty(sb2_empty),
      // The following should not be needed until one actually wants
      // to use the spy-buffer functionality, whereas for now we just
      // want to use the fifo functionality.
      .freeze(1'b0),
      .spy_read_enable(1'b0), .spy_meta_read_enable(1'b0),
      .spy_read_addr(1'b0), .spy_meta_read_addr(1'b0),
      .spy_write_addr(), .spy_meta_write_addr(),
      .spy_data(), .spy_meta_read_data());
   
   reg sb2_dvout = 0;
   always @ (posedge clk) begin
      // check this: we are assuming that sb2_dout is valid one clock
      // cycle after we request next word
      sb2_dvout <= sb2_ren;
   end

   // Output of toy "chip" is output of second spy buffer
   assign dout_valid = sb2_dvout;
endmodule // tp

`default_nettype wire

