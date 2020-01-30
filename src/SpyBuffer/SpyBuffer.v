// SpyBuffer.v
// Prototype implementation of a a Spy Buffer for ATLAS TDAQ HTT
// Track Processor board.
// This is the main module/interface definition.
// Ben Rosser <bjr@sas.upenn.edu>

`default_nettype none

module SpyBuffer #(
    // The width of input data (e.g. 2^WIDTH bytes + 1 for metadata).
    parameter DATA_WIDTH = 64,

    // Width of the spy buffer's memory block. (e.g. 2^WIDTH rows of DATA_WIDTH size).
    parameter SPY_MEM_WIDTH = 7,

    // The width of the flow control buffer's memory.
    // If this is pushed to 5 or higher, block RAM will be inferred.
    // (Do we want that?)
    // (Presumably, the threshold coul also be adjusted!)
    parameter FC_FIFO_WIDTH = 3,

    // The size and width of the event list / metadata list memory.
    parameter EL_MEM_SIZE = 16,
    parameter EL_MEM_WIDTH = 4
) (

    // The read and write clocks, respectively.
    input wire rclock,
    input wire wclock,

    // TODO: is a reset necessary on both sides? Probably...
    input wire rreset,
    input wire wreset,

    input wire [DATA_WIDTH:0] write_data,
    input wire write_enable,
    input wire read_enable,

    // Freeze the spy buffer.
    input wire freeze,

    // This is a proxy for some more sophisticated readout mechanism.
    // (involving block transfer protocols?)
    input wire spy_read_enable,
    input wire spy_meta_read_enable,

    input wire [SPY_MEM_WIDTH-1:0] spy_read_addr,
    input wire [EL_MEM_WIDTH-1:0] spy_meta_read_addr,
    output wire [EL_MEM_WIDTH-1:0] spy_meta_write_addr,
    output wire [SPY_MEM_WIDTH-1:0] spy_write_addr,

    output wire [DATA_WIDTH:0] read_data,
    output wire almost_full,
    output wire empty,

    // Spy outputs.
    output wire [DATA_WIDTH:0] spy_data,
    output wire [SPY_MEM_WIDTH:0] spy_meta_read_data
);

    // To first order, I think we want an asynchronous FIFO.
    // The write data should get passed to the spy writer block
    // Which should sit on top of a differently structured FIFO for spying.
    // And there should be an internal spy controller which reads out.

    // So, we grab the aFifo source code here for the "memory".
    // Then at some point we modify it's internal memory to use some Xilinx interface.

    // Flow control buffer, provided by an aFifo.
    aFifo #(
        .DSIZE(DATA_WIDTH+1),
        .ASIZE(FC_FIFO_WIDTH)
    ) buffer (
        .rdata(read_data),
        .wdata(write_data),
        .rclk(rclock),
        .wclk(wclock),
        .rempty(empty),
        .walmostfull(almost_full),
        .wfull(),
        .ralmostempty(),
        .wrst_n(wreset),
        .rrst_n(rreset),
        .winc(write_enable),
        .rinc(read_enable)
    );

    // This is the block that actually is the "spy controller".
    // It handles the "spy" part of the "spy buffer".
    // It wants to live in the write clock domain.

    // Note that with this naive implementation, there is no "spy memory"
    // readout block (everything's contained beneath the "spy controller").
    // In reality, possibly we would want that to live in the toplevel and
    // have some block transfer protocol thing, presumably powered by Xilinx
    // libraries.

    SpyController #(
        .DATAWIDTH(DATA_WIDTH),
        .MEMWIDTH(SPY_MEM_WIDTH),
        .METASIZE(EL_MEM_SIZE),
        .METAWIDTH(EL_MEM_WIDTH)
    ) spy (
        .clock(wclock),
        .reset(wreset),
        .freeze(freeze),
        .data_in(write_data),
        .write_enable_in(write_enable),
        .read_addr(spy_read_addr),
        .read_enable_in(spy_read_enable),
        .meta_read_enable(spy_meta_read_enable),
        .meta_read_addr(spy_meta_read_addr),
        .data_out(spy_data),
        .mem_wptr(spy_write_addr),
        .meta_write_addr(spy_meta_write_addr),
        .meta_read_data(spy_meta_read_data)
    );

endmodule
