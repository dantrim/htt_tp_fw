/*
 * SkeletonWrapper.v
 *
 * begun 2019-11-11 by Bill Ashmanskas
 * adjusted 2020-01-27 by Ben Rosser.
 */

`timescale 1ns / 1ps
`default_nettype none

module TopLevel #(
    // inclusive of metadata flag (bit 64)
    parameter SIZE = 65,
    parameter DATA_WIDTH   = 65,
    parameter FIFO_DEPTH = 6,
    parameter TOTAL_BOARDS = 14,
    parameter TOTAL_CLUSTERS=4

) (
    // main TP clock, nominally 200 MHz
    input wire clock,
    input wire reset,
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
   
//kludge    //
//kludge    // kludge to register the aFifo read_data line
//kludge    //
//kludge    reg [SIZE-1:0] cluster_data_reg [TOTAL_CLUSTERS];
//kludge    always @ (posedge clock)
//kludge    begin
//kludge        if (~reset)
//kludge            begin
//kludge                for(int i = 0; i < TOTAL_CLUSTERS; i++)
//kludge                begin
//kludge                    cluster_data_reg[i] <= 0;
//kludge                end
//kludge            end
//kludge        else
//kludge            begin
//kludge                for(int i = 0; i < TOTAL_CLUSTERS; i++)
//kludge                begin
//kludge                    cluster_data_reg[i] <= cluster_data[i];
//kludge                end
//kludge            end
//kludge    end
  
   
    //
    // Input buffers
    //
    generate
        for(genvar z=0;z<TOTAL_CLUSTERS;z++)
            begin:input_cluster_SpyBuffer
                SpyBuffer #(
                    .DATA_WIDTH(SIZE-1),
                    .FC_FIFO_WIDTH(FIFO_DEPTH)
                    ) input_buffer (
                        .rclock(clock),
                        .wclock(clock),
                        .rreset(reset),
                        .wreset(reset),
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
        .b2b_rst_n(reset),
        .b2b_srst_n(reset),
        
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
            begin:output_cluster_SpyBuffer
                SpyBuffer #(
                     .DATA_WIDTH(SIZE-1),
                     .FC_FIFO_WIDTH(FIFO_DEPTH)
                    ) output_buffer (
                        .rclock(clock),
                        .wclock(clock),
                        .rreset(reset),
                        .wreset(reset),
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
