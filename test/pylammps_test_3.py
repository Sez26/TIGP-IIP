from lammps import PyLammps

L = PyLammps()

# Initialize LAMMPS and set up simulation box
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

# Setup thermodynamics and timestep
L.timestep(0.001)
L.thermo_style("custom step temp pe vol density pxx pyy pzz")
L.thermo(100)

# Set velocity
L.velocity("all create 300.0 12345678")

# Define NPT ensemble
L.fix(1, "all", "npt", "temp", 300, 300, 0.1, "aniso", 0, 0, 1.0)

# Set up fix print to output desired properties
L.fix(2, "all", "print", 100, "$(step) $(temp) $(pe) $(vol) $(density) $(pxx) $(pyy) $(pzz)", "file", "Record_npt.txt")

# Define dump command
L.command("dump 1 all custom 1000 md_npt_dump.cfg id type x y z v_sa_hydro v_sa_von")

# Ensure fix ave/time has a compatible output frequency
L.command("fix avg all ave/time 10 1000 10000 v_lenx v_leny v_lenz")

# RUN
L.run(100000)

# Cleanup
L.undump(1)
L.unfix(1)
L.unfix(2)
L.unfix("avg")