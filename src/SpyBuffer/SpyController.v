// Spy Buffer "controller" module - using sentinel words.
// The spy buffer controller handles making the decision to
// record incoming information in the spy buffer.
// Ben Rosser <bjr@sas.upenn.edu>

// NOTE: this version of the block (TODO rename) uses sentinel bits
// in the event list to indicate wrap-around. This requires a state
// machine.

// NOTE: an implicit assumption here is made that we will NEVER
// have two start-of-event metadata words in a row.

// NOTE: the "readout" pieces here are probably going to go away,
// in the long term, and be replaced entirely by block RAM instantiations.
// It should be possible to have different readout controls altogether.
// e.g. some kind of block transfer protocol rather than just this.

`default_nettype none

module SpyController #(
    // Width of data being passed into the system, *without* extra metadata bit.
    parameter DATAWIDTH = 64,

    // Width of the spy buffer's spy memory. This is also the width of addresess.
    parameter MEMWIDTH = 6,

    // Size *and* width of the event list FIFO memory.
    parameter METASIZE = 16,
    parameter METAWIDTH = 4
) (
    // Input wires -- clock, reset.
    input wire clock,
    input wire reset,

    // Input -- control signal to freeze.
    input wire freeze,

    // Inputs -- spy write enable and spy data.
    input wire [DATAWIDTH:0] data_in,
    input wire write_enable_in,

    // Inputs -- spy read enable and read address.
    input wire [MEMWIDTH-1:0] read_addr,
    input wire read_enable_in,

    // Same for the event / metadata list.
    input wire meta_read_enable,
    input wire [METAWIDTH-1:0] meta_read_addr,

    // Output -- data being read out from spy memory.
    output wire [DATAWIDTH:0] data_out,
    output wire [MEMWIDTH-1:0] mem_wptr,

    // Output -- metadata write address and occupancy.
    // These are the two things we could possibly need to read
    // the metadata event list, regardless of which mode is used.
    output wire [METAWIDTH-1:0] meta_write_addr,
    output wire [MEMWIDTH:0] meta_read_data
);

    // Include the SpyProtocol.vh file.
    `include "SpyBuffer/SpyProtocol.vh"

    // Define the states of the state machine
    // that controls the metadata FIFO.
    localparam STATE_RESET = 3'b000;
    localparam STATE_IDLE = 3'b001;
    localparam STATE_WRITE = 3'b010;
    localparam STATE_DATA_LOOP = 3'b011;
    localparam STATE_FROZEN = 3'b100;
    localparam STATE_EXTRA_LOOP = 3'b101;

    // Define the state registers.
    reg [2:0] state_reg;
    reg [2:0] state_next;

    // Internal version of spy write and read enables.
    reg write_enable;

    // We need to decide if this is the start of an event or not.
    // For now, let's assume the following naive protocol:
    // Data passed here will be 2**WIDTH + 1 bytes long.
    // The extra byte, if "1" will mean "SOE". Otherwise it's not.
    wire [DATAWIDTH:0] data;
    wire start_event;

    // Wire indicating that the memory has looped.
    wire mem_looped;

    // Control signals for the spy memory block.
    reg [MEMWIDTH-1:0] mem_wptr_reg;

    // Control signals for the metadata list.
    reg ml_push;
    reg [MEMWIDTH:0] ml_data;

    reg start_event_reg = 0;

    // At the rising edge of the clock-- propagate state.
    always @(posedge clock, negedge reset) begin
        if (!reset) begin
            state_reg <= STATE_RESET;
            start_event_reg <= 0;
            mem_wptr_reg <= 0;
            write_enable <= 0;
        end else begin
            state_reg <= state_next;
            start_event_reg <= start_event;
            mem_wptr_reg <= mem_wptr;
            write_enable <= write_enable_in && (state_reg != STATE_FROZEN);
        end
    end

    // The state machine for the metadata FIF O(event list).
    always @* begin
        case (state_reg)
            STATE_RESET: begin
                ml_push = 0;
                ml_data = 0;
                state_next = STATE_WRITE;
            end

            // This is the write state; we know we're not frozen.
            // It's somewhat misleadingly named; this is essentially a "normal operations"
            // state, which could include that the system is idle.
            STATE_WRITE: begin
                ml_push = 0;
                ml_data = 0;
                state_next = STATE_WRITE;

                // If we're frozen, proceed immediately to STATE_FROZEN.
                if (freeze) begin
                    state_next = STATE_FROZEN;
                end else if (write_enable) begin

                    // Now, we need to decide how to handle the metadata FIFO.
                    // If this is the start of event, we want to write the SOE word to the event list.
                    // If this write *will* loop the metadata FIFO, we want to-- on the next clock--
                    // insert a sentinel word into the FIFO.
                    // This handles the edge case. The only problem is that, in STATE_DATA_LOOP...
                    // we need to be able to duplicate all this logic without the loop check.

                    // In this condition, we must go to DATA_LOOP.
                    if (mem_looped && start_event_reg) begin
                        state_next = STATE_DATA_LOOP;

                        // Assign the ml data = current mem_wptr + no sentinel bit.
                        ml_data = {1'b0, mem_wptr_reg};
                        ml_push = 1;

                    end else begin

                        // If mem_looped *xor* start event are set, write the correct thing.
                        // I guess it doesn't actually matter what is written in the sentinel word.
                        // It should matter in theory. some kind of control code.
                        if (mem_looped) begin
                            ml_data = {1'b1, mem_wptr_reg};
                            ml_push = 1;
                        end else if (start_event_reg) begin
                            ml_data = {1'b0, mem_wptr_reg};
                            ml_push = 1;
                        end else begin
                            ml_push = 0;
                        end

                        // Technically, this line is redundant.
                        state_next = STATE_WRITE;
                    end
                end
            end

            // This is our "we are about to loop in the memory FIFO" state.
            // This state does not interfere with normal writes.
            STATE_DATA_LOOP: begin
                // We need to handle the ml_data and ml_push writes.
                ml_data = {1'b1, mem_wptr_reg};
                ml_push = 1;

                // Great, now we get to decide the next state!
                if (freeze) begin
                    state_next = STATE_FROZEN;
                end else begin
                    state_next = STATE_WRITE;
                end
            end

            STATE_FROZEN: begin
                // If "freeze" is still held down, remain in state frozen and prevent writing.
                // TODO XXX: should we be able to go directly to STATE_WRITE from here? Probably not.

                ml_push = 0;
                ml_data = 0;

                if (freeze) begin
                    state_next = STATE_FROZEN;
                end else begin
                    state_next = STATE_WRITE;
                end
            end

            // We need more states, I think.
            default: begin
                state_next = STATE_RESET;
                ml_push = 0;
                ml_data = 0;
            end
        endcase
    end

    // It turns out we probably can just use the *same* memory block for the event list.
    SpyMemory #(
        .WIDTH(METAWIDTH),
        .DATAWIDTH(MEMWIDTH+1)
    ) metalist (
        .clock(clock),
        .reset(reset),
        .write_enable(ml_push),
        .write_data(ml_data),
        .read_addr(meta_read_addr),
        .read_enable(meta_read_enable),
        .write_pointer(meta_write_addr),
        .read_data(meta_read_data),
        // We don't need to know that the spy memory has looped... do we?
        // Might be good to be able to measure how frequently this occurs.
        .looped()
    );

    // Instantiate the actual memory block used by the spy buffer.
    SpyMemory #(
        .WIDTH(MEMWIDTH),
        .DATAWIDTH(DATAWIDTH+1)
    ) memory (
        .clock(clock),
        .reset(reset),
        .write_enable(write_enable_in && (state_reg != STATE_FROZEN)),
        .write_data(data),
        .read_addr(read_addr),
        .read_enable(read_enable_in),
        .write_pointer(mem_wptr),
        .read_data(data_out),
        .looped(mem_looped)
    );

    // I think this syntax is legal. Split "data_in".
    // We should do something smarter in the real system!
    // I think this (and the overflow detection code at the bottom) needs state-machine-ification.
    assign start_event = data_in[DATAWIDTH] && (data_in[DATAWIDTH-1:DATAWIDTH-8] == START_EVENT);

    // TODO: This is redundant now: we store metadata bits!
    assign data[DATAWIDTH:0] = data_in[DATAWIDTH:0];

endmodule
