`timescale 1ns/1ps
module cluster_routing_engine #(
				parameter DATA_WIDTH=65,
				parameter TOTAL_BOARDS = 14,
				parameter CRE_ID=0,
				parameter FIFO_DEPTH_BITS = 9,
				parameter THIS_MODULE="B2B",
				parameter BOARD_ID=0
		     )
   ( 
     input logic 			b2b_clk,
     input logic 			b2b_rst_n,
     input logic 			b2b_srst_n,
     input logic [DATA_WIDTH-1:0] 	cluster_event,
     output logic 			cluster_req,
     input logic 			cluster_almost_full,
     input logic 			cluster_empty,
     
     output logic [DATA_WIDTH-1:0] 	board_event[TOTAL_BOARDS], 
     input logic 			board_req[TOTAL_BOARDS],
 //    output logic [TOTAL_BOARDS-1 : 0] 	board_almost_full,
//     output logic [TOTAL_BOARDS-1:0] 	board_half_full,  
     output logic 			board_full[TOTAL_BOARDS],
     output logic 			board_empty[TOTAL_BOARDS],
     output logic [FIFO_DEPTH_BITS : 0] board_rd_count[TOTAL_BOARDS]
     );

`include "TP_DataFormat.sv"
   
   parameter TRK_TYPE_WIDTH   =     2;
   enum 			   bit[2:0] {PARSE_E_HDR, TX_E_HDR, TX_MHDR_EFTR,TX_M,TX_E_FTR} b2b_cluster_state;

   
   
   logic [3:0] 			   count;
   logic [TRK_TYPE_WIDTH-1:0] 	   trk;
   logic 			   cluster_vld;
   
   logic 			   cluster_empty_d;
   logic [TOTAL_BOARDS-1 : 0] 	   board_almost_full;   
   logic [TOTAL_BOARDS-1:0] 	   b_almost_full;  
   logic [TOTAL_BOARDS-1:0] 	   fifo_wr_rst_busy;
   logic [TOTAL_BOARDS-1:0] 	   fifo_rd_rst_busy;
  
   
   logic [DATA_WIDTH-1:0] 	   board_i_event[TOTAL_BOARDS];
   logic 			   board_i_vld[TOTAL_BOARDS];
   logic 			   board_route_flag[TOTAL_BOARDS];
   logic 			   pixel0_strip1;
   logic 			   pending_m_ftr;
   logic 			   pending_m_hdr;
   
   
   genvar 			   m;
  // integer 			   z;
   

   assign cluster_vld = ~cluster_empty & cluster_req;
   

   generate
      for(genvar k=0; k<TOTAL_BOARDS; k++)
	begin
	   assign b_almost_full[k] = board_almost_full[k];
	end
   endgenerate
   
     generate
	for(genvar z=0;z<TOTAL_BOARDS;z++)
	  begin:board_fifos
	     fifo_65 cre_fifo (
			       .clk(b2b_clk),
			       .srst(!(b2b_rst_n & b2b_srst_n)),
			       .din(board_i_event[z]),       
			       .wr_en(board_i_vld[z]),       
			       .rd_en(board_req[z]),              
			       .dout(board_event[z]),                
			       .full(board_full[z]),
			       //.almost_full(board_almost_full[z]),
			       .prog_full(board_almost_full[z]),
			       .data_count(board_rd_count[z]),			      
			     //  .prog_empty(board_half_full[z]),      // output wire prog_empty
			       .wr_rst_busy(fifo_wr_rst_busy[z]),    // output wire wr_rst_busy
			       .rd_rst_busy(fifo_rd_rst_busy[z]),    // output wire rd_rst_busy
			       .empty(board_empty[z])             
			       );  
	  
	     
	end // for (integer z=0;z<TOTAL_BOARDS;z++)
   endgenerate



   
   //Cluster clock domain
   always @ (posedge b2b_clk)
     begin
	if((!b2b_rst_n) | (!b2b_srst_n) | (fifo_wr_rst_busy & fifo_rd_rst_busy))
	  begin
	     cluster_req          <= 0;
	     cluster_empty_d      <= 0;
	     count                <= 4'b0;
	     b2b_cluster_state    <= PARSE_E_HDR;
	     pixel0_strip1        <= 0;
	     pending_m_ftr        <= 0;
	     pending_m_hdr        <= 0;
	     
	     for(integer k=0; k<TOTAL_BOARDS; k++)
	       begin
		  board_i_event[k]       <= 0;
		  board_i_vld[k]         <= 0;
		  board_route_flag[k]    <= 0;
		  
	       end
	  end
	else 
	  begin
	     cluster_empty_d             <= cluster_empty;
	     
	     for(integer k=0; k<TOTAL_BOARDS; k++)
	       board_i_event[k]              <= cluster_event;
	     
	     if((!cluster_empty) & (b_almost_full == 0)) 
	       begin
		  cluster_req <= 1'b1;		
	       end
	     else
	       begin
		  cluster_req <= 1'b0;		
	       end
	     if(cluster_vld)
	       begin
		  case(b2b_cluster_state)
		    PARSE_E_HDR:
		      begin
			 pixel0_strip1      <= 0;
			 pending_m_ftr      <= 0;
			 pending_m_hdr      <= 0;
			 
			 for(integer k=0; k<TOTAL_BOARDS; k++)
			   begin
			      board_route_flag[k] <= 0;
			   end
			 if((cluster_event[DATA_WIDTH-1]==1) && (cluster_event[EVT_HDR_W1_FLAG_msb:EVT_HDR_W1_FLAG_lsb] == EVT_HDR_W1_FLAG_FLAG))
			   begin
			   
			      for(integer k=0; k<TOTAL_BOARDS; k++)
				begin
				   if(k != BOARD_ID)
				     begin
					board_i_vld[k]         <= 1'b1;
				     end
				   else
				     board_i_vld[BOARD_ID]           <= 1'b0;
				end
			      count                      <= 1;
			      b2b_cluster_state          <= TX_E_HDR;
			   end
			 else //TODO - Timeout if waiting for a long time
			   begin
			      for(integer k=0; k<TOTAL_BOARDS; k++)
				begin
				   board_i_vld[k]                <= 0;
				end
			      b2b_cluster_state           <= PARSE_E_HDR;
			      count                       <= 0;
			   end
		      end // case: PARSE_E_HDR
		    TX_E_HDR:
		      begin
			 pixel0_strip1      <= 0;
			 pending_m_ftr      <= 0;
			 pending_m_hdr      <= 0;
			 for(integer k=0; k<TOTAL_BOARDS; k++)
			   begin
			      board_route_flag[k] <= 0;
			   end
			 if(!cluster_empty_d)
			   begin
			      if(count == EVT_HDR_LWORDS-1)
				begin
				   b2b_cluster_state      <= TX_MHDR_EFTR;
				   count                  <= 0;
				end
			      else
				begin
				   count                  <= count + 1;
				end
		      end // if (!cluster_empty_d)
			 
			 
			 if(cluster_empty) //TODO same check for board_almost_full[m], stop requesting data
			   begin
			      for(integer k=0; k<TOTAL_BOARDS; k++)
				begin
				   board_i_vld[k]                  <= 1'b0;
				end
			   end
			 else
			   begin
			    
			      for(integer k=0; k<TOTAL_BOARDS; k++)
				begin
				   if(k != BOARD_ID)
				     board_i_vld[k]                <= 1'b1;
				   else
				     board_i_vld[k]                <= 1'b0;
				   
				end
			      if(b_almost_full != 0)
				begin
				end
			      else
				begin
				end
			   end // else: !if(cluster_empty)
			 
		      end // case: TX_E_HDR
		    
		    TX_MHDR_EFTR: //First long word of module header or event Footer
		      begin
			 count                           <= 0;
			 pending_m_ftr                   <= 0;
			 if(!cluster_empty_d)
			   begin
			      if((cluster_event[DATA_WIDTH-1]==1) && (cluster_event[M_HDR_FLAG_msb:M_HDR_FLAG_lsb] == M_HDR_FLAG_FLAG))
				begin
				   pixel0_strip1     <= cluster_event[M_HDR_DET_msb];//cluster_event[M_HDR_DET_msb:M_HDR_DET_lsb];
				   if(THIS_MODULE == "B2B")
				     begin
					for(integer k=M_HDR_ROUTING_TFM_lsb-1, int j=TOTAL_BOARDS-3; k > 3; k=k-4,j--)
					  begin
					     if(j != BOARD_ID)
					       begin
						  board_i_vld[j]       <=  (cluster_event[k -: 3]===4'b0)? 0 : 1;
						  board_route_flag[j]  <=  (cluster_event[k -: 3]===4'b0)? 0 : 1;
						  //	$display("k=%d, cluster_event[%d : %d] = 0x%x, board_i_vld[%d]=%d", k, k, k-3, cluster_event[k -: 3], j, 	board_i_vld[j] );
					       end
					     else
					       begin
						  board_i_vld[BOARD_ID]      <= 0;
						  board_route_flag[BOARD_ID] <= 0;
					       end
					  end
					
					
					for(integer k=M_HDR_ROUTING_msb, int j=TOTAL_BOARDS-1; k > M_HDR_ROUTING_TFM_lsb ; k=k-2,j--)
					  begin
					     begin
						if(j != BOARD_ID)
						  begin
						     board_i_vld[j]      <=  (cluster_event[k -: 1]===4'b0)? 0 : 1;
						     board_route_flag[j] <=  (cluster_event[k -: 1]===4'b0)? 0 : 1;
						  end
						else
						  begin
						     board_i_vld[BOARD_ID]      <= 0;
						     board_route_flag[BOARD_ID] <= 0;		      
						  end
					     end
					  end // for (integer k=M_HDR_ROUTING_msb, int j=TOTAL_BOARDS-1; k > M_HDR_ROUTING_TFM_lsb ; k=k-2,j--)
				     end // if (THIS_MODULE == "B2B")
				   else
				     begin
					if(BOARD_ID < 12)
					  begin
					     for(integer z=0;  z < TOTAL_BOARDS; z=z+1)
					       begin
						  board_i_vld[z] = cluster_event[ (z << 2) + z + 1];
					       end
					  end
					else
					  begin
					     for(integer z=0;  z<TOTAL_BOARDS; z=z+1)
						 begin
						    //Need Routing Flag definition for TFM in SSTP (only two bits available)
						 end
					  end
				     end // else: !if(THIS_MODULE == "B2B")
				   
				   b2b_cluster_state              <= TX_M; //_HDR;
				   pending_m_hdr                  <= 1;
				end
			      else if ( (cluster_event[DATA_WIDTH-1]==1) && (cluster_event[EVT_FTR_W1_FLAG_msb:EVT_FTR_W1_FLAG_lsb] == EVT_FTR_W1_FLAG_FLAG ))
				begin
				   pending_m_hdr              <= 0;
				   
				   for(integer k=0; k<TOTAL_BOARDS; k++)
				     begin
					board_route_flag[k] <=  0;
				     end
				   for(integer k=0; k<TOTAL_BOARDS; k++)
				     begin
					if(k!=BOARD_ID)
					  board_i_vld[k]               <= 1'b1;
					else
					  board_i_vld[BOARD_ID]      <= 0;
				     end
				   
				   b2b_cluster_state          <= TX_E_FTR;
				   count                      <= 1;
				   pixel0_strip1              <= 0;
				end
			      else //ERROR
				begin
				   pending_m_hdr      <= 0;
				   for(integer k=0; k<TOTAL_BOARDS; k++)		
				     begin
					board_i_vld[k]               <= 0;
				     end
				end 
			   end // if (!cluster_empty_d)
			 else
			   begin
			      pending_m_hdr      <= 0;
			      for(integer k=0; k<TOTAL_BOARDS; k++)
			   begin
			      board_i_vld[k]                    <= 0;
			   end
			   end // else: !if(!cluster_empty_d)
		      end // case: TX_MHDR_EFTR	
		    TX_M:
		      begin
			 if(pixel0_strip1 == 0) //pixel
			   begin
			     // $display($time, "CRE_ID=%d ROUTING ENGINE Pixel cluster_event = 0x%x\n",CRE_ID,cluster_event);
			      if(~pending_m_ftr & cluster_event[PIXEL_CLUSTER_LAST_lsb])
				begin
				   pending_m_ftr         <= 1;
				   pending_m_hdr         <= 0;
				   b2b_cluster_state     <= TX_M;
				   if(cluster_empty)
				     begin
					for(integer k=0; k<TOTAL_BOARDS; k++)
					  begin
					     board_i_vld[k]                  <= 1'b0;
					  end
				     end
				   else//ERROR, stall and timeout if event Footer does not arrive for long time
				     for(integer k=0; k<TOTAL_BOARDS; k++)
				       begin
					  board_i_vld[k]        <= board_route_flag[k];
				       end
				end // if (~pending_m_ftr & cluster_event[PIXEL_CLUSTER_LAST_lsb])
			      else if(~pending_m_ftr & ~pending_m_hdr & cluster_event[PIXEL_CL_FTR_FLAG_msb: PIXEL_CL_FTR_FLAG_lsb] == PIXEL_CL_FTR_FLAG_FLAG  & (cluster_event[32 + PIXEL_CLUSTER_LAST_lsb]))
				begin
				   b2b_cluster_state     <= TX_MHDR_EFTR;
				   pending_m_hdr         <= 0;
				   if(cluster_empty)
				     begin
					for(integer k=0; k<TOTAL_BOARDS; k++)
					  begin
					     board_i_vld[k]                  <= 1'b0;
					  end
				     end
				   else 
				     begin
					for(integer k=0; k<TOTAL_BOARDS; k++)
					  begin
					     board_i_vld[k]        <= board_route_flag[k];
					  end
				     end
				end // if (~pending_m_ftr & cluster_event[PIXEL_CL_FTR_FLAG_msb: PIXEL_CL_FTR_FLAG_lsb] == PIXEL_CL_FTR_FLAG_FLAG  & (cluster_event[32 + PIXEL_CLUSTER_LAST_lsb]))
			      else if(pending_m_ftr)
				begin
				   if( cluster_event[32 + PIXEL_CL_FTR_FLAG_msb: 32 + PIXEL_CL_FTR_FLAG_lsb] == PIXEL_CL_FTR_FLAG_FLAG)
				     begin
					b2b_cluster_state     <= TX_MHDR_EFTR;
					pending_m_ftr         <= 0;
					pending_m_hdr         <= 0;
					if(cluster_empty)
					  begin
					     for(integer k=0; k<TOTAL_BOARDS; k++)
					       begin
						  board_i_vld[k]                  <= 1'b0;
					       end
					  end
					else
					  begin
					     for(integer k=0; k<TOTAL_BOARDS; k++)
					       begin
						  board_i_vld[k]        <= board_route_flag[k];
					       end
					  end // else: !if(cluster_empty)
				     end // if ( cluster_event[32 + PIXEL_CL_FTR_FLAG_msb: 32 + PIXEL_CL_FTR_FLAG_lsb] == PIXEL_CL_FTR_FLAG_FLAG)
				   else
				     begin
					$display($time,", CRE_ID=%d ROUTE ENGINE, PIXEL MODULE FOOTER NOT RECEIVED!!0x%x prev=x%x",CRE_ID,cluster_event,board_i_event[0]);
					#100
					  $finish();
					
				     end
				end // if (pending_m_ftr)
			      else
				begin
				   pending_m_hdr         <= 0;
				   for(integer k=0; k<TOTAL_BOARDS; k++)
				     begin
					board_i_vld[k]        <= board_route_flag[k];
				     end
				end // else: !if(pending_m_ftr)
			   end // if (pixel0_strip1 == 0)
			 else
			   begin
			  //    $display($time, ":CRE_ID=%d. ROUTING ENGINE Strip cluster_event = 0x%x\n",CRE_ID,cluster_event);
			      if ( ~pending_m_ftr & cluster_event[STRIP_CLUSTER_LAST_msb])
				begin
				   pending_m_ftr         <= 1;
				   pending_m_hdr         <= 0;
				   b2b_cluster_state     <= TX_M;
				   if(cluster_empty)
				     begin
					for(integer k=0; k<TOTAL_BOARDS; k++)
					  begin
					     board_i_vld[k]                  <= 1'b0;
					  end
				     end
				   else//ERROR, stall and timeout if event Footer does not arrive for long time
				     for(integer k=0; k<TOTAL_BOARDS; k++)
				       begin
					  board_i_vld[k]        <= board_route_flag[k];
				       end
				end
			      else if(~pending_m_ftr & 
				      (((cluster_event[STRIP_CL_FTR_FLAG_msb: STRIP_CL_FTR_FLAG_lsb] == STRIP_CL_FTR_FLAG_FLAG) & cluster_event[STRIP_CLUSTER_bits + STRIP_CLUSTER_LAST_msb ] )
				       |(~pending_m_hdr & ((cluster_event[16+STRIP_CL_FTR_FLAG_msb: STRIP_CLUSTER_bits+STRIP_CL_FTR_FLAG_lsb]   == STRIP_CL_FTR_FLAG_FLAG) & cluster_event[STRIP_CLUSTER_bits*2 + STRIP_CLUSTER_LAST_msb ] )) 
				       |(~pending_m_hdr & ((cluster_event[32+STRIP_CL_FTR_FLAG_msb: STRIP_CLUSTER_bits*2+STRIP_CL_FTR_FLAG_lsb] == STRIP_CL_FTR_FLAG_FLAG) & cluster_event[STRIP_CLUSTER_bits*3 +STRIP_CLUSTER_LAST_msb ]))//=> check last condition only when not module hdr W2
				       ))
				begin
				   b2b_cluster_state     <= TX_MHDR_EFTR;
				   pending_m_hdr         <= 0;
				   if(cluster_empty)
				     begin
					for(integer k=0; k<TOTAL_BOARDS; k++)
					  begin
					     board_i_vld[k]                  <= 1'b0;
					  end
				     end
				   else
				     begin
					for(integer k=0; k<TOTAL_BOARDS; k++)
					  begin
					     board_i_vld[k]        <= board_route_flag[k];
					  end
				     end // else: !if(cluster_empty)
			//	   $display($time, ": CRE_ID=%d Last strip cluster_event = 0x%x\n",CRE_ID,cluster_event);
				end
			      else if(pending_m_ftr)
				begin
				   pending_m_hdr      <= 0;
				   if( cluster_event[48 + STRIP_CL_FTR_FLAG_msb: 48 + STRIP_CL_FTR_FLAG_lsb] == STRIP_CL_FTR_FLAG_FLAG)
				     begin
					b2b_cluster_state     <= TX_MHDR_EFTR;
					pending_m_ftr         <= 0;
					if(cluster_empty)
					  begin
					     for(integer k=0; k<TOTAL_BOARDS; k++)
					       begin
						  board_i_vld[k]                  <= 1'b0;
					       end
					  end
					else
					  begin
					     for(integer k=0; k<TOTAL_BOARDS; k++)
					       begin
						  board_i_vld[k]        <= board_route_flag[k];
					       end
					  end
				     end // if ( cluster_event[48 + STRIP_CL_FTR_FLAG_msb: 48 + STRIP_CL_FTR_FLAG_lsb] == STRIP_CL_FTR_FLAG_FLAG)
				   else
				     begin
					$display($time,", :CRE_ID=%d ROUTE ENGINE, STRIP MODULE FOOTER NOT RECEIVED!!0x%x prev=x%x",CRE_ID,cluster_event,board_i_event[0]);
					#10000
					  $finish();
					
				     end // else: !if( cluster_event[48 + STRIP_CL_FTR_FLAG_msb: 48 + STRIP_CL_FTR_FLAG_lsb] == STRIP_CL_FTR_FLAG_FLAG)
				end // if (pending_m_ftr)
			      else
				begin
				   pending_m_hdr      <= 0;
				   for(integer k=0; k<TOTAL_BOARDS; k++)
				     begin
					board_i_vld[k]        <= board_route_flag[k];
				     end
				end
			   end // else: !if(pixel0_strip1 == 1)
		      end // case: TX_M
		    TX_E_FTR: //Remaining long words of event Footer
		      begin
			 pending_m_hdr      <= 0;
			 for(integer k=0; k<TOTAL_BOARDS; k++)
			   begin
			      board_route_flag[k] <= 0;
			   end
			 if(!cluster_empty_d)
			   begin
			      if(count == EVT_FTR_LWORDS-1)
				begin
				   b2b_cluster_state             <= PARSE_E_HDR;
				   count                         <= 0;
				end
			 else
			   begin
			      count                         <= count + 1;
			   end
		      end // if (!cluster_empty_d)
			 
			 
			 if(cluster_empty)
			   begin
			      for(integer k=0; k<TOTAL_BOARDS; k++)
				begin
				   board_i_vld[k]                  <= 1'b0;
				end
			   end
			 else
			   begin
			    
			      for(integer k=0; k<TOTAL_BOARDS; k++)
				begin
				   if(k!=BOARD_ID)
				     board_i_vld[k]                  <= 1'b1;
				   else
				     board_i_vld[BOARD_ID]           <= 1'b0;
				end
			   end // else: !if(cluster_empty)
			 
		      end // case: TX_E_FTR
		    
		    
		  endcase // case (b2b_cluster_state)
	       end // if (cluster_vld)
	     else
	       begin
		  for(integer k=0; k<TOTAL_BOARDS; k++)
		    begin
		       board_i_vld[k]                  <= 1'b0;
		    end
	       end // else: !if(cluster_vld)
	     
	     
	  end // else: !if(!b2b_rst_n)
	
     end // always @ (posedge b2b_clk)
   
   
   
   
endmodule // b2b_cluster

