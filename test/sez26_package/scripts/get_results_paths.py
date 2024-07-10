import os
import glob
import click

@click.command()
@click.argument('project_directory', type=click.Path(exists=True, dir_okay=True))
@click.argument('searcher')
def get_results_paths(project_directory, searcher):
    # Use glob to find all .snap files in the specified directory
    # click.echo(directory +'/*.snapcoeff')
    results_files = glob.glob(project_directory +'/**/project/data/output/' + searcher, recursive=True)

    # Checks
    if len(results_files)==0:
        click.echo("Results files matching your search criteria (searcher) not found in project directory. Please rectify.")
    else:
        click.echo(results_files)
        # this be dodgy for some reason but idk why

# running function
if __name__ == '__main__':
    results_files = get_results_paths()
