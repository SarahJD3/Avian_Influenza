#bin

#Sarah Schoem
#27Feb2025

from Bio import SeqIO

def fasta_to_phylip(input_fasta, output_phylip):
    with open(input_fasta, "r") as fasta_file:
        sequences = SeqIO.parse(fasta_file, "fasta")
        
        with open(output_phylip, "w") as phylip_file:
            # First, write the number of sequences and sequence length
            seq_list = list(sequences)
            num_sequences = len(seq_list)
            seq_length = len(seq_list[0].seq)  # Assuming all sequences have the same length
            phylip_file.write(f"{num_sequences} {seq_length}\n")
            
            # Write the sequences in phylip format
            for record in seq_list:
                phylip_file.write(f"{record.id.ljust(10)} {str(record.seq)}\n")

# Example usage:
fasta_to_phylip("H5_Aligned.fasta", "H5_Aligned.phy")
