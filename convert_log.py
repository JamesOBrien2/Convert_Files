#!/bin/python3
import sys
import numpy as np
import argparse
import textwrap

# NB Add necessary keywords to arrays
calculation_array = ['spe', 'opt', 'opt freq', 'ts']
functional_array = ['wb97xd', 'b3lyp']
basis_set_array = ['def2svp', 'def2tzvp']
solvent_array = ['dichloromethane', 'dimethylformamide']
element_array = [
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
    'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
    'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe'
]
element_dict = {'iodine': 'I', 'Iodine': 'I'}
calculation_dict = {'spe': '', 'ts': 'opt=(calcfc,ts,noeigentest) freq'}

# Help - with Improved Formatting 
wrapped_calculation_types = textwrap.wrap(', '.join(calculation_array), width=60)
wrapped_functionals = textwrap.wrap(', '.join(functional_array), width=60)
wrapped_basis_sets = textwrap.wrap(', '.join(basis_set_array), width=60)
wrapped_solvents = textwrap.wrap(', '.join(solvent_array), width=60)
wrapped_pseudo_elements = textwrap.wrap(', '.join(element_array), width=60)

parser = argparse.ArgumentParser(description='Available Options for Inputs')
parser.add_argument('-c', '--calculations', nargs='+', help='List of available calculations: {}'.format('\n'.join(wrapped_calculation_types)))
parser.add_argument('-f', '--functionals', nargs='+', help='List of available functionals: {}'.format('\n'.join(wrapped_functionals)))
parser.add_argument('-b', '--basis-sets', nargs='+', help='List of available basis sets: {}'.format('\n'.join(wrapped_basis_sets)))
parser.add_argument('-s', '--solvents', nargs='+', help='List of available solvents: {}'.format('\n'.join(wrapped_solvents)))
parser.add_argument('-p', '--pseudo', nargs='+', help='List of available atoms for pseudopotential: {}'.format('\n'.join(wrapped_pseudo_elements)))

args = parser.parse_args()

# File name check
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = input("What's the log file name? (with extension): ")

# Creating Arrays
all_lines = []
coordinates = []
elements = []
xyz_angs = []
xyz_bohr = []
atomic_number = {
    '1': 'H', '2': 'He', '3': 'Li', '4': 'Be', '5': 'B', '6': 'C', '7': 'N', '8': 'O', '9': 'F', '10': 'Ne',
    '11': 'Na', '12': 'Mg', '13': 'Al', '14': 'Si', '15': 'P', '16': 'S', '17': 'Cl', '18': 'Ar', '19': 'K',
    '20': 'Ca', "21": "Sc", "22": "Ti", "23": "V", "24": "Cr", "25": "Mn", "26": "Fe",
    "27": "Co", "28": "Ni", "29": "Cu", "30": "Zn", "31": "Ga", "32": "Ge", "33": "As",
    "34": "Se", "35": "Br", "36": "Kr", "37": "Rb", "38": "Sr", "39": "Y", "40": "Zr",
    "41": "Nb", "42": "Mo", "43": "Tc", "44": "Ru", "45": "Rh", "46": "Pd", "47": "Ag",
    "48": "Cd", "49": "In", "50": "Sn", "51": "Sb", "52": "Te", "53": "I", "54": "Xe",
    "55": "Cs", "56": "Ba", "57": "La", "58": "Ce", "59": "Pr", "60": "Nd", "61": "Pm",
    "62": "Sm", "63": "Eu", "64": "Gd", "65": "Tb", "66": "Dy", "67": "Ho", "68": "Er",
    "69": "Tm", "70": "Yb", "71": "Lu", "72": "Hf", "73": "Ta", "74": "W", "75": "Re",
    "76": "Os", "77": "Ir", "78": "Pt", "79": "Au", "80": "Hg", "81": "Tl", "82": "Pb",
    "83": "Bi", "84": "Po", "85": "At", "86": "Rn", "87": "Fr", "88": "Ra", "89": "Ac",
    "90": "Th", "91": "Pa", "92": "U", "93": "Np", "94": "Pu", "95": "Am", "96": "Cm",
    "97": "Bk", "98": "Cf", "99": "Es", "100": "Fm", "101": "Md", "102": "No", "103": "Lr",
    "104": "Rf", "105": "Db", "106": "Sg", "107": "Bh", "108": "Hs", "109": "Mt", "110": "Ds",
    "111": "Rg", "112": "Uub", "113": "Uut", "114": "Uuq", "115": "Uup", "116": "Uuh", "117": "Uus", "118": "Uuo"
}


# Open Gaussian Text File
with open(f'{file_name}', 'r') as file:
    for each_line in file:
        all_lines.append(each_line.strip())

i = 0
j = 0

#Reads the Input orientation information
for s in range(len(all_lines)):            
    if "Input orientation:" in all_lines[s]:
        start = s
        i = i + 1
    elif "Standard orientation:" in all_lines[s]:
        start = s
        i = i + 1

for e in range(start + 5, len(all_lines)):
    if "----" in all_lines[e]:
        end = e
        break
    j = j + 1

for line in all_lines[start + 5: end]:
    words = line.split()
    elements.append(atomic_number.get(words[1]))
    xyz_angs.append(words[3:])

xyz_angs = np.array(xyz_angs, float)
xyz_bohr = list(xyz_angs / 0.529177)

coordinates = list(zip(elements, xyz_bohr))
coordinates.sort(key=lambda coordinates: coordinates[0][0])

# Inputs for keywords
calculation_type = input("Calculation Type?: ").lower()
if calculation_type not in calculation_array:
    raise ValueError(f"{calculation_type} is not in calculation_array")
calculation_type = calculation_dict.get(calculation_type, calculation_type)

functional = input("What's the functional?: ").lower()
if functional not in functional_array:
    raise ValueError(f"{functional} is not in functional_array")

basis_set = input('Whats the basis set?: ').lower()
if basis_set not in basis_set_array:
    raise ValueError(f"{basis_set} is not in Basis Set array")

solvent_dict = {'dcm': 'dichloromethane', 'dmf': 'dimethylformamide'}
solvent = input("What's the solvent?: ").lower()
solvent = solvent_dict.get(solvent)
if solvent not in solvent_array:
    raise ValueError(f"{solvent} is not in solvent_array")

charge_multiplicity = input("What's the charge & multiplicity?: ")


# Pseudo Keyword
pseudo = input("Pseudopotential? (y/n): ")
if pseudo == 'y':
    pseudo_element = input("Which element?: ")
    pseudo_element = element_dict.get(pseudo_element, pseudo_element)
    if pseudo_element not in element_array:
        raise ValueError(f"{pseudo_element} is not in element_array")
    basis_set_if_pseudo = basis_set
    basis_set = 'gen'
    pseudo_read = 'pseudo=read'
else:
    pseudo_element = ''
    pseudo_read = ''

output_name = input("Name of Output file (Different to input!): ")


# Creating output file & inserting last geometry & all keywords

with open(f'{output_name}.com', 'w') as file:
    file.write(f'# {calculation_type} {functional}/{basis_set} scrf=(smd,solvent={solvent}) {pseudo_read}\n\n')
    file.write(f'{output_name}\n\n')
    file.write(f'{charge_multiplicity}\n')
    for coord in coordinates:
        coord_str = f'{coord[0]:<2} {coord[1][0]:>12.6f} {coord[1][1]:>12.6f} {coord[1][2]:>12.6f}'
        file.write(f'{coord_str}\n')
    if pseudo_read != '':
    
        file.write(f'\n{" ".join(sorted(set(elements), key=lambda x: element_array.index(x)))} 0\n')


        file.write(f'{basis_set_if_pseudo}\n')
        file.write(f'****\n\n')
        file.write(f'{pseudo_element} 0\n')
        file.write(f'{basis_set_if_pseudo}\n')
    file.write('\n')

