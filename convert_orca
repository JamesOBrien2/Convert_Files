#!/usr/bin/python3
import argparse

# Import the argparse module to handle command-line arguments
parser = argparse.ArgumentParser(description='Convert XYZ file to COM file')
parser.add_argument('-conv', '--conversion', type=str, choices=['xyz2com', 'rerun'], required=True, 
                    help="""Conversion type
                    xyz2com: convert output.xyz to gaussian.com,
                    rerun: convert output.xyz and input.inp to rerun.inp""")

# File Arguments
parser.add_argument('-xyz', nargs='?', type=str, help='.xyz file name')
parser.add_argument('-com', nargs='?', type=str, help='.com file name')
parser.add_argument('-inp', nargs='?', type=str, help='.inp file name')
args = parser.parse_args()

# Variables
xyz_file = args.xyz
com_file = args.com
inp_file = args.inp

################################################
#     Convert output .xyz to gaussian .com     #
################################################
if args.conversion == 'xyz2com':
    if not args.xyz.endswith('.xyz'):
        print("Please provide a valid .xyz file.")
        exit()

    # Get the output file name without extension
    output_file = args.xyz.replace('.xyz', '.com')

    # Read the content of the input file
    with open(args.xyz, 'r') as file:
        lines = file.readlines()

    # Remove leading and trailing whitespaces from each line
    lines = [line.strip() for line in lines]

    # Create a new list to store the modified lines
    new_lines = []

    # Iterate through the lines and modify them accordingly
    for i, line in enumerate(lines):
        if i < 4:
            if i == 3:
                new_lines.append('#\n\ntitle\n\n0 1')
            continue
        if not line.startswith('*'):
            new_line = line.replace('xyz', 'C').replace('*', '').replace('  ', ' ')
            new_lines.append(new_line)
    new_lines.append('')

    # Write the modified content to the output file
    with open(output_file, 'w') as file:
        file.write('\n'.join(new_lines))
        file.write('\n')

    print(f"Conversion completed successfully! Output saved as {output_file}")


################################################
#     Convert output .xyz to a rerun .inp      #
################################################
elif args.conversion == 'rerun':
    # Read the .inp file
    with open(str(inp_file), 'r') as input_file:
        inp_lines = input_file.readlines()

    # Find the line number where the coordinates start in the .inp file
    for i, line in enumerate(inp_lines):
        if '* xyz' in line:
            start_xyz_line = i + 1
        if line.strip() == '*':
            end_xyz_line = i

    # Read the .xyz file
    with open(str(xyz_file), 'r') as xyz:
        xyz_lines = xyz.readlines()

    # Extract coordinates from the .xyz file
    xyz_coords = [line.strip().split() for line in xyz_lines[2:]]

    # Generate new .inp file with updated coordinates
    new_inp_filename = inp_file.strip('.inp') + '_rerun.inp'
    with open(new_inp_filename, 'w') as new_inp_file:
        for i, line in enumerate(inp_lines):
            if i == start_xyz_line:
                for coord in xyz_coords:
                    new_inp_file.write(f"{' '.join(coord)}\n")
            elif i > start_xyz_line and i < end_xyz_line:
                continue  # Skip writing coordinates from .inp file
            else:
                new_inp_file.write(line)

    print(f'New .inp file "{new_inp_filename}" has been created with updated coordinates.')
