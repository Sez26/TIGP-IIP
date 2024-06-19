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
b2NiTi_atnum = b2NiTi.get_atomic_numbers()
print(b2NiTi_atnum) # Success