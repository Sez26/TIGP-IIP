from lammps import PyLammps
import os
from mpi4py import MPI
import sys
from contextlib2 import redirect_stdout, redirect_stderr

## im not sure why this one needs MPI and the other doesn't?

# Initialize PyLammps
L = PyLammps()

# Specify the file to save the output
output_file = "./lammps_output.log"
# Open the file and redirect stdout and stderr to this file
with open(output_file, 'w') as f:
    with redirect_stdout(f), redirect_stderr(f):
        # Initialize simulation
        L.units("metal")
        L.atom_style("atomic")
        L.read_data("HEA_II.lmp")

        # edit this to have 5 elements
        # Ni Co Ti Zr Hf
        # has to match order given in snap coefficient files
        L.mass(1, 58.693)
        L.mass(2, 58.933)
        L.mass(3, 47.867)
        L.mass(4, 91.224)
        L.mass(5, 178.49)

        L.pair_style("snap", "")

        L.pair_coeff("* *", "HEA_var1.snapcoeff HEA_var1.snapparam", "Ni Co Ti Zr Hf")

        # Setup standard output
        L.command("thermo_style	custom step temp pe pxx pyy pzz density")
        L.command("thermo 100")

        # Set up and run minimization
        L.command("dump 1 all custom 100 min_dump.cfg id type x y z")
        L.command("min_style cg")
        L.command("fix 1 all box/relax aniso 0.0")
        L.command("minimize " + "0.0" + " " + "0.02" + " 5000 1000")
        L.command("unfix 1")
        L.command("minimize " + "0.0" + " " + "0.02" + " 5000 1000")
        L.undump(1)

        # RUN
        L.run(100)

        # save shit
        # Specify the file path to save the data
        output_file_path = "/home/winniebird/sfarrelly2024/test/after_min.data"

        # Write the current state of the simulation to the specified file
        L.write_data(output_file_path + " nocoeff")

        print(f"Simulation data saved to {output_file_path}")
