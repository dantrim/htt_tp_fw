`timescale 1ns / 1ps
`default_nettype none

module TopLevel_evt_sync #(
    parameter SIZE = 65,
    parameter DATA_WIDTH = 65,
    parameter FIFO_DEPTH = 6,
    parameter TOTAL_CLUSTERS = 17,
    parameter TOTAL_OUTPUT_BOARDS = 4,
    parameter BOARD_ID = 0
) (
    input wire clock,
    input wire reset_n,
    input wire [SIZE-1:0] input_data [TOTAL_CLUSTERS],
    output wire [SIZE-1:0] output_data [TOTAL_OUTPUT_BOARDS]
);

    // connections between input Spy+FIFO and EventSync
    wire evt_sync_input_wren [TOTAL_CLUSTERS];
    wire [DATA_WIDTH-1:0] evt_sync_input_data [TOTAL_CLUSTERS];
    wire evt_sync_input_read_request [TOTAL_CLUSTERS];
    wire evt_sync_input_almost_full [TOTAL_CLUSTERS]; // dantrim: does EvtSync input need this almost_full flag if it is just *pulling* data from the input fifos?
    wire evt_sync_input_empty [TOTAL_CLUSTERS];
    

    // connections between output Spy+FIFO and EventSync
    wire [DATA_WIDTH-1:0] evt_sync_output_data [TOTAL_OUTPUT_BOARDS];
    wire evt_sync_output_write_enable [TOTAL_OUTPUT_BOARDS];
    wire evt_sync_output_almost_full [TOTAL_OUTPUT_BOARDS];

    //
    // Input buffers
    //
    generate
        for(genvar i = 0; i < TOTAL_CLUSTERS; i++)
            begin:input_spybuffers
                SpyBuffer #(
                    .DATA_WIDTH(SIZE-1),
                    .FC_FIFO_WIDTH(FIFO_DEPTH)
                ) spybuffer (
                    .rclock(clock),
                    .wclock(clock),
                    .rreset(reset_n),
                    .wreset(reset_n),
                    .write_data(input_data[i]),
                    .read_data(evt_sync_input_data[i]),
                    .read_enable(evt_sync_input_read_request[i]),
                    .write_enable(evt_sync_input_wren[i]),
                    .almost_full(evt_sync_input_almost_full[i]),
                    .empty(evt_sync_input_empty[i])
                );
            end
    endgenerate
                    

    //
    // EventSync block
    //
    event_sync #(
        .DATA_WIDTH(DATA_WIDTH),
        .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
        .TOTAL_OUTPUT_BOARDS(TOTAL_OUTPUT_BOARDS),
        .FIFO_DEPTH_BITS(FIFO_DEPTH),
        .BOARD_ID(BOARD_ID)
    )
    event_sync_inst (
        .es_clk(clock),
        .es_rst_n(reset_n),
        .es_srst_n(reset_n),
        .cluster_data(evt_sync_input_data),
        .cluster_req(evt_sync_input_read_request),
        .cluster_almost_full(evt_sync_input_almost_full),
        .cluster_empty(evt_sync_input_empty),
        .output_board_event(evt_sync_output_data),
        .output_board_wren(evt_sync_output_write_enable),
        .output_board_almost_full(evt_sync_output_almost_full)
    );

    //
    // Output buffers
    //
    generate
        for(genvar i = 0; i < TOTAL_OUTPUT_BOARDS; i++)
            begin:output_spybuffers
                SpyBuffer #(
                    .DATA_WIDTH(SIZE-1),
                    .FC_FIFO_WIDTH(FIFO_DEPTH)
                ) spybuffer (
                    .rclock(clock),
                    .wclock(clock),
                    .rreset(reset_n),
                    .wreset(reset_n),
                    .read_data(output_data[i]),
                    .write_data(evt_sync_output_data[i]),
                    .write_enable(evt_sync_output_write_enable[i]),
                    .almost_full(evt_sync_output_almost_full[i])
                );
            end
    endgenerate

endmodule

`default_nettype wire

