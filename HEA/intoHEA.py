## importing poscar from atomsk
## editing to turn from 2 element B2 structure into 5 element HEA

from ase import Atoms # importing atoms package
from ase.io import vasp # for reading and writing files
from ase.visualize import view
import numpy as np

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
b2NiTi_A = (b2NiTi_pos % 3.128) == 0 # dependent on symmetrical square lattice (b2 specific so pretty dodge)
b2NiTi_B = (b2NiTi_pos % 3.128)==1.564 # not necessarily needed because only 2 sublattices
# print(b2NiTi_A.shape)
# print(b2NiTi_A)

# find row indexes of sublattices
b2NiTi_A = np.all(b2NiTi_A, axis = 1) # testing that spacing interval is true for all x,y and z directions + combination into column vector
b2NiTi_B = np.all(b2NiTi_B, axis = 1)
# print(b2NiTi_A.shape)
# print(b2NiTi_A)

b2NiTi_Aidx = np.where(b2NiTi_A == True)[0] # finding the indicies, [0] to change from tuple type O/P into np.array
b2NiTi_Bidx = np.where(b2NiTi_B == True)[0]

# print(b2NiTi_Aidx)
# print(type(b2NiTi_Aidx))

# 2) Assigning tags
# sublattice A atoms are tagged with 1, sublattice B tagged 0
subLatTags = b2NiTi_A * 1
# print(subLatTags.shape)
# print(b2NiTi.get_tags().shape)
b2NiTi.set_tags(subLatTags)

# 3) Writing element assignment def functions
def ChangeElement(atoms, desAtNum, desAtMass, desChemSym):
    atoms.set_atomic_numbers(desAtNum)
    atoms.set_masses(desAtMass)
    atoms.set_chemical_symbols(desChemSym)
    return atoms

# setting up HEA 5 element parameters (this could probably be called from a library somewhere)
HEA_AtNum = [27, 28, 72, 22, 40]
HEA_AtMass = [58.933, 58.963, 178.49, 47.867, 91.224]
HEA_ChemSym = ['Co', 'Ni', 'Hf', 'Ti', 'Zr']

# 4) Random assignment
# From literature Co, Ni occupy sublattice A and Hf, Ti and Zr occupy sublattice B
# in unedited state the B2 structure already has a Ni sublattice A and a Ti sublattice B
# therefore additional elements only need be added.

# find row indexes of sublattices

