import inspect
import os
import sys

import cocotb
from cocotb import triggers, result, utils, clock

def CocotbTest(label="", skip=False, package_name=None):
    """ I don't think I understand decorators quite well enough to make this
        work. But the idea was to wrap the call to cocotb.test() with an
        automatically generated switch for each and every test.
        I was hoping to also do stuff like set the random seed, but I couldn't
        make that work."""


    # Here's what should happen.
    # If I set RUN_ALL, *all tests should run*.
    # If I don't set RUN_ALL:
    # * All tests with skip=False should run.
    # * All tests selected explicitly by TESTCASE= or by LABEL=1 should run.

    # RUN_ALL environment variable. Run all tests, ignore skip.
    run_all = (os.environ.get("RUN_ALL", "") == "1")
    if skip:
        skip = not run_all

    # Environment variable/label. Ignore skip.
    if label != "":
        env_var = (os.environ.get(label, "") == "1")
        if skip:
            skip = not env_var

    def internal_test(test):
        tester = cocotb.test(skip=skip)

        # To make the sorting better, CHANGE the "name" of the module that
        # the function we're calling is found in to exclude sub-modules.
        # This isn't necessarily something we always want to do, and it's
        # pretty serious black magic, but it works...
        if package_name is not None:
            test.__module__ = package_name

        tester_evaluated = tester(test)
        return tester_evaluated

    return internal_test
