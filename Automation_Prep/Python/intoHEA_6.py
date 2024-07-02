"""
Using click to turn intoHEA script into something I can run from bash with input arguements!
ie: commandline tool
LETS GOOOOO
"""

import click

"""
Establishing options and arguments
args:       working directory
            (could work towards: element composition input)

options:    save file name (default of HEA_I, HEA_II etc...)
            save all function (as we have kind of established that we don't need model 1 could just do away with those parts of the script altogether)

"""

# importy thingies
from ase import Atoms # importing atoms package
from ase.io import vasp # for reading and writing vasp POSCAR input files
from ase.visualize import view
import numpy as np
import random
from ase.io import lammpsdata # for exporting (writing) to .lmp file

# Change element function external to command
def ChangeElement(atoms, idx, desChemSym):
    # loop to assign new values to chemical symbol (cos string data type be tricky)
    desChemSymList = atoms.get_chemical_symbols() # originally setting as old chemical symbols
    # Assign the new value to selected elements in the list
    for i_sym in idx:
        desChemSymList[i_sym] = desChemSym
    atoms.set_chemical_symbols(desChemSymList)
    return atoms

# introducing command
@click.command()
@click.argument('wdir', type=click.Path(exists=True, dir_okay=True))
# argument names not case sensistive!
def intoHEA_6(wdir):
    # intoducing help text
    """ intoHEA_6.py is a function which converts a b2 crystal lattice into a ordered HEA.
    It requires an input of the path (WDIR) to the directory where a POSCAR file has been saved.
    Created by SF 2024 as part of TIGP-IIP project.
    """
    # importing poscar
    # specifying path to file
    PoscarFile = wdir + 'POSCAR'
    b2NiTi = vasp.read_vasp(PoscarFile) # vasp.read_vasp function reads POSCAR files as Atoms type
    click.echo('POSCAR file loaded.')
    # 1) Split coordinates into sublattice A and B
    b2NiTi_atNum = b2NiTi.get_atomic_numbers()

    # logical arrays
    b2NiTi_A = b2NiTi_atNum == 28 # Ni
    b2NiTi_B = b2NiTi_atNum == 22 # Ti # not necessarily needed because only 2 sublattices

    b2NiTi_Aidx = np.where(b2NiTi_A == True)[0] # finding the indicies, [0] to change from tuple type O/P into np.array
    b2NiTi_Bidx = np.where(b2NiTi_B == True)[0]
    
    total_atoms = int(len(b2NiTi.get_tags()))
    numAatoms = len(b2NiTi_Aidx)
    numBatoms = len(b2NiTi_Bidx)
    click.echo('Sublattices identified.')

    # setting up HEA 5 element parameters (this could probably be called from a library somewhere/put into a class system)
    HEA_AtNum = [27, 28, 72, 22, 40]
    HEA_AtMass = [58.933, 58.963, 178.49, 47.867, 91.224]
    HEA_ChemSym = ['Co', 'Ni', 'Hf', 'Ti', 'Zr']

    click.echo('Adding HEA elements.')
    numSel = numAatoms//2

    SelAidx = np.random.choice(b2NiTi_Aidx, size = numSel, replace=False)

    # Call replacement function
    SubLatA_HEA = ChangeElement(b2NiTi, SelAidx, HEA_ChemSym[0])

    # Similar for sublattice B
    # for sublattice B, Hf, Ti, and Zr are in equal proportion
    numSel = numBatoms//3

    SelBidx = np.random.choice(b2NiTi_Bidx, size = (2,numSel), replace=False)

    # Call replacement function
    SubLatBHf_HEA = ChangeElement(SubLatA_HEA, SelBidx[0,:], HEA_ChemSym[2])
    SubLatBZr_HEA = ChangeElement(SubLatBHf_HEA, SelBidx[1,:], HEA_ChemSym[4])

    HEA_ordered = SubLatBZr_HEA.copy() # copy function for atoms object not equate
    
    click.echo('Saving file.')
    spec_order = ['Ni', 'Co', 'Ti', 'Zr', 'Hf']
    save_file_name = wdir + 'HEA_II.lmp'
    lammpsdata.write_lammps_data(save_file_name, HEA_ordered, specorder = spec_order)

# running function
if __name__ == '__main__':
    intoHEA_6()