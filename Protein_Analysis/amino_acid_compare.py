#!/usr/bin/env python3
import warnings

import pandas as pd
import tkinter as tk
from tkinter import filedialog
from pandastable import Table

"""
File name: amino_acid_compare.py
Author: Debra Pacheco
Created: 02/13/25
Version: 1.0
Description:
    This script will generate a table containing the mutations between consensus sequences. Table includes position 
    number, amino acids, side chain changes, binding site, and frequency.

License: MIT License
"""

# Provided Data
mutations = [63, 107, 338]
human_seq = "MERIKELRDLMSQSRTREILTKTTVDHMAIIKKYTSGRQEKNPALRMKWMMAMKYPITADKRIIEMIPERNEQGQTLWSKTNDAGSDRVMVSPLAVTWWNRNGPTTSAVHYPKVYKTYFEKVERLKHGTFGPVHFRNQVKIRRRVDINPGHADLSAKEAQDVIMEVVFPNEVGARILTSESQLTITKEKKEELQDCKIAPLMVAYMLERELVRKTRFLPVAGGTSSVYIEVLHLTQGTCWEQMYTPGGEVRNDDVDQSLIIAARNIVRRATVSADPLASLLEMCHSTQIGGIRMVDILRQNPTEEQAVDICKAAMGLRISSSFSFGGFTFKRTSGSSVTKEEEVLTGNLQTLKIRVHEGYEEFTMVGRRATAILRKATRRLIQLIVSGRDEQSIAEAIIVAMVFSQEDCMIKAVRGDLNFVNRANQRLNPMHQLLRHFQKDAKVLFQNWGIEPIDNVMGMIGILPDMTPSTEMSLRGVRVSKMGVDEYSSTERVVVSIDRFLRVRDQRGNVLLSPEEVSETQGTEKLTITYSSSMMWEINGPESVLVNTYQWIIRNWETVKIQWSQDPTMLYNKMEFEPFQSLVPKAARGQYSGFVRTLFQQMRDVLGTFDTVQIIKLLPFAAAPPEQSRMQFSSLTVNVRGSGMRILVRGNSPVFNYNKATKRLTVLGKDAGALTEDPDEGTAGVESAVLRGFLILGKEDKRYGPALSINELSNLAKGEKANVLIGQGDVVLVMKRKRDSSILTDSQTATKRIRMAIN"
animal_seq = "MERIKELRDLMSQSRTREILTKTTVDHMAIIKKYTSGRQEKNPALRMKWMMAMKYPITADKRIMEMIPERNEQGQTLWSKTNDAGSDRVMVSPLAVTWWNRNGPTTSTVHYPKVYKTYFEKVERLKHGTFGPVHFRNQVKIRRRVDINPGHADLSAKEAQDVIMEVVFPNEVGARILTSESQLTITKEKKEELQDCKIAPLMVAYMLERELVRKTRFLPVAGGTSSVYIEVLHLTQGTCWEQMYTPGGEVRNDDVDQSLIIAARNIVRRATVSADPLASLLEMCHSTQIGGIRMVDILRQNPTEEQAVDICKAAMGLRISSSFSFGGFTFKRTSGSSVKKEEEVLTGNLQTLKIRVHEGYEEFTMVGRRATAILRKATRRLIQLIVSGRDEQSIAEAIIVAMVFSQEDCMIKAVRGDLNFVNRANQRLNPMHQLLRHFQKDAKVLFQNWGIEPIDNVMGMIGILPDMTPSTEMSLRGVRVSKMGVDEYSSTERVVVSIDRFLRVRDQRGNVLLSPEEVSETQGTEKLTITYSSSMMWEINGPESVLVNTYQWIIRNWETVKIQWSQDPTMLYNKMEFEPFQSLVPKAARGQYSGFVRTLFQQMRDVLGTFDTVQIIKLLPFAAAPPEQSRMQFSSLTVNVRGSGMRILVRGNSPVFNYNKATKRLTVLGKDAGALTEDPDEGTAGVESAVLRGFLILGKEDKRYGPALSINELSNLAKGEKANVLIGQGDVVLVMKRKRDSSILTDSQTATKRIRMAIN"

# Your MSA position frequency data
position_counts_animal = {
    63: {'M': 1200, 'I': 800, '-': 1431},
    107: {'K': 100, 'T': 1900, '-': 1431},
    338: {'V': 300, 'K': 1700, '-': 1431}
}

position_counts_human = {
    63: {'M': 5, 'I': 50, '-': 5},
    107: {'K': 10, 'T': 40, '-': 10},
    338: {'V': 2, 'K': 38, '-': 20}
}


def compare_pb2_mutations(human_seq, animal_seq, position_counts_animal, position_counts_human, mutations):
    """ Given sequences, position counts, and a mutation table this will return a data frame containing the position
        number, amino acid residues, side chain changes, binding site boolean, and frequency of mutation

    Parameters:
    human sequence (str): sequence of human consensus
    animal sequence (str): sequence of animal consensus

    human position count (dict): nested dictionary of position counts
    animal position count (dict): nested dictionary of position counts

    mutations (list): List of differences between consensus sequences

    Returns:
    data frame: data frame containing Position, Human Residue, Animal Residue, Mutation, Side Chain Change,
                               Binding Site?, Mutation Frequency in Animals, Mutation Frequency in Humans

    """

    binding_sites = {28, 32, 35, 46, 50, 51, 56, 57, 58, 60, 83, 85, 86, 88, 36, 37, 38, 40, 46, 49, 83, 116, 117, 123,
                     210, 323, 339, 355, 357, 361, 363,
                     376, 404, 406, 429, 431, 432}

    aa_properties = {
        'A': 'Nonpolar', 'R': 'Positively Charged', 'N': 'Polar', 'D': 'Negatively Charged',
        'C': 'Polar', 'Q': 'Polar', 'E': 'Negatively Charged', 'G': 'Nonpolar',
        'H': 'Positively Charged', 'I': 'Hydrophobic', 'L': 'Hydrophobic', 'K': 'Positively Charged',
        'M': 'Nonpolar', 'F': 'Hydrophobic', 'P': 'Nonpolar', 'S': 'Polar',
        'T': 'Polar', 'W': 'Hydrophobic', 'Y': 'Polar', 'V': 'Hydrophobic', '-': 'Gap'
    }

    # Create table
    table_data = []

    for pos in mutations:
        # Convert 1-based index (from `mutations`) to 0-based for Python sequences
        zero_based_pos = pos - 1

        human_residue = human_seq[pos]
        animal_residue = animal_seq[pos]
        mutation = f"{animal_residue} → {human_residue}"

        side_chain_change = f"{aa_properties[animal_residue]} → {aa_properties[human_residue]}"
        binding_site = 'Yes' if (pos + 1) in binding_sites else 'No'

        human_residue_zero = human_seq[zero_based_pos]
        animal_residue_zero = animal_seq[zero_based_pos]

        # Get mutation frequencies (handling missing data)
        pos = pos +1
        if pos in position_counts_animal:
            total_count_animal = sum(position_counts_animal[pos].values())
            animal_frequency = (position_counts_animal[pos].get(human_residue, 0) / total_count_animal) * 100

        else:
            animal_frequency = 0  # Default to 0% if data is missing

        if position_counts_human and pos in position_counts_human:
            total_count_human = sum(position_counts_human[pos].values()) or 1  # Avoid division by zero
            human_frequency = (position_counts_human[pos].get(human_residue, 0) / total_count_human) * 100
        else:
            human_frequency = 100

        table_data.append([pos, animal_residue, human_residue, mutation, side_chain_change, binding_site,
                           f"{animal_frequency:.2f}%", f"{human_frequency:.2f}%"])

    df = pd.DataFrame(table_data,
                      columns=['Position', 'Animal Residue', 'User Residue', 'Mutation', 'Side Chain Change',
                               'Binding Site?', 'Animal Mutation Frequency', 'User Mutation Frequency'])
    return df
    # print(df)


def show_table(df):
    warnings.simplefilter(action='ignore', category=FutureWarning)


    root = tk.Tk()
    root.title("Mutation Analysis Table")

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    pt = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    pt.show()

    root.mainloop()


def file_selector():
    selector = tk.Tk()
    selector.withdraw()  # Hide the main menu

    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("Text files", "*.fa"), ("All files", "*.*"))
    )
    if file_path:
        selector.destroy()
        return file_path

    else:
         print("No file selected.")


# df = compare_pb2_mutations(human_seq, animal_seq, position_counts_animal, position_counts_human)
# Call this after creating your DataFrame
# show_table(df)
