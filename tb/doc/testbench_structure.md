# Testbench Structure

The following details the components of a valid testbench.
Described is the minimal structure required to simply begin passing
data through a testbench.

Additional structure or complexity, 
as needed on a per-testbench status, can be added by users, **but the
additions should be kept to the specific testbench's directory under
tp_tb/testbench/\<name-of-testbench\>!** (see below).

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

Here is a description of each of the files in the above schematic:

## test_config/config_tp_block.json

This is the testbench configuration file specific to `tp_block`'s testbench.
As mentioned in the [README](../README.md), this configuration file must satisfy
the `jsonschema` defined under [schema_test_config.json](../schema/schema_test_config.json).

The [tb check-config](../README.md#tb-check-config) can be used to check that a testbench
configuration file is valid.

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







