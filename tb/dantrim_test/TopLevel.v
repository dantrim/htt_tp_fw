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

    // Random wires for the spy buffers.
    // I wrote the testbench in such a way that none of these matter;
    // the driver/monitor reaches into the spy buffer's toplevel
    // rather than look at these. But maybe that was a bad idea.

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

endmodule

`default_nettype wire
