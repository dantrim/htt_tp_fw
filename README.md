# TP-FW

This repository holds the source code for several of the firmware blocks of the
Trigger Processor (TP) of the ATLAS Hardware Tracking for the Trigger (HTT) project.
It also houses the associated testbench infrastructure, based around the
[cocotb framework](https://docs.cocotb.org/en/latest/) testing framework.

## TP-FW Structure

The repository is laid out following a directory structure illustrated here:

```
tp-fw/
├── src/
│   ├── board2board_switching/
│   ├── evt_sync/
│   └── SpyBuffer/
├── tb/
│   ├── default_makefiles/
│   ├── schema/
│   ├── src/
│   └── test_config/
└── top/
    └── tp/
```
Below, a brief description of each (sub-)directory is given.

### tp-fw/src

Contains HDL description of TP firmware blocks. Separate firmware blocks each have
their own sub-directory. In the above, we see three such sub-directories for
three different blocks: `board2board_switching`, `evt_sync`, and `SpyBuffer`.
The structure of each of these block-specific sub-directories is specific to that
block and up to the developer.

### tp-fw/tb

This directory contains the [cocotb](https://docs.cocotb.org/en/latest/)-based
testbench infrastructure.

  * `default_makefiles/`: Default CocoTB makefiles for simulators, etc...
  * `schema/`: Files describing the enforced schema for testbench configuration, results, etc...
  * `test_config/`: Where users place their testbench configuration files, which are used to run specific testbenches
  * `src/`: Implementation of the testbench infrastructure and firmware testbenches

### tp-fw/top

Standalone firmware blocks and top-level for testbench creation. (?)