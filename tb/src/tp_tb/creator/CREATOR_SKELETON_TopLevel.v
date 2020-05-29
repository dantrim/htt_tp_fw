`timescale 1ns / 1ps
`default_nettype wire

module TopLevel_CREATORTESTNAME #(
    parameter DATA_WIDTH = 65,
    parameter FIFO_DEPTH = 6,
    parameter N_OUTPUTS = CREATORNOUTPUTS,
    parameter N_INPUTS = CREATORNINPUTS

) (
    input wire clock,
    input wire reset_n,
    input wire [DATA_WIDTH-1:0] input_data [CREATORNINPUTS],
    output wire [DATA_WIDTH-1:0] output_data [CREATORNOUTPUTS]
);

    //
    // Here define the signals to connect the input and output Spy+FIFO
    // blocks with the input and output of the DUT.
    // Here we define one for each of the FIFO signals, but the test
    // creator should remove unnecessary signals.
    //

    wire BLOCK_input_write_enable [CREATORNINPUTS];
    wire [DATA_WIDTH-1:0] BLOCK_input_data [CREATORNINPUTS];
    wire BLOCK_input_read_enable [CREATORNINPUTS];
    wire BLOCK_input_almost_full [CREATORNINPUTS];
    wire BLOCK_input_empty [CREATORNINPUTS];

    wire BLOCK_output_write_enable [CREATORNOUTPUTS];
    wire [DATA_WIDTH-1:0] BLOCK_output_data [CREATORNOUTPUTS];
    wire BLOCK_output_read_enable [CREATORNOUTPUTS];
    wire BLOCK_output_almost_full [CREATORNOUTPUTS];
    wire BLOCK_output_empty [CREATORNOUTPUTS];

    //
    // Input buffers
    //
    generate
        for(genvar i = 0; i < CREATORNINPUTS; i++)
            begin:input_spybuffers
                SpyBuffer #(
                    .DATA_WIDTH(DATA_WIDTH-1),
                    .FC_FIFO_WIDTH(FIFO_DEPTH)
                    ) spybuffer (
                        .rclock(clock),
                        .wclock(clock),
                        .rreset(reset_n),
                        .wreset(reset_n),
                        .write_data(input_data[i]),
                        .write_enable(BLOCK_input_write_enable[i]),
                        .read_data(BLOCK_input_data[i]),
                        .read_enable(BLOCK_input_read_enable[i]),
                        .almost_full(BLOCK_input_almost_full[i]),
                        .empty(BLOCK_input_empty[i])
                    );
            end
    endgenerate // end input_spybuffers generate

    //
    // Here place the DUT block(s)
    //

    //
    // Output buffers
    //
    generate
        for(genvar i = 0; i < CREATORNOUTPUTS; i++)
            begin:output_spybuffers
                SpyBuffer #(
                     .DATA_WIDTH(DATA_WIDTH-1),
                     .FC_FIFO_WIDTH(FIFO_DEPTH)
                    ) spybuffer (
                        .rclock(clock),
                        .wclock(clock),
                        .rreset(reset_n),
                        .wreset(reset_n),
                        .write_data(BLOCK_output_data[i]),
                        .write_enable(BLOCK_output_write_enable[i]),
                        .read_data(output_data[i]),
                        .read_enable(BLOCK_output_read_enable[i]),
                        .almost_full(BLOCK_output_almost_full[i]),
                        .empty(BLOCK_output_empty[i])
                    );
            end
    endgenerate // end output_spybuffers generate

endmodule // end TopLevel module definition
