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
Here each of the `tb` commands will be briefly described.
</details>