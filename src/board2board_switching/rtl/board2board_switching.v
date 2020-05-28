module board2board_switching #(
			       parameter DATA_WIDTH = 65,
			       parameter TOTAL_CLUSTERS=4,
			       parameter TOTAL_OUTPUT_BOARDS=14,
			       parameter FIFO_DEPTH_BITS=9,
			       parameter BOARD_ID=0
			       )
   (
    input logic 		  b2b_clk,
    input logic 		  b2b_rst_n,
    input logic 		  b2b_srst_n,

    input logic [DATA_WIDTH-1:0]  cluster_data[TOTAL_CLUSTERS], //define as input wire logic [DATA_WIDTH-1:0] to get rid of Questasim warning
    output logic 		  cluster_req[TOTAL_CLUSTERS],
    input logic 		  cluster_almost_full[TOTAL_CLUSTERS],
    input logic 		  cluster_empty[TOTAL_CLUSTERS],

    output logic [DATA_WIDTH-1:0] output_board_event[TOTAL_OUTPUT_BOARDS],
    output logic 		  output_board_wren[TOTAL_OUTPUT_BOARDS],
    input logic 		  output_board_almost_full[TOTAL_OUTPUT_BOARDS]
        
    );
   

   genvar 			  i,j;


   logic [DATA_WIDTH-1:0] 	  cre_op_event[TOTAL_CLUSTERS][TOTAL_OUTPUT_BOARDS];
   logic 			  cre_op_req[TOTAL_CLUSTERS][TOTAL_OUTPUT_BOARDS];
 //  logic [TOTAL_OUTPUT_BOARDS-1 :0] cre_op_almost_full[TOTAL_CLUSTERS];
//   logic [TOTAL_OUTPUT_BOARDS-1 :0] cre_op_half_full[TOTAL_CLUSTERS];
   logic			    cre_op_empty[TOTAL_CLUSTERS][TOTAL_OUTPUT_BOARDS];
   logic [FIFO_DEPTH_BITS:0] 	    cre_fifo_rd_count[TOTAL_CLUSTERS][TOTAL_OUTPUT_BOARDS];
   

   logic [DATA_WIDTH-1:0] 	    cme_ip_event[TOTAL_OUTPUT_BOARDS][TOTAL_CLUSTERS];
   logic 			    cme_ip_req[TOTAL_OUTPUT_BOARDS][TOTAL_CLUSTERS];
   logic 			    cme_ip_empty[TOTAL_OUTPUT_BOARDS][TOTAL_CLUSTERS];
 //  logic [TOTAL_CLUSTERS-1:0] 	    cme_ip_almost_full[TOTAL_OUTPUT_BOARDS];
   //logic [TOTAL_CLUSTERS-1:0] 	    cme_ip_half_full[TOTAL_OUTPUT_BOARDS]; 
   logic [FIFO_DEPTH_BITS:0] 	    cme_fifo_rd_count[TOTAL_OUTPUT_BOARDS][TOTAL_CLUSTERS];
				  
   generate
     for(i=0; i< TOTAL_CLUSTERS; i++)
       begin: route_engine
	  cluster_routing_engine  #(
				    .DATA_WIDTH(DATA_WIDTH),
				    .TOTAL_BOARDS(TOTAL_OUTPUT_BOARDS),
				    .CRE_ID(i),
				    .FIFO_DEPTH_BITS(FIFO_DEPTH_BITS),
				    .BOARD_ID(BOARD_ID)
				    )
	  cluster_routing_engine_inst (
				       .cluster_event(cluster_data[i]),
				       .cluster_req(cluster_req[i]),
				       .cluster_almost_full(cluster_almost_full[i]),
				       .cluster_empty(cluster_empty[i]),
				       
				       .board_event(cre_op_event[i]),
				       .board_req(cre_op_req[i]),
//				       .board_almost_full(cre_op_almost_full[i]),
//				       .board_half_full(cre_op_half_full[i]),
				       .board_full(),
				       .board_empty(cre_op_empty[i]),
				       .board_rd_count(cre_fifo_rd_count[i]),
				       
				       .b2b_clk(b2b_clk),
				       .b2b_rst_n(b2b_rst_n),
				       .b2b_srst_n(b2b_srst_n)
				       
				       );

       end
   endgenerate

   generate
    for(j=0;j<TOTAL_CLUSTERS;j++)
       begin
	  for(i=0; i< TOTAL_OUTPUT_BOARDS; i++)
	    begin
	       assign cme_ip_event[i][j]        =  cre_op_event[j][i];
//	       assign cme_ip_almost_full[i][j]  =  cre_op_almost_full[j][i];
//	       assign cme_ip_half_full[i][j]    = cre_op_half_full[j][i];	       
	       assign cme_ip_empty[i][j]        =  cre_op_empty[j][i];
	       assign cre_op_req[j][i]          =  cme_ip_req[i][j] ;
	       assign cme_fifo_rd_count[i][j]   = cre_fifo_rd_count[j][i];
	    end
       end
   endgenerate

   
   generate
      for(i=0; i< TOTAL_OUTPUT_BOARDS; i++)
	begin: merge_engine
	   cluster_merge_engine #(
				  .DATA_WIDTH(DATA_WIDTH),
				  .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
				  .CME_ID(i),
				  .FIFO_DEPTH_BITS(FIFO_DEPTH_BITS)
				  )
	   cluster_merge_engine_inst(
				     .b2b_clk(b2b_clk),
				     .b2b_rst_n(b2b_rst_n),
				     .b2b_srst_n(b2b_srst_n),
				
				     .input_board_event(cme_ip_event[i]),  //define as input wire logic [DATA_WIDTH-1:0] to get rid of Questasim warning
				     .input_board_req(cme_ip_req[i]),				   
//				     .input_board_almost_full(cme_ip_almost_full[i]),
//				     .input_board_half_full(cme_ip_half_full[i]),
				     .input_board_empty(cme_ip_empty[i]),
				     
				     .output_board_event(output_board_event[i]),
				     .output_board_wren(output_board_wren[i]),
				     .output_board_almost_full(output_board_almost_full[i]),
				     .output_board_empty(),
				     .route_engine_fifo_rd_data_count(cme_fifo_rd_count[i])
				     );
	end // block: merge_engine
   endgenerate
endmodule // board2board_switching
