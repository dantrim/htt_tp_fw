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

    // These are outputs.
    wire input_afull;
    wire input_empty;
    wire output_afull;
    wire output_empty;

    // These are inputs, and should get zero'd.
    wire input_we;
    wire input_re;
    wire output_we;
    wire output_re;

    wire [SIZE-1:0] input_data_out;
    reg [SIZE-1:0] output_data_in;

    // Create an input spy buffer.
    // NOTE: size is exclusive of metadata flag bit here.
    SpyBuffer #(
        .DATA_WIDTH(SIZE-1)
    ) input_buffer (
        .rclock(clock),
        .wclock(clock),
        .rreset(reset),
        .wreset(reset),
        .write_data(input_data),
        .write_enable(input_we),
        .read_data(input_data_out),
        .read_enable(input_re),
        .almost_full(input_afull),
        .empty(input_empty),
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

    SpyBuffer #(
        .DATA_WIDTH(SIZE-1)
    ) output_buffer (
        .rclock(clock),
        .wclock(clock),
        .rreset(reset),
        .wreset(reset),
        .write_data(output_data_in),
        .write_enable(output_we),
        .read_data(output_data),
        .read_enable(output_re),
        .almost_full(output_afull),
        .empty(output_empty),
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
