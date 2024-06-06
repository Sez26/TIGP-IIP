#!/bin/bash

# Check if the environment file exists
if [ ! -f environment.yml ]; then
    echo "Error: environment.yml file not found."
    exit 1
fi

# Define the name of the Conda environment
env_name="TIGP_IIP_ASE_env"

# Create Conda environment from environment file with specified name
conda env create -n $env_name -f environment.yml

# Activate the newly created environment
source activate $env_name
