from scipy import stats
import numpy as np  # to set random seed


# from tb_b2b import b2b_utils
from . import b2b_utils
from tp_tb.testbench.b2b.b2b_ports import B2BPorts

random_seed_set = []


def bound(low, high, value):
    return max(low, min(high, value))


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def event_rate_delay(io_enum, event, pass_through=False):

    if pass_through:
        return {}

    ##
    ## UNIT rates from Table 3.8 of HTT specifications document.
    ##
    unit_event_rates = [20 * x * 1e3 for x in (320, 330, 420)]  # kHz -> Hz

    #    if io_enum.value == 0 :
    #        unit_event_rates = [x * 1e3 for x in (100, 100, 100)]

    # We use scipy to sample a PDF of the expected cluster rates.
    # Scipy relies on numpy.random for its random number generator,
    # so we should set numpy's random seed so as to ensure some level
    # of reproducibility.
    # We set the random seed based on the observed event's header and footer,
    # which will make the dataflow reproducible for a given set of input
    # test vectors.
    #
    # Note: Here a random seed is set each time a new IO input is seen, which
    # is done so that each IO input has it's own randomized sets of delays.
    # This is done so that the sets of delays are the same across each of the inputs
    # being driven regardless of how many number of events the test is loading into
    # the DUT (if you run N events in one test, and N-1 events in the next test,
    # the sequence of random numbers will be different and the delays for IO 0 and IO 1
    # will be different for IO 1 between the two scenarios). This assumes that
    # the events for each input are loaded all at once, that is: all events
    # for IO 0 are loaded, then all events for IO 1 are loaded, ...
    #
    global random_seed_set
    if io_enum.value not in random_seed_set:
        random_seed = sum(
            [int(x.contents) for x in event.header_words + event.footer_words]
        )
        # random seeds must be convertible to 32-bit unsigned ints
        # see: https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.RandomState.seed.html#numpy.random.RandomState.seed
        random_seed = random_seed & 0xFFFFFFFF
        random_seed_set.append(io_enum.value)
        np.random.seed(seed=random_seed)

    lo = unit_event_rates[0]
    hi = unit_event_rates[2]
    median = unit_event_rates[1]
    sample_rate_in = stats.expon.rvs(size=1, scale=median)[0]
    sample_rate = bound(lo, hi, sample_rate_in)

    delay = 1.0 / float(sample_rate)  # rate to time
    delay *= 1e9  # convert from seconds to nanoseconds

    delay_dict = {"delay": int(delay), "delay_unit": "ns"}  # go to ~nearest whole unit
    return delay_dict
