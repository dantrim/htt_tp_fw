`timescale 1ns/1ps

module merge_event_handler #(
			     parameter DATA_WIDTH = 65,
			     parameter EVT_HDR_BITS=40,
			     parameter MEH_ID=0
			     )
   (	
	input logic 			clk,
	input logic 			rst_n,
	input logic 			srst_n,
	input logic [DATA_WIDTH-1:0] 	cluster_evt,
	output logic 			cluster_evt_req,
//	input logic 			cluster_almost_full,
	input logic 			cluster_full,
	input logic 			cluster_empty,
	input logic [1:0] 		evt_ctrl,
	output logic [EVT_HDR_BITS-1:0] evt_l0id,
	output logic [1:0] 		evt_available,
	input logic 			cluster_evt2b_almost_full,
	output logic [DATA_WIDTH-1:0] 	cluster_evt2b,
	output logic 			cluster_evt2b_wren	
    );
`include "TP_DataFormat.sv"
   enum 				bit [1:0] {E_NOT_AV, EHDR_AV, M_AV, EFTR_AV}evt_state;
   
  
   enum 				bit[3:0] {E_HDR_REQ, E_HDR_HNDLR, MHDR_EFTR_REQ ,M_HDR_TX, M_TX,  E_FTR_HNDLR, E_REQ}evt_hndlr_state;

   //enum 	     bit[1:0] {WAIT, TX, DROP};
   parameter  WAIT = 0;
   parameter  TX   = 1;
   parameter  DROP = 2;
   
   logic [3:0] 				counter;
   logic [3:0] 				prev_evt_hndlr_state;
   
   logic 				fifo_rdy;
   logic 				fifo_rdy_shft;
   
   logic [1:0] 				evt_ctrl_d;
   logic [3:0] 				tx_wrd_cnt;
   logic 				pixel0_strip1;
   logic 				get_next_cluster;
   logic 				send_module_clusters;
   logic 				pending_m_ftr;
   logic 				pending_m_hdr;
   
   
   logic 				evt_hdr_available;
   logic 				evt_ftr_available;
   logic 				cluster_evt2b_wren_internal;
   logic 				get_hdr;
   logic 				cluster_empty_d;
   logic 				cluster_empty_negedge;
   logic [EVT_HDR_BITS-1:0] 		evt_l0id_i;
   
   
  
   
     
   assign fifo_rdy        = ~cluster_evt2b_almost_full & ~cluster_empty ;
   assign cluster_evt_req = fifo_rdy & get_next_cluster & (get_hdr  || evt_ctrl == TX || evt_ctrl == DROP);
   assign cluster_evt2b_wren    =  cluster_evt_req; //cluster_evt2b_wren_internal;
   assign cluster_evt2b         = cluster_evt;
   assign cluster_empty_negedge = (~cluster_empty) & cluster_empty_d;
   
   always_comb
     begin
	evt_available = evt_state;
	evt_l0id      = evt_l0id_i;
     end // always_comb
   
   
  

     always @ (posedge clk)
       begin
	  if(!rst_n | !srst_n)
	    begin
	       evt_ctrl_d                  <= 0;
	       counter                     <= 0;	   
	       cluster_evt2b_wren_internal <= 1'b0;
	       cluster_empty_d             <= 1'b0;
	   	       
	    end
	  else
	    begin
	       evt_ctrl_d           <= evt_ctrl;
	       cluster_empty_d      <= cluster_empty;
	      
	       
	       case(evt_ctrl)
		 WAIT : begin
		    cluster_evt2b_wren_internal <= 1'b0;
		    if(cluster_empty)
		      counter <= 0;
		    else
		      counter <= 1;
		    
		    
		 //     end
		 end // case: WAIT
		 
		 TX   : begin	
		    if(~cluster_empty)
		      begin
			 
			 cluster_evt2b_wren_internal <= 1'b1;
			 
			 if(counter == tx_wrd_cnt  || send_module_clusters == 1)
			   begin
			      counter           <= 0;
			   end
			 else 
			   begin
			      counter            <= counter + 1'b1;
			   end
		      end 
		    else
		      begin
			 cluster_evt2b_wren_internal <= 1'b0;
		      end
		   
		 end // case: TX
		 DROP:
		   begin
		      cluster_evt2b_wren_internal <= 1'b0;		
		      if(~cluster_empty)
			begin
		      	   
			   if(counter == tx_wrd_cnt)
			     begin
				counter <= 0;
			     end
			   else
			     begin
				counter <= counter + 1;
			     end
			end
		   end // case: DROP
		 		      
	       endcase
	    end
       end // always @ (posedge clk, negedge rst_n , negedge srst_n)

   
     always @ (posedge clk )
       begin
	  if(!rst_n | !srst_n)
	    begin	    
	       evt_hndlr_state    <= E_HDR_REQ;
	       fifo_rdy_shft      <= 0;
	       tx_wrd_cnt         <= 0;
	       pixel0_strip1      <= 0;
	       get_next_cluster   <= 0;    
	       send_module_clusters <= 1;
	       pending_m_ftr        <= 0;
	       pending_m_hdr        <= 0;
	       evt_l0id_i           <= 0;
	       evt_state            <= E_NOT_AV;
	       get_hdr              <= 0;
	       prev_evt_hndlr_state <= E_HDR_REQ;
	       
	       
	    end // if (!rst_n | !srst_n)
	  else
	    begin
	       fifo_rdy_shft        <= fifo_rdy;
	       send_module_clusters <= 0;
	       prev_evt_hndlr_state <= evt_hndlr_state;
	       
	       
	       case (evt_hndlr_state)
		 E_HDR_REQ:
		   begin
		      tx_wrd_cnt        <= 0;
		      pixel0_strip1     <= 0;
		      pending_m_ftr     <= 0;
		      pending_m_hdr     <= 0;
		      evt_l0id_i        <= 0;		
		   
		      if(cluster_evt[DATA_WIDTH-1] && cluster_evt[EVT_HDR_W1_FLAG_msb:EVT_HDR_W1_FLAG_lsb] == EVT_HDR_W1_FLAG_FLAG)
			begin
			   tx_wrd_cnt           <= EVT_HDR_LWORDS;
			   pixel0_strip1        <= 0;
			   pending_m_ftr        <= 0;
			   pending_m_hdr        <= 0;
			   evt_state            <= EHDR_AV;
			   evt_l0id_i           <= cluster_evt[EVT_HDR_W1_L0ID_msb:EVT_HDR_W1_L0ID_lsb];
			   evt_hndlr_state      <= E_HDR_HNDLR;
			   get_next_cluster     <= 0;
			end
		      else if (fifo_rdy)
			begin
			   if(get_hdr)
			     get_hdr <= 0;
			   else
			     get_hdr <= 1;
			   
			   get_next_cluster  <= 1;
			end	  
		      else
			begin
			   get_hdr           <= 0;
			   get_next_cluster  <= 0;
			end // else: !if(fifo_rdy)
		      

		   end // case: E_HDR_REQ
		 E_HDR_HNDLR,
		 M_HDR_TX,
		 E_FTR_HNDLR:
		   begin
		     
		      pending_m_ftr     <= 0;
		    		    		
		      if(~cluster_empty && counter == tx_wrd_cnt ) 
			begin
			   evt_hdr_available   <= 0;
			   evt_ftr_available   <= 1'b0;
			   tx_wrd_cnt          <= 0;
		
			   
			   if(evt_hndlr_state == E_FTR_HNDLR)
			     begin
				pending_m_hdr        <= 0;
				send_module_clusters <= 0;
				get_next_cluster     <= 0;
				get_hdr              <= 0;
				pixel0_strip1        <= 0;		
				begin
				   evt_hndlr_state   <= E_HDR_REQ;
				   evt_state         <= E_NOT_AV;
				end
			     end
			   else if(evt_hndlr_state == E_HDR_HNDLR)
			     begin
				pending_m_hdr        <= 0;
				evt_hndlr_state      <= MHDR_EFTR_REQ;
				send_module_clusters <= 0;
				evt_state            <= E_NOT_AV;
				get_next_cluster     <= 0;
				get_hdr              <= 1;
				pixel0_strip1        <= 0;			
				
			     end
			   else //M_HDR_TX
			     begin
				evt_hndlr_state      <= M_TX;
				pending_m_hdr        <= 1;
				send_module_clusters <= 1;
				evt_state            <= M_AV;
				get_next_cluster     <= 0;
				get_hdr              <= 1;
			     end
			end // if (counter == tx_wrd_cnt)
		      else
			begin

			   get_hdr            <= 0;
			   get_next_cluster   <= 1;
						 
			end
			/*if(counter == tx_wrd_cnt - 1)
			  begin
			  end
			 */
		   end // case: E_HDR_HNDLR:...
		 MHDR_EFTR_REQ:
		   begin
		      pending_m_ftr        <= 0;	      
		      pending_m_hdr        <= 0;
		      
		      
		      if(cluster_evt_req) // || cluster_empty_negedge)
			begin
			   get_hdr              <= 0;
			   if(cluster_evt[DATA_WIDTH-1] && cluster_evt[M_HDR_FLAG_msb:M_HDR_FLAG_lsb] == M_HDR_FLAG_FLAG)
			     begin
				send_module_clusters <= 1;
				evt_state         <= M_AV;
				evt_hndlr_state   <= M_TX; //M_HDR_TX;
				pending_m_hdr     <= 1;
				tx_wrd_cnt        <= 0; //M_HDR_LWORDS;
				pixel0_strip1     <= cluster_evt[M_HDR_DET_msb];//cluster_evt[M_HDR_DET_msb:M_HDR_DET_lsb];
				get_next_cluster  <= (cluster_evt_req == 0)? 0 : 1;
				//  $display("pixel0_strip1=%d , cluster_evt=0x%x p0s1=%d %d %d \n",pixel0_strip1, cluster_evt, cluster_evt[53], M_HDR_DET_msb, M_HDR_DET_lsb);
				
				send_module_clusters <= 0;
			     end
			   else if(cluster_evt[DATA_WIDTH-1] && cluster_evt[EVT_FTR_W1_FLAG_msb:EVT_FTR_W1_FLAG_lsb] == EVT_FTR_W1_FLAG_FLAG )
			     begin
				send_module_clusters<= 0;
				pending_m_hdr       <= 0;
				evt_ftr_available   <= 1'b1;
				evt_state           <= EFTR_AV;
				evt_hndlr_state     <= E_FTR_HNDLR;
				tx_wrd_cnt          <= EVT_FTR_LWORDS;
				pixel0_strip1       <= 0;
				get_next_cluster    <= (cluster_evt_req == 0)? 0 : 1;
			     end
			   else
			     begin
				$display($time,":MEH_ID=0x%h Merge Event Handler- Expecting Module Header!! evt = 0x%x prev_evt=0x%x",MEH_ID, cluster_evt, cluster_evt2b);
				get_next_cluster <= 0;
				pending_m_hdr    <= 0;
				#1000
				  $finish();
				
				//Error -> drop or add event footer and request next event ( E_HDR_REQ)
			     end // else: !if(cluster_evt[DATA_WIDTH-1] && cluster_evt[EVT_FTR_W1_FLAG_msb:EVT_FTR_W1_FLAG_lsb] == EVT_FTR_W1_FLAG_FLAG )
			end // if (cluster_evt_req)
		      else //Wait for module header or footer
			begin
			   send_module_clusters<= 0;
			   //get_next_cluster    <= (prev_evt_hndlr_state == MHDR_EFTR_REQ)? 1 : 0;
			   //   evt_hndlr_state     <= E_REQ;
			   pending_m_hdr       <= 0;
			   get_hdr             <= 0;
			   
			   if (cluster_evt[DATA_WIDTH-1] && cluster_evt[M_HDR_FLAG_msb:M_HDR_FLAG_lsb] == M_HDR_FLAG_FLAG)
			     begin
				evt_state         <= M_AV;
				get_next_cluster  <= 1;
				tx_wrd_cnt        <= 0; //M_HDR_LWORDS;
			     end
			   else if (cluster_evt[DATA_WIDTH-1] && cluster_evt[EVT_FTR_W1_FLAG_msb:EVT_FTR_W1_FLAG_lsb] == EVT_FTR_W1_FLAG_FLAG )
			     begin
				evt_state         <= EFTR_AV;
				get_next_cluster  <= 1;		
				tx_wrd_cnt        <= EVT_FTR_LWORDS;		
			     end
			   else
			     begin
				get_hdr         <= 1'b0;
				if(~cluster_empty)
				  begin
				     get_hdr          <= 1'b0;
				     get_next_cluster <= 1;
				  end
				else
				  begin
				     get_hdr         <= 1'b0;
				     
				  end
			     end
			end // else: !if(cluster_evt_req)
		   end // case: MHDR_EFTR_REQ

		 E_REQ:
		   begin
		      pending_m_hdr     <= 0;
		      if(get_hdr)
			  begin
			     evt_hndlr_state  <= MHDR_EFTR_REQ;
			     get_hdr          <= 0;
			  end
			else
			  begin
			     if(fifo_rdy)
			     begin
				get_hdr          <= 1;
				get_next_cluster <= 1;
			     end
			  end // else: !if(get_hdr)
		   end
		 M_TX: //Tranmit pixel and strip, give back control at module boundary
		   begin
		      send_module_clusters <= 1;
		      get_hdr              <= 0;

		      if(cluster_evt_req)
			begin
			   if(pending_m_hdr && cluster_evt[DATA_WIDTH-1] && (cluster_evt[M_HDR_FLAG_msb:M_HDR_FLAG_lsb] == M_HDR_FLAG_FLAG) )
			     begin
				evt_state          <= M_AV;
				get_next_cluster   <= 1;
				pending_m_hdr      <= 0;
			     end
			   else if(pixel0_strip1 == 0) //pixel
			     begin
			//	$display(" MEH_ID=0x%h Pixel cluster_evt = 0x%x\n",MEH_ID, cluster_evt);
				if(~pending_m_ftr &  cluster_evt[PIXEL_CLUSTER_LAST_lsb])
				  begin
				     pending_m_ftr      <= 1;
				     pending_m_hdr      <= 0;
				     evt_state          <= M_AV;
				     get_next_cluster   <= 1;
				  end
				else if(~pending_m_ftr &  cluster_evt[PIXEL_CL_FTR_FLAG_msb: PIXEL_CL_FTR_FLAG_lsb] == PIXEL_CL_FTR_FLAG_FLAG  & (cluster_evt[32 + PIXEL_CLUSTER_LAST_lsb]))
				  begin
//				     pending_m_hdr       <= 0;
				     evt_hndlr_state     <= MHDR_EFTR_REQ;
				     evt_state           <= E_NOT_AV;
				     get_next_cluster     <= 0;
				  end
				else if(pending_m_ftr)
				  begin
				     if( cluster_evt[32 + PIXEL_CL_FTR_FLAG_msb: 32 + PIXEL_CL_FTR_FLAG_lsb] == PIXEL_CL_FTR_FLAG_FLAG)
				       begin
					  evt_hndlr_state     <= MHDR_EFTR_REQ;
					  get_next_cluster    <= 0;
					  evt_state           <= E_NOT_AV;
					  pending_m_ftr       <= 0;
//					  pending_m_hdr       <= 0;
				       end
				     else
				       begin
					  $display($time,", MEH_ID=0x%h, PIXEL MODULE FOOTER NOT RECEIVED!!0x%x",MEH_ID,cluster_evt);
					  #1000
					    $finish();
					  
				       end
				  end // if (pending_m_ftr)
				else
				  begin
				     get_next_cluster  <= (evt_ctrl == TX)? 1 : 0;
				     evt_state         <= M_AV;
				     pending_m_hdr     <= 0;
				  end // else: !if(pending_m_ftr)
			     end // if (pixel0_strip1 == 0)
			   else
			     begin
//				$display("Strip cluster_evt = 0x%x\n",cluster_evt);
				if ( ~pending_m_ftr &  cluster_evt[STRIP_CLUSTER_LAST_msb])
				  begin
				     pending_m_ftr      <= 1;
				     pending_m_hdr      <= 0;
				     evt_state          <= M_AV;
				     get_next_cluster   <= 1;
				  end
				else if(~pending_m_ftr &  
					(((cluster_evt[STRIP_CL_FTR_FLAG_msb: STRIP_CL_FTR_FLAG_lsb] == STRIP_CL_FTR_FLAG_FLAG) & cluster_evt[STRIP_CLUSTER_bits + STRIP_CLUSTER_LAST_msb ] )
					 |(~pending_m_hdr & ((cluster_evt[16+STRIP_CL_FTR_FLAG_msb: STRIP_CLUSTER_bits+STRIP_CL_FTR_FLAG_lsb]   == STRIP_CL_FTR_FLAG_FLAG) & cluster_evt[STRIP_CLUSTER_bits*2 + STRIP_CLUSTER_LAST_msb ] )) 
					 |(~pending_m_hdr & ((cluster_evt[32+STRIP_CL_FTR_FLAG_msb: STRIP_CLUSTER_bits*2+STRIP_CL_FTR_FLAG_lsb] == STRIP_CL_FTR_FLAG_FLAG) & cluster_evt[STRIP_CLUSTER_bits*3 +STRIP_CLUSTER_LAST_msb ]))//=> check last condition only when not module hdr W2
					 ))
				  begin
				     evt_hndlr_state     <= MHDR_EFTR_REQ;
				     evt_state           <= E_NOT_AV;
				     get_next_cluster    <= 0;
				     pending_m_hdr       <= 0;
				  //   $display("Last strip cluster_evt = 0x%x\n",cluster_evt);
				  end
				else if(pending_m_ftr)
				  begin
				     pending_m_hdr       <= 0;
				     if( cluster_evt[48 + STRIP_CL_FTR_FLAG_msb: 48 + STRIP_CL_FTR_FLAG_lsb] == STRIP_CL_FTR_FLAG_FLAG)
				       begin
					  evt_hndlr_state     <= MHDR_EFTR_REQ;
					  get_next_cluster    <= 0;
					  evt_state           <= E_NOT_AV;
					  pending_m_ftr       <= 0;
				       end
				     else
				       begin
					  $display($time,", MEH_ID=0x%h, STRIP MODULE FOOTER NOT RECEIVED!!0x%x",MEH_ID,cluster_evt);
					  #10000
					    $finish();
					  
				       end // else: !if( cluster_evt[48 + STRIP_CL_FTR_FLAG_msb: 48 + STRIP_CL_FTR_FLAG_lsb] == STRIP_CL_FTR_FLAG_FLAG)
				  end
				else
				  begin
				     get_next_cluster  <= 1;
				     evt_state         <= M_AV;
				     pending_m_hdr     <= 0;
				  end
			     end // else: !if(pixel0_strip1 == 1)
			end // if (cluster_evt_req)
		      else
			begin
			   if(cluster_evt[DATA_WIDTH-1] && (cluster_evt[M_HDR_FLAG_msb:M_HDR_FLAG_lsb] == M_HDR_FLAG_FLAG))
			     begin
				pending_m_hdr      <= 1;
				evt_state          <= M_AV;
				get_next_cluster   <= 1;
				pixel0_strip1      <= cluster_evt[M_HDR_DET_msb];//cluster_evt[M_HDR_DET_msb:M_HDR_DET_lsb];
			     end
			end
		   end // case: M_TX
	
	       endcase // case (evt_hndlr_state)
	    end // else: !if(!rst_n | !srst_n)
       end // always @ (posedge clk )
   
   
endmodule // merge_evt_handler

