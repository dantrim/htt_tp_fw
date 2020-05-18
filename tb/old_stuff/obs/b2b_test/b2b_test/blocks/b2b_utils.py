
import enum
from pathlib import Path
from glob import glob

import cocotb

class B2BIO :

    class B2BInputs(enum.Enum) :
        PIXEL_0 = 0
        PIXEL_1 = 1
        STRIP_0 = 2
        STRIP_1 = 3

    class B2BOutputs(enum.Enum) :
        AMTP_0 = 13
        AMTP_1 = 12
        AMTP_2 = 11
        AMTP_3 = 10
        AMTP_4 = 9
        AMTP_5 = 8
        AMTP_6 = 7
        AMTP_7 = 6
        AMTP_8 = 5
        AMTP_9 = 4
        AMTP_10 = 3
        AMTP_11 = 2
        SSTP_0 = 1
        SSTP_1 = 0

    @staticmethod
    def allowed_tps() :
    
        tps = set()
        for b2b in B2BIO.B2BOutputs :
            tps.append( str(b2b.name).split("_")[0] )
        return tps

    @staticmethod
    def to_clean_name(io_enum_val) :

        return str( io_enum_val.name ).replace("_","")

    @staticmethod
    def clean_names(io_enum) :

        names = []
        for io in io_enum :
            names.append( B2BIO.to_clean_name(io) )
        return names

def testvec_dir_from_env() :

    import os
    testvecdir = os.environ.get("TESTVECDIR")
    if not testvecdir :
        raise Exception("ERROR Environment \"TESTVECDIR\" is not set")
    return testvecdir

def get_testvector_files(base_tp, testvec_dir, input_or_output) :

    if type(base_tp) != B2BIO.B2BOutputs :
        raise Exception("ERROR base_tp must be of type {}".format(type(B2BIO.B2BOutputs)))

    tdir = Path( str(testvec_dir) )
    ok = tdir.exists() and tdir.is_dir()
    if not ok :
        raise Exception("ERROR Provided testvector directory not found (={})".format(str(testvec_dir)))

    file_fmt = {
        "input" : "BoardToBoardInput_"
        ,"output" : "TPtoSync_src"
    }[input_or_output.lower()]

    file_fmt += B2BIO.to_clean_name(base_tp)
    testvec_files = list(tdir.glob("{}_*".format(file_fmt)))

    ordered_files = []
    io_enum = {
        "input" : B2BIO.B2BInputs
        ,"output" : B2BIO.B2BOutputs
    }[input_or_output.lower()]

    for i, io in enumerate(io_enum) :
        cn = B2BIO.to_clean_name(io).lower()
        for j, tf in enumerate(testvec_files) :
            final_tag = str(tf).split("_")[-1].replace(".evt","").replace("dest","").lower()
            if final_tag == cn :
                ordered_files.append(tf)
                break
    return ordered_files
