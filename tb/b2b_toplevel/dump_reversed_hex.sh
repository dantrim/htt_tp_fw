#!/bin/bash

testvector=${1}
oname=${testvector/.evt/}
oname=${oname}.hex
echo "oname = ${oname}"
tmpname=${oname}
xxd -p -c 9 ${testvector} > ${tmpname}
python reverse.py ${tmpname}
