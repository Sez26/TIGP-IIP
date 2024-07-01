"""
Generating a lattice using ASE functions (rather than atomsk to keep it all in one script) THIS DIDN'T WORK LOL
Editing to turn it into a 5 element HEA (maybe the lattice could orginally be generated as a 5 element HEA)
Making a larger lattice model to test the validity of the SNAP potentials on it
"""
from ase import Atoms # importing atoms package
from ase.io import vasp # for reading and writing vasp POSCAR input files
from ase.visualize import view
import numpy as np
import random
from ase.io import lammpsdata # for exporting (writing) to .lmp file
# from ase.lattice.cubic import FaceCenteredCubicFactory

# class NiTiFactory(FaceCenteredCubicFactory):
#     """Making a NiTi BCC (B2) lattice"""
#     bravais_basis = [[0, 0, 0], [0.5, 0.5, 0.5]]
#     element_basis = (0, 1)
#     # directions = [[100], [010], [001]]

# b2NiTi = NiTi = NiTiFactory()
# view(b2NiTi)

# Working Directory
wDir = '/home/sez26/TIGP-IIP/HEA_dislocation/Screw/Var2/'

# importing poscar
# specifying path to file
PoscarFile = wDir + 'POSCAR'
b2NiTi = vasp.read_vasp(PoscarFile) # vasp.read_vasp function reads POSCAR files as Atoms type

# 1) Split coordinates into sublattice A and B
b2NiTi_atNum = b2NiTi.get_atomic_numbers()

# logical arrays
b2NiTi_A = b2NiTi_atNum == 28
b2NiTi_B = b2NiTi_atNum == 22 # not necessarily needed because only 2 sublattices

b2NiTi_Aidx = np.where(b2NiTi_A == True)[0] # finding the indicies, [0] to change from tuple type O/P into np.array
b2NiTi_Bidx = np.where(b2NiTi_B == True)[0]

print('Length of sublattice index arrays: ', len(b2NiTi_Aidx))

# 2) Assigning tags
# sublattice A atoms are tagged with 1, sublattice B tagged 0
subLatTags = b2NiTi_A * 1 # pretty sure this line is unneccessary
b2NiTi.set_tags(subLatTags)

# 3) Writing element assignment def functions
def ChangeElement(atoms, idx, desChemSym):
    # loop to assign new values to chemical symbol (cos string data type be tricky)
    desChemSymList = atoms.get_chemical_symbols() # originally setting as old chemical symbols
    # Assign the new value to selected elements in the list
    for i_sym in idx:
        desChemSymList[i_sym] = desChemSym
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
total_atoms = int(len(b2NiTi.get_tags()))

# for sublattice A, Co and Ni are in equal proportion
numSel = total_atoms//4

SelAidx = np.random.choice(b2NiTi_Aidx, size = numSel, replace=False)

# Call replacement function
SubLatA_HEA = ChangeElement(b2NiTi, SelAidx, HEA_ChemSym[0])

# Similar for sublattice B
# for sublattice B, Hf, Ti, and Zr are in equal proportion
numSel = total_atoms//6

SelBidx = np.random.choice(b2NiTi_Bidx, size = (2,numSel), replace=False)

# Call replacement function
SubLatBHf_HEA = ChangeElement(SubLatA_HEA, SelBidx[0,:], HEA_ChemSym[2])
SubLatBZr_HEA = ChangeElement(SubLatBHf_HEA, SelBidx[1,:], HEA_ChemSym[4])

HEA_ordered = SubLatBZr_HEA.copy() # copy function for atoms object not equate

# view(HEA_ordered)

############################################################

# 5) making disordered lattice

numSelArr = [total_atoms//4, total_atoms//4, total_atoms//6, total_atoms//6, total_atoms//6]
# SelRand = np.zeros(max(numSelArr), len(numSelArr))
AtomIdx = np.arange(0,len(b2NiTi.get_tags()))
HEA_dis = b2NiTi
for i in range(len(numSelArr)):
    SelRandi = np.random.choice(AtomIdx, size = numSelArr[i], replace = False)
    # # Add SelRand to Array
    # Redefine AtomIdx
    AtomIdx = np.setdiff1d(AtomIdx, SelRandi)
    HEA_dis_new = ChangeElement(HEA_dis, SelRandi, HEA_ChemSym[i])
    HEA_dis = HEA_dis_new.copy()

HEA_disordered = HEA_dis.copy()

# view(HEA_disordered)

# 6) Swap Zr atoms

# find indices of Zr atoms (list comprehension)
ZrIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[4])[0]
ZrIdxInt = ZrIdx.astype('int')
CoIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[0])[0]
CoIdxInt = CoIdx.astype('int')
NiIdx = np.where(HEA_ordered.get_atomic_numbers() == HEA_AtNum[1])[0]
NiIdxInt = NiIdx.astype('int')

# Select % of Zr atoms to swap
percZrSwap = 25
numSel = int((percZrSwap/100)*len(ZrIdx))

ZrSwap = np.zeros([numSel//2-1, 2])
ZrSwap = ZrSwap.astype('int')
ZrSwap[:,0] = np.random.choice(CoIdxInt, size = (numSel//2-1), replace=False)
ZrSwap[:,1] = np.random.choice(NiIdxInt, size = (numSel//2-1), replace=False)

# Select corresponding % of Co/Ni atoms to swap
CoNiSwap = np.random.choice(ZrIdxInt, size = numSel, replace=False)

Working_HEA = HEA_ordered.copy()
HEA_III_CoSwap = ChangeElement(Working_HEA, CoNiSwap[0:len(CoNiSwap)//2-1], HEA_ChemSym[0])
HEA_III_NiSwap = ChangeElement(HEA_III_CoSwap, CoNiSwap[len(CoNiSwap)//2:-1], HEA_ChemSym[1])
HEA_III_ZrSwap1 = ChangeElement(HEA_III_NiSwap, ZrSwap[:,0], HEA_ChemSym[4])
HEA_III_ZrSwap2 = ChangeElement(HEA_III_ZrSwap1, ZrSwap[:,1], HEA_ChemSym[4])

HEA_partially_ordered = HEA_III_ZrSwap2.copy()

# view(HEA_partially_ordered)

# 8) write to .lmp file

# Debugging

# Function to check proportions
def PropCheck (atoms, DesNum, DesAtNum):
    TotNum = len(atoms.get_tags())
    Idx = np.where(atoms.get_atomic_numbers() == DesAtNum)[0]
    ActNum = len(Idx)
    if DesNum%ActNum==0:
        # print('Proportion Correct')
        prop_check = 1
    elif ActNum > DesNum and ActNum%DesNum < 2:
        # print('Proportion Correct')
        prop_check = 1
    elif DesNum > ActNum and DesNum%ActNum <2:
        # print('Proportion Correct')
        prop_check = 1
    else:
        print('Proportion Incorrect')
        prop_check = 0
    return prop_check

# Function to check success of swapping (whether there is Zr present in lattice A)
def LatticeCheck(atoms, DesAtNum):
    SearchAtoms = atoms.get_atomic_numbers() == DesAtNum
    GetLatA = atoms.get_tags()==1
    GetLatB = atoms.get_tags()==0
    # check if desired element is in lattice A and B
    if sum(GetLatA*SearchAtoms)!=0:
        print('Elements with atomic number ', DesAtNum, ' is present in lattice A.')
        print('Number of desired element atoms in lattice A: ', sum(GetLatA*SearchAtoms))
    if sum(GetLatB*SearchAtoms)!=0:
        print('Elements with atomic number ', DesAtNum, ' is present in lattice B.')
        print('Number of desired element atoms in lattice B: ', sum(GetLatB*SearchAtoms))
    else:
        print('Error: Desired element not found')

# check all lattices
# Desired values
CoDes = total_atoms//4
NiDes = CoDes
HfDes = total_atoms//6
TiDes = HfDes
ZrDes = HfDes
DesNum = [CoDes, NiDes, HfDes, TiDes, ZrDes]

print('Total Atoms = ', total_atoms, ' CoDes = ', CoDes, ' HfDes = ', HfDes)

print('Checking HEA_ordered')
HEA_II_prop_check = np.zeros([len(HEA_AtNum),1])
for i in range(len(HEA_AtNum)):
    # call checking function
    HEA_II_prop_check[i] = PropCheck(HEA_ordered, DesNum[i], HEA_AtNum[i])

# ORDERED PASS

print('Checking HEA_disordered')
HEA_I_prop_check = np.zeros([len(HEA_AtNum),1])
for i in range(len(HEA_AtNum)):
    # call checking function
    HEA_I_prop_check[i] = PropCheck(HEA_disordered, DesNum[i], HEA_AtNum[i])

# DISORDERED PASS

print('Checking HEA_partially_ordered')
HEA_III_prop_check = np.zeros([len(HEA_AtNum),1])
for i in range(len(HEA_AtNum)):
    # call checking function
    HEA_III_prop_check[i] = PropCheck(HEA_partially_ordered, DesNum[i], HEA_AtNum[i])

# PARTIALLY ORDERED PASSED

# Check swapping
print('Checking swapping in partially ordered')
LatticeCheck(HEA_partially_ordered, HEA_AtNum[4])
LatticeCheck(HEA_partially_ordered, HEA_AtNum[0])
LatticeCheck(HEA_partially_ordered, HEA_AtNum[1])

# Check swapping
# print('Checking swapping in ordered')
# LatticeCheck(HEA_ordered, HEA_AtNum[4])
# LatticeCheck(HEA_ordered, HEA_AtNum[0])
# LatticeCheck(HEA_ordered, HEA_AtNum[1])

# Check swapping
print('Checking Ti and Hf in partially ordered')
LatticeCheck(HEA_partially_ordered, HEA_AtNum[2])
LatticeCheck(HEA_partially_ordered, HEA_AtNum[3])

# Checking chemical symbol order
# gives the metals in alphabetical order
# Co, Hf, Ni, Ti, Zr

# MAKE CONSISTENT WITH SNAP PAIR COEFFICIENTS
# Ni, Co, Ti, Zr, Hf
spec_order = ['Ni', 'Co', 'Ti', 'Zr', 'Hf']

# Conditional Export
if sum(HEA_I_prop_check) == len(HEA_AtNum):
    print('All tests passed for HEA_I')
    lammpsdata.write_lammps_data(wDir+'HEA_I.lmp', HEA_disordered, spec_order)
    # write('./HEA/HEA_I.lmp', HEA_disordered, format = 'lammps-data',specorder = spec_order)
else:
    print('Error: HEA_I Element composition incorrect. Please check code.')

if sum(HEA_II_prop_check) == len(HEA_AtNum):
    print('All tests passed for HEA_II')
    lammpsdata.write_lammps_data(wDir+'HEA_II.lmp', HEA_ordered, spec_order)
    # write('./HEA/HEA_II.lmp', HEA_ordered, format = 'lammps-data',specorder = spec_order)
else:
    print('Error: HEA_II Element composition incorrect Please check code.')

if sum(HEA_III_prop_check) == len(HEA_AtNum):
    print('All tests passed for HEA_III')
    lammpsdata.write_lammps_data(wDir+'HEA_III.lmp', HEA_partially_ordered, spec_order)
    # write('./HEA/HEA_III.lmp', HEA_partially_ordered, format = 'lammps-data',specorder = spec_order)
else:
    print('Error: HEA_III Element composition incorrect. Please check code.')