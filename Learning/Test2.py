## testing building unique lattice structure (mimic nitrol) and saving lattice coordinates

# import ase # think this line is obsolete
from ase import * # import all of ase
from ase.visualize import view # import visualisation stuff to get view function to work
from ase.lattice.cubic import BodyCenteredCubic # import lattice stuff

# define some test atoms (copied from MD_example.py)
size = 3
# Set up a nitinol crystal (B19' strucuture!)
atoms = BodyCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                          symbol='Ni', 'Ti'
                          size=(size, size, size),
                          pbc=True)


# visualised in ase gui using view function
view(atoms)
## success!