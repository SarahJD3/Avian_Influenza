#!/usr/bin/env python3

"""
File name: Extracted_codons.py
Author: Sarah Schoem
Created: 3/9/2025
Version: 1.0
Description:
    This code extracts codons from a previously aligned fasta file, trims the sequences to the same length, and writes the results to a new file.
"""

from Bio import SeqIO

def extract_codons(sequence):
    """
    Extracts codons (triplets of nucleotides) from a given DNA sequence.

    Args:
    - sequence (str): A string of nucleotides (A, T, C, G)

    Returns:
    - List of codons (list of strings)
    """
    # Remove gaps (if any) from aligned sequences
    sequence = sequence.replace('-', '')  # Removes gaps from alignment

    codons = []

    # Extract codons by splitting the sequence into triplets
    for i in range(0, len(sequence), 3):
        codon = sequence[i:i + 3]
        if len(codon) == 3:  # Only add complete codons
            codons.append(codon)

    return codons

def trim_sequences(sequences):
    """
    Trims all sequences in the list to the length of the shortest sequence,
    after removing gaps.

    Args:
    - sequences (list of str): List of nucleotide sequences

    Returns:
    - List of trimmed sequences
    """
    # Remove gaps from all sequences first
    sequences_no_gaps = [seq.replace('-', '') for seq in sequences]

    # Find the minimum length sequence (after removing gaps)
    min_length = min(len(seq) for seq in sequences_no_gaps)

    # Trim all sequences to the minimum length (after removing gaps)
    trimmed_sequences = [seq[:min_length] for seq in sequences_no_gaps]

    return trimmed_sequences



def process_fasta(input_fasta, output_file):
    """
    Processes a FASTA file, trims the sequences to the same length, extracts codons from each sequence, and writes the results to a FASTA file.

    Args:
    - input_fasta (str): Path to the input FASTA file
    - output_file (str): Path to the output FASTA file where codons will be saved
    """
    try:
        # Read the sequences from the input FASTA file
        records = list(SeqIO.parse(input_fasta, "fasta"))
        if not records:
            print(f"Error: The input file '{input_fasta}' does not contain any sequences.")
            return

        # Extract the sequences into a list of strings
        sequences = [str(record.seq) for record in records]

        # Debug: Check sequence lengths before trimming
        print(f"Original Sequences Lengths: {[len(seq) for seq in sequences]}")

        # Trim the sequences to the same length
        trimmed_sequences = trim_sequences(sequences)

        # Debug: Check sequence lengths after trimming
        print(f"Trimmed Sequences Lengths: {[len(seq) for seq in trimmed_sequences]}")

        # Write the trimmed codons to the output FASTA file
        with open(output_file, 'w') as out_file:
            for record, trimmed_seq in zip(records, trimmed_sequences):
                # Extract the codons from the trimmed sequence
                codons = extract_codons(trimmed_seq)

                # Debug: Check codons extracted
                print(f"Extracted Codons for {record.id}: {codons[:10]}")  # Display the first 10 codons

                # Write the codons in FASTA format with the original header
                out_file.write(f">{record.id}\n")
                out_file.write("".join(codons) + "\n")  # Combine the codons without spaces for a proper FASTA format

        print(f"Codons extraction complete! Output saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_fasta}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the paths to the input FASTA file and the output file
input_fasta = "H5_Aligned.fasta"  # Replace with your FASTA file path
output_file = "Extracted_Codons.fasta"  # Replace with desired output FASTA file path

# Run the process
process_fasta(input_fasta, output_file)
