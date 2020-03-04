#!/bin/env python

from __future__ import print_function
from argparse import ArgumentParser

from event_table import EventTable

def main() :

    parser = ArgumentParser()
    parser.add_argument("-i", "--input_file", required = True
        ,help = "Input events file to parse"
    )
    parser.add_argument("-v", "--verbose", default = False, action = "store_true"
        ,help = "Set verbose mode on"
    )
    args = parser.parse_args()

    et = EventTable()
    et.load_from_file(args.input_file, verbose = args.verbose)

if __name__ == "__main__" :
    main()
