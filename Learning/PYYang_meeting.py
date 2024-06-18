## add atomsk to environment

## tar  -xvf ../atomsk
## add jupyter notebooks


##../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 2.866 Fe orient [100] [010] [001] -duplicate 15 15 15 lmp

## can be exported as lmp or pos file types

## atomsk can only do B2 with two element types
## in post processing the export file has to be edited to swap certain atoms in the lattice with others in order to turn into a HEA
## pos (POSCAR) file time makes this easier as atom positions are packed by element when exporting

## LAMMPS
## variable varname1 equals defvar1 # equals = scalar value, atom = atomic vectors

# time step given in ps
# neighbour defining far field cut off where molecules 'far enough' away are not effected by studied molecule

# velocity ~~ temperature (300K)

# dump to o/p stuff

# fix avg all ave/time 5 1000 20000 c_termo_temp v_avg_lxyz 
# for heated simulation only sample averages from the last 5000 timesteps after equlm has been reached


#### TO DO

# write code to edit NiTi B2 lattice into HEA alloy
# set up jupyter notebooks
# Adapt lammps code to run HEA job (get estimate for thermal expansion (strain as a function of temperature increase))

# generalise HEA lattice building code
