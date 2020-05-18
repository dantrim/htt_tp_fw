/*
 * TopLevel.v
 *
 */

`timescale 1ns / 1ps
`default_nettype none

module TopLevel #(
    // inclusive of metadata flag (bit 64)
    parameter SIZE = 65
) (
    // main TP clock, nominally 200 MHz
    input wire clock,
    input wire reset,
    input wire [SIZE-1:0] input_data,
    output reg [SIZE-1:0] output_data
);

    // These are outputs of the SpyBuffer block
    wire buffer_almost_full;
    wire buffer_empty;

    // These are inputs, and should get zero'd.
    wire buffer_write_enable;
    wire buffer_read_enable;

    // Create an input spy buffer.
    // NOTE: size is exclusive of metadata flag bit here.
    SpyBuffer #(
        .DATA_WIDTH(SIZE-1)
    ) spybuffer (
        .rclock(clock),
        .wclock(clock),
        .rreset(reset),
        .wreset(reset),
        .write_data(input_data),
        .write_enable(buffer_write_enable),
        .read_data(output_data),
        .read_enable(buffer_read_enable),
        .almost_full(buffer_almost_full),
        .empty(buffer_empty),
    );
endmodule

`default_nettype wire
