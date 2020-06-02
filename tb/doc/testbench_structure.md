# Testbench Structure

The following details the components of a valid testbench.
Described is the minimal structure required to simply begin passing
data through a testbench. Additional structure or complexity, 
as needed on a per-testbench status, can be added by users.

## Testbench Anatomy

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
