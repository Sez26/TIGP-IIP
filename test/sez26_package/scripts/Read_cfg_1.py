import os
from pathlib import Path
import click
import sys

class LAMMPS_OP_CFGParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}

    def parse(self):
        current_section = None
        with open(self.file_path, 'r') as file:
            idx_BB = 0
            idx_Atms = 0
            for line in file:
                line = line.strip() # gets rid of leading and tailing white spaces
                if not line or line.startswith('#'):
                    continue  # Ignore empty lines and comments
                # if line.startswith('[') and line.endswith(']'): # making the section titles
                #     current_section = line[1:-1].strip()
                #     self.data[current_section] = {}
                if ':' in line: # making the section titles
                    _, current_section = map(str.strip, line.split(':', 1))
                    self.data[current_section] = {}
                if current_section == 'TIMESTEP' or current_section == 'NUMBER OF ATOMS':
                    self.data[current_section] = line # for single line data sections
                elif current_section == 'BOX BOUNDS pp pp pp':
                    # check its not the title line
                    if line.startswith('ITEM:') != True:
                        # split the data and calculate simulation side lengths
                        b1, b2 = map(str.strip, line.split(' ', 1))
                        b1 = float(b1)
                        b2 = float(b2)
                        self.data[current_section][idx_BB] = abs(b2-b1)
                        idx_BB = idx_BB+1
                        # Im so confused as to why the index is returning 15?
                        # how does it get that high? I'm confused but the actual values are right?
                    else:
                        continue # the work of the title done in the current section setting
                elif current_section == 'ATOMS id type x y z v_sa_hydro v_sa_von':
                    # check its not the title line
                    if line.startswith('ITEM:') != True:
                        id, Atomtype, x, y, z, v_sa_hydro, v_sa_von = map(str.strip, line.split(' ', 6))
                        self.data[current_section][idx_Atms] = {}
                        self.data[current_section][idx_Atms]['id'] = id
                        self.data[current_section][idx_Atms]['Atom type'] = Atomtype
                        self.data[current_section][idx_Atms]['x'] = x
                        self.data[current_section][idx_Atms]['y'] = y
                        self.data[current_section][idx_Atms]['z'] = z
                        self.data[current_section][idx_Atms]['v_sa_hydro'] = v_sa_hydro
                        self.data[current_section][idx_Atms]['v_sa_von'] = v_sa_von
                        idx_Atms = idx_Atms+1
                    else:
                        continue # the work of the title done in the current section setting
                else:
                    raise ValueError(f"Invalid line format: {line}")

        return self.data

@click.command()
@click.argument('path', type=click.Path(exists=True, dir_okay=True))
@click.argument('file_name')
@click.argument('duplication', type=click.FLOAT)
def read_config(path, file_name, duplication):
    file_path = Path(path + "/" + file_name)
    parser = LAMMPS_OP_CFGParser(file_path)
    parsed_data = parser.parse()
    BB = parsed_data["BOX BOUNDS pp pp pp"]
    # print(len(BB))
    avg_latt_parameter = sum(BB.values())/len(BB)
    # print(avg_latt_parameter) # GAHHH you have to be so careful about printing stuff in click

    # divide by number of duplications
    div_avg = avg_latt_parameter/duplication

    # click.echo(f"The new lattice parameter after minimisation is {div_avg}")
    return div_avg

if __name__ == "__main__":
    div_avg = read_config.main(standalone_mode=False)
    print(div_avg)