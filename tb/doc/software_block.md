# Creating a Logic Block in Python

Creating a logic block in python is not difficult to do, especially given
that some of the work is already done for you if you leverage the
[`SoftwareBlock`](../src/tp_tb/utils/software_block.py)
base class provided by the testbench infrastructure.

For the following, we will assume that you wish to design a logic block in python
and have no logic defined in HDL *at all*. That is, the figures appearing
in the [testbench overview section](../README.md#overview-of-the-testbench-infrastructure)
are changed to look something like the following figure,
<div align="center">
    <img src="figures/tp_fw_full_swPNG.png" height="800">
</div>

where the HDL logic block interfacing to `input_spybuffers` and `output_spybuffers`
is replaced by a software-defined logic block (`"SoftwareBlock"`) written using the `python` programming
language and `cocotb` constructs.

In the following we will present a tutorial showing how to implement such a scenario.
Follow the items in the following Table of Contents sequentially.

The example testbench that we create here is provided under `testbench/example_sw_block`.

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!--------------------------- TABLE OF CONTENTS ------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->

Table of Contents
==================
   * [Requirements](#requirements)
   * [Environment Preparation](#prepare-your-environment)
   * [Define the Purpose of the Software Logic Block](#purpose-of-the-software-block)
   * [Run `tb create` to Initialize the Testbench](#run-tb-create)
   * [Implement the Logic Block](#implement-the-logic-block)
      * [Implement Input Handlers](#create-input-handlers)
      * [OutputDrivers](#output-drivers)
      * [Implement Output Handler Coroutines](#create-output-handler-coroutines)
         * [Giving the Logic Some Work to Do](#giving-the-logic-some-work-to-do)
   * [Turn your Software Block On](#turning-your-block-on)
   * [Run the Testbench](#run-the-testbench)

   
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
<!---------------------------------- PURPOSE ---------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
# Purpose of the Software Block

Before implementing the logic block, you must first have a clear idea of what
you want it to do.

For the sake of this tutorial, let's assume that we want a block that swaps
the order of it's inputs. That is, the "first" input gets mapped to the "last" output.
We will call this block `sw_switcher`.

So if we have two inputs and two outputs, the dataflow would look like:

<div align="center">
    <img src="figures/tp_fw_swswitcher.png" height="150">
</div>

That is, the data coming into `input 0` (`input 1`) is output by `output 1` (`output 0`).
   

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!---------------------------- RUN TB CREATE ---------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
# Run `tb-create`

We generate the testbench for the software block with the [tb create](../README.md#tb-create)
command, specifying that we wish it to generate the starting blocks of a
software block:
```bash
(env) $ tb create --test-name sw_switcher --n-inputs 2 --n-outputs 2 --software-block
Creating test "sw_switcher" with 2 inputs and 2 outputs
```

This creates the following new directories and files:

```
tb/
 ├── src/
 │   └── tp_tb/
 │       └── testbench/
 │           └── sw_switcher/
 │               ├── test/
 │               │   ├── Makefile
 │               │   ├── TopLevel_sw_switcher.v
 │               │   └── test_sw_switcher.py
 │               ├── sw_switcher_ports.py
 │               ├── sw_switcher_wrapper.py
 │               ├── sw_switcher_utils.py
 │               └── sw_switcher_block.py
 │
 └── test_config/
     └── config_sw_switcher.json
```

Where we see that the module `sw_switcher_block.py` is created.
This is the module where we will define our logic block.

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!---------------------- IMPLEMENT THE LOGIC BLOCK ---------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
# Implement the Logic Block

If we open up the `sw_switcher_block.py` file, we see a class `SwSwitcherBlock`:

```python
from tp_tb.utils import software_block

class SwSwitcherBlock(software_block.SoftwareBlock):
    def __init__(self, clock, name):
        super().__init__(clock, name)

    def input_handler_gen(self, input_num):
        return self._default_input_data_handler # raises NotImplementedError!

    def output_handler_gen(self, output_num):
        return self._default_output_handler # raises NotImplementedError!

```

The bulk of implementing a sub-clas of `SoftwareBlock` is defining the "handlers".

The function `input_handler_gen(self, input_num)` is a function generator and
is expected to return a function whose main purpose is to receive data
at this logic block's input port at index `input_num`.

The function `output_handler_gen(self, output_num)` is a function generator and
is expected to return a **`cocotb` coroutine** whose main purpose is to implement
the logic of the data that will eventually be exposed to the logic block's
output port at index `output_num`.

## Create Input Handlers

The `sw_switcher` block considered in this tutorial has two inputs.
We can define the *per-input-specific* input handlers as so:

```python
    def input_handler_gen(self, input_num):
        if input_num == 0 :
            return self._input_port_0_handler
        elif input_num == 1 :
            return self._input_port_1_handler
    
    def _input_port_0_handler(self, transaction):

        ##
        ## here we tell the data at INPUT 0 to be handled
        ## by the driver connected to OUTPUT 1 -- this
        ## effectively performs our "switching" logic
        ##
        self.output_drivers[1].append(transaction)
        
    def _input_port_1_handler(self, transaction)

        ## here we tell the data at INPUT 1 to be handled
        ## by the driver connected to OUTPUT 0 -- this
        ## effectively performs our "switching" logic
        ##   
        self.output_drivers[0].append(transaction)
```

In the above, we have defined the handlers for each of the two inputs of the
`sw_switcher` logic block: we map data arriving at input 0 (1) to output 1 (0).

You see that we use `output_drivers`. In the next section we'll explain what these are.


## Output Drivers

In the previous section we saw calls to:
```python
self.output_drivers[0].append(transaction)
```
The `output_drivers` array is a list of [`OutputDriver`](https://gitlab.cern.ch/atlas_hllhc_uci_htt/tp-fw/-/blob/master/tb/src/tp_tb/utils/software_block.py#L49)
objects are sub-classed [`cocotb Driver`](https://docs.cocotb.org/en/latest/_modules/cocotb/drivers.html) objects.
There is one `OutputDriver` per output of your logic block, and its responsibility
is driving the signals onto the `output_spybuffers` (see figure at the [start of
this page](#creating-a-logic-block-in-python)) of your `DUT`.
The `append` method of a `cocotb Driver` essentially will enqueue the
data to be written to the signal/bus that the driver is connected to (see the
[Driver documentation](https://docs.cocotb.org/en/latest/_modules/cocotb/drivers.html)).

## Create Output Handler Coroutines

As mentioned above, the `output_handler_gen` should produce `cocotb` coroutines
that implement the logic of your block.
When the data transactions enqueued by the `OutputDriver` objects in your
input handlers are actually serviced by the simulation, the output handler
will be called to act upon that transaction.

Let's define the `output_handler_gen` function as follows:
```python
def output_handler_gen(self, output_num):
    if output_num == 0:
        return self._output_port_0_handler
    elif output_num == 1:
        return self._output_port_1_handler
    
@cocotb.coroutine
def _output_port_0_handler(self, transaction):
    data, timestamp = transaction # transaction is a tuple
    driver = self.output_drivers[0]
    yield driver.write_to_fifo(data) # push the data to the output Spy+FIFO block at output 0
    
@cocotb.coroutine
def _output_port_1_handler(self, transaction)
    data, timestamp = transaction # transaction is a tuple
    driver = self.output_drivers[1]
    yield driver.write_to_fifo(data) # push the data to the output Spy+FIFO block at output 1
```

In the above we have implemented the bare minimum of what any output handler
needs to do: write the incoming data to the corresponding `Spy+FIFO` block in the
`output_spybuffers`. This is done by `yield`ing back the `write_to_fifo`
coroutine of the corresponding `OutputDriver` object.

Since our logic of "switching" the inputs was already handled by the input handlers
mapping the input data to the "switched" `OutputDriver` object, we have already
completed our objective of defining a logic block that swaps input 0 (1) with output 1 (0).

## Giving the Logic Some Work to Do

As we saw above, the bare minimum that your output handlers must do is perform the
writing of the data transactions to the `output_spybuffers` using the `write_to_fifo`
methods.

Doing the bare minimum, however, is not very realistic and, in simulation time,
happens "instantaneously". As the output handlers are cocotb coroutines, we
can leverage cocotb functionality to give the output handler coroutines
some realistic interaction with simulation time and/or data flow.

For example, suppose in our `sw_switcher` logic block that the data path
from input 0 to output 1 takes a longer (or different) amount of time compared
to that of the data path from input 1 to output 0. This could be the case
if each data path, in addition to performing the input/output swapping, performs
other logic functionalities.

In the following we will implement some logic to mimic this. We will add to our
logic the following:
   1. Add different latencies between the two data paths
   2. Synchronize the output writing

The first item is relatively clear to understand conceptually. What is meant by
the second item is that, despite the different latencies introduced by
the first time, we wish to have the data from each event latched onto the
output `Spy+FIFO` blocks at the same time. So if data from an event arrives
to the output number 1 prior to data arriving at output 0, the the data
at output number 1 will not be written until the data from output 0 is ready.

### Adding Latency to the Data Paths

Using a `cocotb` [`Timer`](https://docs.cocotb.org/en/latest/triggers.html#timing)
we can add some delays between the time at which the data arrives to
the output handler and the time when that data is written to the output `Spy+FIFO`
block.

We augment the output handlers defined above in the following way:
```python
from cocotb.triggers import Timer
...
...
def output_handler_gen(self, output_num):
    if output_num == 0:
        return self._output_port_0_handler
    elif output_num == 1:
        return self._output_port_1_handler
    
@cocotb.coroutine
def _output_port_0_handler(self, transaction):
    data, timestamp = transaction # transaction is a tuple
    driver = self.output_drivers[0]
        
    ##
    ## add 50 ns delay
    ##
    timer = Timer(50, "ns")
    yield timer
        
    ##
    ## simulation time has advanced 50 ns, now we write
    ##
    yield driver.write_to_fifo(data) # push the data to the output Spy+FIFO block at output 0
    
@cocotb.coroutine
def _output_port_1_handler(self, transaction)
    data, timestamp = transaction # transaction is a tuple
    driver = self.output_drivers[1]
        
    ##
    ## add 200 ns delay
    ##
    timer = Timer(200, "ns")
    yield timer
        
    ##
    ## simulation time has advanced 200 ns, now now we write
    ##
    yield driver.write_to_fifo(data) # push the data to the output Spy+FIFO block at output 1
```

By `yield`ing back the `Timer` triggers, each output handler is halted for
the specified amount of simulation time before continuing. It is important
to realize that the `OutputDriver` objects that are calling these output handlers
behind the scenes, are operating concurrently. As such, each handler will
stop and go essentially independently of one another as the simulation
of our logic progresses.

### Synchronizing the Outputs
In the previous section, we added arbitrary delays between the
two data paths of the `sw_switcher` logic. As a result, if we
drive events onto the inputs of our `DUT` at the same time, they will
definitely not arrive at the outputs of our `DUT` at the same time.
Hence, the events will be skewed relative to one another.

What if the logic downstream expects data from a given event (i.e. L0ID) to
be written to the outputs at the same time? We will need a synchronizing mechanism
to achieve this, which will be made possibly through the use of a
[`cocotb` Event](https://docs.cocotb.org/en/latest/triggers.html#synchronization)
shared between the two handlers.

Here we'll present the full source code with the event synchronization in place,
and discuss it after:

```python
from collections import Counter

from cocotb.Triggers import Timer, Event

from tp_tb.utils import software_block
from tp_tb.utils import utils

class SwSwitcherBlock(software_block.SoftwareBlock):
    def __init__(self, clock, name):
        super().__init__(clock, name)

        self._l0id_recvd = [] # a list of L0IDs that we have received so far
        self._event_hook = Event()  # used to sync up writing to outputs

    def input_handler_gen(self, input_num):
        if input_num == 0 :
            return self._input_port_0_handler
        elif input_num == 1 :
            return self._input_port_1_handler
    
    def _input_port_0_handler(self, transaction):

        ##
        ## here we tell the data at INPUT 0 to be handled
        ## by the driver connected to OUTPUT 1 -- this
        ## effectively performs our "switching" logic
        ##
        self.output_drivers[1].append(transaction)
        
    def _input_port_1_handler(self, transaction)

        ## here we tell the data at INPUT 1 to be handled
        ## by the driver connected to OUTPUT 0 -- this
        ## effectively performs our "switching" logic
        ##   
        self.output_drivers[0].append(transaction)

    def event_is_ready(self, l0id):
        self._l0id_recvd.append(l0id)
        c = Counter(self._l0id_recvd)
        if c[l0id] >= len(self.output_drivers):
            self._event_hook.set()
            return True
        elif c[l0id] >= 1:
            return False
        else:
            self._event_hook.clear()
            return False

    @cocotb.coroutine
    def _sync_event_header(self, l0id, output_num=-1, data_word=-1):
        if l0id and not self.event_is_ready(l0id):
            yield self._event_hook.wait()
            self._event_hook.clear()
        
    @cocotb.coroutine
    def _output_port_0_handler(self, transaction):
        data, timestamp = transaction # transaction is a tuple
        driver = self.output_drivers[0]

        data_word = utils.transaction_to_data_word(data) # convert to DataWord object to get decode L0ID
        l0id = utils.l0id_from_data_word(data_word) # get the L0ID
        
        ##
        ## add 50 ns delay
        ##
        timer = Timer(50, "ns")
        yield timer
        
        ##
        ## simulation time has advanced 50 ns, continue
        ##
        
        ##
        ## sync up the writing of output data between the
        ## two outputs, based on event-boundaries
        ##
        yield self._sync_event_header(l0id)
        
        ##
        ## the events are now synchronized, so we can write
        ##
        yield driver.write_to_fifo(data)
    
    @cocotb.coroutine
    def _output_port_1_handler(self, transaction)
        data, timestamp = transaction # transaction is a tuple
        driver = self.output_drivers[1]

        data_word = utils.transaction_to_data_word(data) # convert to DataWord object to get decode L0ID
        l0id = utils.l0id_from_data_word(data_word) # get the L0ID
        
        ##
        ## add 200 ns delay
        ##
        timer = Timer(200, "ns")
        yield timer

        ##
        ## simulation time has advanced 200 ns, continue
        ##
        
        ##
        ## sync up the writing of output data between the
        ## two outputs, based on event-boundaries
        ##
        yield self._sync_event_header(l0id)

        ##
        ## the events are now synchronized, so we can write
        ##
        yield driver.write_to_fifo(data)
```

In the above, we have added a few things:

   * (variable) `_l0id_recvd`: A `python` list that will hold the L0ID of all events seen at a given point in time
   * (variable) `_event_hook`: A synchronizing `cocotb` Event that will be used synchronize the output writing
   * (function) `event_is_ready`: Responsible for waking up any  handlers waiting on the `_event_hook` Event object at the right time
   * (function) `_sync_event_header`: Sets a given handler to wait until the `_event_hook` Event is triggered (by calling `_event_hook.set()`)

We have added to the handlers calls that will wait until the synchronizing event occurs,
```python
yield self._sync_event_header(l0id)
```
This method will halt the progression of the handler (via `_event_hook.wait()`) under two cases:
   1. The provided L0ID (`l0id`) has been seen **zero** times
   2. The provided L0ID (`l0id`) has been seen **one** time

In all other cases it is assumed that both outputs will be ready to write the event.
This is because we have two outputs, and if the event header containing each the L0ID
has reached **both outputs** (i.e. **two** outputs), then we can proceed with writing
the data to the output `Spy+FIFO` blocks.

It is important to realize that the calls,
```python
l0id = utils.l0id_from_data_word(data_word)
```
set the value of `l0id` to meaningful (i.e. `!= None`) values only when the `data_word` corresponds
to the first word of an event header. In this way, data writing proceeds as soon
as the first word of a given event header (defined by its L0ID) has reached the output.
Output handlers will enter a waiting stage until subsequent event headers are observed (by the other outputs) and if
the event headers arrive at different times (if the events arrive all at the same
time across all outputs then the waiting stage will not be entered).

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!--------------------- TURNING YOUR LOGIC BLOCK ON --------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
# Turning Your Block On

Now that we have implemented some non-trivial logic, let's turn it on
and pass some data through it.

When providing the `tb create` command with the `--software-block` flag,
it adds to the testbench test module the necessary block of code to connect
your sub-classed `SoftareBlock` instance to the `input_spybuffers` and `output_spybuffers`.

Looking in `test/test_sw_switcher.py` we see the following lines,

```python
...
import tp_tb.testbench.sw_switcher.sw_switcher_block as sw_switcher_block
...
@cocotb.test()
def sw_switcher_test(dut):
    ...
    ##
    ## start the software block instance
    ##
    sw_switcher_block_instance = sw_switcher_block.SwSwitcherBlock(dut.clock, "SwSwitcherBlock")
    for i, io in enumerate(SwSwitcherPorts.Inputs):
        sw_switcher_block_instance.add_fifo(
            dut.input_spybuffers[i].spybuffer,
            dut.clock,
            f"{sw_switcher_block_instance.name}_Input_{i}",
            io,
            direction="in",
        )
    for i, io in enumerate(SwSwitcherPorts.Outputs):
        sw_switcher_block_instance.add_fifo(
            dut.output_spybuffers[i].spybuffer,
            dut.clock,
            f"{sw_switcher_block_instance.name}_Output_{i}",
            io,
            direction="out",
        )
    sw_example_block_instance.start()    
```
In those lines we see the `Spy+FIFO` blocks in the `input_spybuffers` and `output_spybuffers`
arrays being connected to the instance of our `sw_switcher` logic block via the
`add_fifo` method.

Software blocks are `started` by calling their `start()` method, as seen in the above snippet.
This sets off the `OutputDrivers` running and sets the block in a state ready
to start receiving and handling incoming data.

<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------- RUN THE TESTBENCH ----------------------------->
<!----------------------------------------------------------------------------->
<!----------------------------------------------------------------------------->
# Run the Testbench

The `sw_switcher` logic block as two inputs and two outputs.
We expect the data seen at output 1 (0) to be the same as the
data seen at input 0 (1). So we setup the testvector configuration
in `test_config/config_sw_switcher.json` as:
```json
"testvectors" :
{
    "testvector_dir" : "/path/to/testvector_dir",
    "input":
    [
        { "0" : "BoardToBoardInput_AMTP0_Pixel0.evt" },
        { "1" : "BoardToBoardInput_AMTP0_Pixel1.evt" }
    ],
    "output":
    [
        { "0" : "BoardToBoardInput_AMTP0_Pixel1.evt" },
        { "1" : "BoardToBoardInput_AMTP0_Pixel0.evt" }
    ]
}
```
where we have chosen two arbitrary testvector files to use as an example.

With this we can run the `sw_switcher` testbench:

```bash
(env) $ tb run ./test_config/config_sw_switcher.json
...
# |----------------------------|--------------------|----------------------------|
# |PORT/PATH TESTED            |RESULT SUMMARY      |FAILED TESTS                |
# |                            |                    |                            |
# |==============================================================================|
# |TEST_SWSWITCHER_DEST00      |PASS                |                            |
# |----------------------------|--------------------|----------------------------|
# |TEST_SWSWITCHER_DEST01      |PASS                |                            |
# |----------------------------|--------------------|----------------------------|
...
...
(env) $
```
So we see it passed the test, meaning that it swapped the inputs (since our input
and output testvectors are the same, but swapped)!

In order to observe the event writing synchronization we can use the `tb dump`
utility:
```bash
(env) $ tb dump -a ./test_output/sw_switcher/test_output/sw_switcher/fifomonitor_SWSwitcher_00_Outupt00.evt > sw_switcher_output0.txt
(env) $ tb dump -a ./test_output/sw_switcher/test_output/sw_switcher/fifomonitor_SWSwitcher_01_Outupt01.evt > sw_switcher_output1.txt
```
If you look at the output of the `tb dump` commands captured in those two text files,
and compare the timestamp values (the numbers in the second column) at each
instance of a start of event header (words beginning with `0x1ab`) you will
see that the timestamp for the events between the two outputs (comparing the same event)
are always the same. If you look at the timestamp of the previous word written
by the outputs, however, you will see that the two times are much different.

Part of `tb dump` from output 0:

```bash
...
----------------------------------------------------------------------------------------------------------- [FOOTER 000]
423      23610.0        0x1cd00000f2300bdf9   423   FLAG: 0xcd, META_COUNT: 0xf, HDR_CRC: 0x2300bdf9
424      23665.0        0x00000000000000000   424   ERROR_FLAGS: 0x0
425      23720.0        0x0000001a79a54bfb3   425   WORD_COUNT: 0x1a7, CRC: 0x9a54bfb3
=========================================================================================================== [EVENT 001]
426      95465.0        0x1ab02000000000005   0     FLAG: 0xab, TRK_TYPE: 0x2, L0ID: 0x5
...
```

Part of `tb dump` from output 1:
```bash
...
----------------------------------------------------------------------------------------------------------- [FOOTER 000]
461      94850.0        0x1cd0000102300bdf9   461   FLAG: 0xcd, META_COUNT: 0x10, HDR_CRC: 0x2300bdf9
462      95055.0        0x00000000000000000   462   ERROR_FLAGS: 0x0
463      95260.0        0x0000001cd4db98940   463   WORD_COUNT: 0x1cd, CRC: 0x4db98940
=========================================================================================================== [EVENT 001]
464      95465.0        0x1ab02000000000005   0     FLAG: 0xab, TRK_TYPE: 0x2, L0ID: 0x5
...
```

From the partial dumps above, showing the start of event with `L0ID=0x5` for both
outputs, that the handler at output 0 was waiting for almost **72 µs** before it
began writing out the data for event with `L0ID=0x5`. That is, it took output 1
almost 72 µs longer for data from the event with `L0ID=0x5` than it did for output 0.
The time differences here do not correspond to the time delays of `50 ns` and `200 ns`
that we introduced in our logic block since the two input testvectors present drastically
different amounts of data to the inputs.
However, you will see the artificial delay that we injected into our
logic block occurring in the dump of the slower of the two
outputs (output 1): `95465 ns - 95260 ns = 205 ns`. This number is `205 ns`
and not exactly `200 ns` as we injected into our output handler
for output 1 since there is a one-clock clock-cycle for synchronization
and we have configured the clock period to be `5 ns` by default.

You can also see this in the simulator waveforms too, by loading the dataset
contained in `test_output/sw_switcher/vsim.wlf` into your favorite waveform viewer
and looking at the output `read_data` signals of the `output_spybuffers` object.




