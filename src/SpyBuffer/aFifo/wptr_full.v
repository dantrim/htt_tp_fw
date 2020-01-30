
`timescale 1ns/1ps

module wptr_full  #(parameter ADDRSIZE = 4,
                    parameter ALMOSTFULL = 1)
   (
    output wire                wfull,
    output wire                walmostfull,
    output wire [ADDRSIZE-1:0] waddr,
    output wire [ADDRSIZE  :0] wptr,
    input  wire [ADDRSIZE  :0] wq2_rptr,
    input  wire                winc,
    input  wire                wclk,
    input  wire                wrst_n
    );
   
   reg [ADDRSIZE:0] 	      wbin;
   wire [ADDRSIZE:0] 	      wgraynext, wbinnext;
   wire [ADDRSIZE:0] 	      wgraynextnext, wbinnextnext;
   wire [ADDRSIZE:0] 	      wgraynextby2, wbinnextby2;

   wire 		      walmostfull_val;

   reg                wfull_int;
   reg                walmostfull_int;
   reg [ADDRSIZE  :0] wptr_int;
   assign wfull = wfull_int;
   assign walmostfull = walmostfull_int;
   assign wptr = wptr_int;
   
   
   // GRAYSTYLE2 pointer
   always @(posedge wclk or negedge wrst_n)
     if (!wrst_n) {wbin, wptr_int} <= {{ADDRSIZE{1'b0}}, 1'b0,
				   {ADDRSIZE{1'b0}}, 1'b0};
     else         {wbin, wptr_int} <= {wbinnext, wgraynext};
   
   // Memory write-address pointer (okay to use binary to address memory)
   assign waddr = wbin[ADDRSIZE-1:0];
   assign wbinnext  = wbin + (winc & ~wfull_int);
   assign wgraynext = (wbinnext>>1) ^ wbinnext;

   /*
    * Almost full by 1
    */
   assign wbinnextnext  = wbinnext + 1'b1;
//   assign wbinnextnext  = wbin + (winc & ~wfull_int) + (~wfull_int);
   assign wgraynextnext = (wbinnextnext>>1) ^ wbinnextnext;


   
   /*
    * Almost full by 2
    */
   assign wbinnextby2  = wbinnext + 2'd2;
//   assign wbinnextnext  = wbin + (winc & ~wfull_int) + (~wfull_int);
   assign wgraynextby2 = (wbinnextby2>>1) ^ wbinnextby2;
   
   //------------------------------------------------------------------
   // Simplified version of the three necessary full-tests:
   // assign wfull_val=((wgnext[ADDRSIZE]    !=wq2_rptr[ADDRSIZE]  ) &&
   //                   (wgnext[ADDRSIZE-1]  !=wq2_rptr[ADDRSIZE-1]) &&
   //                   (wgnext[ADDRSIZE-2:0]==wq2_rptr[ADDRSIZE-2:0]));
   //------------------------------------------------------------------
   assign wfull_val = (wgraynext=={~wq2_rptr[ADDRSIZE:ADDRSIZE-1],
                                   wq2_rptr[ADDRSIZE-2:0]});

   generate
      if ( ALMOSTFULL == 1 )
	/*
	 * Almost full by 1
	 */
	 assign walmostfull_val = (wfull_val || 
			     (wgraynextnext=={~wq2_rptr[ADDRSIZE:ADDRSIZE-1],
					      wq2_rptr[ADDRSIZE-2:0]}));
      else if ( ALMOSTFULL == 2 )
	/*
	 * Almost full by 2
	 */
	assign walmostfull_val = (wfull_val ||
			     (wgraynextnext=={~wq2_rptr[ADDRSIZE:ADDRSIZE-1],
					      wq2_rptr[ADDRSIZE-2:0]}) ||
			     (wgraynextby2=={~wq2_rptr[ADDRSIZE:ADDRSIZE-1],
					      wq2_rptr[ADDRSIZE-2:0]}));
      else
	assign walmostfull_val = 1'b0;
   endgenerate
 
   
   always @(posedge wclk or negedge wrst_n)
     if (!wrst_n) begin
	wfull_int  <= 1'b0;
	walmostfull_int <= 1'b0;
     end
     else begin
        wfull_int  <= wfull_val;
	walmostfull_int <= walmostfull_val;
     end
   
endmodule // wptr_full
