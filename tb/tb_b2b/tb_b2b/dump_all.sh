#!/bin/bash

for i in {1..9}; do
    python b2b_dump.py -i /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/tb_b2b/tb_b2b/test/sim_build/fifomonitor_B2B_AMTP${i}_0${i}.evt > blah_obs_0${i}.txt
    python b2b_dump.py -i /home/dantrim/work/tdaq-htt-firmware/testvecs/20200124/TPtoSync_srcAMTP0_destAMTP${i}.evt -n 2 > blah_exp_0${i}.txt
done

for i in {10..11}; do
    python b2b_dump.py -i /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/tb_b2b/tb_b2b/test/sim_build/fifomonitor_B2B_AMTP${i}_${i}.evt > blah_obs_${i}.txt
    python b2b_dump.py -i /home/dantrim/work/tdaq-htt-firmware/testvecs/20200124/TPtoSync_srcAMTP0_destAMTP${i}.evt -n 2 > blah_exp_${i}.txt
done

python b2b_dump.py -i /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/tb_b2b/tb_b2b/test/sim_build/fifomonitor_B2B_SSTP0_12.evt > blah_obs_12.txt
python b2b_dump.py -i /home/dantrim/work/tdaq-htt-firmware/testvecs/20200124/TPtoSync_srcAMTP0_destSSTP0.evt -n 2 > blah_exp_12.txt

python b2b_dump.py -i /home/dantrim/work/tdaq-htt-firmware/tp-fw/tb/tb_b2b/tb_b2b/test/sim_build/fifomonitor_B2B_SSTP1_13.evt > blah_obs_13.txt
python b2b_dump.py -i /home/dantrim/work/tdaq-htt-firmware/testvecs/20200124/TPtoSync_srcAMTP0_destSSTP1.evt -n 2 > blah_exp_13.txt
