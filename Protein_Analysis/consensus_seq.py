#!/usr/bin/env python3

from Bio import AlignIO
from collections import Counter

"""
File name: consensus_seq.py
Author: Debra Pacheco
Created: 02/01/25
Version: 1.0
Description:
    This script will generate a consensus sequence 

License: MIT License
"""

Accession_list = []


def get_consensus_sequence(msa_file, accession_file, accession_list=Accession_list):
    """
    Given a multiple sequence alignment (MSA) and a file with human host accession numbers,
    this function returns consensus sequences for human and animal viruses.

    Parameters:
    msa_file (str): Path to the MSA FASTA file.
    accession_file (str): Path to the file containing human host accession numbers.

    Returns:
    tuple: (human_consensus, animal_consensus), where each is a string representing
           the most frequent amino acids at each position.
    """

    # Load the alignment
    alignment = AlignIO.read(msa_file, "fasta")

    # Load accession numbers from human hosts
    with open(accession_file) as file:
        human_accessions = {line.strip() for line in file}

    # Separate sequences into human and animal groups
    human_seqs = []
    animal_seqs = []

    if len(human_accessions) == 0:
        human_accessions = Accession_list

    for record in alignment:
        if record.id in human_accessions:
            human_seqs.append(record.seq)
        else:
            animal_seqs.append(record.seq)

    # Identify differences at each position
    sequence_length = len(alignment[0].seq)

    def get_most_common_base(sequences):
        """ Returns the most common base at each position in a given set of sequences. """
        consensus = []
        for pos in range(sequence_length):
            column = [seq[pos] for seq in sequences]
            freq = Counter(column)
            most_common_base, _ = freq.most_common(1)[0]  # Get the most frequent amino acid
            consensus.append(most_common_base)
        return "".join(consensus)

    # Generate consensus sequences
    #    print(human_seqs)
    #    print(animal_seqs)
    human_consensus = get_most_common_base(human_seqs) if human_seqs else None
    animal_consensus = get_most_common_base(animal_seqs) if animal_seqs else None

    # Remove any gaps in the consensus to match positions to NCBI positions
    try:
        human_consensus = (human_consensus.replace('-', ''))
    except AttributeError:
        pass
    try:
        animal_consensus = (animal_consensus.replace('-', ''))
    except AttributeError:
        pass

    return human_consensus, animal_consensus


# Obtain the consensus sequence from labeled human accessions and a consensus of everything else
# consensus = (get_consensus_sequence("clustalo-I20250131-012913-0270-28960768-p1m.fa", accession_file="HumanAcessions.fa"))

# print(consensus)

# split the tuple into separate variables for future use
# human_consensus = consensus[0]
# animal_consensus = consensus[1]


def seq_compare(sequences, length):
    """ Given a tuple of sequences returns each position that has a difference between two sequences.

    Parameters:
    sequences (str): tuple of consensus sequences
    sequence length (int): length of each consensus

    Returns:
    List: zero based position of each amino acid difference

    """
    bases_differences = []
    for pos in range(length):
        column = [seq[pos] for seq in sequences]
        if column[0] != column[1]:
            bases_differences.append(pos)
    return bases_differences

# print(seq_compare(consensus, len(human_consensus)))
