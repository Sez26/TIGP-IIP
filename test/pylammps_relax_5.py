import click

@click.command()
@click.argument('relax_file_path', type=click.Path(exists=True, dir_okay=True))
@click.argument('coeff_name')
@click.argument('param_name')
@click.argument('temp', type=click.FLOAT)
@click.argument('run_steps', type=click.INT)
def RelaxAnalysis(relax_file_path, coeff_name, param_name, temp, run_steps):
    in_file_path = relax_file_path + "output/in.relax.HEA"
    lmp_file_path = relax_file_path + "input/HEA_II.lmp"
# Redirect commands to a file
    with open(in_file_path, 'w') as f:
        f.write("# LAMMPS input script generated by PyLammps\n")
        f.write("# Initialise simulation\n")
        f.write("atom_style     atomic\n")
        f.write("units          metal\n")
        f.write(f"read_data     {lmp_file_path}\n") # can parameterise this

        f.write("# 5 elements of HEA: Ni Co Ti Zr Hf specorder\n")
        f.write("mass           1 58.693\n")
        f.write("mass           2 58.933\n")
        f.write("mass           3 47.867\n")
        f.write("mass           4 91.224\n")
        f.write("mass           5 178.49\n")

        f.write("# Reading snap potential files\n")
        f.write("pair_style     snap\n")
        coeff = relax_file_path + "/input/" + coeff_name
        param = relax_file_path + "/input/" + param_name
        f.write(f"pair_coeff     * * {coeff} {param} Ni Co Ti Zr Hf\n") # parameterise
        
        f.write("# Setup standard output\n")
        f.write("thermo_style   custom step temp pe pxx pyy pzz density\n")
        f.write("thermo         100\n")

        f.write("# Set up and run minimization\n")
        f.write(f"dump		    1 all custom 100 {relax_file_path}/output/min_dump.cfg id type x y z\n")
        f.write("min_style	    cg\n")
        f.write("fix		    1 all box/relax aniso 0.0\n")
        f.write("minimize	    0.0 0.02 5000 10000\n") # parameterise
        f.write("unfix		    1\n")
        f.write("minimize	    0.0 0.02 5000 10000\n") # parameterise
        f.write("undump		    1\n")
        f.write(f"write_data	{relax_file_path}/output/after_min.data nocoeff\n") # parameterise for file systems

        f.write("# Define some properties you are instrested in\n")
        f.write("variable	    lenx equal lx\n")
        f.write("variable	    leny equal ly\n")
        f.write("variable	    lenz equal lz\n")

        f.write("# computing more variables\n")
        f.write("compute		    sta all stress/atom NULL\n")
        f.write("compute		    vol_atom all voronoi/atom\n")
        f.write("variable	    va atom c_vol_atom[1]\n")
        f.write("variable	    sa_xx atom 1E-4*c_sta[1]/v_va\n")
        f.write("variable	    sa_yy atom 1E-4*c_sta[2]/v_va\n")
        f.write("variable	    sa_zz atom 1E-4*c_sta[3]/v_va\n")
        f.write("variable	    sa_xy atom 1E-4*c_sta[4]/v_va\n")
        f.write("variable	    sa_xz atom 1E-4*c_sta[5]/v_va\n")
        f.write("variable	    sa_yz atom 1E-4*c_sta[6]/v_va\n")
        f.write("variable	    sa_hydro atom (v_sa_xx+v_sa_yy+v_sa_zz)/3.0\n")
        f.write("variable	    sa_von atom sqrt(0.5*((v_sa_xx-v_sa_yy)^2+(v_sa_yy-v_sa_zz)^2+(v_sa_zz-v_sa_xx)^2)+3.0*((v_sa_xy)^2+(v_sa_xz)^2+(v_sa_yz)^2))\n")

        f.write("# Set up and run MD in NPT ensemble\n")
        f.write("timestep       0.001\n")
        f.write("neighbor       1.0 bin\n")
        f.write("neigh_modify   every 5 delay 0 check yes\n")
        f.write("reset_timestep 0\n")
        f.write(f"velocity	    all create {temp} 12345678\n") # parameterise
        f.write(f"dump		    1 all custom 1000 {relax_file_path}/output/md_npt_dump.cfg id type x y z v_sa_hydro v_sa_von\n")  # parameterise for file system
        f.write(f"fix		    2 all print 100 \"$(step) $(temp) $(pe) $(vol) $(density) $(pxx) $(pyy) $(pzz)\" file {relax_file_path}/output/Record_npt.txt\n") # parameterise for file system
        f.write(f"fix		    1 all npt temp {temp} {temp} 0.1 aniso 0 0 1.0\n")
        f.write("fix		    avg all ave/time 10 1000 100000 v_lenx v_leny v_lenz\n") # parameterise
        f.write(f"run		    {run_steps}\n") # parameterise
        f.write("undump		    1\n")
        f.write("unfix		    1\n")
        f.write("unfix		    2\n")

        f.write("variable	    newlx equal f_avg[1]\n")
        f.write("variable	    newly equal f_avg[2]\n")
        f.write("variable	    newlz equal f_avg[3]\n")
        f.write("change_box     all x final 0 ${newlx} y final 0 ${newly} z final 0 ${newlz} remap units box\n")
        f.write("unfix          avg\n")
        f.write(f"write_data     {relax_file_path}/output/after_relax.data nocoeff\n") # parameterise

        f.write("# Add a minimisation (perfect mesh analysis)\n")
        f.write(f"dump           1 all custom 100 {relax_file_path}/output/min_dump.cfg id type x y z v_sa_hydro v_sa_von\n") # parameterise for file system
        f.write("minimize       0.0 0.02 5000 10000\n") # parameterise
        f.write("undump         1")




