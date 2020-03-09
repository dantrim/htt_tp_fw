
def check_fifo_block(spy_buffer_block, name = "") :

    """
    Check that the object has the expected
    RTL signals for a SpyBuffer block
    """

    required_signals = [
        "write_enable"
        ,"read_enable"
        ,"write_data"
        ,"almost_full"
        ,"empty"
    ]

    missing_signals = []
    for req_sig in required_signals :
        if not hasattr(spy_buffer_block, req_sig) :
            missing_signals.append(req_sig)
    if missing_signals :
        name_str = "" if not name else name
        cocotb.error("Provided FIFO block{} is missing required signal(s): {}".
            format(" {}".format(name) if name else ""))
        return False
    return True
