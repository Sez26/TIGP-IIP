import subprocess
import click
from lammps import PyLammps

@click.command()
@click.argument('project_path', type=click.Path(exists=True, dir_okay=True))
@click.argument('file_name')
@click.argument('analysis_type')
def Run_PyLammps(project_path, file_name, analysis_type):
    # paths
    in_file_path = project_path + "/project/data/input/" + file_name
    log_file_path = project_path + f"/project/logs/{analysis_type}_log.log" 
    # Initialize PyLammps
    L = PyLammps()
    L.log(log_file_path)

    # Read and execute the LAMMPS input file
    L.file(in_file_path)

    print("LAMMPS simulation completed successfully.")

# running function
if __name__ == '__main__':
    Run_PyLammps()


