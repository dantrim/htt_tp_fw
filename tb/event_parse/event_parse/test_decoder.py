#!/bin/env python

import sys
import argparse
from pathlib import Path

from DataFormat import DataFormat

import decoder

def next_word(input_file) :

    meta_flag = bool(int.from_bytes(input_file.read(1), DataFormat.ENDIAN))
    data = int.from_bytes(input_file.read(8), DataFormat.ENDIAN)

    return meta_flag, data

def decode(input_file, verbose = False, n_events = -1) :

    meta_flag, data_word = next_word(input_file)

    events = []
    event = decoder.EventData()
    footer_count = 0
    in_footer = False

    while True :

        if not meta_flag :
            if len(input_file.read(1)) == 0 :
                if verbose :
                    print("End of Stream")
                pass
            else :
                print("ERROR: expected meta_flag, word = {}".format(data_word))
            break

        flag = decoder.get_flag(data_word)

        if decoder.is_start_of_event(flag) :
            if verbose :
                print("---- HEADER ----")
            for i in range(6) :
                if verbose :
                    print(hex(data_word))
                event.words.append(data_word)
                meta_flag, data_word = next_word(input_file)

        elif decoder.is_start_of_module(flag) :
            if verbose :
                print("---- MODULE ---- (meta = {})".format(meta_flag))
                print(hex(data_word))
            start_idx = len(event.words)
            event.words.append(data_word)
            event.n_modules += 1
            while True :
                meta_flag, data_word = next_word(input_file)
                if meta_flag :
                    break
                if verbose :
                    print("{} (meta = {})".format(hex(data_word), meta_flag))
                event.words.append(data_word)
            end_idx = len(event.words)
            event.module_bounds.append( (start_idx, end_idx) )

        elif decoder.is_start_of_event_footer(flag) :
            if verbose :
                print("---- FOOTER ----")
            for i in range(3) :
                if verbose :
                    print(hex(data_word))
                event.words.append(data_word)
                meta_flag, data_word = next_word(input_file)

            events.append(event)
            if n_events > 0 and len(events) >= n_events :
                break
            event.clear()
        else :
            print("WHOOPS")

    return events

def main() :

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in-file", required = True)
    parser.add_argument("-v", "--verbose", action = "store_true", default = False)
    parser.add_argument("-n", "--n-events", default = -1)
    args = parser.parse_args()

    events_data = []

    with open(args.in_file, "rb") as input_file :

        events_data = decode(input_file, args.verbose, int(args.n_events))
    print("Loaded {} events (data)".format(len(events_data)))

    events = []
    for ie, ev in enumerate(events_data) :
        event = decoder.Event(ev)
        events.append(event)
    print("Loaded {} events".format(len(events)))


if __name__ == "__main__" :
    main()
