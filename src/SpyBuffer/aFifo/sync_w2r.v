
`timescale 1ns/1ps

module sync_w2r #(parameter ADDRSIZE = 4)
   (
    output wire [ADDRSIZE:0] rq2_wptr,
    input  wire [ADDRSIZE:0] wptr,
    input  wire              rclk,
    input  wire              rrst_n
    );
   
   reg [ADDRSIZE:0] 	    rq1_wptr;
   reg [ADDRSIZE:0] 	    rq2_wptr_int;
   assign rq2_wptr = rq2_wptr_int;
   
   
   always @(posedge rclk or negedge rrst_n)
     if (!rrst_n) {rq2_wptr_int,rq1_wptr} <= {{ADDRSIZE{1'b0}}, 1'b0,
					  {ADDRSIZE{1'b0}}, 1'b0};
     else         {rq2_wptr_int,rq1_wptr} <= {rq1_wptr,wptr};
   
endmodule // sync_w2r
