"""
making a file system for a HEA LAMMPS project
this code is mostly copied from chatGPT

adapted to include click
"""

import os
from pathlib import Path
import click

directory_structure = {
    "project": {
        # "scripts": [],
        "data": {
            "input": [],
            "output": []
        },
        "config": [],
        "logs": [],
        # "environment": ["requirements.txt", "environment.yml"],
        # "README.md": None
    }
}

def create_structure(base_path, structure):
    for name, sub_structure in structure.items():
        current_path = base_path / name
        if isinstance(sub_structure, dict):
            # Create directory if it doesn't exist
            if not current_path.exists():
                current_path.mkdir()
            # Recurse into subdirectory
            create_structure(current_path, sub_structure)
        elif isinstance(sub_structure, list):
            # Create directory if it doesn't exist
            if not current_path.exists():
                current_path.mkdir()
            # Create files inside the directory
            for file_name in sub_structure:
                file_path = current_path / file_name
                if not file_path.exists():
                    file_path.touch()
        elif sub_structure is None:
            # Create a file if it doesn't exist
            if not current_path.exists():
                current_path.touch()

@click.command()
@click.argument('base_path', type=click.Path(exists=True, dir_okay=True))
@click.argument('project_name')
def setup_test_environment(base_path, project_name):
    project_path = Path(base_path + "/" + project_name)
    if not project_path.exists():
        project_path.mkdir()
    create_structure(project_path, directory_structure)

if __name__ == "__main__":
    setup_test_environment()
