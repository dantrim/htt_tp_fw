
import sys
infile = sys.argv[1]
ofile = "{}_reverse.hex".format(infile.split("/")[-1].split(".")[0])
with open(ofile, "w") as ofile :

    with open(infile, "r") as ifile :
        for iline, line in enumerate(ifile) :
            line = line.strip()
            #print(line[2:]) # remove first byte
            data = int(line[2:], 16)
            ds = line[2:]
            meta = line[:2]
    
            new_data = []
            new_data.append(ds[-2:])
            lidx = -4
            ridx = -2
            word_size = 16 # number of bytes in 64 bit word
            while True :
                new_data.append(ds[lidx:ridx])
                lidx -= 2
                ridx -= 2
                if lidx == -1 * (word_size+2) :
                    break
            rdata = ""
            rdata = rdata.join(new_data)
            rdata = meta + rdata
            ofile.write("{}\n".format(rdata))
