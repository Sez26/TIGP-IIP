import click
import os

@click.command()
@click.option('--config-file', required=True, help='Path to the configuration file.')
@click.option('--key', required=True, help='The key to add or update in the configuration file.')
@click.option('--value', required=True, help='The value to set for the key in the configuration file.')
def add_or_update_variable(config_file, key, value):
    """Add or update a variable in the configuration file."""
    
    # Check if the configuration file exists
    if not os.path.isfile(config_file):
        click.echo(f"Config file {config_file} does not exist.")
        return
    
    # Read the content of the config file
    with open(config_file, 'r') as file:
        lines = file.readlines()
    
    # Check if the key exists
    key_exists = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            key_exists = True
            break
    
    # If the key does not exist, append it
    if not key_exists:
        lines.append(f"{key}={value}\n")
    
    # Write the updated content back to the config file
    with open(config_file, 'w') as file:
        file.writelines(lines)
    
    click.echo(f"{key} has been set to {value} in {config_file}.")

if __name__ == '__main__':
    add_or_update_variable()
