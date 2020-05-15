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

```bash
(env) $ tb test-summary -h
Usage: tb test-summary [OPTIONS] [INPUT]...

  Dump the test results *.json file.

Options:
  -q, --quiet         Do not print anything to standard output.
  -r, --result-only   Simply return whether the test is passed or not.
  -e, --event-detail  Report event-level test details.
  -d, --detail        Report test details in addition to final summary.
  -h, --help          Show this message and exit.
```

The testbenches result in `test_result_summary*.json` JSON files which report summaries of all tests
run. The `test-summary` utility provides the user with functionality to dump the
information contained in these files with varying levels of detail in tabular form.

The option `-r|--result-only` reports in a single line the OR of all test results contained in the
provided summary files:
```bash
(env) $ tb test-summary -r test_output/b2b/test_result_summary_B2B_srcAMTP00_destAMTP01.json
Test result: PASS
```

The option `-d|--detail` reports a summary table for each of the provided input summary files, e.g.:

```bash
(env) $ tb test-summary -d test_output/b2b/test_result_summary_B2B_srcAMTP00_destAMTP01.json
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|PORT/PATH TESTED                        |TEST                |RESULT(ACROSS ALL EVENTS)|INFO                                    |
|================================================================================================================================|
|B2B_SRC00_DEST01                        |N_EVENTS            |PASS                     |                                        |
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|                                        |RECVD_L0IDS         |PASS                     |                                        |
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|                                        |EVENT_ORDER         |PASS                     |                                        |
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|                                        |--------------------|-------------------------|----------------------------------------|
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|                                        |N_WORDS             |PASS                     |                                        |
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|                                        |EVENT_HEADER        |PASS                     |                                        |
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|                                        |EVENT_FOOTER        |FAIL                     |bad_fields: ['CRC']                     |
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|                                        |MODULE_COUNT        |PASS                     |                                        |
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|                                        |MODULE_DATA         |PASS                     |                                        |
|----------------------------------------|--------------------|-------------------------|----------------------------------------|
|                                        |FLOATING_DATA       |PASS                     |                                        |
|----------------------------------------|--------------------|-------------------------|----------------------------------------|

|----------------------------------------|--------------------|----------------------------------------|
|PORT/PATH TESTED                        |RESULT SUMMARY      |FAILED TESTS                            |
|======================================================================================================|
|TEST_B2B_SRC00_DEST01                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
```

Providing `test-summary` the `-e|--event-detail` option provides additional breakdown for each of the tests reported in the above (with
the `-d|--detail` option) but *for each event*.

You can provide `test-summary` any number of `test_result_summary*.json` JSON input files (>=1) and it will
concatenate their results into a single table. For example:

```bash
(env) $ tb test-summary -d test_output/b2b/test_results_summary_B2B_srcAMTP00_dest*
... 
...
|----------------------------------------|--------------------|----------------------------------------|
|PORT/PATH TESTED                        |RESULT SUMMARY      |FAILED TESTS                            |
|======================================================================================================|
|TEST_B2B_SRC00_DEST00                   |PASS                |                                        |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST01                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST02                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST03                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST04                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST05                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST06                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST07                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST08                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST09                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST10                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST11                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST12                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
|TEST_B2B_SRC00_DEST13                   |FAIL                |EVENT_FOOTER                            |
|----------------------------------------|--------------------|----------------------------------------|
```
</details>

<details> <summary> <strong>diff</strong> (click to expand) </summary>

```bash
(env) $ tb diff -h
Usage: tb diff [OPTIONS] INPUTS...

  Diff two *.evt files and test for differences.

Options:
  -n, --n-events INTEGER     The number of events to load and be diffed.
  -e, --endian [little|big]  Endian-ness of data within the files to load.
  -l, --l0id INTEGER         Select an event with a specific L0ID from the
                             input files to diff.

  -v, --verbose
  -t, --table                Print out results of the diff in a table at the
                             end.

  --event-detail             Print out more detailed information for each
                             event when tabling is enabled.

  -h, --help                 Show this message and exit.
```

The `diff` utility is a very useful one. The testbenches output *.evt files (in the same format as the
testvector files) and the `diff` utility allows for comparing any two of them to each other.

For example, if you drive your design with a given set of testvectors and it produces an output file
called `fifomonitor_OUTPUT_01.evt` which has an associated testvector providing the *expected* output called `testvector_OUTPUT_01.evt`,
you can use the `diff` utility as a means to compare them to each other. Choosing to compare only the first event,

```bash
(env) $ tb diff -n 1 test_output/b2b/fifomonitor_OUTPUT_01.evt ${TESTVECDIR}/testvector_OUTPUT_01.evt
(env) $ echo $? # non-zero return code indicates that differences exist between the files
1 # differences exist!
```
In the above we see that `tb diff` by default does not print anything to screen, and instead provides a return code.
Non-zero return codes indicate that there are differences between the two files provided.

To make `tb diff` a bit more informative to the user, you can provide the `-v|--verbose` option:
```bash
(env) $ tb diff -n 1 -v test_output/b2b/fifomonitor_OUTPUT_01.evt ${TESTVECDIR}/testvector_OUTPUT_01.evt
================================================================================
File0: ./test_output/b2b/fifomonitor_OUTPUT_01.evt
File1: /foo/bar/testvector_OUTPUT_01.evt
====================================================================================================
Comparing event at L0ID=0x2
           NWORDS   = 61        NWORDS   = 61
           NMODULES = 3         NMODULES = 3
           ----------------------------------------
           0x1ab02000000000002  0x1ab02000000000002  FLAG: 0xab / 0xab          TRK_TYPE: 0x2 / 0x2        SPARE: 0x0 / 0x0           L0ID: 0x2 / 0x2
           0x004c00000000785a1  0x004c00000000785a1  BCID: 0x4c / 0x4c          SPARE: 0x0 / 0x0           RUNNUMBER: 0x785a1 / 0x785a1
           0x0000000000fffffff  0x0000000000fffffff  ROI: 0xfffffff / 0xfffffff
           0x00e3bc00100000000  0x00e3bc00100000000  EFPU_ID: 0xe3bc / 0xe3bc   EFPU_PID: 0x1 / 0x1        TIME: 0x0 / 0x0
           0x00000000000000002  0x00000000000000002  Connection_ID: 0x0 / 0x0   Transaction_ID: 0x2 / 0x2
           0x0000000002300bdf9  0x0000000002300bdf9  STATUS: 0x0 / 0x0          CRC: 0x2300bdf9 / 0x2300bdf9
           ----------------------------------------
           0x155400000000001fe  0x155400000000001fe  MODULE #000 FLAG: 0x55 / 0x55        TYPE: 0x1 / 0x1          DET: 0x0 / 0x0           ROUTING: 0xff / 0xff
           0x0130440002e4fc45e  0x01304400034b65f77  MODID: 0x4c11 / 0x4c11   MODTYPE: 0x0 / 0x0       ORIENTATION: 0x0 / 0x0
           0x067affe58322904d3  0x03e8bf76806b37792
           0x00b04bf7e1bb54174  0x023ce63e265272015
           0x032d17a79164ff0fb  0x00fa5d2922513a41f
           0x04ea95c1830c6d1e5  0x0088e9e156901719f
           0x04b2054a327c4bc66  0x00697c6c046f7a5d0
           0x013fde2055ae6eebb  0x05f2b442567e074e4
           ...
           ...
           ...
           0x05277e6db9cfdd243  0x027061d1bfcba14e7
           0x0771b000000000000  0x0771b000000000000  FLAG: 0x77 / 0x77    COUNT: 0x1b / 0x1b   ERROR: 0x0 / 0x0
           ----------------------------------------
           0x1cd0000042300bdf9  0x1cd0000042300bdf9  FLAG: 0xcd / 0xcd         SPARE: 0x0 / 0x0          META_COUNT: 0x4 / 0x4     HDR_CRC: 0x2300bdf9 / 0x2300bdf9
           0x00000000000000000  0x00000000000000000  ERROR_FLAGS: 0x0 / 0x0
           0x00000003adeadbeef  0x00000003a7f812270  WORD_COUNT: 0x3a / 0x3a   CRC DIFFERROR: 0xdeadbeef / 0x7f812270
                      ^^^^^^^^             ^^^^^^^^
           ----------------------------------------
           EVENT OK? NO

```
Here you see the data being printed word-by-word within each of the files. The column of data on the left corresponds to the data contained in "File0", which is the
first input file provided at the command line (in our case `test_output/b2b/fifomonitor_OUTPUT_01.evt`), and the column of data on the right corresponds to the second file
(`${TESTVECDIR}/testvector_OUTPUT_01.evt`).

In addition to printing side-by-side the data words from the two files, there is decoded information to the right. Currently,
decoded information is provided only for **EVENT HEADER**, **EVENT FOOTER**, **MODULE HEADER**, and **MODULE FOOTER**, given that the testvector
data for the cluster data words is random and not correlated between the input and output testvectors. The decoded values for each
field within each of these are shown on the right, alongside the corresponding data word in which the field resides. The
format of the decoded values are **`FIELD_NAME: VALUE_FILE0 / VALUE_FILE1`**. For example,
```bash
WORD_COUNT: 0x3a / 0x3a
```
indicates that the `EVENT FOOTER` field "`WORD_COUNT`" had the value of `0x3a` in both input files for the event being parsed.

Any differences that exist between the two files are indicated in the printout and are indicated in **red**. The positions within
the data itself where the differences are found are subscripted with "`^`" characters indicating the positions
in the formatted hex-strings where the differences are. For example, from the above:
```bash
           0x00000003adeadbeef  0x00000003a7f812270  WORD_COUNT: 0x3a / 0x3a   CRC DIFFERROR: 0xdeadbeef / 0x7f812270
                      ^^^^^^^^             ^^^^^^^^
```
points to the `CRC` fields between the files being different: `0xdeadbeef` (for File0) and `0x7f812270` (for File1).
Any field where an error occurs is also indicated with the flag `DIFFERROR`, as in the above with `CRC DIFFERROR`.

If any of the two files being compared has a different number of modules within a given event, then
the `diff` utility will report "unmatched" data:
```bash
====================================================================================================
Comparing event at L0ID=0x2
           NWORDS   = 61        NWORDS   = 61
           NMODULES = 4         NMODULES = 3
           ----------------------------------------
           0x1ab02000000000002  0x1ab02000000000002  FLAG: 0xab / 0xab          TRK_TYPE: 0x2 / 0x2        SPARE: 0x0 / 0x0           L0ID: 0x2 / 0x2
           0x004c00000000785a1  0x004c00000000785a1  BCID: 0x4c / 0x4c          SPARE: 0x0 / 0x0           RUNNUMBER: 0x785a1 / 0x785a1
           0x0000000000fffffff  0x0000000000fffffff  ROI: 0xfffffff / 0xfffffff
           0x00e3bc00100000000  0x00e3bc00100000000  EFPU_ID: 0xe3bc / 0xe3bc   EFPU_PID: 0x1 / 0x1        TIME: 0x0 / 0x0
           0x00000000000000002  0x00000000000000002  Connection_ID: 0x0 / 0x0   Transaction_ID: 0x2 / 0x2
           0x0000000002300bdf9  0x0000000002300bdf9  STATUS: 0x0 / 0x0          CRC: 0x2300bdf9 / 0x2300bdf9
           ----------------------------------------
           0x155400000000001fe  0x155400000000001fe  MODULE #000 FLAG: 0x55 / 0x55        TYPE: 0x1 / 0x1          DET: 0x0 / 0x0           ROUTING: 0xff / 0xff
           0x0130440002e4fc45e  0x01304400034b65f77  MODID: 0x4c11 / 0x4c11   MODTYPE: 0x0 / 0x0       ORIENTATION: 0x0 / 0x0
           0x067affe58322904d3  0x03e8bf76806b37792
           ...
           ...
           0x155400001e00001fe       unmatched          MODULE #002 FLAG: 0x55        TYPE: 0x1          DET: 0x0           ROUTING: 0xf00000ff
           0x013b2400003a67598       unmatched          MODID: 0x4ec9   MODTYPE: 0x0       ORIENTATION: 0x0
           0x04722466e08cc527b       unmatched
           0x00aab117b39c97d15       unmatched
           0x01fcbfc2526d1e64b       unmatched
           ...
           ...
```
where we see that the data in File0 had an extra module in it not associated with any module contained in the event data in File1.

In cases where event or module boundaries are not correctly reported in the data (e.g. if the fw block under test discards them by accident),
then the event building in the `diff` utility will not associate those words to any event or module since it is the event/module headers
within the data where that data is placed. For example, if a module header is missed, then the subsequent data words
*until the next observed header or start of footer*, will be "floating", so to speak. If such data is found, it is reported as "headless" by the `diff` utility
(and indicated with a **blue** text color):
```bash
           0x155400001e00001fe       headless
           0x013b2400003a67598       headless
           0x04722466e08cc527b       headless
           0x00aab117b39c97d15       headless
           0x01fcbfc2526d1e64b       headless
```

Giving `tb diff` the `-t|--table` option (in combination with the `--event-detail` option) provides tabulated results
of tests of differences in the same format as the `test-summary` utility.

</details>

<details> <summary> <strong>dump</strong> (click to expand) </summary>

```bash
(env) $ tb dump -h
Usage: tb dump [OPTIONS] INPUT_FILE

  Dump the contents of an *.evt file.

Options:
  -b, --boundary          Indicate event and module boundaries.
  -p, --parse             Print out (any) decoded information.
  -t, --timestamp         Indicate timestamps of each word in the file (if
                          available).

  -n, --n-events INTEGER  Dump a specific number of events.
  -l, --l0id TEXT         Print out a specific L0ID (can be comma-separated
                          list for multiple, or a range indicated via
                          <min>-<max>, e.g. 0x1-0x20).

  -c, --word-count        Indicate the overall word count.
  -e, --event-word-count  Indicate the word count within each event.
  -a, --all-opt           Set all options (except for timestamp).
  --start-l0id INTEGER    Dump events with L0ID >= "start-l0id".
  --stop-l0id INTEGER     Do not dump events with L0ID > "stop-l0id".
  --list-l0id             Print L0IDs for the events in the input file.
  -h, --help              Show this message and exit.
```

The `dump` utility provides the means to dump in a human-readable form the data contained in the binary *.evt files associated with
the testvectors and the data files generated by the testbenches. It takes a single input file and dumps the hex-string formatted datawords
to the screen.

There are a lot of configuration options available to the `dump` utility, all primarily related to the level of detail or decoding performed.
Providing no options just dumps the data words line-by-line:
```bash
(env) $ tb dump ./test_output/b2b/fifomonitor_B2B_OUTPUT0.evt
0x1ab02000000000002
0x004c00000000785a1
0x0000000000fffffff
0x00e3bc00100000000
0x00000000000000002
0x0000000002300bdf9
0x155400000000001fe
0x0130440002e4fc45e
0x067affe58322904d3
...
...
0x01120a229593ae9b5
0x00675239167b879e2
0x05277e6db9cfdd243
0x0771b000000000000
0x1cd0000042300bdf9
0x00000000000000000
0x00000003adeadbeef
```

The `-b|--boundary` option places line indicators of where the EVENT, MODULE, and FOOTER boundaries lie:
```bash
(env) $ tb dump -b ./test_output/b2b/fifomonitor_B2B_OUTPUT0.evt
=================== [EVENT 000]
0x1ab02000000000002
0x004c00000000785a1
0x0000000000fffffff
0x00e3bc00100000000
0x00000000000000002
0x0000000002300bdf9
------------------- [MODULE 000/000]
0x155400000000001fe
0x0130440002e4fc45e
...
...
0x05277e6db9cfdd243
0x0771b000000000000
------------------- [FOOTER 000]
0x1cd0000042300bdf9
0x00000000000000000
0x00000003adeadbeef
```

The `-p|--parse` option decodes the EVENT HEADER, MODULE HEADER, MODULE FOOTER, and EVENT FOOTER datawords and places the decoded
fields on the right hand side. For example,
```bash
========================================================================== [EVENT 000]
0x1ab02000000000002   FLAG: 0xab, TRK_TYPE: 0x2, L0ID: 0x2
...
```

The `-c|--word-count` option prints the overall word count of the printed dataword within the file. If there are `N` datawords (and `M << N` events)
in the file, then the word-count is contained in `[0,N-1]`. This word count is indicated to the left of the data words:
```bash
(env) $ tb dump -b -c test_output/b2b/fifomonitor_B2B_OUTPUT1.evt
============================== [EVENT 000]
0         0x1ab02000000000002
1         0x004c00000000785a1
2         0x0000000000fffffff
...
57        0x0771b000000000000
------------------------------ [FOOTER 000]
58        0x1cd0000042300bdf9
59        0x00000000000000000
60        0x00000003adeadbeef
============================== [EVENT 001]
61        0x1ab02000000000005
62        0x00cb00000000785a1
...
```

The `-e|--event-word-count` option prints the *inter-event* dataword count. This count repeats after each new event is printed and is printed to the right
of the data word:
```bash
(env) $ tb dump -b -c -e test_output/b2b/fifomonitor_B2B_OUTPUT1.evt
===================================== [EVENT 000]
0         0x1ab02000000000002   0
1         0x004c00000000785a1   1
2         0x0000000000fffffff   2
3         0x00e3bc00100000000   3
...
56        0x05277e6db9cfdd243   56
57        0x0771b000000000000   57
------------------------------------- [FOOTER 000]
58        0x1cd0000042300bdf9   58
59        0x00000000000000000   59
60        0x00000003adeadbeef   60
===================================== [EVENT 001]
61        0x1ab02000000000005   0
62        0x00cb00000000785a1   1
63        0x0000000000fffffff   2
64        0x026f9400b00000000   3
...
```

The `-t|--timestamp` option prints the simulator timestamp value at which point the printed dataword was made available.
For example, the `fifomonitor_*.evt` files produced by the testbench are data put into the output FIFOs by
the DUT. The timestamp is therefore the time at which the DUT wrote the dataword into the FIFO.
The timestamp values correspond to what would appear in a waveform alongside a given register transition event.
The timestamps are given in the simulator timescale (default to "ns") and are printed to the left of the datawords:
```bash
(env) $ tb dump -b -c -e -t test_output/b2b/fifomonitor_B2B_OUTPUT1.evt
==================================================== [EVENT 000]
0        300.0          0x1ab02000000000002   0
1        305.0          0x004c00000000785a1   1
2        310.0          0x0000000000fffffff   2
3        315.0          0x00e3bc00100000000   3
4        320.0          0x00000000000000002   4
5        325.0          0x0000000002300bdf9   5
---------------------------------------------------- [MODULE 000/000]
6        570.0          0x155400000000001fe   6
7        575.0          0x0130440002e4fc45e   7
8        580.0          0x067affe58322904d3   8
...
```

**Note**: The timestamps are only available to those \*.evt files generated by the testbenches, and **NOT the testvector files.**

The remaining options (`-n`, `--list-l0id`, `--start/stop-l0id`, `-l`) should all be self-explanatory.

Any combination of these options can be provided to the `dump` utility. Provide the `-a|--all-opt` option to provide
the combination of `-b -c -e -t -p`.


</details>



</details>
