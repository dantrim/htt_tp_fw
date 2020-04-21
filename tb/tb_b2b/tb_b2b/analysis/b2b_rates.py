
import os, sys
from pathlib import Path
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt

from tb_utils import events, tb_plot
DATA_ENDIAN = "little"

def check_inputs(input_filelist = []) :

    all_ok = True
    for ifile, filename in enumerate(input_filelist) :
        p = Path(filename)
        ok = p.exists() and p.is_file()
        if not ok :
            print("ERROR Input file #{:02} (={}) is not found".format(ifile, filename))
            all_ok = False

    plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.jet(np.linspace(0,1,len(input_filelist)+1)))
    
    return all_ok

def make_dummy_plot(args) :

    ##
    ## load the data
    ##
    input_filenames = args.input
    input_event_lists = []
    for ifile, filename in enumerate(args.input) :
        loaded_events = events.load_events_from_file(filename
            ,endian = DATA_ENDIAN
            ,load_timing_info = True
        )
        print("INFO Loaded {} events from file #{:02} (={})".format(len(loaded_events), ifile, filename))
        input_event_lists.append(loaded_events)

    ##
    ## generate the data
    ##
    timestamp_unit = ""
    x_data = []
    event_boundaries = []
    y_data = []
    labels = []
    for input_num, input_events in enumerate(input_event_lists) :
        n_words = 0
        input_x_data = []
        input_y_data = []
        for ievent, event in enumerate(input_events) :
            for iword, word in enumerate(event.words) :
                n_words += 1
                if not timestamp_unit :
                    timestamp_unit = word.timestamp_units
                if iword == 0 :
                    event_boundaries.append( [word.timestamp, n_words] )
                input_x_data.append(word.timestamp)
                input_y_data.append(n_words)
        x_data.append( input_x_data )
        y_data.append( input_y_data )
        label = Path( input_filenames[input_num] ).stem
        labels.append(label)

    ##
    ## create the canvas
    ##
    fig, ax = tb_plot.default_canvas(x_label = "Time [{}]".format(timestamp_unit)
                                            ,y_label = "Number of words"
                                    )

    ##
    ## plot the data
    ##
    for i in range(len(input_event_lists)) :
        ax.plot(x_data[i], y_data[i], label = labels[i])
    event_bounds_x, event_bounds_y = zip(*event_boundaries)
    ax.plot(event_bounds_x, event_bounds_y, "ro", markersize = 2)
    ax.legend(loc = "best", frameon = False, fontsize = 8)

    ##
    ## save the figure
    ##
    outname = "b2b_dummy_plot.pdf"
    print("Saving figure: {}".format(os.path.abspath(outname)))
    fig.savefig(outname, bbox_inches = "tight")

def main() :

    parser = ArgumentParser(description = "Utility for analyzing B2B data rates")
    parser.add_argument("-i", "--input", required = True, nargs = "*",
        help = "Input FIFO dump *.evt file. Corresponding timing file must exist."
    )
    parser.add_argument("--dummy", action = "store_true", default = False,
        help = "Produce a dummy plot."
    )
    args = parser.parse_args()

    input_files_ok = check_inputs(args.input)
    if not input_files_ok :
        sys.exit(1)
    if args.dummy :
        make_dummy_plot(args)

if __name__ == "__main__" :
    main()
