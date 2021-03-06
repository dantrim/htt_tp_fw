The following details the components of a valid testbench.
Described is the minimal structure required to simply begin passing
data through a testbench.

Additional structure or complexity, 
as needed on a per-testbench status, can be added by users, **but the
additions should be kept to the specific testbench's directory under
tp_tb/testbench/\<name-of-testbench\>!** (see below).

[[_TOC_]]

# Testbench Anatomy

```
tb/
 ├── src/
 │   └── tp_tb/
 │       └── testbench/
 │           └── tp_block/
 │               ├── test/
 │               │   ├── Makefile
 │               │   ├── TopLevel_tp_block.v
 │               │   └── test_tp_block.py
 │               ├── tp_block_ports.py
 │               ├── tp_block_wrapper.py
 │               └── tp_block_utils.py
 └── test_config/
     └── config_tp_block.json
```


Let's assume that you have a firmware block that you wish to test, and
that that firmware block is called `tp_block`. The above schematic
illustrates all relevant directories and files under the `tp-fw/tb/` directory
that relate to the testbench for `tp_block`.

For the following, let us further assume that the firmware block `tp_block` has two
input ports, and two output ports.

Below is a description of each file and directory illustrated above for the `tp_block` testbench.



# Testbench configuration

Each testbench is required to have defined a `JSON` configuration file located
under the `test_config/` directory. The name of each configuration file should be
unique and should follow the `config_<test_name>.json` scheme.

Validation of a testbench configuration is done by running the [tb check-config](../README.md#tb-check-config)
utility.

In the case of the testbench for the `tp_block`, this file is called `config_tp_block.json`:

## config_tp_block.json

This is the testbench configuration file specific to `tp_block`'s testbench.
As mentioned in the [README](../README.md), this configuration file must satisfy
the `jsonschema` defined under [schema_test_config.json](../schema/schema_test_config.json).

A valid schema for `tp_block` would look something like:
```json
{
    "testbench_config" :
    {
       "test_name" : "tp_block"
       ,"input_args" :
       {
           "n_events" : 5
           ,"clock_period" : 5
           ,"clock_time_unit" : "ns"
       },
       "run_config" :
       {
           "output_directory_name" : "tp_block"
           ,"test_location" : "src/tp_tb/testbench/tp_block/test"
           ,"expected_is_observed" : false
           ,"components_lib_dir" : "/path/to/any/external/ip/xilinx/compiled_libraries/"
       },
        "testvectors" :
        {
           "testvector_dir" : "/full/path/to/testvectors/",
            "input":
            [
                { "0" : "testvector_tp_block_input0.evt" },
                { "1" : "testvector_tp_block_input1.evt" }
            ],
            "output":
            [
                { "0" : "testvector_tp_block_output0.evt" },
                { "1" : "testvector_tp_block_output1.evt" }
            ]
        }
    }
}
```

Let's look closely at this configuration.

The `testbench_config` node is the top-level node of any testbench configuration file. A description of the subsequent nodes
is as follows:

   * `test_name`: The name of the test, should be the same as the name of the testbench directory, which for the `tp_block` testbench is the "tp_block" from the path `tp_tb/testbench/tp_block`
   * `input_args`: Variable names and values used to pass to the underlying testbenches (see [schema_test_config.json](../schema/schema_test_config.json) for required `input_args`)
   * `run_config`: Define names for output paths, locations to external libs, etc...
      * `/output_directory_name`: This can be anything you wish, and will be the name of the directory housing the output from the testbench run (under `tb/test_output/`)
      * `/test_location`: This is the (relative) path to where the `cocotb` test module, `Makefile`, and top-level dut are located
      * `/expected_is_observed`: This flag can be used by the `cocotb` test module to toggle whether or not to treat the observed outputs as the expected; when "true" the testvectors for the block output are ignored and the observed data is treated as the correct data
      * `/components_lib_dir`: This is a location to external IP required for compilation of any HDL source files
   * `testvectors`: Locations of any testvectors
      * `/testvector_dir`: The directory containing the testvector (*.evt) files
      * `/input`: A list of testvectors used to drive the firmware block inputs (each item in the list has a map of { "port-number" : "filename" } pairs, where "port-number" is the firmware block input port index to be driven with the data in the  testvector with name "\<testvector_dir\>/filename")
      * `/output`: As with `/input` but corresponds to the *expected* output for each of the output ports of the firmware block under test

With this, then, we see that the `tp_block` testbench is set to drive signals from 5 events, using a clock with period 5 ns.
The `expected_is_observed` flag is `"false"`, therefore the signals  from the two outputs of the `tp_block` (resulting from driving signals
onto the `tp_block`'s two inputs generated from the input testvectors) will be tested
against those signals contained in the output testvectors.

A convenience method "[get_testvector_files_from_config](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/utils/test_config.py#L11)"
is provided to properly retrieve the testvector files as specified in the testbench configuration file. An example of
using this method is provided in the testbench for the `board2board_switching`
block [here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py#L129).

**Important Note 1:** More items can be placed under the `input_args` node than those listed above
(i.e. [schema_test_config.json](../schema/schema_test_config.json) only specifies the *minimum* requirements).
You may wish to add more configuration to your testbenches, and such configuration can be
passed to your underlying `cocotb` testbench modules by defining the configurable
parameters (and their values) under your testbench's `input_args` configuration.

**Important Note 2:** If you specify `expected_is_observed` to be `"true"` you can leave the output testvector list (`testvectors/output`) empty.

**Important Note 3:** You can actually leave the `testvectors/input` and `testvectors/output` lists completely empty, as in:
```json
"testvectors" :
{
    "testvector_dir" : "/full/path/to/testvectors/",
    "input":[]
    ,"output":[]
}
```
If you do this, you are required to implement a `get_testvector_files` method for
your testbench. This method should be placed under your testbench's `utils.py` file.
For example, for `tp_block`, the file `testbench/tp_block/tp_block_utils.py` will have a
```python
def get_testvector_files(testvector_dir="", **kwargs) :
    input_testvectors = []
    output_testvectors = []
    # do stuff and fill each list with paths to the testvectors
    ...
    return input_testvectors, output_testvectors
```
function implemented. An example of such a method is implemented for the `board2board_switching`
firmware block [here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/b2b_utils.py#L7).

# I/O Port Description

The firmware block under test will have a specified number of inputs and outputs.
Description of these inputs and outputs for a given firmware block are defined
in the `testbench/<test_name>_ports.py` file -- **the "ports file"**.

A testbench's ports file defines a class with two enums: `Inputs` and `Outputs`
that provide `{ "port-name" : "port-number" }` pairs. The "port-name" is typically
a descriptive (logical) name that can be used for naming output files, etc... For example,
if output port number `0` of a given firmware block is sending data to another block
called `TPBlockDownStream`, then the "port-name" could be something like "TPBlockDownStream".
The association with the output port for the firmware block under test is given
by the value of the enum.

In the case of the `tp_block` testbench this file is `tp_block_ports.py`:

## tp_block_ports.py

For the two inputs and two outputs of the firmware block `tp_block`, a minimal
ports file will look like the following:

```python
import enum

from tp_tb.utils import port_descriptor


class TPBlockPorts(port_descriptor.PortDescriptor):
    def __init__(self):
        super().__init__()

    class Inputs(enum.Enum):
        Input_0 = 0
        Input_1 = 1

    class Outputs(enum.Enum):
        Output_0 = 0
        Outupt_1 = 1
```
The input (output) ports have names `Input_0` and `Input_1` (`Output_0` and `Output_1`).
The values of the enum, for example `1` for `Input_1`, are what correspond to the
actual firmware IO port in the HDL and the ordering in the ports file does **not necessarily
need to be sequential or ordered**. For example, the following is valid:
```python
class Inputs(enum.Enum):
    Input_FOO = 1
    Input_BAR = 0
```
This reinforces the fact that the names (e.g. `Input_0`) are relatively arbitrary.
The enum *values*, and not their names, are what are used in associating with the hardware description of the
firmware block.

# Block Wrappers

The HDL design under test in your `cocotb` testbench needs to have it's inputs driven
and outputs monitored. The testbench infrastructure provides "block wrappers" to handle this,
and each testbench must implement a block wrapper that is a sub-class of
[BlockWrapper](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/utils/block_wrapper.py).

The [BlockWrapper](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/utils/block_wrapper.py) class
handles methods for associating [FifoWrapper](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/utils/fifo_wrapper.py)
objects to each of the inputs ([FifoDrivers](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/utils/fifo_wrapper.py#L146))
and to each of the outputs ([FifoMonitors](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/utils/fifo_wrapper.py#L204)).

At its minimum, a testbench must implement it's own [BlockWrapper](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/utils/block_wrapper.py)
sub-class and define a `send_input_events` method,

```python
def send_input_events(self, input_testvectors, n_to_send=-1, l0id_request=-1, **kwargs):
```

For our hypothetical two input, two output block `tp_block`, this is `tp_block_wrapper.py`:

### tp_block_wrapper.py

The minimal content of a testbench block wrapper can be seen in the
[sw_switcher_block example](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/example_sw_block/sw_switcher_wrapper.py).
Refer to this and understand it's [send_input_events function](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/example_sw_block/sw_switcher_wrapper.py#L18)
and you will understand the minimum requirement for a testbench block wrapper.

# Block Utilities

Your testbench may require additional functions and methods. By default, a test has a `<test_name>_utils.py`
file for this purpose.

### tp_block_utils.py

# CocoTB Testbench Module

Each testbench will have an `test` directory under which the `cocotb` test module, `Makefile`, and top-level HDL file housing
the firmware block under test will be located.

### test/Makefile

The `test/Makefile` file provides `cocotb` with the necessary information for compiling your
HDL for simulation and points to the `cocotb` TopLevel and testing module.
A minimal example is provided in the
[sw_switcher_block testbench](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/example_sw_block/test/Makefile).

Further information on `cocotb` requirements for its Makefiles is given by the official
[cocotb documentation](https://docs.cocotb.org/en/stable/quickstart.html#creating-a-makefile).

### test/TopLevel_tp_block.v

The HDL top-level for the testbench is defined using the following naming scheme: `TopLevel_<test_name>.v`.
In the case of the testbench for the `tp_block`, this translates to `TopLevel_tp_block.v`.

The top-level file defines the DUT that will be manipulated within the `cocotb` test module.
It is here where a user wraps the inputs and outputs of their firmware block under test with
Spy+FIFO blocks.
The `cocotb` test module will then drive and monitor these Spy+FIFO blocks, with the firmware block
under test interacting directly with them.

An example of a top-level HDL file for the `board2board_switching` block is
[here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/TopLevel_b2b.v).
The firmware block under test is instantiated as
[board2board_inst](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/TopLevel_b2b.v#L76)
and its inputs (outputs) are interfaced to the
[input_spybuffers](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/TopLevel_b2b.v#L42)
([output_spybuffers](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/TopLevel_b2b.v#L104))
Spy+FIFO blocks.

**Important Note:** The naming scheme of the *outer most* Spy+FIFO blocks of the DUT defined
in the `TopLevel_<test_name>.v` file should be `"input_spybuffers"` and `"output_spybuffers"`.


### test/test_tp_block.py

The actual `cocotb` tests that are run are defined in so-called `cocotb` test modules.
For a given testbench, these are defined under the `test` directory and must follow
the naming scheme `"test_<test_name>.py"`.

The test module files are where the user defines the logic of their testbench.
An example can be found in the testbench for the
[board2board_switching test module](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py)
where the main `cocotb` test is defined with the ```python @cocotb.test``` decorator
[here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py#L69).

Further information on how to implement a `cocotb` test module is provided by the
[official documentation](https://docs.cocotb.org/en/stable/quickstart.html#creating-a-test).

#### Accessing the Testbench Configuration
Test modules can gain access to the testbench configuration data
(see the [Testbench configuration section](#testbench-configuration)) using the `test_config.get_config()` method,
as exampled [here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py#L74).
This provides access to the `input_args`, `run_config`, and `testvectors` data defined
in the current test's testbench configuration file.

#### Starting the Simulation Clock
The simulation clock is configured within the test module, as
[here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py#L107).

#### Initializing Input and Output FIFO Wrappers
Input and output drivers and monitors for the input and output Spy+FIFO blocks are
added to the instantiated block wrapper instance within the test module, as exampled
[here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py#L132).

#### Driving Inputs
Signals from the input testvectors are driven onto the firmware block under test's
input ports using the instantiated block wrapper's `send_input_events` method, as
exampled [here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py#L165).

#### Compare the Observed with Expected
Minimal tests compare the signals observed at the firmware block under test's output
ports with those signals provided by the testvectors for the output ports.
This can be done by looping over the output monitors (via the instantiated block wrapper object)
and comparing the observed output data with the expected using the [tb diff utility](../README.md#tb-diff).
This is exampled [here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py#L221).

#### Store the Test Results
Minimal tests comparing the observed signals with the expected can use the
[result_handler module](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/utils/result_handler.py)
to produce and store the test results in the
[specified format](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/schema/schema_test_results_summary.json).

**Generation of the formatted test results** is exampled
[here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py#L224).

**Storing the formatted test results** is exampled
[here](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/testbench/b2b/test/test_b2b.py#L242).


