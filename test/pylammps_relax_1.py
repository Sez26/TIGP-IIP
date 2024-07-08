from lammps import PyLammps
import os
from mpi4py import MPI
import sys
from contextlib2 import redirect_stdout, redirect_stderr

## im not sure why this one needs MPI and the other doesn't?

# Initialize PyLammps
L = PyLammps()

# Specify the file to save the output
output_file = "./lammps_output_relax.log"
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
        # L.command("thermo 100")
        # L.command("thermo_style	custom step temp pe pxx pyy pzz density")
        L.thermo(100)
        L.thermo_style("custom step temp pe vol density pxx pyy pzz")

        # Set up and run minimization
        L.command("dump 1 all custom 100 min_dump.cfg id type x y z")
        L.command("min_style cg")
        L.command("fix 1 all box/relax aniso 0.0")
        L.command("minimize " + "0.0" + " " + "0.02" + " 5000 10000")
        L.command("unfix 1")
        L.command("minimize " + "0.0" + " " + "0.02" + " 5000 10000")
        L.undump(1)

        # define some properties you are interested in
        L.command("variable lenx equal lx")
        L.command("variable leny equal ly")
        L.command("variable lenz equal lz")

        # compute things
        L.command("compute sta all stress/atom NULL")
        L.command("compute vol_atom all voronoi/atom")
        L.command("variable	va atom c_vol_atom[1]")
        L.command("variable	sa_xx atom 1E-4*c_sta[1]/v_va")
        L.command("variable	sa_yy atom 1E-4*c_sta[2]/v_va")
        L.command("variable	sa_zz atom 1E-4*c_sta[3]/v_va")
        L.command("variable	sa_xy atom 1E-4*c_sta[4]/v_va")
        L.command("variable	sa_xz atom 1E-4*c_sta[5]/v_va")
        L.command("variable	sa_yz atom 1E-4*c_sta[6]/v_va")
        L.command("variable	sa_hydro atom (v_sa_xx+v_sa_yy+v_sa_zz)/3.0")
        L.command("variable	sa_von atom sqrt(0.5*((v_sa_xx-v_sa_yy)^2+(v_sa_yy-v_sa_zz)^2+(v_sa_zz-v_sa_xx)^2)+3.0*((v_sa_xy)^2+(v_sa_xz)^2+(v_sa_yz)^2))")

        # Set up and run MD in NPT ensemble
        L.timestep(0.001)
        L.command("neighbor	1.0 bin")
        L.command("neigh_modify	every 5 delay 0 check yes")
        L.command("reset_timestep 0")
        L.velocity("all create 300.0 12345678")
        
        L.command("dump	1 all custom 1000 md_npt_dump.cfg id type x y z v_sa_hydro v_sa_von")
        # L.command("fix 	1 all npt temp 300 300 0.1 aniso 0 0 1.0")
        L.fix(2, "all", "print", 100, "$(step) $(temp) $(pe) $(vol) $(density) $(pxx) $(pyy) $(pzz)", "file", "Record_npt.txt")
        L.fix(1, "all", "npt", "temp", 300, 300, 0.1, "aniso", 0, 0, 1.0)
        L.command("fix 	avg all ave/time 10 1000 100000 v_lenx v_leny v_lenz")
        
        # RUN
        L.run(100000)

        L.undump(1)
        L.unfix(1)
        L.unfix(2)

        # Reassigning variables
        L.command("variable newlx equal f_avg[1]")
        L.command("variable newly equal f_avg[2]")
        L.command("variable newlz equal f_avg[3]")
        L.command("change_box all x final 0 ${newlx} y final 0 ${newly} z final 0 ${newlz} remap units box")
        L.command("unfix avg")
        # This writes post relaxation to file for Thermal expansion analysis
        L.command("write_data after_relax.data nocoeff")

        # adding a minimisation
        L.command("dump 1 all custom 100 min_dump.cfg id type x y z v_sa_hydro v_sa_von")
        L.command("minimize 0.0 0.02 5000 10000")
        # this writes to .cfg file of perfect mesh relaxation to be read and used to calculate new lattice parameter for dislocation
        # and stress strain analysis
        L.command("undump 1")
