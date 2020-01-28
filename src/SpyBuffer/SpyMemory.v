// The actual spy buffer memory block.
// This block contains the "circular buffer" which stores
// words from events as they transit the spy buffer.

// It is an RTL-only implementation that MUST obviously be redone
// to use block RAM on the FPGA, eventually.

// For now, we "trust" that the read and write pointers can't
// be asserted simultaneously.
// But it actually does not mtater if they are.

// Ben Rosser <bjr@sas.upenn.edu>


`default_nettype none

module SpyMemory #(
    parameter WIDTH=6,

    // Width of the actual data.
    parameter DATAWIDTH=64
) (
    input wire clock,
    input wire reset,

    // Write enable and write data.
    input wire write_enable,
    input wire [DATAWIDTH-1:0] write_data,

    // Address to read.
    input wire [WIDTH-1:0] read_addr,
    input wire read_enable,

    // Output containing the "write pointer"
    // current position.
    output wire [WIDTH-1:0] write_pointer,

    // Output containing the result of the read command.
    output reg [DATAWIDTH-1:0] read_data,

    // Output wire that toggles when occupancy == 0.
    output wire looped
);

    localparam SIZE = 1 << WIDTH;

    // Memory block.
    reg [DATAWIDTH-1:0] memory [0:SIZE-1];

    // Write pointer.
    reg [WIDTH-1:0] wptr;

    // Continuously update output write pointer.
    assign write_pointer = wptr;

    // Continuously update the "looped" flag.
    // Fire this *when we have looped*, not before.
    assign looped = (~| wptr);

    // Handle writes to memory.
    always @(posedge clock) begin
        if (!reset) begin
            wptr <= 0;
        end else begin
            if (write_enable) begin
                memory[wptr] <= write_data;
                wptr <= wptr + 1;
            end
        end
    end

    // Handle reads from the memory.
    // We don't care about whether the buffer is "full" or "empty".
    // We just assign "rptr" = the read address requested.
    // There's a race condition here if wptr = read_addr. I think it's
    // okay if we require that never happen.
    always @(posedge clock) begin
        if (!reset) begin
            read_data <= 0;
        end else begin
            if (read_enable) begin
                read_data <= memory[read_addr];
            end
        end
    end

endmodule
