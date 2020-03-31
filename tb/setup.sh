#!/bin/sh

# Setup script for tp-fw cocotb testbench.
# This requires: python 2.7+ with pip and virtualenv.
# It doesn't _need_ to be a shell script.
# It should be portable to Windows, too.

py_cmd="python"
pip_cmd="pip"
env_mod="virtualenv"

function print_usage {
    echo "------------------------------------------------------------"
    echo "cocotb testbench for TP-FW"
    echo ""
    echo " Options:"
    echo "  --py3           use python3 (default is to use python2)"
    echo "  -h|--help       print this help message"
    echo ""
    echo " Example usage:"
    echo "  $ source setup.sh --py3"
    echo "------------------------------------------------------------"
}

function main {

    use_python3=0
    while test $# -gt 0
    do
        case $1 in
            -h)
                print_usage
                return 0
                ;;
            --help)
                print_usage
                return 0
                ;;
            --py3)
                use_python3=1
                ;;
            *)
                echo "Invalid argument: $1"
                return 1
                ;;
        esac
        shift
    done

    if [[ $use_python3 == 1 ]]; then
        py_cmd="python3"
        pip_cmd="pip3"
        env_mod="venv"
    fi

    if [ -d env ]; then
        source env/bin/activate
    else

        # Activate the virtual environtment and call it "env"
        $py_cmd -m $env_mod env
        source env/bin/activate

        # Install dependencies
        $pip_cmd install cocotb
        if [[ $use_python3 == 0 ]]; then
            $pip_cmd install enum34
        fi
        $pip_cmd install -e tptest
        $pip_cmd install -e b2b_test
        $pip_cmd install -e tb_b2b
        $pip_cmd install -e event_parse
        $pip_cmd install -e ../../system-simulation/
    fi

    echo "Activated virtual environment for cocotb. Type 'deactivate' to restore normal environment."
}

main $*

#if [ -d env ]; then
#	source env/bin/activate
#else
#
#	# Create a virtualenv in the "env" directory.
#	# Apparently, on Windows this should be "py -m" instead.
#	# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
#    python3 -m venv env
#
#	# Activate the virtualenv.
#	source env/bin/activate
#
#	# Install dependencies into the virtualenv.
#
#    # Install cocotb
#    pip3 install cocotb
#
#    # If this is python2: install the enum34 package.
#    # (If it isn't, do nothing).
#    #pip2 install enum34 || true
#
#    # Install the local "tptest" package.
#    pip3 install -e tptest
#
#    # Install the "system-simulation" DataFormat package,
#    # also in editable mode. Note: requires this to be cloned.
#    pip3 install -e ../../system-simulation/
#fi

