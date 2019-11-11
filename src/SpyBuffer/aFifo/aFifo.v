`timescale 1ns/1ps
`default_nettype none

module aFifo #(parameter DSIZE = 8,
               parameter ASIZE = 4,
               parameter ALMOSTFULL = 1)
   (
    output wire [DSIZE-1:0] rdata,
    output wire             wfull,
    output wire             walmostfull,
    output wire             rempty,
    output wire             ralmostempty,
    input  wire [DSIZE-1:0] wdata,
    input  wire             winc, wclk, wrst_n,
    input  wire             rinc, rclk, rrst_n
    );

   wire [ASIZE-1:0]    waddr, raddr;
   wire [ASIZE:0]      wptr, rptr, wq2_rptr, rq2_wptr;

   sync_r2w #(.ADDRSIZE(ASIZE)) sync_r2w  (.wq2_rptr(wq2_rptr), .rptr(rptr),
				.wclk(wclk), .wrst_n(wrst_n));
   sync_w2r #(.ADDRSIZE(ASIZE)) sync_w2r  (.rq2_wptr(rq2_wptr), .wptr(wptr),
				.rclk(rclk), .rrst_n(rrst_n));

   fifomem #(.DATASIZE(DSIZE), .ADDRSIZE(ASIZE)) fifomem
     (.rdata(rdata), .wdata(wdata),
      .waddr(waddr), .raddr(raddr),
      .wclken(winc), .wfull(wfull),
      .wclk(wclk)/*, .rclk(rclk)*/);

   rptr_empty #(.ADDRSIZE(ASIZE))     rptr_empty
     (.rempty(rempty), .ralmostempty(ralmostempty),
      .raddr(raddr),
      .rptr(rptr),
      .rq2_wptr(rq2_wptr),
      .rinc(rinc), .rclk(rclk),
      .rrst_n(rrst_n));

   wptr_full  #(.ADDRSIZE(ASIZE), .ALMOSTFULL(ALMOSTFULL))     wptr_full
     (.wfull(wfull), .walmostfull(walmostfull), .waddr(waddr),
      .wptr(wptr), .wq2_rptr(wq2_rptr),
      .winc(winc), .wclk(wclk),
      .wrst_n(wrst_n));

endmodule // fifo1

