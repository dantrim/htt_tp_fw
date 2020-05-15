# cocotb-bashed testbench infrastructure for the HTT trigger processor (TP)

This directory contains the TP's [cocotb](https://github.com/cocotb/cocotb)-based testbench
infrastructure.

## Requirements

In order to run the testbenches defined here you must have Python3 (>=3.6) installed
on your machine and accessible via the `python3` command in your `$PATH`.
If you need to install python3, there are many places online showing how to do this.
For example, [here](https://realpython.com/installing-python/).

## Installation and Setup
<details> <summary> Expand </summary>

If you have confirmed that you have `python3` on your machine, then the only
thing that you need to do to install all requirements for running the cocotb-based
testbenches is to run,
```bash
$ source setup_env.sh
(env) $
```
which will install all dependencies (cocotb, third-party packages, etc...). The installation
is handled by [pip](https://pypi.org/project/pip/) and [setuptools](https://pypi.org/project/setuptools/).
You can inspect [setup.py](setup.py) to see the package and installation configuration.

Once the above command completes succesfully, you will be in a python virtual environment
(indicated by the "`(env) $`" at your terminal command prompt instead of the usual "`$`").
If you are unfamiliar with the concept of virtual environments, see [here](https://docs.python.org/3/tutorial/venv.html)
or [here](https://realpython.com/python-virtual-environments-a-primer/).

To exit the virtual environment run,
```bash
(env) $ deactivate
$
```

To ensure that the testbench infrastructure has been installed properly, after sourcing
the `setup_env.sh` script as in the above you should have the command "`tb`" available to you in your
path (within the virtual environment). You should be able to print its help message to
the screen by running,
```bash
(env) $ tb -h
Usage: tb [OPTIONS] COMMAND [ARGS]...

  Top-level entrypoint into TP fw cocotb test-bench infrastructure.

Options:
  -h, --help  Show this message and exit.

Commands:
  check-config  Check/inspect a testbench's configuration (*.json) file.
  diff          Diff two *.evt files and test for differences.
  dump          Dump the contents of an *.evt file.
  list          List all available testbenches (and their tests).
  run           Setup and run cocotb-based testbenches.
  test-summary  Dump the test results *.json file.
```
If you see the above help message after running the top-level "`tb`" command then
you should be on your way to running the testbench infrastructure.

### The virtual environment is necessary for running the testbench
In order to return back to the virtual environment for the cocotb testbenches,
simply run,
```bash
$ source setup_env.sh
(env) $
```
Subsequent calls to this script will not attempt to re-install the package, but will only
initialize the virtual environment and ensure that the top-level entrypoint "`tb`" is accessible.

That is, **`setup_env.sh` must be sourced every time you return back to running the testbenches**.

### Fresh Installation / Re-installation
If you wish to make a clean installation, simply delete the `env/` directory created when you
ran `setup_env.sh` and re-run the installation procedure,
```bash
$ rm -rf env/
$ source setup_env.sh
(env) $ # everything is all fresh now
```

### Note:

If you do not have `pip`, this is because
you do not have `python3` (`pip` comes with `python3` by default). You must check that your
version of `pip` corresponds to your `python3` instance by running,
```bash
$ pip3 --version
pip 9.0.3 from /foo/bar/python3.6/site-packages (python 3.6)
$ python --version
Python 3.6.8 # looks good!
```
</details>

## Functionality
<details> <summary> Expand </summary>

Here each of the ```tb``` commands will be briefly described.

All `tb` commands available to are listed by printing the help message:
```bash
(env) $ tb -h
Usage: tb [OPTIONS] COMMAND [ARGS]...

  Top-level entrypoint into TP fw cocotb test-bench infrastructure.

Options:
  -h, --help  Show this message and exit.

Commands:
  check-config  Check/inspect a testbench's configuration (*.json) file.
  diff          Diff two *.evt files and test for differences.
  dump          Dump the contents of an *.evt file.
  list          List all available testbenches (and their tests).
  run           Setup and run cocotb-based testbenches.
  test-summary  Dump the test results *.json file.
```
Each command has it's own set of arguments and options, which can be accessed by
```bash
(env) $ tb [command] -h
```

<details> <summary> <strong>check-config</strong> (click to expand) </summary>

```bash
(env) $ tb check-config -h
Usage: tb check-config [OPTIONS] CONFIG

  Check/inspect a testbench's configuration (*.json) file.

Options:
  --dump      Dump contents of valid test configuration.
  -h, --help  Show this message and exit.
```

The `check-config` command is for inspecting a testbench configuration JSON file.
A testbench's configuration is placed in the [test_config/](test_config/) directory.
For example, here is [test_config/config_b2b.json](test_config/config_b2b.json):
```json
{
    "testbench_config" :
    {
       "test_name" : "b2b"
       ,"input_args" :
       {
           "n_events" : 10
           ,"event_delays" : true
           ,"event_detail" : false
           ,"clock_period" : 5
           ,"clock_time_unit" : "ns"
       },
       "run_config" :
       {
           "output_directory_name" : "b2b"
           ,"test_location" : "src/tp_tb/testbench/b2b/test"
       }
    }
}
```


To check that a testbench configuration is sound, simply provide `check-config` the path to
a testbench JSON configuration file. If the configuration is valid you will be told accordingly.
Here is an example using [test_config/config_b2b.json](test_config/config_b2b.json):
```bash
(env) $ tb check-config test_config/config_b2b.json
Test configuration OK
```

The flag `--dump` additionally prints the configuration content to screen:
```bash
(env) $ tb check-config --dump test_config/config_b2b.json
Test configuration OK
------------------------------------------------------------
Configuration for test "b2b":
{
    "test_name": "b2b",
    "input_args": {
        "n_events": 10,
        "event_delays": true,
        "event_detail": false,
        "clock_period": 5,
        "clock_time_unit": "ns"
    },
    "run_config": {
        "output_directory_name": "b2b",
        "test_location": "src/tp_tb/testbench/b2b/test"
    }
}
------------------------------------------------------------
```

</details>

<details> <summary> <strong>list</strong> (click to expand)  </summary>

```bash
(env) $ tb list -h
Usage: tb list [OPTIONS]

  List all available testbenches (and their tests).

Options:
  -h, --help  Show this message and exit.
```
 
The `list` utility inspects the testbench directories and finds all properly configured
testbenches that are available to be run. It takes no arguments:
 
```bash
(env) $ tb list
Defined testbenches:
b2b
```

</details>

<details> <summary> <strong> run </strong> (click to expand)  </summary>

```bash
(env) $ tb run -h
Usage: tb run [OPTIONS] CONFIG

  Setup and run cocotb-based testbenches.

Options:
  -h, --help  Show this message and exit.
```

The `run` command is the primary driver of testbenches. You call this when you want to run a testbench.
It takes only a single argument, which is the testbench configuration JSON file that describes the
test you wish to run. For example,

```bash
(env) $ tb run test_config/config_b2b.json
```
Calling `run` will check that the testbench is configured properly and will construct the
command that will ultimately execute the compilation of the RTL source files and the running
of cocotb. Basically, it is nearly the same as setting up your testbench environment and calling
`make` on the cocotb-configured Makefile for your test.

The path to the provided testbench configuration file is passed to the cocotb tests and
can be used internally. In this way, the user can specify "input arguments" to pass to their
test that may change it's behavior. This is the "`input_args`" field of the testbench configuration
file. In the case of the `b2b` testbench these are (c.f. `tb check-config --dump test_config/config_b2b.json`):
```bash
"input_args" :
{
    "n_events" : 10
    ,"event_delays" : true
    ,"event_detail" : false
    ,"clock_period" : 5
    ,"clock_time_unit" : "ns"
}
```
It is up to the designer of the specific testbench to ensure that these "input_args" are properly
handled within their test, or have suitable defaults in the case of their absence within the
testbench's JSON configuration.

</details>

<details> <summary> <strong>test-summary</strong> (click to expand) </summary>

</details>

<details> <summary> <strong>diff</strong> (click to expand) </summary>

</details>

<details> <summary> <strong>dump</strong> (click to expand) </summary>
</details>



</details>
