# convert_log
A Python script to extract the final geometry from Gaussian Output files (.log) and convert them to Gaussian Input files (.com) with new keywords for quick submission.

Keywords must be edited to fit your own personal needs. (Eg. solvent, calculation types, basis sets etc.) Thus it should be used as a scaffold.

# convert_sp
A Python script to easily produce input files for Atoms-In-Molecules (AIM), Non-Bonding Orbitals (NBO), and Molecular Electrostatic Potential (MEP) calculations.

# convert_orca
A python script with multiple functions for converting files when using ORCA.

For when looking to visualise a .xyz file in Gaussview, I use 'xyz2com' to quickly convert a .xyz file to a general .com file.

For when running out of optimisation steps, I use 'rerun' to create a new .inp file from with the same keywords & the new .xyz coordinates from the output .xyz file.