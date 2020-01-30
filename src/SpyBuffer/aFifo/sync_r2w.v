`timescale 1ns/1ps

module sync_r2w #(parameter ADDRSIZE = 4)
   (
    output wire [ADDRSIZE:0] wq2_rptr,
    input wire     [ADDRSIZE:0] rptr,
    input wire                  wclk,
    input wire                  wrst_n
    );
   
   reg [ADDRSIZE:0] 	    wq1_rptr;
   reg [ADDRSIZE:0] 	    wq2_rptr_int;
   assign wq2_rptr = wq2_rptr_int;
   
		    
   always @(posedge wclk or negedge wrst_n)
     if (!wrst_n) {wq2_rptr_int,wq1_rptr} <= {{ADDRSIZE{1'b0}}, 1'b0,
					  {ADDRSIZE{1'b0}}, 1'b0};
     else         {wq2_rptr_int,wq1_rptr} <= {wq1_rptr,rptr};
   
endmodule // sync_r2w
