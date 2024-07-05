## mpi test
# from mpi4py import MPI
from lammps import lammps, PyLammps
import os
# from mpi4py import MPI

# gonna try and recreate the relax analysis

# we be doing class things
class Relax:
    def __init__(self, lmp_file, coefficient, parameter):
        # assigning which .lmp file, which coefficients
        self.lmp_file = lmp_file
        self.coefficient = coefficient
        self.parameter = parameter
    def simulation(self, delE="1e-7", delF="1e-6", n_iter=10000):
        # making instance of lammps
        lmp = lammps()
        L = PyLammps(ptr=lmp)

        # Initialize simulation
        L.units("metal")
        L.atom_style("atomic")
        L.read_data(self.lmp_file)

        # edit this to have 5 elements
        # Ni Co Ti Zr Hf
        # has to match order given in snap coefficient files
        L.mass(1, 58.693)
        L.mass(2, 58.933)
        L.mass(3, 47.867)
        L.mass(4, 91.224)
        L.mass(5, 178.49)

        L.pair_style("snap", "")
        SNAP_IP = str(self.coefficient+""+self.parameter)
        L.pair_coeff("* *", SNAP_IP, "Ni Co Ti Zr Hf")

        # Setup standard output
        L.command("thermo_style	custom step temp pe pxx pyy pzz density")
        L.command("thermo 100")

        # Set up and run minimization
        L.command("dump 1 all custom 100 min_dump.cfg id type x y z")
        L.command("min_style cg")
        L.Command("fix 1 all box/relax aniso 0.0")
        L.command("minimize " + delE + " " + delF + " 5000 1000")
        L.command("unfix 1")
        L.command("minimize " + delE + " " + delF + " 5000 1000")
        L.undump(1)
        L.write_data("/home/winniebird/sfarrelly2024/test/after_min.data noceoff")

        # RUN
        L.run(100)

#RUN THAT SHIT
Test_Sim = Relax('./HEA_II.lmp', './HEA_var1.snapcoeff', './HEA_var1.snapparam')
Test_Sim.simulation(delE="0.0", delF="0.02", n_iter=10000)

# MPI.Finalize()