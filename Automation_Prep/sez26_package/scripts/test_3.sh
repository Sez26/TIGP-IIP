#!/usr/bin/bash

set -e # makes the program stop if any of the commands fail

# ok lets begin
wdir='/home/sez26/TIGP-IIP/Automation_Prep/Python/'
cd $wdir

# Read the config file
CONFIG_FILE="config.cfg"

# Initialize variables
base_path=""
project_name=""
wdir=""
atomskdir=""
duplication=""
latt_param_0=""

# Read the file line by line
while IFS='=' read -r key value
do
    case "$key" in
        'base_path') base_path="$value" ;;
        'project_name') project_name="$value" ;;
        'wdir') wdir="$value" ;;
        'atomskdir') atomskdir="$value" ;;
        'duplication') duplication=$(printf "%d" "$value") ;;
        'latt_param_0') latt_param_0=$(printf "%.6f" "$value") ;;
    esac
done < "$CONFIG_FILE"

python file_system_gen.py $base_path $project_name

project_path="$base_path$project_name"
cd $project_path

cd project/data/input

$atomskdir --create bcc $latt_param_0 Ni Ti orient [100] [010] [001] -duplicate $duplication $duplication $duplication pos

cd $base_path

python intoHEA_6.py $project_path/project/data/input/ $project_path/project/data/input/

latt_param_1=$(python Read_cfg_1.py $wdir 'min_dump.cfg'  $duplication)

python add_or_update_cfg.py --config-file=config.cfg --key=latt_param_1 --value=$latt_param_1