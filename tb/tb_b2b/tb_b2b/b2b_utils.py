import enum
import os
from pathlib import Path
from glob import glob
import cocotb

class B2BIO :

    class Inputs(enum.Enum) :
        PIXEL_0 = 0
        PIXEL_1 = 1
        STRIP_0 = 2
        STRIP_1 = 3

    class Outputs(enum.Enum) :
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
    def allowed_outputs() :

        outputs = set()
        for output in B2BIO.Outputs :
            outputs.add( str(output.name) )
        return outputs

    @staticmethod
    def simplename(io_enum) :

        if type(io_enum) == type(B2BIO.Outputs) or type(io_enum) == type(B2BIO.Inputs) :
            io_enum = io_enum.name
        return str(io_enum).replace("_","")

def testvec_dir_from_env() :

    testvecdir = os.environ.get("TESTVECDIR")
    if not testvecdir :
        raise Exception("ERROR Environtment \"TESTVECDIR\" is empty")
    return testvecdir

def get_testvector_files(base_tp, testvec_dir, which) :

    if type(base_tp) != B2BIO.Outputs :
        raise Exception("ERROR base_tp must be of type {}".format(type(B2BIO.Outputs)))

    tdir = Path( str(testvec_dir) )
    ok = tdir.exists() and tdir.is_dir()
    if not ok :
        raise Exception("ERROR Provided testvector directory (={}) not found".format(str(testvec_dir)))

    file_fmt = {
        "input" : "BoardToBoardInput_"
        ,"output" : "TPtoSync_src"
    } [which.lower()]

    file_fmt += B2BIO.simplename( base_tp )
    testvec_files = list(tdir.glob("{}_*".format(file_fmt)))

    io_enum = {
        "input" : B2BIO.Inputs
        ,"output" : B2BIO.Outputs
    }[which.lower()]

    ##
    ## order files by their io port number
    ##
    ordered_files = []
    n_io = len(io_enum)
    for i in range(n_io) :
        for io in io_enum :
            if io.value == i : # this is the io port that we want
                name = B2BIO.simplename(io).lower()
                for tfile in testvec_files :
                    final_tag = str(tfile).split("_")[-1].replace(".evt","").replace("dest","").lower()
                    if final_tag == name :
                        ordered_files.append(tfile)
                        break
    return ordered_files
