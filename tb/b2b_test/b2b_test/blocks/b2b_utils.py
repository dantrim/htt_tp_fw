import enum
from pathlib import Path
from glob import glob


class B2BIO :

    class B2BInputs(enum.Enum) :
        PIXEL_0 = 0
        PIXEL_1 = 1
        STRIP_0 = 2
        STRIP_1 = 3

    class B2BOutputs(enum.Enum) :
        AMTP_0 = 0
        AMTP_1 = 1
        AMTP_2 = 2
        AMTP_3 = 3
        AMTP_4 = 4
        AMTP_5 = 5
        AMTP_6 = 6
        AMTP_7 = 7
        AMTP_8 = 8
        AMTP_9 = 9
        AMTP_10 = 10
        AMTP_11 = 11
        SSTP_0 = 12
        SSTP_1 = 13

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
    testvec_files = tdir.glob("{}_*".format(file_fmt))

    return list(testvec_files)
