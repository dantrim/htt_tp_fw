`timescale 1ns / 1ps
`default_nettype none

module TopLevel_sw_block #(
    parameter SIZE = 65,
    parameter DATA_WIDTH = 65,
    parameter FIFO_DEPTH = 6,
    parameter TOTAL_INPUTS = 2,
    parameter TOTAL_OUTPUTS = 2
) (
    input wire clock,
    input wire reset_n,
    input wire [SIZE-1:0] input_data [TOTAL_INPUTS],
    output wire [SIZE-1:0] output_data [TOTAL_OUTPUTS]
);

    wire [SIZE-1:0] input_data_out [TOTAL_INPUTS];
    wire [SIZE-1:0] output_data_in [TOTAL_OUTPUTS];

    //
    // input buffers
    //
    generate
        for(genvar i=0;i<TOTAL_INPUTS;i++)
            begin:input_spybuffers
                SpyBuffer #(
                    .DATA_WIDTH(SIZE-1),
                    .FC_FIFO_WIDTH(FIFO_DEPTH)
                ) spybuffer (
                    .rclock(clock),
                    .wclock(clock),
                    .rreset(reset_n),
                    .wreset(reset_n),
                );
            end
    endgenerate

    //
    // output buffers
 
    generate
        for(genvar i=0;i<TOTAL_OUTPUTS;i++)
            begin:output_spybuffers
                SpyBuffer #(
                    .DATA_WIDTH(SIZE-1),
                    .FC_FIFO_WIDTH(FIFO_DEPTH)
                ) spybuffer (
                    .rclock(clock),
                    .wclock(clock),
                    .rreset(reset_n),
                    .wreset(reset_n),
                );
            end
    endgenerate

endmodule

`default_nettype wire
