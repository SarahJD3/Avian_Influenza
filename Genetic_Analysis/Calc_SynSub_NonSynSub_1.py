#!/usr/bin/env python3

"""
File name: Calc_SynSub_NonSynSub_1.py
Author: Sarah Schoem
Created: 09Mar2025
Version: 2.0
Edit: 18Apr2025
Description:
    This code calculates the dN/dS ratio using aligned codon sequences
    either manually or via PAML's codeml.
"""

from Bio import SeqIO
from collections import defaultdict
from Bio.Phylo.PAML import codeml

# Codon to amino acid mapping (standard genetic code)
codon_to_aa = {
    "ATA": "I", "ATC": "I", "ATT": "I", "ATG": "M",
    "ACA": "T", "ACC": "T", "ACG": "T", "ACT": "T",
    "AAC": "N", "AAT": "N", "AAA": "K", "AAG": "K",
    "AGC": "S", "AGT": "S", "AGA": "R", "AGG": "R",
    "CTA": "L", "CTC": "L", "CTG": "L", "CTT": "L",
    "CCA": "P", "CCC": "P", "CCG": "P", "CCT": "P",
    "CAC": "H", "CAT": "H", "CAA": "Q", "CAG": "Q",
    "CGA": "R", "CGC": "R", "CGG": "R", "CGT": "R",
    "GTA": "V", "GTC": "V", "GTG": "V", "GTT": "V",
    "GCA": "A", "GCC": "A", "GCG": "A", "GCT": "A",
    "GAC": "D", "GAT": "D", "GAA": "E", "GAG": "E",
    "GGA": "G", "GGC": "G", "GGG": "G", "GGT": "G",
    "TCA": "S", "TCC": "S", "TCG": "S", "TCT": "S",
    "TTC": "F", "TTT": "F", "TTA": "L", "TTG": "L",
    "TAC": "Y", "TAT": "Y", "TAA": "*", "TAG": "*",
    "TGC": "C", "TGT": "C", "TGA": "*", "TGG": "W"
}

def codon_to_aa_func(codon):
    """Converts a codon into its corresponding amino acid."""
    return codon_to_aa.get(codon.upper(), "X")

def calculate_substitutions(alignments):
    """Calculate synonymous and non-synonymous substitutions."""
    syn = 0
    nonsyn = 0

    for i in range(0, len(alignments[0][1]), 3):
        codons = [seq[1][i:i+3] for seq in alignments]
        ref_codon = codons[0]
        ref_aa = codon_to_aa_func(ref_codon)

        for codon in codons[1:]:
            aa = codon_to_aa_func(codon)
            if aa == ref_aa:
                syn += 1
            else:
                nonsyn += 1

    return syn, nonsyn

def process_fasta(input_fasta):
    """Processes a FASTA file and prints manual dN/dS analysis."""
    alignments = [(record.id, str(record.seq)) for record in SeqIO.parse(input_fasta, "fasta")]
    syn, nonsyn = calculate_substitutions(alignments)

    print(f"Synonymous substitutions: {syn}")
    print(f"Non-synonymous substitutions: {nonsyn}")
    
    if syn == 0:
        print("Warning: Synonymous substitutions = 0. Cannot compute dN/dS.")
        return

    dnds = nonsyn / syn
    print(f"dN/dS ratio: {dnds:.2f}")

    if dnds > 1:
        print("→ Positive selection.")
    elif dnds < 1:
        print("→ Purifying selection.")
    else:
        print("→ Neutral evolution.")

"""
def run_paml():
    #Runs codeml via BioPython and prints dN/dS from NSsites model.
    cml = codeml.Codeml(
        alignment="Extracted_Codons.py",
        tree="tree.nwk",
        out_file="codeml_out.txt",
        working_dir="."
    )
    cml.set_options(
        seqtype=1,
        model=0,
        NSsites=[0],
        runmode=0,
        fix_omega=0
    )

    results = cml.run()

    omega = results.get("NSsites", {}).get(0, {}).get("omega", None)
    if omega is not None:
        print(f"\nPAML-calculated dN/dS ratio (omega): {omega:.2f}")
    else:
        print("Could not extract omega value from codeml output.")
"""

#Choose method to run
if __name__ == "__main__":
    input_fasta = "Extracted_Codons.fasta"
    print("Calculating dN/dS manually using FASTA file...\n")
    process_fasta(input_fasta)

    
"""
    print("\nNow running codeml (PAML)...\n")
    run_paml()

"""

