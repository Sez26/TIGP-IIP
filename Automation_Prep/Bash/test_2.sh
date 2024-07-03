#!/usr/bin/bash

set -e # makes the program stop if any of the commands fail

### careful no spaces when generating variables
### directory inputs
base_path='/home/sez26/TIGP-IIP/Automation_Prep/Python/'
project_name='test_project_3'

wdir='/home/sez26/TIGP-IIP/Automation_Prep/Python/'

# ideally we want this to run from conda package
atomskdir='/home/sez26/TIGP-IIP/atomsk_b0.13.1_Linux-amd64/atomsk'

### lattice generation specifics (these can be put into a config file)
duplication=18
latt_param=3.128

echo "Original lattice parameter: $latt_param"

# ok lets begin
cd $wdir
python file_system_gen.py $base_path $project_name

project_path="$base_path$project_name"
cd $project_path
cd project/data/input
$atomskdir --create bcc $latt_param Ni Ti orient [100] [010] [001] -duplicate $duplication $duplication $duplication pos
cd $base_path
python intoHEA_6.py $project_path/project/data/input/ $project_path/project/data/input/

o_p=$(python Read_cfg_1.py $wdir 'min_dump.cfg'  $duplication)
latt_param_new=$o_p

echo $latt_param_new