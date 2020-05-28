`timescale 1ns/1ps

module cluster_merge_engine #(
			      parameter DATA_WIDTH = 65,
			      parameter TOTAL_CLUSTERS=4,
			      parameter CME_ID=0,
			      parameter FIFO_DEPTH_BITS=9
			      )(
				input logic 			 b2b_clk,
				input logic 			 b2b_rst_n,
				input logic 			 b2b_srst_n,
				
				input logic [DATA_WIDTH-1:0] 	 input_board_event[TOTAL_CLUSTERS], //define as input wire logic [DATA_WIDTH-1:0] to get rid of Questasim warning
				output logic 			 input_board_req[TOTAL_CLUSTERS],
//				input logic [TOTAL_CLUSTERS-1:0] input_board_almost_full,
//				input logic [TOTAL_CLUSTERS-1:0] input_board_half_full,
				input logic 			 input_board_full[TOTAL_CLUSTERS],
				input logic 			 input_board_empty[TOTAL_CLUSTERS],
				input logic [FIFO_DEPTH_BITS:0]  route_engine_fifo_rd_data_count[TOTAL_CLUSTERS],

				output logic [DATA_WIDTH-1:0] 	 output_board_event,
				output logic 			 output_board_wren,
				input logic 			 output_board_almost_full,
				input logic 			 output_board_empty
				);
`include "TP_DataFormat.sv"
		
   logic [EVT_HDR_W1_L0ID_bits:0] 			      evt_hdr_available[TOTAL_CLUSTERS]; //Includes vld bit 			      
   logic [2:0] 						      evt_hdr_ctrl[TOTAL_CLUSTERS];
   logic [2:0] 						      evt_mhdr_ctrl[TOTAL_CLUSTERS];
   logic 						      evt_m_available[TOTAL_CLUSTERS];
   logic [2:0] 						      evt_m_ctrl[TOTAL_CLUSTERS];
   logic 						      evt_ftr_available[TOTAL_CLUSTERS];
   logic [2:0]						      evt_ftr_ctrl[TOTAL_CLUSTERS];
   
   logic [2 : 0] 					      cluster_sel;
      logic [DATA_WIDTH-1:0] 				      cluster_evt2b[TOTAL_CLUSTERS];
   logic 						      cluster_evt2b_wren[TOTAL_CLUSTERS];
   
   logic [2:0] 						      cluster_src_id[TOTAL_CLUSTERS];
   
   logic [EVT_HDR_W1_L0ID_bits-1:0] 			      evt_l0id[TOTAL_CLUSTERS];
   logic [1:0] 						      evt_available[TOTAL_CLUSTERS];
   logic [1:0] 						      evt_ctrl[TOTAL_CLUSTERS];

   logic [15:0] 					      meta_count;
   logic [31:0] 					      word_count;
   logic [1:0] 						      evt_ftr_words;
 						      
   logic [DATA_WIDTH-1:0] 				      output_board_event_i;
   logic 						      output_board_wren_i;
   
	      
   generate
      for(genvar i=0; i<TOTAL_CLUSTERS;i++)
	begin:gen_meh
	   assign cluster_src_id[i]  = i;
	   
	   merge_event_handler #(
				 .DATA_WIDTH(DATA_WIDTH),
				 .EVT_HDR_BITS(EVT_HDR_W1_L0ID_bits),
				 .MEH_ID((CME_ID<<8)|i)
			       )
	   merge_event_handler_inst(
				    .clk(b2b_clk),
				    .rst_n(b2b_rst_n),
				    .srst_n(b2b_srst_n),
				    .cluster_evt(input_board_event[i]),
				    .cluster_evt_req(input_board_req[i]),
//				    .cluster_almost_full(input_board_almost_full[i]),
				    .cluster_full(input_board_full[i]),
				    .cluster_empty(input_board_empty[i]),
				    .evt_ctrl(evt_ctrl[i]),
				    .evt_l0id(evt_l0id[i]),
	  			    .evt_available(evt_available[i]),
	 			    .cluster_evt2b_almost_full(output_board_almost_full),
				    .cluster_evt2b(cluster_evt2b[i]),
				    .cluster_evt2b_wren(cluster_evt2b_wren[i])
				    );
	   
	end
   endgenerate
   


     
			
   cluster_sync_engine #(
			 .DATA_WIDTH(DATA_WIDTH),
			 .EVT_HDR_BITS(EVT_HDR_W1_L0ID_bits),
			 .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
			 .FIFO_DEPTH_BITS(FIFO_DEPTH_BITS)
			 )
   cluster_sync_engine_inst(
			    .clk(b2b_clk),
			    .rst_n(b2b_rst_n),
			    .srst_n(b2b_srst_n),
			    .evt_l0id(evt_l0id),
			    .evt_available(evt_available),
			    .evt_ctrl(evt_ctrl),
			    .cluster_sel(cluster_sel),
			    .cre_fifo_rd_data_count(route_engine_fifo_rd_data_count)
//			    .cre_fifo_almost_full(input_board_almost_full)
//			    .cre_fifo_half_full(input_board_half_full)
			    );
   
   assign output_board_event_i = (cluster_sel < TOTAL_CLUSTERS)? cluster_evt2b[cluster_sel] : 1'b0;
   assign output_board_wren_i  = (cluster_sel < TOTAL_CLUSTERS)? cluster_evt2b_wren[cluster_sel] : 1'b0;

 always @ (posedge b2b_clk)
     begin
	if((!b2b_rst_n) | (!b2b_srst_n))
	  begin
	     meta_count         <= 0;
	     word_count         <= 0;
	     evt_ftr_words      <= 0;
  	  end
	else
	  begin
	     if(output_board_wren_i)
	       begin
		  if(output_board_event_i[DATA_WIDTH-1] == 1)
		    begin
		       if(output_board_event_i[EVT_HDR_W1_FLAG_msb:EVT_HDR_W1_FLAG_lsb] == EVT_HDR_W1_FLAG_FLAG)
			 begin
			    meta_count        <= 1;
			    word_count         <= 1;
			    evt_ftr_words      <= 0;
			 end
		       else
			 begin
			    if(output_board_event_i[EVT_FTR_W1_FLAG_msb:EVT_FTR_W1_FLAG_lsb] != EVT_FTR_W1_FLAG_FLAG)
			      begin
				 meta_count <= meta_count + 1;
				 word_count <= word_count + 1;
			      end
			    else
			      begin
				 evt_ftr_words <= 1;
			      end
			 end
		    end
		  else
		    begin
		       if(evt_ftr_words == 0)
			 word_count         <= word_count + 1;
		       else
			 evt_ftr_words      <= evt_ftr_words + 1;
		    end
 	       end // if (output_board_wren_i)
	  end // else: !if((!b2b_rst_n) | (!b2b_srst_n))
     end // always @ (posedge b2b_clk)
   


    always @ (posedge b2b_clk)
     begin
	if((!b2b_rst_n) | (!b2b_srst_n))
	  begin
	     output_board_event <= 0;
	     output_board_wren  <= 0;
	  end
	else
	  begin
	     if(output_board_wren_i)
	       begin
		  output_board_wren  <= 1'b1;
		  
		  if(output_board_event_i[DATA_WIDTH-1] == 1 && output_board_event_i[EVT_FTR_W1_FLAG_msb:EVT_FTR_W1_FLAG_lsb] == EVT_FTR_W1_FLAG_FLAG)
		    begin
		       output_board_event[EVT_FTR_W1_META_COUNT_msb:EVT_FTR_W1_META_COUNT_lsb] <= meta_count;
		       output_board_event[EVT_FTR_W1_META_COUNT_lsb-1:0]                       <= output_board_event_i[EVT_FTR_W1_META_COUNT_lsb-1:0];
		       output_board_event[DATA_WIDTH-1: EVT_FTR_W1_META_COUNT_msb+1]           <= output_board_event_i[DATA_WIDTH-1: EVT_FTR_W1_META_COUNT_msb+1];
		    end
		  else if(evt_ftr_words == 2)
		    begin
		       output_board_event[EVT_FTR_W3_WORD_COUNT_msb:EVT_FTR_W3_WORD_COUNT_lsb] <= word_count;
		       output_board_event[EVT_FTR_W3_CRC_msb : EVT_FTR_W3_CRC_lsb]             <= 32'hdeadbeef;
		    end
		  else
		    begin
		       output_board_event = output_board_event_i;
		    end
	       end
	     else
	       begin
		  output_board_event <= 0;
		  output_board_wren  <= 0;
	       end
	  end
     end // always @ (posedge b2b_clk)
   
endmodule // cluster_merge_engine
