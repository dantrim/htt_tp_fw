from scipy import stats
import numpy as np  # to set random seed


# from tb_b2b import b2b_utils
from . import b2b_utils

random_seed_set = []


def bound(low, high, value):
    return max(low, min(high, value))


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def event_rate_delay(io_enum, event, pass_through=False):

    if type(io_enum) != b2b_utils.B2BIO.Inputs:
        raise TypeError(
            f'Expected type for io_enum is "b2b_utils.B2BIO.Inputs", bot "{type(io_enum)}"'
        )

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


# def event_rate_delay(io_enum, event, pass_through = False) :
#
#    """
#    Determine the cumulative event delay based on the data type
#    and event. Cluster rates are taken from ATL-COM-DAQ-2018-162(_020419)
#    in
#    https://www.dropbox.com/home/HTT_SharedArea/HTT_Specifications?preview=ATL-COM-DAQ-2018-162_020419_HTT.pdf
#
#    :io_enum: b2b_utils.B2BIO.Inputs
#    :event: tb_utils.events DataEvent
#    :pass_through: whether or not to implement a delay
#
#    :note: The precision of time delays is taken as nanosecond
#
#    :rtype: dict
#    :returns: dictionary describing delay for sending next data word
#    """
#    if type(io_enum) != b2b_utils.B2BIO.Inputs :
#        raise TypeError("Expected type for io_enum is \"{}\", got \"{}\"".format("b2b_utils.B2BIO.Inputs", type(io_enum)))
#
#    if pass_through :
#        return  {}
#
#    ##
#    ## assumes inputs to AMTP only, numbers come from
#    ## Table 3.7 of HTT specifications document.
#    ## These numbers are not super specific (e.g. eta/phi or gHTT/rHTT breakdown)
#    ## but doing that is not necessarily our goal, rather we just want some
#    ## representative event delays (I think)
#    ##
#    pixel_cluster_rates = [x * 1e6 for x in (37, 64, 420)] # Hz
#    strip_cluster_rates = [x * 1e6 for x in (0, 540, 860)] # Hz
#
#    n_modules = event.n_modules
#    modules = event.get_modules()
#
#    # We use scipy to sample a PDF of the expected cluster rates.
#    # Scipy relies on numpy.random for its random number generator,
#    # so we should set numpy's random seed so as to ensure some level
#    # of reproducibility.
#    # We set the random seed based on the observed event's header and footer,
#    # which will make the dataflow reproducible for a given set of input
#    # test vectors.
#    #
#    # Note: Here a random seed is set each time a new IO input is seen, which
#    # is done so that each IO input has it's own randomized sets of delays.
#    # This is done so that the sets of delays are the same across each of the inputs
#    # being driven regardless of how many number of events the test is loading into
#    # the DUT (if you run N events in one test, and N-1 events in the next test,
#    # the sequence of random numbers will be different and the delays for IO 0 and IO 1
#    # will be different for IO 1 between the two scenarios). This assumes that
#    # the events for each input are loaded all at once, that is: all events
#    # for IO 0 are loaded, then all events for IO 1 are loaded, ...
#    #
#    global random_seed_set
#    if io_enum.value not in random_seed_set :
#        random_seed = sum([ int(x.contents) for x in event.header_words + event.footer_words ])
#        # random seeds must be convertible to 32-bit unsigned ints
#        # see: https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.RandomState.seed.html#numpy.random.RandomState.seed
#        random_seed = random_seed & 0xffffffff
#        random_seed_set.append(io_enum.value)
#        np.random.seed(seed = random_seed)
#
#    # Table 3.7 gives the overall cluster rates in MHz, so for a given
#    # event with N clusters, the average time should just be the sum of N
#    # periods from rates sampled from a PDF constructed from the Table 3.7 values.
#    # the PDF sampled from here is an exponential PDF with a mean simply taken
#    # from the median values from the Table 3.7 values (mean and median of
#    # exponential PDF differ by ln(2) but we're not going for accuracy here
#    # in these numbers, just behavior
#
#    accumulated_delay = 0.0
#    for imodule, module in enumerate(modules) :
#        if module.is_pixel() :
#            lo = pixel_cluster_rates[0]
#            hi = pixel_cluster_rates[2]
#            median = pixel_cluster_rates[1]
#        elif module.is_strip() :
#            lo = strip_cluster_rates[0]
#            hi = strip_cluster_rates[2]
#            median = strip_cluster_rates[1]
#        sample_rate = stats.expon.rvs(size=1, scale = median)
#        sample_rate = bound(lo,  hi, sample_rate)
#        accumulated_delay += (1.0 / float(sample_rate)) # Hz -> time in seconds
#
#    accumulated_delay *= 1e9 # convert from seconds to nanoseconds
#    accumulated_delay = int(accumulated_delay) # ~convert to nearest ns
#
#    delay_dict = {
#        "delay" : accumulated_delay
#        ,"delay_unit" : "ns"
#    }
#    return delay_dict
