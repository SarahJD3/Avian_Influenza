#!/usr/bin/env python3
import requests
from Bio import SeqIO, AlignIO, Align
from collections import Counter

from Protein_Analysis.amino_acid_compare import compare_pb2_mutations, show_table
from Protein_Analysis.consensus_seq import seq_compare, get_consensus_sequence

"""
File name: seq_frequency.py
Author: Debra Pacheco
Created: 02/01/25
Version: 1.3
Description:
    This script contains two functions. Calculate_amino_acid_freq takes a multiple sequence alignment file and creates a 
    dictionary of all amino acid residues at each position.
    
    multiple_sequence_welcome allows the user to choose a sequence entry type and generates a table containing the 
    mutations between consensus sequences using multiple functions.

License: MIT License
"""

# Define default file path for animal sequences
msa_file = "Protein_Analysis/clustalo-I20250131-012913-0270-28960768-p1m.fa"


def calculate_amino_acid_freq(msa_file):
    """ Given a file of sequences returns a dictionary of amino acids at each given position.

    Parameters:
    msa_file (file path): file path to a FASTA formatted file containing aligned sequence data

    Returns:
    Dictionary: one based position of amino acids at each position

    """

    # Load the alignment
    alignment = AlignIO.read(msa_file, "fasta")

    # Identify amino acid frequencies at each position
    sequence_length = len(alignment[0].seq)
    position_frequencies = {}

    consensus_position = 0

    for position in range(sequence_length):
        column = [record.seq[position] for record in alignment]
        freq = Counter(column)

        # Skip positions where the most common amino acid is a gap
        most_common_aa, most_common_count = freq.most_common(1)[0]
        if most_common_aa == '-':
            continue

        # This position will appear in the consensus
        consensus_position += 1

        # Store frequencies for non-gap positions
        position_frequencies[consensus_position] = freq

    return position_frequencies


position_count_animal = calculate_amino_acid_freq(msa_file)
position_count_human = {}


def multiple_sequence_welcome():
    print("                Welcome to the amino acid comparison program.")
    print("  You can currently compare amino acid sequences from influenza PB2 segments.\n")

    file_type = "4"

    print("  Do you have a single sequence to manually enter or a FASTA multiple sequence alignment file?\n")
    print("                    Please choose from the following options.\n")

    print("1. Single Sequence")
    print("2. Multiple Sequence Alignment File")
    print("3. Return to main menu")
    print("4. Exit\n")

    while file_type != "3":

        file_type = file_type.strip()

        if file_type == "1":
            user_sequence = input("\nPlease enter your amino acid sequence.\n")
            user_sequence = user_sequence.replace("\n", "")
            user_sequence = user_sequence.replace(" ", "")
            animal_sequence = get_consensus_sequence(msa_file, "Protein_Analysis/HumanAcessions.fa")
            aligner = Align.PairwiseAligner()
            alignments = aligner.align(user_sequence, animal_sequence[1])

            #            print(alignments.sequences)

            sequence_tuple = (alignments.sequences[0], alignments.sequences[1])
            #            print(sequence_tuple)
            base_differences = seq_compare(sequence_tuple, len(sequence_tuple[0]))
            df = compare_pb2_mutations(sequence_tuple[0], sequence_tuple[1], position_count_animal,
                                       position_count_human,
                                       base_differences)
            show_table(df)

            return print("Table generated.")

        if file_type == "2":
            msa = input("Please enter multiple sequence alignment file name.")
            return print("Table generated.")

        if file_type == "3":
            exit()

        else:
            file_type = input("Invalid choice. Please Enter 1 for single sequence"
                              "\nEnter 2 for a multiple sequence alignment file.\n Or enter 3 to return to main menu.\n")


if __name__ == "__main__":
    msa_file = input("Enter the MSA filename: ")
    frequencies = calculate_amino_acid_freq(msa_file)

    print("\nAmino Acid Frequencies (Consensus Positions):")
    for pos, freq in frequencies.items():
        print(f"Position {pos}: {freq}")
