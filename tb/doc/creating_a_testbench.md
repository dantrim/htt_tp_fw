# Creating a Testbench

Here we walk through how to create a testbench using the [tb create](../README.md#tb-create)
command provided by the testbench infrastructure.

Each of the sections in this Table of Contents should be followed sequentially in order
to create a testbench:

   * [Requirements](#requirements)
   * [Environment Preparation](#prepare-your-environment)
   * [Run `tb create` to Initialize the Testbench](#run-tb-create)
   * [Plug Your Logic Block into the Testbench Toplevel](#adding-your-logic-block)
      * [Update the Toplevel Makefile](#update-the-toplevel-makefile)
         * [Predefined Makefile Variables](#predefined-makefile-variables)
      * [Instantiate your Logic Block and Connect it to the Spy+FIFO blocks](#connecting-the-blocks)
      * [Complete the Testbench Configuration](#configure-your-testbench)
         * [input_args](#testbench-input-args)
         * [run_config](#testbench-run-config)
         * [testvectors](#testbench-testvectors)
   * [Run the Testbench](#run-the-testbench)
   * [Finished!](#all-done)
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------- REQUIREMENTS ---------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
   
# Requirements

You must satisfy the [requirements](../README.md#requirements) and
[installation](../README.md#installation-and-setup) of the testbench
infrastructure.

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------- PREPARE YOUR ENVIRONMENT ---------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->

# Prepare Your Environment

Move to the `tp-fw/tb` directory and setup the testbench environment:

```bash
$ cd /your/specific/path/tp-fw/tb
$ source setup_env.sh
Virtual environment "env" has been activated. Type 'deactivate' to exit.
(env) $ tb -h # <-- run this to ensure that the "tb" command is working properly
Usage: tb [OPTIONS] COMMAND [ARGS]...

  Top-level entrypoint into TP fw cocotb test-bench infrastructure.

Options:
  -h, --help  Show this message and exit.

Commands:
  check-config     Check/inspect a testbench's configuration (*.json) file.
  create           Create a new test.
  diff             Diff two *.evt files and test for differences.
  dump             Dump the contents of an *.evt file.
  list             List all available testbenches and their status.
  run              Setup and run cocotb-based testbenches.
  test-summary     Dump the test results *.json file.
  update-makefile  Update the QuestaSim makefile used by CocoTB to dump all...
```

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!---------------------------- RUN TB CREATE ---------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
# Run tb create

The `tb create` command takes a few required inputs (see [tb create](../README.md#tb-create)).

It requires that you know how many inputs and outputs will be exposed at the
outermost level of your `DUT`. That is, how many `input_spybuffers`
and `output_spybuffers` does your toplevel `DUT` require (where we use the terms
`input_spybuffers` and `output_spybuffers` as in the figures appearing in the
[Overview of the Testbench Infrastructure section](../README.md#overview-of-the-testbench-infrastructure))?
This will most of the time simply be the number
of inputs and outputs your logic block has.

It also requires that your logic block have an identifiable name. For example,
in the case of the `board2board_switching` block this can be something like `b2b`.
Just something that clearly identifies the logic block(s) in the TP.

For the current example, we'll assume that our logic block has the following
values for these quantities:

 * name: `tutorial_block`
 * number of inputs: `4`
 * number of outputs: `14`

With this information, let's run `tb create`:
```bash
(env) $ tb create --test-name tutorial_block --n-inputs 4 --n-outputs 14
Creating test "tutorial_block" with 4 inputs and 14 outputs.
```

This creates the following new directories and files:

```
tb/
 ├── src/
 │   └── tp_tb/
 │       └── testbench/
 │           └── tutorial_block/
 │               ├── test/
 │               │   ├── Makefile
 │               │   ├── TopLevel_tutorial_block.v
 │               │   └── test_tutorial_block.py
 │               ├── tutorial_block_ports.py
 │               ├── tutorial_block_wrapper.py
 │               └── tutorial_block_utils.py
 └── test_config/
     └── config_tutorial_block.json
```
More information of each of these files, and directory structure, can be found
in the [Testbench Structure page](testbench_structure.md).

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!-------------------------- ADDING THE LOGIC BLOCK --------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->

# Adding Your Logic Block

## Update the Toplevel Makefile

For the current tutorial, we'll use an already existing logic block: the
`board2board_switching` block.
First, we'll need to know where the requisite HDL source files are located
for this logic block. We'll need the source files for the block itself as well
as any external IP that the block depends on:

   * `board2board_switching` logic: [tp-fw/src/board2board_switching/rtl](../../src/board2board_switching/rtl)
   * external IP (Vivado IP): [tp-fw/src/board2board_switching/ip](../../src/board2board_switching/ip)

If we now look into the `cocotb` test module `Makefile` generated by the `tb create`
command, which should be located at `tp-fw/tb/src/tp_tb/testbench/tutorial_block/test/Makefile`,
we will need to add these source files to the `VERILOG_SOURCES` listing.

Running `tb create` initializes the `VERILOG_SOURCES` variable with the source files
necessary to compile the `Spy+FIFO` blocks and should initially look something like:

```make
# Location of HDL source files
SRCDIR = $(PWD)/../../../../../../src
SBDIR = $(SRCDIR)/SpyBuffer
VERILOG_SOURCES = \
    $(PWD)/$(TESTBENCH_TOPLEVEL).v \
    $(SBDIR)/SpyBuffer.v \
    $(SBDIR)/SpyController.v \
    $(SBDIR)/SpyMemory.v \
    $(SBDIR)/aFifo/aFifo.v \
    $(SBDIR)/aFifo/fifomem.v \
    $(SBDIR)/aFifo/rptr_empty.v \
    $(SBDIR)/aFifo/sync_r2w.v \
    $(SBDIR)/aFifo/sync_w2r.v \
    $(SBDIR)/aFifo/wptr_full.v
```

We can then define, for simplicity, the variable,
```make
TUTORIAL_SRC_DIR=$(SRCDIR)/board2board_switching
```
and update the `VERILOG_SOURCES` variable to be:

```make
# Location of HDL source files
SRCDIR = $(PWD)/../../../../../../src
SBDIR = $(SRCDIR)/SpyBuffer
TUTORIAL_SRC_DIR=$(SRCDIR)/board2board_switching
VERILOG_SOURCES = \
    $(PWD)/$(TESTBENCH_TOPLEVEL).v \
    $(SBDIR)/SpyBuffer.v \
    $(SBDIR)/SpyController.v \
    $(SBDIR)/SpyMemory.v \
    $(SBDIR)/aFifo/aFifo.v \
    $(SBDIR)/aFifo/fifomem.v \
    $(SBDIR)/aFifo/rptr_empty.v \
    $(SBDIR)/aFifo/sync_r2w.v \
    $(SBDIR)/aFifo/sync_w2r.v \
    $(SBDIR)/aFifo/wptr_full.v \
    $(TUTORIAL_SRC_DIR)/rtl/find_idx.v \
    $(TUTORIAL_SRC_DIR)/ip/fifo_65/fifo_65_sim_netlist.v \
    $(TUTORIAL_SRC_DIR)/rtl/merge_event_handler.v \
    $(TUTORIAL_SRC_DIR)/rtl/cluster_merge_engine.v \
    $(TUTORIAL_SRC_DIR)/rtl/cluster_routing_engine.v \
    $(TUTORIAL_SRC_DIR)/rtl/cluster_sync_engine.v \
    $(TUTORIAL_SRC_DIR)/rtl/board2board_switching.v
```
where we have simply added all source files appearing in the directories listed above.

In addition to including these source files, we'll need to point the `cocotb` compilation
to the source directories as well as to the directories housing the external
components. This corresponds to adjusting the `EXTRA_ARGS` and `VSIM_ARGS` variables
appearing in the `Makefile`, which initially look something like this:
```make
EXTRA_ARGS += +incdir+$(SRCDIR)
VSIM_ARGS  += -debugDB -voptargs="+acc"
```

For compiling the `board2board_switching` logic, we adjust these variables as so:
```make
EXTRA_ARGS += +incdir+$(SRCDIR) +incdir+$(TUTORIAL_SRC_DIR)/include +incdir+$(TUTORIAL_SRC_DIR)/ip -L $(COMPONENTS_LIB_DIR)/unisims_ver -L $(COMPONENTS_LIB_DIR)/unisim
VSIM_ARGS  += glbl -debugDB -voptargs="+acc"
```

A note on these changes:
   * The variable `COMPONENTS_LIB_DIR` should point to external IP generated, for example, by Vivado and is picked up based on the `components_lib_dir` variable that appears in the testbench configuration file (see the [Testbench Structure page](testbench_structure.md#testbench-configuration))
   * The `glbl` module provided to `VSIM_ARGS` is required by the Vivado-generated IP for the fifo used by the `board2board_switching` logic

## Predefined Makefile Variables

You will see predefined variables in your toplevel `Makefile`.
**These variables should not be manipulated by the user.**

These variables are `SIM_BUILD`, `TESTBENCH_TOPLEVEL`, `TESTBENCH_TEST_MODULE`, and `COMPONENTS_LIB_DIR`
(at the time of writing this). These variables
are generated during the execution of your testbench (via the [tb run command](../README.md#tb-run)).
Logically, they correspond to:
   * `SIM_BUILD`: This will point to the directory in which all [testbench output](../README.md#output-generated-by-the-testbenches) is placed
   * `TESTBENCH_TOPLEVEL`: This is the name of the toplevel HDL file for your testbench, and is located in the same directory as the `Makefile` and named `TopLevel_<test-name>.v` (the variable `TESTBENCH_TOPLEVEL` does not include the "`.v`" extension)
   * `TESTBENCH_TEST_MODULE`: This is the name of the python file wherein you will implement the `cocotb` testbench module, and is located in the same directory as the `Makefile` and named `test_<test-name>.py` (the variable `TESTBENCH_TEST_MODULE` does not include the "`.py`" extension)
   * `COMPONENTS_LIB_DIR`: This is taken from the `components_lib_dir` variable appearing under the `run_config` section of the [testbench configuration](testbench_structure.md#testbench-configuration)

In general, all variables defined in the `run_config` section of the [testbench configuration](testbench_structure.md#testbench-configuration)
will be made available as environment variables with their name in all capital letters (e.g. `components_lib_dir` gets set to `COMPONENTS_LIB_DIR`).





<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!-------------------------- CONNECTING THE BLOCKS ---------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
## Connecting the Blocks

The `TopLevel_tutorial_block.v` file created by `tb create` will initially
be populated with the `input_spybuffers` and `output_spybuffers` blocks,
in quantity corresponding to the `--n-inputs` and `--n-outputs`, respectively,
provided to `tb create`. These blocks look something like,

```verilog
generate
    for(genvar i = 0; i < 4; i++)
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
```

There are pre-defined elements for connecting your logic block to the
`input_spybuffers` and `output_spybuffers` blocks. They may or may not be
needed by your logic block and of course they may be re-named as desired.
In our case, these elements are:

```verilog
wire BLOCK_input_write_enable [4];
wire [DATA_WIDTH-1:0] BLOCK_input_data [4];
wire BLOCK_input_read_enable [4];
wire BLOCK_input_almost_full [4];
wire BLOCK_input_empty [4];

wire BLOCK_output_write_enable [14];
wire [DATA_WIDTH-1:0] BLOCK_output_data [14];
wire BLOCK_output_read_enable [14];
wire BLOCK_output_almost_full [14];
wire BLOCK_output_empty [14];
```

We instantiate the `board2board_switching` block and connect it to these
signals as follows:
```verilog
//
// Here place the DUT block(s)
//
board2board_switching #(
    .DATA_WIDTH(DATA_WIDTH),
    .TOTAL_CLUSTERS(N_INPUTS),
    .TOTAL_OUTPUT_BOARDS(N_OUTPUTS),
    .FIFO_DEPTH_BITS(6),
    .BOARD_ID(0)
)
board2board_switching_inst (
    .b2b_clk(clock),
    .b2b_rst_n(reset_n),
    .b2b_srst_n(reset_n),
    .cluster_data(BLOCK_input_data),
    .cluster_req(BLOCK_input_read_enable),
    .cluster_almost_full(BLOCK_input_almost_full),
    .cluster_empty(BLOCK_input_empty),
    .output_board_event(BLOCK_output_data),
    .output_board_wren(BLOCK_output_write_enable),
    .output_board_almost_full(BLOCK_output_almost_full)
);
```
Here we see that we have connected the `BLOCK_input` signals to those signals
responsible for *pulling* data from `input_spybuffers`, and the `BLOCK_output`
signals to those responsible for *pushing* data into `output_spybuffers`.

With this done, the logic is connected and we are almost ready to start
driving the testbench.

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!------------------------ TESTBENCH CONFIGURATION ---------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->

## Configure your Testbench

As mentioned in the [Testbench Structure page](testbench_structure.md#testbench-configuration),
every testbench is required to have a `JSON` configuration file satisfying the
[testbench configuration schema](../../schema/schema_test_config.json).

Running `tb create` generates an initial testbench configuration file. For our
testbench for `tutorial_block`, this file is `config_tutorial_block.json`.

### Testbench Input Args

The `input_args` block of the configuration generated by `tb create` is pre-filled
with the requisite variables:

```json
"input_args": {
    "n_events": 5,
    "event_detail": false,
    "clock_period": 5,
    "clock_time_unit": "ns"
}
```

These are responsible for:
   * `n_events`: The number of events to load from the input testvectors and drive onto the testbench
   * `event_detail`: A flag to specify if the test output should dump to screen test details for every single event (versus summary reporting) (**note:** regardless of whether or not you set this variable to `true` or `false`, the event-detailed information is still saved in the `test_results_summary*.json` files generated as part of the [testbench output](../README.md#output-generated-by-the-testbenches))
   * `clock_period`: Sets the simulator's clock period
   * `clock_time_unit`: The unit of time for the simulator clock

Additional quantities can be added to the `input_args` block. For example,
let's say that in your testbench you put in the ability to scramble event order
but you want this to be something that you can toggle on/off between runs.
You can add a field `scramble_event_order` to the `input_args` field and this
will be available to your testbench module (`test_tutorial_block.py`):
```python
import test_config
...
@cocotb.test()
def tutorial_block_test(dut):
   ...
   config = test_config.get_config()
   input_args = config["input_args"]
   ...
   do_event_order_scramble = input_args["scramble_event_order"]
   ...
```

### Testbench Run Configuration

The testbench configuration file created by `tb create` fills the required `run_config`
variables with:
```json
"run_config": {
    "output_directory_name": "tutorial_block",
    "test_location": "/full/path/tp-fw/tb/src/tp_tb/testbench/tutorial_block/test",
    "expected_is_observed": false,
    "components_lib_dir": "/another/full/path/xilinx/compiled_libraries/v2019.1/"
}
```
The `output_directory_name` and `test_location` variables can generally be left alone.
The `components_lib_dir` path location will need to be updated to the specific path
on your system, and of course can be left blank if you do not depend on it.

### Testbench Testvectors

The `testvectors` field of the testbench configuration generated by `tb create`
fills in a dummy path to the `testvector_dir`, which is a path pointing to a 
directory housing testvector files. The `input` and `output` testvector files
themselves have dummy names, but appear in correct quantity corresponding to
the `--n-inputs` and `--n-outputs` variables provided to the `tb create` command:
```json
"testvectors" :
{
    "testvector_dir" : "/foo/bar/foo/baz",
    "input": [
        { "0": "INPUT_FILENAME_0.evt" },
        { "1": "INPUT_FILENAME_1.evt" },
        { "2": "INPUT_FILENAME_1.evt" },
        { "3": "INPUT_FILENAME_1.evt" }
    ]
    ...
    ...
}
```
You will need to update the `testvector_dir` path, and the filenames according to your
needs.

For example, for the `tutorial_block` testbench, which instantiates the `board2board_switching`
block, we can fill these files out as follows:
```json
{
    "testvector_dir" : "/foo/bar/foo/baz",
    "input": [
        { "0" : "BoardToBoardInput_AMTP0_Pixel0.evt" },
        { "1" : "BoardToBoardInput_AMTP0_Pixel1.evt" },
        { "2" : "BoardToBoardInput_AMTP0_Strip0.evt" },
        { "3" : "BoardToBoardInput_AMTP0_Strip1.evt" }
    ],
    "output": [
        { "0" : "TPtoSync_srcAMTP0_destAMTP0.evt" },
        { "1" : "TPtoSync_srcAMTP0_destAMTP1.evt" },
        { "2" : "TPtoSync_srcAMTP0_destAMTP2.evt" },
        { "3" : "TPtoSync_srcAMTP0_destAMTP3.evt" },
        { "4" : "TPtoSync_srcAMTP0_destAMTP4.evt" },
        { "5" : "TPtoSync_srcAMTP0_destAMTP5.evt" },
        { "6" : "TPtoSync_srcAMTP0_destAMTP6.evt" },
        { "7" : "TPtoSync_srcAMTP0_destAMTP7.evt" },
        { "8" : "TPtoSync_srcAMTP0_destAMTP8.evt" },
        { "9" : "TPtoSync_srcAMTP0_destAMTP9.evt" },
        { "10" : "TPtoSync_srcAMTP0_destAMTP10.evt" },
        { "11" : "TPtoSync_srcAMTP0_destAMTP11.evt" },
        { "12" : "TPtoSync_srcAMTP0_destSSTP0.evt" },
        { "13" : "TPtoSync_srcAMTP0_destSSTP1.evt" }
    ]
}
```

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!-------------------------- RUN THE TESTBENCH -------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->

# Run the Testbench

If you have performed the steps detailed above, you are now ready to run the
testbench using the minimal setup where you simply:

   1. Load the input testvectors
   2. Drive the input signals contained in the input testvectors into the `input_spybuffers`
   3. Monitor the output signals generated by the `output_spybuffers`
   4. Compare the output signals generated by the `output_spybuffers` to those signals that are expected as given by the output testvectors

If all goes according to plan, the result of the comparison of step `4` will be
displayed onto the screen.

To run the testbench, do:
```bash
(env) $ cd /path/to/tp-fw/tb
(env) $ tb run ./test_config/config_tutorial_block.py
...
... # lots of output
(env) $ # test done
```

If the test completes, the output will be located under the `tp-fw/tb/test_output/tutorial_block/`
directory:
```bash
(env) $ ls ./test_output/tutorial_block/
fifodriver_TutorialBlock_00_Input00.evt           fifomonitor_TutorialBlock_06_Output06_timing.txt  test_results_summary_TutorialBlock_srcOutput00_destOutput00.json
fifodriver_TutorialBlock_00_Input00_timing.txt    fifomonitor_TutorialBlock_07_Output07.evt         test_results_summary_TutorialBlock_srcOutput00_destOutput01.json
fifodriver_TutorialBlock_01_Input01.evt           fifomonitor_TutorialBlock_07_Output07_timing.txt  test_results_summary_TutorialBlock_srcOutput00_destOutput02.json
fifodriver_TutorialBlock_01_Input01_timing.txt    fifomonitor_TutorialBlock_08_Output08.evt         test_results_summary_TutorialBlock_srcOutput00_destOutput03.json
fifodriver_TutorialBlock_02_Input02.evt           fifomonitor_TutorialBlock_08_Output08_timing.txt  test_results_summary_TutorialBlock_srcOutput00_destOutput04.json
fifodriver_TutorialBlock_02_Input02_timing.txt    fifomonitor_TutorialBlock_09_Output09.evt         test_results_summary_TutorialBlock_srcOutput00_destOutput05.json
fifodriver_TutorialBlock_03_Input03.evt           fifomonitor_TutorialBlock_09_Output09_timing.txt  test_results_summary_TutorialBlock_srcOutput00_destOutput06.json
fifodriver_TutorialBlock_03_Input03_timing.txt    fifomonitor_TutorialBlock_10_Output10.evt         test_results_summary_TutorialBlock_srcOutput00_destOutput07.json
fifomonitor_TutorialBlock_01_Output01.evt         fifomonitor_TutorialBlock_10_Output10_timing.txt  test_results_summary_TutorialBlock_srcOutput00_destOutput08.json
fifomonitor_TutorialBlock_01_Output01_timing.txt  fifomonitor_TutorialBlock_11_Output11.evt         test_results_summary_TutorialBlock_srcOutput00_destOutput09.json
fifomonitor_TutorialBlock_02_Output02.evt         fifomonitor_TutorialBlock_11_Output11_timing.txt  test_results_summary_TutorialBlock_srcOutput00_destOutput10.json
fifomonitor_TutorialBlock_02_Output02_timing.txt  fifomonitor_TutorialBlock_12_Output12.evt         test_results_summary_TutorialBlock_srcOutput00_destOutput11.json
fifomonitor_TutorialBlock_03_Output03.evt         fifomonitor_TutorialBlock_12_Output12_timing.txt  test_results_summary_TutorialBlock_srcOutput00_destOutput12.json
fifomonitor_TutorialBlock_03_Output03_timing.txt  fifomonitor_TutorialBlock_13_Output13.evt         test_results_summary_TutorialBlock_srcOutput00_destOutput13.json
fifomonitor_TutorialBlock_04_Output04.evt         fifomonitor_TutorialBlock_13_Output13_timing.txt  transcript
fifomonitor_TutorialBlock_04_Output04_timing.txt  modelsim.ini                                      vish_stacktrace.vstf
fifomonitor_TutorialBlock_05_Output05.evt         results.xml                                       vsim.dbg
fifomonitor_TutorialBlock_05_Output05_timing.txt  runsim.do                                         vsim.wlf
fifomonitor_TutorialBlock_06_Output06.evt         sim.log                                           work
```

The output from the testbench is described in the [testbench output section of the README](../README.md#testbench-output).

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!-------------------------------- ALL DONE ----------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->

# All Done

At this point, if you successfully went through the steps outlined in the sections
above, you have a testbench that will drive testvector-generated signals
through your logic block, with the block's outputs compared to the expected output
provided by the output testvectors.

If you require more complex testbenches (e.g. adding delays, skews, testing logic edge cases, etc...)
you will need to write some code. You will likely need to modify
the `test_<test-name>.py` file if you adjust `input_args`, for example.
If you adjust the dataflow through your block, you will likely need to add
code to `<test-name>_wrapper.py` and perhaps methods to `<test_name>_utils.py`.
Adding modules is also allowed, of course. For example, in the `board2board_switching`
testbench, we add event delays that add simulation time between driving
new events onto the inputs. This is done by adding a module
[b2b_flow.py](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/b2b_flow.py)
which is used in [b2b_wrapper.py](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/b2b_wrapper.py#L47)
to add delays to the driving of signals onto the `input_spybuffers`.
This option is configurable via the `input_args` variable ["event_delays"](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/test_config/config_b2b.json#L8).










