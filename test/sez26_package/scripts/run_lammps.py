import subprocess
import click
from lammps import PyLammps

@click.command()
@click.argument('project_path', type=click.Path(exists=True, dir_okay=True))
@click.argument('file_name')
def Run_PyLammps(project_path, file_name):
    # paths
    in_file_path = project_path + "/project/data/input/" + file_name
    log_file_path = project_path + "/project/logs/relax_log.log" 
    # Initialize PyLammps
    L = PyLammps()
    L.log(log_file_path)

    # Read and execute the LAMMPS input file
    L.file(in_file_path)

    print("LAMMPS simulation completed successfully.")

# running function
if __name__ == '__main__':
    Run_PyLammps()


