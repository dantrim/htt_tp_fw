# cocotb-based testbench infrastructure for the HTT Track Processor

This directory contains the TP's [cocotb](https://github.com/cocotb/cocotb) testbench.

## Installation and Setup

### Questa

Cocotb supports many simulators (though not the built-in Vivado
simulator). By default, this testbench has been tested with
and should automatically run with Questa.

### Python Setup

To run the cocotb tests, you need Python 2.7 or 3.x (in theory,
both will work). You'll need to install cocotb, and-- on Python
2.7-- the [enum34](https://pypi.org/project/enum34/) package.

The simplest way to get started is to use a Python [virtual
environment](https://docs.python.org/3/tutorial/venv.html). Included
in this directory are two setup scripts, one for bash and one for tcsh,
that will automatically create a virtual environment for you, but
you can also do it by hand.

The provided setup scripts do the following:

* Create a virtual environment in the ```tp-fw/tb/env``` directory,
if it doesn't already exist.
* Install cocotb and any Python dependencies into it.
* Install the local tptest package in "editable" mode. (Editable
mode means that the package is only linked into the virtual environment,
not copied, so changes and updates will copy).
* Install the DataFormat package from the [system-simulation]()
repo, also in "editable" mode.
* Activate the virtual environment.

This is very similar to setting up an Athena release; the virtual
environment overrides your system Python installation. You can
deactivate the virtual environment by typing ```deactivate```;
this will restore your normal shell.

Running the setup script again will automatically activate
the virtual environment, if it's already there. (If you want to
recreate the virtual environment, you can just delete the "env"
directory and run it again).

To get things going on a Linux machine, you can do the following
(depending on whether you have bash or tcsh) to set up the virtual
environment. The setup scripts assume you've cloned both the tp-fw
and system-simulation directories in the same git area; we could
eventually make system-simulation a submodule if that turns out
to be more convenient.

```
mkdir git
cd git
git clone [tp-fw repository]
git clone [system-simulation repository]
cd tp-fw/tb/
source setup.(c)sh
```

The use of virtual environments avoids having to set the PYTHONPATH
environment variable or modify ```sys.path``` in code.

### Windows Support

Python virtual environments and cocotb should both work on Windows,
but I don't know the best way to configure things, so I haven't
included any instructions.

## The Skeleton Testbench

The "skeleton" testbench is an example of how to flow test vectors
through a skeleton of the Track Processor using cocotb. Included
in the "skeleton" directory is a cocotb testbench which instantiates
two spy buffers (note that when I say "spy buffer" in this document,
I mean "spy buffer + flow control FIFO").

The skeleton testbench uses the Python dataflow controller (provided
in the ```tptest``` Python package) to load events into the input
spy buffer, feed them through an "empty" block (controlled by Python),
and monitor the output of the output spy buffer. The dataflow class
supports configuring an arbitrary number of inputs and outputs, and
zero or multiple empty blocks. This example could be easily adapted to
test a real block sitting between two (or more) spy buffers.

The DataFormat package (from system-simulation) is used to format
events correctly, check for the right start-of-event and end-of-event
metadata words, and also read and write binary event files.

Inside the skeleton directory, the file ```SkeletonTests.py``` contains
two example tests: one which generates random "events" and another which
loads events from a binary event file. In both cases, the spy buffer
monitors save all received words to an output binary file (written into
the ```sim_build``` directory where the tests are ran).

The example is minimally self-checking: it confirms that all expected
events sent to the input were received, that no unexpected events were
received, and that all events began with a start-of-event word and ended
with an end-of-event word. Information about event structure is sourced
from the DataFormat package.

To run the skeleton, just type ```make``` in the "skeleton" directory.

## Cocotb Documentation

The official cocotb [docs](https://cocotb.readthedocs.io/en/latest/) are
pretty complete; a collection of [further resources](https://github.com/cocotb/cocotb/wiki/Further-Resources)
are also available.
