#!/bin/bash

set -e # makes the program stop if any of the commands fail

# ok lets begin
cd config
config_origin=$(pwd)

# Read the config file
CONFIG_FILE="config_2.cfg"

# Initialize variables
wdir=""
base_path=""
project_name=""
snap_dir=""
snap_it=""
project_name=""
duplicationx=""
duplicationy=""
duplicationz=""
orient1=""
orient2=""
orient3=""
latt_param_0=""
temp=""
run_step=""
etol=""
ftol=""
max_iter=""
max_eval=""
heat_loop=""
heat_int=""
compress_loop=""

# Read the file line by line
while IFS='=' read -r key value
do
    case "$key" in
        'wdir') wdir="$value" ;;
        'base_path') base_path="$value" ;;
        'project_name') project_name="$value" ;;
        'snap_dir') snap_dir="$value" ;;
        'snap_it') snap_it=$(printf "%d" "$value") ;; #int
        'duplicationx') duplicationx=$(printf "%d" "$value") ;; #int
        'duplicationy') duplicationy=$(printf "%d" "$value") ;; #int
        'duplicationz') duplicationz=$(printf "%d" "$value") ;; #int
        'orient1') orient1="$value" ;;
        'orient2') orient2="$value" ;;
        'orient3') orient3="$value" ;;
        'latt_param_0') latt_param_0=$(printf "%.6f" "$value") ;; # float (6dp)
        'temp') temp=$(printf "%.6f" "$value") ;; # float (6dp)
        'run_step') run_step=$(printf "%d" "$value") ;; #int
        'etol') etol=$(printf "%.6f" "$value") ;; # float (6dp)
        'ftol') ftol=$(printf "%.6f" "$value") ;; # float (6dp)
        'max_iter') max_iter=$(printf "%d" "$value") ;; # int
        'max_eval') max_eval=$(printf "%d" "$value") ;; # int
        'heat_loop') heat_loop=$(printf "%d" "$value") ;; # int
        'heat_int') heat_int=$(printf "%d" "$value") ;; # int
        'compress_loop') compress_loop=$(printf "%d" "$value") ;; # int
    esac
done < "$CONFIG_FILE"

echo $wdir
cd $wdir

echo $snap_dir
# count snap potentials (get total number of iterations)
num_snap=$(printf "%d" "$(python count_snap.py $snap_dir )")

echo $num_snap

while [ $snap_it -le $num_snap ]; do

    python file_system_gen.py $base_path $project_name/var_$snap_it

    project_path="$base_path/$project_name/var_$snap_it"
    cd $project_path

    # copy config into the project file
    scp $config_origin/$CONFIG_FILE $project_path/project/config

    cd project/data/input

    ### GENERATING BASIC LATTICE

    atomsk --create bcc $latt_param_0 Ni Ti orient [$orient1] [$orient2] [$orient3] -duplicate $duplicationx $duplicationy $duplicationz pos

    cd $wdir

    python intoHEA_6.py $project_path/project/data/input/ $project_path/project/data/input/

    # generate input file for relax analysis
    python pylammps_relax_5.py $project_path/project/data/ $snap_dir/HEA_var$snap_it.snapcoeff $snap_dir/HEA_var$snap_it.snapparam $temp $run_step $etol $ftol $max_iter $max_eval

    # run LAMMPS relax (this needs to be changed when moved to slurm to allow for GPU processing)
    export LD_LIBRARY_PATH=/home/winniebird/anaconda3/lib:$LD_LIBRARY_PATH
    python run_lammps.py $project_path in.relax.HEA relax

    # read output
    latt_param_1=$(python Read_cfg_1.py $project_path/project/data/output 'min_dump.cfg'  $duplicationx)

    # update parameters (this is for dislocation stuffs remember)
    python add_or_update_cfg.py --config-file=$project_path/project/config/config.cfg --key=latt_param_1 --value=$latt_param_1

    ### HEAT ANALYSIS
    # generate input file for heat analysis
    python pylammps_heat_1.py $project_path/project/data $snap_dir/HEA_var1.snapcoeff $snap_dir/HEA_var1.snapparam $temp $run_step $heat_loop $heat_int

    # run LAMMPS heat (this needs to be changed when moved to slurm to allow for GPU processing)
    export LD_LIBRARY_PATH=/home/winniebird/anaconda3/lib:$LD_LIBRARY_PATH
    python run_lammps.py $project_path in.heat.HEA heat

    ((snap_it++))
done

# post processing