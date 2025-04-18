# Filename
# Date
# Author
# Mock Directory: # Mock Directory: C:\Users\Avian_Influenza-main\Genetic_Analysis\paml4.9j\bin

import os

# Define the content of the 'codeml.ctl' file for PAML 4.9j
codeml_content = """seqfile = cleaned_H5_Aligned.phy  # Sequence alignment file (in Phylip format)
treefile = H5_Aligned.fasta.treefile  # Phylogenetic tree file
outfile = H5_results.txt  # Output file

noisy = 9
verbose = 1
runmode = 0  # Standard codon model analysis

seqtype = 1  # Codon sequences
CodonFreq = 2  # F3x4 model for codon frequencies

clock = 0
model = 0  # One-ratio model (same dN/dS for all branches)
NSsites = 2  # Positive selection model (M2a: neutral + selection)

icode = 0
fix_kappa = 0
kappa = 2
fix_omega = 0
omega = 1"""

# Prompt the user for the directory where the file should be saved
user_directory = input("Please enter the directory where codeml.ctl should be saved: ")

# Ensure the directory exists
os.makedirs(user_directory, exist_ok=True)

# Define the full path for the control file
file_path = os.path.join(user_directory, "codeml.ctl")

# Write the modified content to the file
with open(file_path, "w") as f:
    f.write(codeml_content)

print(f"codeml.ctl file has been written to {file_path}")
