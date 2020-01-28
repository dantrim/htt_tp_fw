#!/bin/tcsh

# Setup script for tp-fw cocotb testbench.
# This requires: python 2.7+ with pip and virtualenv.
# It doesn't _need_ to be a shell script.
# It should be portable to Windows, too.

# TODO: create setup.pys for things.

if ( -d env ) then
	source env/bin/activate.csh
else

	# Create a virtualenv in the "env" directory.
	# Apparently, on Windows this should be "py -m" instead.
	# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
	python -m virtualenv env

	# Activate the virtualenv.
	source env/bin/activate.csh

	# Install dependencies into the virtualenv.

	# Install cocotb
	pip install cocotb

	# Install the local "tptest" package.
	pip install -e tptest

	# Install the "system-simulation" DataFormat package,
	# also in editable mode. Note: requires this to be cloned.
	pip install -e ../../system-simulation/

endif

echo "Activated virtual environment for cocotb. Type 'deactivate' to restore normal environment."
