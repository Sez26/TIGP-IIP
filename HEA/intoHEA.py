## importing poscar from atomsk
## editing to turn from 2 element B2 structure into HEA

from ase import Atoms # importing atoms package
from ase.io import iread, write # for reading and writing files

# importing poscar
b2NiTi = iread('smallPos')

