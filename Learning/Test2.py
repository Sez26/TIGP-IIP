## testing building unique lattice structure (mimic nitrol) and saving lattice coordinates

# import ase # think this line is obsolete
from ase import * # import all of ase
from ase.visualize import view # import visualisation stuff to get view function to work
from ase.lattice.cubic import SimpleCubicFactory # import lattice stuff, factories to make multi element lattices

# define a class for nitinol
class NitinolFactory(SimpleCubicFactory):
    # a factory for making nitinol lattices


# Set up a nitinol crystal (B19' strucuture!)
atoms = BodcdyCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                          symbol='Ni', 'Ti'
                          size=(size, size, size),
                          pbc=True)


# visualised in ase gui using view function
view(atoms)
## success!