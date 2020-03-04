#!/bin/env python

from __future__ import print_function
from argparse import ArgumentParser

from event_table import EventTable

def main() :

    parser = ArgumentParser()
    parser.add_argument("-i", "--input_file", required = True
        ,help = "Input events file to parse"
    )
    args = parser.parse_args()

    et = EventTable()
    et.load_from_file(args.input_file)

if __name__ == "__main__" :
    main()
