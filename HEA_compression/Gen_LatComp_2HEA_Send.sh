#!/usr/bin/bash

# ../../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 3.128 Ni Ti orient [100] [010] [001] -duplicate 18 18 18 ./LMP_Files/100 pos

cd ./LMP_Files/100
../../../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 3.12 Ni Ti orient [100] [010] [001] -duplicate 20 10 10 pos
                                                                # strain is applied to first (X)
                                                                #         Other surfaces are orthogonal
python intoHEA_5.py
scp HEA_II.lmp sfarrelly2024@slurm-ui04.twgrid.org:/ceph/work/CNNL/sfarrelly2024/HEA_compression/100

cd ../110
../../../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 3.12 Ni Ti orient [110] [1-10] [001] -duplicate 14 7 10 pos
                                                                        # this is '-1' not dash 1
python intoHEA_5.py
scp HEA_II.lmp sfarrelly2024@slurm-ui04.twgrid.org:/ceph/work/CNNL/sfarrelly2024/HEA_compression/110

cd ../111
../../../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 3.12 Ni Ti orient [111] [1-10] [11-2] -duplicate 24 7 4 pos
python intoHEA_5.py
scp HEA_II.lmp sfarrelly2024@slurm-ui04.twgrid.org:/ceph/work/CNNL/sfarrelly2024/HEA_compression/111
