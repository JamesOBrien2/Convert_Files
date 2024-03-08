#!/usr/bin/python3

# Author: James O'Brien
# 08-03-2024

# Description:
#       This script will convert the optimized geometry from a Gaussian .log file to a .com file.
#       This script requires inputs to define keywords
#       The user must ammend this script to include the necessary keywords for their calculations.

# Requirements:
#       - Gaussian Output File (.log)
#       - Run the script in the directory containing the .log file


# Usage:
#       convert_log -i <input> [-c <calculation_type>] -f <functional> -b <basis_set> -s <solvent> [-ch <charge>] [-m <multiplicity>]
#

import argparse
import numpy as np


# NB Add necessary keywords to arrays
calculation_array = ["spe", "sp", "opt", "opt freq", "ts"]
functional_array = ["wb97xd", "b3lyp", "m062x", "pbe0", "b2plyp", "b3lyp", "b3lyp-d3bj"]
basis_set_array = ["def2svp", "def2tzvp", "def2tzvpp", "def2qzvp", "def2qzvpp", "6-31g(d,p)", "6-311g(d,p)", "6-311+g(d,p)", "6-311++g(d,p)"]
solvent_array = ["dichloromethane", "dimethylformamide", "dcm", "dmf", "h2o", "water"]
element_array = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", 
    "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", 
    "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", 
    "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe"
]

# Permit arguments to be used in the script
parser = argparse.ArgumentParser(description='Generate Gaussian input file')
parser.add_argument('-i', '--input', help='Log file name (with extension)', required=True)
parser.add_argument('-c', '--calculation', nargs='?', default='sp', help='Calculation Type', choices=calculation_array)
parser.add_argument('-f', '--functional', help='Functional', choices=functional_array)
parser.add_argument('-b', '--basis_set', help='Basis Set', choices=basis_set_array)
parser.add_argument('-s', '--solvent', help='Solvent', choices=solvent_array)
parser.add_argument('-ch', '--charge', nargs='?', default=0, type=int, help='Charge')
parser.add_argument('-m', '--multiplicity', nargs='?', default=1, type=int, help='Multiplicity')

args = parser.parse_args()

log_file_name = args.input
calculation_type = args.calculation
functional = args.functional
basis_set = args.basis_set
solvent = args.solvent
charge = args.charge
multiplicity = args.multiplicity

calculation_dict = {"spe": "", "sp": "", "ts": "opt=(calcfc,ts,noeigentest) freq"}
calculation_type = calculation_dict.get(calculation_type, calculation_type)
solvent_dict = {"dichloromethane": "dcm", "dimethylformamide": "dmf"}

# Open Gaussian Text File
with open(f"{log_file_name}", "r") as file:
    all_lines = [line.strip() for line in file]

# Creating Arrays
all_lines = []
specific_lines = []
coordinates = []
elements = []
xyz_angs = []
xyz_bohr = []
atomic_number = {"1": "H", "2": "He", "3": "Li", "4": "Be", "5": "B", "6": "C", "7": "N", "8": "O", "9": "F", "10": "Ne", 
"11": "Na", "12": "Mg", "13": "Al", "14": "Si", "15": "P", "16": "S", "17": "Cl", "18": "Ar", "19": "K", "20": "Ca", 
"21": "Sc", "22": "Ti", "23": "V", "24": "Cr", "25": "Mn", "26": "Fe", "27": "Co", "28": "Ni", "29": "Cu", "30": "Zn", 
"31": "Ga", "32": "Ge", "33": "As", "34": "Se", "35": "Br", "36": "Kr", "37": "Rb", "38": "Sr", "39": "Y", "40": "Zr", 
"41": "Nb", "42": "Mo", "43": "Tc", "44": "Ru", "45": "Rh", "46": "Pd", "47": "Ag", "48": "Cd", "49": "In", "50": "Sn", 
"51": "Sb", "52": "Te", "53": "I", "54": "Xe", "55": "Cs", "56": "Ba", "57": "La", "58": "Ce", "59": "Pr", "60": "Nd", 
"61": "Pm", "62": "Sm", "63": "Eu", "64": "Gd", "65": "Tb", "66": "Dy", "67": "Ho", "68": "Er", "69": "Tm", "70": "Yb", 
"71": "Lu", "72": "Hf", "73": "Ta", "74": "W", "75": "Re", "76": "Os", "77": "Ir", "78": "Pt", "79": "Au", "80": "Hg", 
"81": "Tl", "82": "Pb", "83": "Bi", "84": "Po", "85": "At", "86": "Rn", "87": "Fr", "88": "Ra", "89": "Ac", "90": "Th", 
"91": "Pa", "92": "U", "93": "Np", "94": "Pu", "95": "Am", "96": "Cm", "97": "Bk", "98": "Cf", "99": "Es", "100": "Fm", 
"101": "Md", "102": "No", "103": "Lr", "104": "Rf", "105": "Db", "106": "Sg", "107": "Bh", "108": "Hs", "109": "Mt", 
"110": "Ds", "111": "Rg", "112": "Uub", "113": "Uut", "114": "Uuq", "115": "Uup", "116": "Uuh", "117": "Uus", "118": "Uuo"}

###########################
# Reading the output file #
###########################

# Open Gaussian Output File
with open(f"{log_file_name}", "r") as file:
    for each_line in file:
        all_lines.append(each_line.strip())

i = 0
j = 0
start = None
end = None
found_end = False
found_optimized_parameters = False
start_optimized_parameters = None

# Find the start and end indices for the optimized parameters
if not all_lines:
    raise ValueError("No Data in File")

# Find the start index for the optimized parameters
for s in range(len(all_lines)):
    if "Stationary point found." in all_lines[s]:
        start = s
        found_optimized_parameters = True
        break

if not found_optimized_parameters:
    raise ValueError("No Optimized Parameters Found")

# Find the end index for the optimized parameters
for e in range(start, len(all_lines)):
    if "----" in all_lines[e]:
        i += 1
        if i == 6:
            start_optimized_parameters = e
        if i == 7:
            end = e
            found_end = True
            break

if not found_end:
    raise ValueError("No End of Optimized Parameters Found")

# Extracting the coordinates
for line in all_lines[start_optimized_parameters + 1 : end]:
    words = line.split()
    elements.append(atomic_number.get(words[1]))
    xyz_angs.append(words[3:])

xyz_angs = np.array(xyz_angs, float)


coordinates = list(zip(elements, xyz_angs))
coordinates.sort(key=lambda coordinates: coordinates[0][0])

###########################
# Creating the input file #
###########################

# file extension
file_extension = "_sp.com" if calculation_type == "sp" else "_input.com"

# Create Gaussian Input File
# Creating output file & inserting last geometry & all keywords
file_name = log_file_name.strip(".log")
with open(f"{file_name}{file_extension}", "w") as file:
    file.write(
        f"# {calculation_type} {functional}/{basis_set} scrf=(smd,solvent={solvent})\n\n"
    )
    file.write(f"{file_name}\n\n")
    file.write(f"{charge} {multiplicity}\n")
    for coord in coordinates:
        coord_str = f"{coord[0]:<2} {coord[1][0]:>12.6f} {coord[1][1]:>12.6f} {coord[1][2]:>12.6f}"
        file.write(f"{coord_str}\n")
    file.write("\n")

# Print to Command-Line
print(f"\033[0;32mFile {file_name}.com has been created with the following keywords:\033[0m")
print(
    f"# {calculation_type} {functional}/{basis_set} scrf=(smd,solvent={solvent})"
)
print(f"{charge} {multiplicity}")
print("...")
print("Coordinates")
print("...")
