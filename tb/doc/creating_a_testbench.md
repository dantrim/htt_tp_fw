# Creating a Testbench

Here we walk through how to create a testbench using the [tb create](../README.md#tb-create)
command provided by the testbench infrastructure.

   * [Requirements](#requirements)
   * [Environment Preparation](#prepare-your-environment)
   * [Run `tb create` to Initialize the Testbench](#run-tb-create)
   * [Plug your Logic Block into the Testbench Toplevel](#adding-your-block)
 
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
   
# Requirements

You must satisfy the [requirements](../README.md#requirements) and
[installation](../README.md#installation-and-setup) of the testbench
infrastructure.

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

# Adding Your Logic Block
