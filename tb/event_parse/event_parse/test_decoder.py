#!/bin/env python

import sys
import argparse
from pathlib import Path

from DataFormat import DataFormat

import decoder

def main() :

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in-file", required = True)
    parser.add_argument("-v", "--verbose", action = "store_true", default = False)
    parser.add_argument("-n", "--n-events", default = -1)
    args = parser.parse_args()

    events = []
    with open(args.in_file, "rb") as input_file :
        events = decoder.decode_events_from_file(input_file, args.verbose, int(args.n_events))
    print(60 * "*")
    print("Loaded {} events from {}".format(len(events), args.in_file))

    for iv, event in enumerate(events) :

        l0id = event.header_l0id
        n_words_class = event.n_words_total
        n_words_header = event.footer_word_count

        print(60 * '=')
        print("Event {}: L0ID={} N_CLASS={} N_FOOTER={} EMPTY={}".format(iv, hex(l0id), int(n_words_class), int(n_words_header), event.empty))
        modules = event.modules
        n_cl = 0
        n_mod_words = 0
        for imod, mod in enumerate(modules) :
            n_cl += mod.n_clusters
            print("  Module {}: TYPE={} FLAG={} N_CLASS={} N_FOOTER={} N_CLUSTERS={}".format(imod, mod.module_type_str(), hex(mod.header_flag), mod.n_words_total, mod.footer_count, mod.n_clusters))
            n_mod_words += mod.n_words_total

if __name__ == "__main__" :
    main()
