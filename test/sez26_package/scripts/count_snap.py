import os
import glob
import click

@click.command()
@click.argument('snap_directory', type=click.Path(exists=True, dir_okay=True))
def count_snap_files(snap_directory):
    # Use glob to find all .snap files in the specified directory
    # click.echo(snap_directory +'/*.snapcoeff')
    snapcoeff_files = glob.glob(snap_directory +'/*.snapcoeff', recursive=True)
    snapparam_files = glob.glob(snap_directory + '/*.snapparam', recursive=True)
    
    # click.echo(len(snapcoeff_files))

    # Count the number of .snap files
    count_coeff = len(snapcoeff_files)
    count_param = len(snapparam_files)
    
    # click.echo(count_param)

    # Checks
    if count_coeff==0 or count_param==0:
        click.echo("There are missing snapparam and snapcoeff files in SNAP potentials directory (snap_dir). Please rectify.")
    if count_coeff!=count_param:
        click.echo("Number of snapparam files != snapcoeff files in SNAP potentials directory (snap_dir). Please rectify.")
    else:
        click.echo(count_coeff)
        # this be dodgy for some reason but idk why

# running function
if __name__ == '__main__':
    num_snap = count_snap_files()
