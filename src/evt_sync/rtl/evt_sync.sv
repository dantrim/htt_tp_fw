module event_sync #(
			       parameter DATA_WIDTH = 65,
			       parameter TOTAL_CLUSTERS=17,
			       parameter TOTAL_OUTPUT_BOARDS=4,
			       parameter FIFO_DEPTH_BITS=6,
			       parameter BOARD_ID=0
			       )
   (
    input logic 		  es_clk,
    input logic 		  es_rst_n,
    input logic 		  es_srst_n,

    input logic [DATA_WIDTH-1:0]  cluster_data[TOTAL_CLUSTERS], //define as input wire logic [DATA_WIDTH-1:0] to get rid of Questasim warning
    output logic 		  cluster_req[TOTAL_CLUSTERS],
    input logic 		  cluster_almost_full[TOTAL_CLUSTERS],
    input logic 		  cluster_empty[TOTAL_CLUSTERS],

    output logic [DATA_WIDTH-1:0] output_board_event[TOTAL_OUTPUT_BOARDS],
    output logic 		  output_board_wren[TOTAL_OUTPUT_BOARDS],
    input logic 		  output_board_almost_full[TOTAL_OUTPUT_BOARDS]
        
    );
   

   board2board_switching #(
			   .DATA_WIDTH(DATA_WIDTH),
			   .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
			   .TOTAL_OUTPUT_BOARDS(TOTAL_OUTPUT_BOARDS),
			   .FIFO_DEPTH_BITS(FIFO_DEPTH_BITS),
			   .BOARD_ID(BOARD_ID)
			   )
   event_sync_inst (
		    .b2b_clk(es_clk),
		    .b2b_rst_n(es_rst_n),
		    .b2b_srst_n(es_srst_n),
		    
		    //kludge.cluster_data(cluster_data_reg), 
		    .cluster_data(cluster_data), 
		    .cluster_req(cluster_req),
		    .cluster_almost_full(cluster_almost_full),
		    .cluster_empty(cluster_empty),
		    
		    .output_board_event(output_board_event),
		    .output_board_wren(output_board_wren),
		    .output_board_almost_full(output_board_almost_full)
		    );
   
   
endmodule 
