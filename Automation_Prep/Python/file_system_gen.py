"""
making a file system for a HEA LAMMPS project
this code is mostly copied from chatGPT
"""

import os
from pathlib import Path

directory_structure = {
    "project": {
        "scripts": [],
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

def setup_test_environment(base_path):
    base_path = Path(base_path)
    if not base_path.exists():
        base_path.mkdir()
    create_structure(base_path, directory_structure)

if __name__ == "__main__":
    test_base_path = Path("/home/sez26/TIGP-IIP/Automation_Prep/Python/test_project")
    setup_test_environment(test_base_path)
