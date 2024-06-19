## importing poscar from atomsk
## editing to turn from 2 element B2 structure into 5 element HEA

from ase import Atoms # importing atoms package
from ase.io import vasp # for reading and writing files
from ase.visualize import view
import numpy as np
import random

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
# print(type(b2NiTi_Aidx[0]))

# 2) Assigning tags
# sublattice A atoms are tagged with 1, sublattice B tagged 0
subLatTags = b2NiTi_A * 1 # pretty sure this line is unneccessary
# print(subLatTags.shape)
# print(b2NiTi.get_tags().shape)
b2NiTi.set_tags(subLatTags)

# 3) Writing element assignment def functions
def ChangeElement(atoms, idx, desChemSym): # desAtNum, desAtMass, desChemSym):
    # ONLY NEED TO CHANGE ONE OF THESE VALUES AND THE OTHERS ALL CHANGE

    # creation of input arrays
    # i = np.zeros(len(atoms.get_tags()))
    # i[idx] = True

    # atoms.set_atomic_numbers(desAtNum*i)
    # atoms.set_masses(desAtMass*i)

    # loop to assign new values to chemical symbol (cos string data type be tricky)
    desChemSymList = atoms.get_chemical_symbols() # originally setting as old chemical symbols
    # print(desChemSymList)
    # Assign the new value to selected elements in the list
    for i_sym in idx:
        desChemSymList[i_sym] = desChemSym
    # print(desChemSymList)
    atoms.set_chemical_symbols(desChemSymList)
    return atoms

# setting up HEA 5 element parameters (this could probably be called from a library somewhere)
HEA_AtNum = [27, 28, 72, 22, 40]
HEA_AtMass = [58.933, 58.963, 178.49, 47.867, 91.224]
HEA_ChemSym = ['Co', 'Ni', 'Hf', 'Ti', 'Zr']

# 4) Random assignment
# From literature Co, Ni occupy sublattice A and Hf, Ti and Zr occupy sublattice B
# in unedited state the B2 structure already has a Ni sublattice A and a Ti sublattice B
# therefore additional elements only need be added.

# finding total number of atoms in each lattice
numA = len(b2NiTi_Aidx)
numB = len(b2NiTi_Bidx)

# for sublattice A, Co and Ni are in equal proportion
numSel = int(numA/2)
SelAidx = np.random.choice(b2NiTi_Aidx, size = numSel, replace=False)

# Call replacement function
SubLatA_HEA = ChangeElement(b2NiTi, SelAidx, HEA_ChemSym[0]) # HEA_AtNum[0], HEA_AtMass[0], HEA_ChemSym[0])
# view(SubLatA_HEA)

# Similar for sublattice B
# for sublattice B, Hf, Ti, and Zr are in equal proportion
numSel = int(numB/3)
SelBidx = np.random.choice(b2NiTi_Bidx, size = (2,numSel), replace=False)
# print(SelBidx.shape)
# print(SelBidx[0,:])

# Call replacement function
SubLatBHf_HEA = ChangeElement(SubLatA_HEA, SelBidx[0,:], HEA_ChemSym[2])
SubLatBZr_HEA = ChangeElement(SubLatBHf_HEA, SelBidx[1,:], HEA_ChemSym[4])

HEA_ordered = SubLatBZr_HEA

view(HEA_ordered)