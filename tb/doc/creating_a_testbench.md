# Creating a Testbench

Here we walk through how to create a testbench using the [tb create](../README.md#tb-create)
command provided by the testbench infrastructure.

   * [Requirements](#requirements)
   * [Environment Preparation](#prepare-your-environment)
   * [Run `tb create` to Initialize the Testbench](#run-tb-create)
   * [Plug Your Logic Block into the Testbench Toplevel](#adding-your-logic-block)
      * [Update the Toplevel Makefile](#update-the-toplevel-makefile)
      * [Predefined Makefile Variables](#predefined-makefile-variables)
      * [Instantiate your Logic Block and Connect it to the Spy+FIFO blocks](#connecting-the-blocks)
 
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















