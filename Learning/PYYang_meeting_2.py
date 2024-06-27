## adding dislocations to crystal lattice 

## remove excessing printing and Record_npt.txt outputs from LAMMPS code
## adding redefinition of perfect box dimensions (newlx etc)

## using ovito to visualise .cfg files
## histogram to see dumped variables (eg: von mises stress)


## after relax get simulation cell dimensions (newlx etc)
## average again cos not perfect to get room temperature lattice parameter

## define a new lattice with lattice parameter and dislocation

## function

#../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 2.878 Fe orient [100] [010] [001] -duplicate 20 20 20 -dislocation 0.5*box 0.5*box screw Y X 2.878 Fe_dis.lmp
                                            # 2.878 = redefined lattice parameter
                                                                                                                                    # Y = slip plane
                                                                                                                                    # X = perpindicular to slip plane


"""
ovito dislocation analysis to visualise dislocations
(reduce particle size to see dislations more clearly, and remove defect mesh)

Run LAMMPS with removed minimisation (very very quick)

Visualise make sure to move to final frame
Color coding to wrt von mises stress in order to make it gay :)


TO DO:
Do this shit with HEA
Edge dislocations?
Cos ideally want to work towards parameterisation of Zr swapping want to work on automating this process with bash codes
Might have to migrate the whole process over to slurm as moving between local and slurm ain't good for automation
"""

"""
Class 2.5
Applying compression

orientation of crystal is important
../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 2.878 Fe orient [100] [010] [001] -duplicate 20 10 10
                                                                strain is applied to first (X)
                                                                        Other surfaces are orthogonal
../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 2.878 Fe orient [110] [1-10] [001] -duplicate 14 7 10
                                                                        this is '-1' not dash 1
../../atomsk_b0.13.1_Linux-amd64/atomsk --create bcc 2.878 Fe orient [111] [1-10] [11-2] -duplicate 24 7 4

duplicated with different values to keep dimensions (could ask more about this but also could just trust)
"""