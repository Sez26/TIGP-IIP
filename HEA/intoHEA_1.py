## importing poscar from atomsk
## editing to turn from 2 element B2 structure into 5 element HEA

# PLAN
# 1) Split coordinates into sublattice A and B
# 2) Assign tags to the atoms in each sublattice
# 3) write def functions in order to change element assignment
# 4) randomly allocate distribution from each sublattice to be reassigned
#######################################################
# 5) replicating model I from paper (disordered)
# 6) write swapping def function to swap a percentage of Zr in sub lattice A
# 7) replicating model III from paper

from ase import Atoms # importing atoms package
from ase.io import vasp # for reading and writing files
from ase.visualize import view
import numpy as np
import random

# importing poscar
# specifying path to file
PoscarFile = '/home/sez26/TIGP-IIP/HEA/smallPos'
b2NiTi = vasp.read_vasp(PoscarFile) # vasp.read_vasp function reads POSCAR files as Atoms type

# 1) Split coordinates into sublattice A and B
b2NiTi_atNum = b2NiTi.get_atomic_numbers()

# logical arrays
b2NiTi_A = b2NiTi_atNum == 28
b2NiTi_B = b2NiTi_atNum == 22 # not necessarily needed because only 2 sublattices

b2NiTi_Aidx = np.where(b2NiTi_A == True)[0] # finding the indicies, [0] to change from tuple type O/P into np.array
b2NiTi_Bidx = np.where(b2NiTi_B == True)[0]

print('length of sublattice index arrays: ', len(b2NiTi_Aidx))

# 2) Assigning tags
# sublattice A atoms are tagged with 1, sublattice B tagged 0
subLatTags = b2NiTi_A * 1 # pretty sure this line is unneccessary
# print(subLatTags.shape)
# print(b2NiTi.get_tags().shape)
b2NiTi.set_tags(subLatTags)

# 3) Writing element assignment def functions
def ChangeElement(atoms, idx, desChemSym):
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
numA = sum(b2NiTi_A)
print('total atoms:', len(b2NiTi_atNum))
print('numA:',numA)
numB = sum(b2NiTi_B)
print('numB: ',numB)
# for sublattice A, Co and Ni are in equal proportion
numSel = int(numA/2)
print('num Co/Ni selected: ', numSel)
SelAidx = np.random.choice(b2NiTi_Aidx, size = numSel, replace=False)

# Call replacement function
SubLatA_HEA = ChangeElement(b2NiTi, SelAidx, HEA_ChemSym[0])
# view(SubLatA_HEA)

CoIdx = np.where(SubLatA_HEA.get_atomic_numbers() == HEA_AtNum[0])[0]
NiIdx = np.where(SubLatA_HEA.get_atomic_numbers() == HEA_AtNum[1])[0]
print('PreSubLat2 num Co: ', len(CoIdx))
print('PreSubLat2 num Ni: ', len(NiIdx))

# Similar for sublattice B
# for sublattice B, Hf, Ti, and Zr are in equal proportion
numSel = int(numB/3)
print('num Hf/Ti/Zr selected: ', numSel)
SelBidx = np.random.choice(b2NiTi_Bidx, size = (2,numSel), replace=False)
print(len(SelBidx[0,:]))

# Call replacement function
SubLatBHf_HEA = ChangeElement(SubLatA_HEA, SelBidx[0,:], HEA_ChemSym[2])
SubLatBZr_HEA = ChangeElement(SubLatBHf_HEA, SelBidx[1,:], HEA_ChemSym[4])

CoIdx = np.where(SubLatBZr_HEA.get_atomic_numbers() == HEA_AtNum[0])[0]
NiIdx = np.where(SubLatBZr_HEA.get_atomic_numbers() == HEA_AtNum[1])[0]
print('PostSubLat2 num Co: ', len(CoIdx))
print('PostSubLat2 num Ni: ', len(NiIdx))
HfIdx = np.where(SubLatBZr_HEA.get_atomic_numbers() == HEA_AtNum[2])[0]
TiIdx = np.where(SubLatBZr_HEA.get_atomic_numbers() == HEA_AtNum[3])[0]
ZrIdx = np.where(SubLatBZr_HEA.get_atomic_numbers() == HEA_AtNum[4])[0]
print('Postnum Hf: ', len(HfIdx))
print('Postnum Ti: ', len(TiIdx))
print('Postnum Zr: ', len(ZrIdx))

# THIS IS RIGHT!!!
# What changes between here and the end of my code????

HEA_ordered = SubLatBZr_HEA

CoIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[0])[0]
NiIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[1])[0]
print('PostSubLat2 num Co: ', len(CoIdx))
print('PostSubLat2 num Ni: ', len(NiIdx))

# view(HEA_ordered)

############################################################

# 5) making disordered lattice

# random selection
# print(len(b2NiTi.get_tags()))
# print(b2NiTi.get_tags().shape)
numSel = int(len(b2NiTi.get_tags())/6) # this be rounding!
Selrand1 = np.random.choice(np.arange(0,len(b2NiTi.get_tags())), size = (3,numSel), replace=False)
# print(Selrand1)
numSel = int(len(b2NiTi.get_tags())/4)
Selrand2 = np.random.choice(np.arange(0,len(b2NiTi.get_tags())), size = (2,numSel), replace=False)#
# print(Selrand2)

# Call replacement function
HEA_Co_Ni = b2NiTi
for i in [0,1]:
    HEA_Co_Ni_new = ChangeElement(HEA_Co_Ni, Selrand2[i,:], HEA_ChemSym[i])
    HEA_Co_Ni = HEA_Co_Ni_new

HEA_Hf_Ti_Zr = HEA_Co_Ni
for i in [0,1,2]:
    HEA_Hf_Ti_Zr_new = ChangeElement(HEA_Hf_Ti_Zr, Selrand1[i,:], HEA_ChemSym[i+2])
    HEA_Hf_Ti_Zr = HEA_Hf_Ti_Zr_new

HEA_disordered = HEA_Hf_Ti_Zr
# view(HEA_disordered)

# 6) Swap Zr atoms

# find indices of Zr atoms (list comprehension)
CoIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[0])[0]
NiIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[1])[0]
HfIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[2])[0]
TiIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[3])[0]
ZrIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[4])[0]
print('num Co: ', len(CoIdx))
print('num Ni: ', len(NiIdx))
print('num Hf: ', len(HfIdx))
print('num Ti: ', len(TiIdx))
print('num Zr: ', len(ZrIdx)) # I don't understand how this is bigger than 576