#!/usr/bin/env python3

from Bio import SeqIO, AlignIO
from collections import Counter

"""
File name: seq_frequency.py
Author: Debra Pacheco
Created: 02/01/25
Version: 1.0
Description:
    This script will generate a dictionary of containing the counts of amino acids at each postion from a multiple sequence
    alignment.

License: MIT License
"""

# Define file paths
msa_file = "clustalo-I20250131-012913-0270-28960768-p1m.fa"

# Load the alignment
alignment = AlignIO.read(msa_file, "fasta")

# List of accession numbers from human hosts
human_accessions = []
with open ("HumanAcessions.fa") as file:
    for line in file:
        line = file.readline()
        human_accessions.append(line.strip())

#print(human_accessions)

# Separate human and animal sequences
human_seqs = []
animal_seqs = []

for record in alignment:
    accession = record.id
    if accession in human_accessions:
        human_seqs.append(record.seq)
    else:
        animal_seqs.append(record.seq)

#print(human_seqs)


def calculate_amino_acid_freq(msa_file):

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


# === Example Usage ===
msa_file = input("Enter the MSA filename: ")

frequencies = calculate_amino_acid_freq(msa_file)

print("\nAmino Acid Frequencies (Consensus Positions):")
for pos, freq in frequencies.items():
    print(f"Position {pos}: {freq}")
