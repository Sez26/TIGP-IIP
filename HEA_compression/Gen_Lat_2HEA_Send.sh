#!/usr/bin/bash

../../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 3.128 Ni Ti orient [100] [010] [001] -duplicate 18 18 18 pos

python intoHEA_4.py

scp HEA_II.lmp sfarrelly2024@slurm-ui04.twgrid.org:/ceph/work/CNNL/sfarrelly2024/HEA_dislocation/Perfect