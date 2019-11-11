`timescale 1ns/1ps
`default_nettype none
  
module rptr_empty #(parameter ADDRSIZE = 4)
   (
    output wire                 rempty,
    output wire                ralmostempty,
    output wire [ADDRSIZE-1:0] raddr,
    output wire [ADDRSIZE  :0] rptr,
    input  wire [ADDRSIZE  :0] rq2_wptr,
    input  wire                rinc,
    input  wire                rclk,
    input  wire                rrst_n
    );
   
   reg [ADDRSIZE:0] 	      rbin;
   wire [ADDRSIZE:0] 	      rgraynext, rbinnext;
   wire [ADDRSIZE:0] 	      rgraynextnext, rbinnextnext;

   wire rempty_val;
   wire ralmostempty_val;

   reg 	rempty_int;
   reg 	ralmostempty_int;
   reg [ADDRSIZE  :0] rptr_int;
   assign rempty = rempty_int;
   assign ralmostempty = ralmostempty_int;
   assign rptr =  rptr_int;
   
   
   
   //-------------------
   // GRAYSTYLE2 pointer
   //-------------------
   always @(posedge rclk or negedge rrst_n)
     if (!rrst_n) {rbin, rptr_int} <= {{ADDRSIZE{1'b0}}, 1'b0,
				   {ADDRSIZE{1'b0}}, 1'b0};
     else         {rbin, rptr_int} <= {rbinnext, rgraynext};
   
   // Memory read-address pointer (okay to use binary to address memory)
   assign raddr     = rbin[ADDRSIZE-1:0];
   assign rbinnext  = rbin + (rinc & ~rempty_int);
   assign rgraynext = (rbinnext>>1) ^ rbinnext;

   /*
    * Almost empty
    */
   assign rbinnextnext  = rbinnext + 1'b1;
   assign rgraynextnext = (rbinnextnext>>1) ^ rbinnextnext;
   
   //---------------------------------------------------------------
   // FIFO empty when the next rptr == synchronized wptr or on reset
   //---------------------------------------------------------------
   assign rempty_val = (rgraynext == rq2_wptr);

   assign ralmostempty_val = (rgraynextnext == rq2_wptr);
   
   always @(posedge rclk or negedge rrst_n)
     if (!rrst_n) rempty_int <= 1'b1;
     else         rempty_int <= rempty_val;

   always @(posedge rclk or negedge rrst_n)
     if (!rrst_n) ralmostempty_int <= 1'b1;
     else         ralmostempty_int <= ralmostempty_val | rempty_val;
   
endmodule // rptr_empty

`default_nettype wire
