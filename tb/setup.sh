#!/bin/tcsh

# Setup script for tp-fw cocotb testbench.
# This requires: python 2.7+ with pip and virtualenv.
# It doesn't _need_ to be a shell script.
# It should be portable to Windows, too.

if [ -d env ]; then
	source env/bin/activate.sh
else

	# Create a virtualenv in the "env" directory.
	# Apparently, on Windows this should be "py -m" instead.
	# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
	python -m virtualenv env

	# Activate the virtualenv.
	source env/bin/activate.sh

	# Install dependencies into the virtualenv.

	# Install cocotb
	pip install cocotb

	# Install the local "tptest" package.
	pip install -e tptest

fi

echo "Activated virtual environment for cocotb. Type 'deactivate' to restore normal environment."
