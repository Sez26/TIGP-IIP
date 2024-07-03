#!/usr/bin/bash

### careful no spaces when generating variables

### directory inputs
wdir='/home/sez26/TIGP-IIP/Automation_Prep/Python/'

# ideally we want this to run from conda package
atomskdir='/home/sez26/TIGP-IIP/atomsk_b0.13.1_Linux-amd64/atomsk'

### lattice generation specifics (these can be put into a config file)
duplication=18
latt_param=3.128

cd $wdir
$atomskdir --create bcc $latt_param Ni Ti orient [100] [010] [001] -duplicate $duplication $duplication $duplication pos
python intoHEA_6.py $wdir