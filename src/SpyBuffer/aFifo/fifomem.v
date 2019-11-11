`timescale 1ns/1ps

module fifomem #(parameter  DATASIZE = 8, // Memory data word width
                 parameter  ADDRSIZE = 4) // Number of mem address bits
   (
    output wire  [DATASIZE-1:0] rdata,
    input  wire [DATASIZE-1:0] wdata,
    input  wire [ADDRSIZE-1:0] waddr,
    input  wire [ADDRSIZE-1:0] raddr,
    input  wire                wclken,
    input  wire                wfull,
    input  wire                wclk/*,
    input  wire                rclk*/
    );

   // RTL Verilog memory model
   localparam DEPTH = 1<<ADDRSIZE;
   reg [DATASIZE-1:0] 	  mem [0:DEPTH-1];

   assign rdata = mem[raddr];

   // NOTE: Modification to original aFifo needs testing!
   // NOTE: so this does not work. It introduces extra latency into the readout.
   // How do we fix it? I don't know.
   //always @(posedge rclk)
   //  rdata <= mem[raddr];

   always @(posedge wclk)
     if (wclken && !wfull) mem[waddr] <= wdata;

endmodule // fifomem

