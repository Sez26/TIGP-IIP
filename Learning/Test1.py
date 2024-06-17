## testing opening ase gui from python code.
import ase
from ase import * # import all of ase
from ase.visualize import view # import visualisation stuff to get view function to work
from ase.lattice.cubic import FaceCenteredCubic # import lattice stuff

# define some test atoms (copied from MD_example.py)
size = 3
# Set up a crystal
atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                          symbol='Cu',
                          size=(size, size, size),
                          pbc=True)


# visualised in ase gui using view function
view(atoms)
## success!