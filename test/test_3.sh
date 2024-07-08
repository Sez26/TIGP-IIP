#!/bin/bash

set -e # makes the program stop if any of the commands fail

# ok lets begin
cd config
config_origin=$(pwd)

# Read the config file
CONFIG_FILE="config.cfg"

# Initialize variables
wdir=""
base_path=""
project_name=""
duplication=""
latt_param_0=""
temp=""
run_step=""
etol=""
ftol=""
max_iter=""
max_eval=""

# Read the file line by line
while IFS='=' read -r key value
do
    case "$key" in
        'wdir') wdir="$value" ;;
        'base_path') base_path="$value" ;;
        'project_name') project_name="$value" ;;
        'duplication') duplication=$(printf "%d" "$value") ;; #int
        'latt_param_0') latt_param_0=$(printf "%.6f" "$value") ;; # float (6dp)
        'temp') temp=$(printf "%.6f" "$value") ;; # float (6dp)
        'run_step') run_step=$(printf "%d" "$value") ;; #int
        'etol') etol=$(printf "%.6f" "$value") ;; # float (6dp)
        'ftol') ftol=$(printf "%.6f" "$value") ;; # float (6dp)
        'max_iter') max_iter=$(printf "%d" "$value") ;; # int
        'max_eval') max_eval=$(printf "%d" "$value") ;; # int
    esac
done < "$CONFIG_FILE"

echo $wdir
cd $wdir

python file_system_gen.py $base_path $project_name

project_path="$base_path/$project_name"
cd $project_path

# copy config into the project file
scp $config_origin/config.cfg $project_path/project/config

cd project/data/input

atomsk --create bcc $latt_param_0 Ni Ti orient [100] [010] [001] -duplicate $duplication $duplication $duplication pos

cd $wdir

python intoHEA_6.py $project_path/project/data/input/ $project_path/project/data/input/

# generate input file for relax analysis
python pylammps_relax_5.py $project_path/project/data/ $wdir/HEA_var1.snapcoeff $wdir/HEA_var1.snapparam $temp $run_step $etol $ftol $max_iter $max_eval

# run LAMMPS relax (this needs to be changed when moved to slurm to allow for GPU processing)
export LD_LIBRARY_PATH=/home/winniebird/anaconda3/lib:$LD_LIBRARY_PATH
python run_lammps.py $project_path in.relax.HEA

# read output
latt_param_1=$(python Read_cfg_1.py $project_path/project/data/output 'min_dump.cfg'  $duplication)

# update parameters
python add_or_update_cfg.py --config-file=$project_path/project/config/config.cfg --key=latt_param_1 --value=$latt_param_1