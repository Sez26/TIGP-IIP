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

# trying atoms functions
view(b2NiTi) # Success