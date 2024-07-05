# Copied from ChatGPT
import sys
from contextlib import redirect_stdout, redirect_stderr
from lammps import PyLammps

# Initialize PyLammps
L = PyLammps()

# Specify the file to save the output
output_file = "./lammps_output.log"

# Open the file and redirect stdout and stderr to this file
with open(output_file, 'w') as f:
    with redirect_stdout(f), redirect_stderr(f):
        # Define atom style and create a simulation box
        L.atom_style("atomic")
        L.region("myreg block 0 10 0 10 0 10")
        L.create_box(1, "myreg")

        # Create atoms
        L.create_atoms(1, "random 100 12345 myreg")

        # Set masses for atom types
        L.mass(1, 1.0)

        # Run a simple simulation (example)
        L.velocity("all create 300 4928459 rot yes dist gaussian")
        L.fix("1 all nve")
        L.run(100)

# Output is now saved to lammps_output.log
