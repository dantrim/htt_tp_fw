/*
 * SkeletonWrapper.v
 *
 * begun 2019-11-11 by Bill Ashmanskas
 * adjusted 2020-01-27 by Ben Rosser.
 */

`timescale 1ns / 1ps
`default_nettype none

module SkeletonWrapper #(
    // inclusive of metadata flag (bit 64)
    parameter SIZE = 65,
    parameter DATA_WIDTH   = 65,
    parameter TOTAL_BOARDS = 14,
    parameter TOTAL_CLUSTERS=4

) (
    // main TP clock, nominally 200 MHz
    input wire clock,
    input wire reset,
    input wire [SIZE-1:0] input_data [TOTAL_CLUSTERS], //ToUpdate
    output reg [SIZE-1:0] output_data [TOTAL_BOARDS] //ToUpdate
);

    // Random wires for the spy buffers.
    // I wrote the testbench in such a way that none of these matter;
    // the driver/monitor reaches into the spy buffer's toplevel
    // rather than look at these. But maybe that was a bad idea.

    // These are outputs.
    //wire input_afull;
    //wire input_empty;
    //wire output_afull;

    // These are inputs, and should get zero'd.
    wire input_we [TOTAL_CLUSTERS];
    //wire input_re;
    //wire output_we;
    wire output_re [TOTAL_BOARDS];

    logic [SIZE-1:0] cluster_data [TOTAL_CLUSTERS];
    logic            cluster_rd_req [TOTAL_CLUSTERS];
    logic            cluster_almost_full [TOTAL_CLUSTERS];
    logic            cluster_empty [TOTAL_CLUSTERS];

    logic [DATA_WIDTH-1:0] board_cluster_data [TOTAL_BOARDS];
    logic                  board_wren [TOTAL_BOARDS];
    logic                  board_almost_full [TOTAL_BOARDS];
    logic                  board_empty [TOTAL_BOARDS];
   
  
   
    //
    // Input buffers
    //
    generate
        for(genvar z=0;z<TOTAL_CLUSTERS;z++)
            begin:input_cluster_SpyBuffer
                SpyBuffer #(
                    .DATA_WIDTH(SIZE-1)
                    ) input_buffer (
                        .rclock(clock),
                        .wclock(clock),
                        .rreset(reset),
                        .wreset(reset),
                        .write_data(input_data[z]),//ToUpdate
                        .write_enable(input_we[z]),//ToUpdate
                        .read_data(cluster_data[z]),
                        .read_enable(cluster_rd_req[z]),
                        .almost_full(cluster_almost_full[z]),
                        .empty(cluster_empty[z]), //ToUpdate
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
	        end // block: input_cluster_SpyBuffer
    endgenerate

    //
    // B2B block
    //
    board2board_switching #(
        .DATA_WIDTH(SIZE),
        .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
        .TOTAL_OUTPUT_BOARDS(TOTAL_BOARDS)
    )
    board2board_switching_inst (
        .b2b_clk(clock),
        .b2b_rst_n(~reset),
        .b2b_srst_n(~reset),
        
        .cluster_data(cluster_data), 
        .cluster_req(cluster_rd_req),
        .cluster_almost_full(cluster_almost_full),
        .cluster_empty(cluster_empty),
        
        .output_board_event(board_cluster_data),
        .output_board_wren(board_wren),
        .output_board_almost_full(board_almost_full)
    );
    //logic [DATA_WIDTH-1:0] board_cluster_data [TOTAL_BOARDS];
    //logic                  board_wren [TOTAL_BOARDS];
    //logic                  board_almost_full [TOTAL_BOARDS];

    //
    // Output buffers
    //
    generate
        for(genvar z=0;z<TOTAL_BOARDS;z++)
            begin:output_cluster_SpyBuffer
                SpyBuffer #(
                     .DATA_WIDTH(SIZE-1)
                    ) output_buffer (
                        .rclock(clock),
                        .wclock(clock),
                        .rreset(reset),
                        .wreset(reset),
                        .write_data(board_cluster_data[z]),
                        .write_enable(board_wren[z]),
                        .read_data(output_data[z]), //ToUpdate
                        .read_enable(output_re[z]), //ToUpdate
                        .almost_full(board_almost_full[z]), //ToUpdate
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
            end // block: board_fifos
    endgenerate

endmodule

`default_nettype wire
