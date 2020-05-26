import os
import sys
from pathlib import Path
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt

from tb_utils import events, tb_plot

DATA_ENDIAN = "little"


def check_inputs(input_filelist=[]):

    all_ok = True
    for ifile, filename in enumerate(input_filelist):
        p = Path(filename)
        ok = p.exists() and p.is_file()
        if not ok:
            print("ERROR Input file #{:02} (={}) is not found".format(ifile, filename))
            all_ok = False

    plt.rcParams["axes.prop_cycle"] = plt.cycler(
        "color", plt.cm.jet(np.linspace(0, 1, len(input_filelist) + 1))
    )

    return all_ok


def event_lists_gen(input_filelist=[]):

    events_list = []
    for ifile, filename in enumerate(input_filelist):
        loaded_events = events.load_events_from_file(
            filename, endian=DATA_ENDIAN, load_timing_info=True
        )
        print(
            "INFO Loaded {} events from file #{:02} (={})".format(
                len(loaded_events), ifile, filename
            )
        )
        events_list.append(loaded_events)
        # yield loaded_events
    return events_list


def make_dummy_plot(args):

    ##
    ## generate the data
    ##
    timestamp_unit = ""
    x_data = []
    event_boundaries = []
    y_data = []
    labels = []
    for input_num, input_events in enumerate(event_lists_gen(args.input)):
        n_words = 0
        input_x_data = []
        input_y_data = []
        for ievent, event in enumerate(input_events):
            for iword, word in enumerate(event.words):
                n_words += 1
                if not timestamp_unit:
                    timestamp_unit = word.timestamp_units
                if iword == 0:
                    event_boundaries.append([word.timestamp, n_words])
                input_x_data.append(word.timestamp)
                input_y_data.append(n_words)
        x_data.append(input_x_data)
        y_data.append(input_y_data)
        label = Path(args.input[input_num]).stem
        labels.append(label)

    ##
    ## create the canvas
    ##
    fig, ax = tb_plot.default_canvas(
        x_label="Time [{}]".format(timestamp_unit), y_label="Number of words"
    )

    ##
    ## plot the data
    ##
    for i in range(len(x_data)):
        ax.plot(x_data[i], y_data[i], label=labels[i])
    event_bounds_x, event_bounds_y = zip(*event_boundaries)
    ax.plot(event_bounds_x, event_bounds_y, "ro", markersize=2)
    ax.legend(loc="best", frameon=False, fontsize=8)

    ##
    ## save the figure
    ##
    outname = "b2b_dummy_plot.pdf"
    print("Saving figure: {}".format(os.path.abspath(outname)))
    fig.savefig(outname, bbox_inches="tight")


def make_rate_plot(args):

    ##
    ## generate the data
    ##

    time_unit = ""
    n_for_average = 2
    n_events = 0
    x_data = []
    y_data = []
    labels = []
    events_lists = event_lists_gen(args.input)
    for input_num, input_events in enumerate(events_lists):
        rate = 0.0
        t0 = 0.0
        x_event = []
        y_event = []
        for ievent, event in enumerate(input_events):

            for iword, word in enumerate(event.words):
                if not time_unit:
                    time_unit = word.timestamp_units
                if word.is_start_of_event():
                    if ievent == 0:
                        t0 = word.timestamp
                        n_events = 1
                    else:
                        n_events += 1
                    if n_events == n_for_average:
                        delta = word.timestamp - t0
                        delta *= 1e-9  # ns -> s
                        rate = n_for_average * 1.0 / delta
                        rate /= 1e3  # Hz -> kHz
                        x_event.append(word.timestamp)
                        y_event.append(rate)
                        t0 = word.timestamp
                        n_events = 1
        x_data.append(x_event)
        y_data.append(y_event)
        labels.append(Path(args.input[input_num]).stem)

    ##
    ## create the canvas
    ##
    fig, pad = tb_plot.default_canvas(
        x_label="Time [{}]".format(time_unit), y_label="Rate [kHz]"
    )

    ##
    ## plot the data
    ##
    for i, _ in enumerate(args.input):
        pad.plot(x_data[i], y_data[i], label=labels[i])
    pad.legend(loc="best", frameon=False, fontsize=8)

    ##
    ## save figure
    ##
    outname = "b2b_rate_plot.pdf"
    print("Saving figure: {}".format(os.path.abspath(outname)))
    fig.savefig(outname, bbox_inches="tight")


def main():

    parser = ArgumentParser(description="Utility for analyzing B2B data rates")
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        nargs="*",
        help="Input FIFO dump *.evt file. Corresponding timing file must exist.",
    )
    parser.add_argument(
        "--dummy", action="store_true", default=False, help="Produce a dummy plot."
    )
    parser.add_argument(
        "--word-rate", action="store_true", default=False, help="Compute word rate"
    )
    args = parser.parse_args()

    input_files_ok = check_inputs(args.input)
    if not input_files_ok:
        sys.exit(1)

    if args.dummy:
        make_dummy_plot(args)

    make_rate_plot(args)


if __name__ == "__main__":
    main()
