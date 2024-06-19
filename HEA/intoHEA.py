## importing poscar from atomsk
## editing to turn from 2 element B2 structure into HEA

from ase import Atoms # importing atoms package
from ase.io import vasp # for reading and writing files
from ase.visualize import view

# importing poscar
# specifying path to file
PoscarFile = '/home/sez26/TIGP-IIP/HEA/smallPos'
b2NiTi = vasp.read_vasp(PoscarFile) # vasp.read_vasp function reads POSCAR files as Atoms type

# print(type(b2NiTi)); # generator
# view(b2NiTi) # Success

# trying atoms functions
# b2NiTi_atnum = b2NiTi.get_atomic_numbers()
# print(b2NiTi_atnum) # Success

# PLAN
# 1) Split coordinates into sublattice A and B
# 2) Assign tags to the atoms in each sublattice
# 3) write def functions in order to change element assignment
# 4) randomly allocate distribution from each sublattice to be reassigned

# 1) Split coordinates into sublattice A and B
# d = 3.128 A
# offset = 1.564 A
b2NiTi_pos = b2NiTi.get_positions()
# print(type(b2NiTi_pos)) # np array
# print(b2NiTi_pos.shape) # 1 row per atom, 3 columns of x,y,z

# logical arrays
b2NiTi_posA = (b2NiTi_pos[:,1] % 3.128)==0 # dependent on symmetrical square lattice (b2 specific so pretty dodge)
# b2NiTi_posB = (b2NiTi_pos % 3.128)==1.564

# 2) Assigning tags
# sublattice A atoms are tagged with 1, sublattice B tagged 0
subLatTags = b2NiTi_posA * 1
# print(subLatTags.shape)
# print(b2NiTi.get_tags().shape)
b2NiTi.set_tags(subLatTags)

# 3) Writing element assignment def functions
 