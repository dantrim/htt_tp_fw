`timescale 1ns / 1ps
`default_nettype none

module B2BTopLevel #(
    // inclusive of metadata flag (bit 64)
    parameter SIZE = 65,
    parameter DATA_WIDTH   = 65,
    parameter FIFO_DEPTH = 6,
    parameter TOTAL_BOARDS = 14,
    parameter TOTAL_CLUSTERS=4

) (
    // main TP clock, nominally 200 MHz
    input wire clock,
    input wire reset_n,
    input wire [SIZE-1:0] input_data [TOTAL_CLUSTERS],
    output wire [SIZE-1:0] output_data [TOTAL_BOARDS]
);

    // Random wires for the spy buffers.
    // I wrote the testbench in such a way that none of these matter;
    // the driver/monitor reaches into the spy buffer's toplevel
    // rather than look at these. But maybe that was a bad idea.

    wire            cluster_wren [TOTAL_CLUSTERS];
    wire [SIZE-1:0] cluster_data [TOTAL_CLUSTERS];
    wire            cluster_rd_req [TOTAL_CLUSTERS];
    wire            cluster_almost_full [TOTAL_CLUSTERS];
    wire            cluster_empty [TOTAL_CLUSTERS];

    wire [DATA_WIDTH-1:0] board_cluster_data [TOTAL_BOARDS];
    wire                  board_wren [TOTAL_BOARDS];
    wire                  board_almost_full [TOTAL_BOARDS];
    wire                  board_empty [TOTAL_BOARDS];
    wire                  board_ren [TOTAL_BOARDS];
   
    //
    // Input buffers
    //
    generate
        for(genvar z=0;z<TOTAL_CLUSTERS;z++)
            begin:input_spybuffers
                SpyBuffer #(
                    .DATA_WIDTH(SIZE-1),
                    .FC_FIFO_WIDTH(FIFO_DEPTH)
                    ) spybuffer (
                        .rclock(clock),
                        .wclock(clock),
                        .rreset(reset_n),
                        .wreset(reset_n),
                        .write_data(input_data[z]),
                        .write_enable(cluster_wren[z]),
                        .read_data(cluster_data[z]),
                        .read_enable(cluster_rd_req[z]),
                        .almost_full(cluster_almost_full[z]),
                        .empty(cluster_empty[z]),
                        // The following should not be needed until one actually wants
                        // to use the spy-buffer functionality, whereas for now we just
                        // want to use the fifo functionality.
                        .freeze(1'b0),
                        .spy_read_enable(1'b0),
                        .spy_meta_read_enable(1'b0),
                        .spy_read_addr(1'b0),
                        .spy_meta_read_addr(1'b0),
                        .spy_write_addr(),
                        .spy_meta_write_addr(),
                        .spy_data(),
                        .spy_meta_read_data()
                    );
	        end
    endgenerate

    //
    // B2B block
    //
    board2board_switching #(
        .DATA_WIDTH(SIZE),
        .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
        .TOTAL_OUTPUT_BOARDS(TOTAL_BOARDS),
        .FIFO_DEPTH_BITS(6),
        .BOARD_ID(0)
    )
    board2board_switching_inst (
        .b2b_clk(clock),
        .b2b_rst_n(reset_n),
        .b2b_srst_n(reset_n),
        
        //kludge.cluster_data(cluster_data_reg), 
        .cluster_data(cluster_data), 
        .cluster_req(cluster_rd_req),
        .cluster_almost_full(cluster_almost_full),
        .cluster_empty(cluster_empty),
        
        .output_board_event(board_cluster_data),
        .output_board_wren(board_wren),
        .output_board_almost_full(board_almost_full)
    );

    //
    // Output buffers
    //
    generate
        for(genvar z=0;z<TOTAL_BOARDS;z++)
            begin:output_spybuffers
                SpyBuffer #(
                     .DATA_WIDTH(SIZE-1),
                     .FC_FIFO_WIDTH(FIFO_DEPTH)
                    ) spybuffer (
                        .rclock(clock),
                        .wclock(clock),
                        .rreset(reset_n),
                        .wreset(reset_n),
                        .write_data(board_cluster_data[z]),
                        .write_enable(board_wren[z]),
                        .read_data(output_data[z]),
                        .read_enable(board_ren[z]),
                        .almost_full(board_almost_full[z]),
                        .empty(board_empty[z]),
                        // The following should not be needed until one actually wants
                        // to use the spy-buffer functionality, whereas for now we just
                        // want to use the fifo functionality.
                        .freeze(1'b0),
                        .spy_read_enable(1'b0),
                        .spy_meta_read_enable(1'b0),
                        .spy_read_addr(1'b0),
                        .spy_meta_read_addr(1'b0),
                        .spy_write_addr(),
                        .spy_meta_write_addr(),
                        .spy_data(),
                        .spy_meta_read_data()
                    );
            end
    endgenerate

endmodule

`default_nettype wire
