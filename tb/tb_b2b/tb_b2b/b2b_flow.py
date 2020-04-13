from scipy import stats

from tb_b2b import b2b_utils

def bound(low, high, value) :
    return max(low, min(high, value))

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def event_rate_delay(io_enum, event, pass_through = False) :

    """
    Determine the cumulative event delay based on the data type
    and event. Cluster rates are taken from ATL-COM-DAQ-2018-162(_020419)
    in
    https://www.dropbox.com/home/HTT_SharedArea/HTT_Specifications?preview=ATL-COM-DAQ-2018-162_020419_HTT.pdf

    :io_enum: b2b_utils.B2BIO.Inputs
    :event: tb_utils.events DataEvent
    :pass_through: whether or not to implement a delay

    :note: The precision of time delays is taken as nanosecond

    :rtype: dict
    :returns: dictionary describing delay for sending next data word
    """
    if type(io_enum) != b2b_utils.B2BIO.Inputs :
        raise TypeError("Expected type for io_enum is \"{}\", got \"{}\"".format("b2b_utils.B2BIO.Inputs", type(io_enum)))

    if pass_through :
        return  {}

    ##
    ## assumes inputs to AMTP only, numbers come from
    ## Table 3.7 of HTT specifications document.
    ## These numbers are not super specific (e.g. eta/phi or gHTT/rHTT breakdown)
    ## but doing that is not necessarily our goal, rather we just want some
    ## representative event delays (I think)
    ##
    pixel_cluster_rates = [x * 1e6 for x in (37, 64, 420)] # Hz
    strip_cluster_rates = [x * 1e6 for x in (0, 540, 860)] # Hz

    n_modules = event.n_modules
    modules = event.get_modules()

    # Table 3.7 gives the overall cluster rates in MHz, so for a given
    # event with N clusters, the average time should just be the sum of N
    # periods from rates sampled from a PDF constructed from the Table 3.7 values.
    # the PDF sampled from here is an exponential PDF with a mean simply taken
    # from the median values from the Table 3.7 values (mean and median of
    # exponential PDF differ by ln(2) but we're not going for accuracy here
    # in these numbers, just behavior

    accumulated_delay = 0.0
    for imodule, module in enumerate(modules) :
        if module.is_pixel() :
            lo = pixel_cluster_rates[0]
            hi = pixel_cluster_rates[2]
            median = pixel_cluster_rates[1]
        elif module.is_strip() :
            lo = strip_cluster_rates[0]
            hi = strip_cluster_rates[2]
            median = strip_cluster_rates[1]
        sample_rate = stats.expon.rvs(size=1, scale = median)
        sample_rate = bound(lo,  hi, sample_rate)
        accumulated_delay += (1.0 / float(sample_rate)) # Hz -> time in seconds

    accumulated_delay *= 1e9 # convert from seconds to nanoseconds
    accumulated_delay = int(accumulated_delay) # ~convert to nearest ns

    delay_dict = {
        "delay" : accumulated_delay
        ,"delay_unit" : "ns"
    }
    return delay_dict
