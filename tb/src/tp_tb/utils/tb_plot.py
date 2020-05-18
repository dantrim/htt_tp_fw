import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def default_canvas(n=1, m=1, grid=True, x_label="", y_label=""):

    """
    Produce a standard figure and axis object ready for plotting on.
    """
    fig = plt.figure()
    grid = GridSpec(100, 100)
    pad = fig.add_subplot(grid[0:100, :])

    pad.tick_params(
        axis="both",
        which="both",
        labelsize=16,
        direction="in",
        labelleft=True,
        bottom=True,
        top=True,
        right=True,
        left=True,
    )

    if grid:
        pad.grid(color="k", which="both", linestyle="--", lw=1, alpha=0.3)

    if x_label:
        pad.set_xlabel(x_label, horizontalalignment="right", x=1.0, fontsize=16)

    if y_label:
        pad.set_ylabel(y_label, horizontalalignment="right", y=1.0, fontsize=16)
        # pad.get_yaxis().set_label_coords(-0.16, 1.0)
    return fig, pad
