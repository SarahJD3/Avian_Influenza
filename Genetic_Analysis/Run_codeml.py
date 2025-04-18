# Filename
# Date
# Author:
# Mock Directory: C:\Users\Avian_Influenza-main\Genetic_Analysis\paml4.9j\bin

import subprocess
import os

def run_codeml(codeml_path="codeml", control_file="codeml.ctl"):
    """
    Runs codeml from PAML using the specified control file.

    Args:
    - codeml_path (str): Path to the codeml executable (default assumes it's in PATH).
    - control_file (str): Path to the codeml control file.

    Returns:
    - Output from codeml as a string.
    """
    # Prompt the user for the directory where the control file is located
    user_directory = input("Please enter the directory where codeml.ctl is located: ")

    # Change the working directory to where the control file is located
    os.chdir(user_directory)

    try:
        # Run codeml with the control file in the specified directory
        result = subprocess.run([codeml_path, control_file], capture_output=True, text=True)
        if result.returncode == 0:
            print("codeml ran successfully.")
            return result.stdout
        else:
            print(f"codeml encountered an error:\n{result.stderr}")
            return None
    except FileNotFoundError:
        print("Error: codeml executable not found. Check if PAML is installed and accessible in PATH.")
        return None

# Run the function
output = run_codeml()
if output:
    print("codeml output:\n", output)
