from Bio import Phylo

"""
File name: analyze_tree.py
Author: Janessa Reed
Created: 2/11/2024
Verstion: 1.0

License: MIT License 

"""


# Load the phylogenetic tree
TREE_FILE = "H5_tree_upgma.nwk"
tree = Phylo.read(TREE_FILE, "newick")

# Identify and print all clades and their branch lengths
print("\nIdentifying Clades and Branch Lengths:\n")
for clade in tree.find_clades():
    if clade.name:
        print(f"Clade: {clade.name}, Branch Length: {clade.branch_length}")

# Find the Most Recent Common Ancestor (MRCA) of two sequences
seq1 = "JX258652.1"
seq2 = "KP286538.1"
mrca = tree.common_ancestor(seq1, seq2)
print(f"\nMost Recent Common Ancestor (MRCA) of {seq1} and {seq2}: {mrca}")

# Compare branch lengths - find the top 5 longest branches
branches = [(clade.name, clade.branch_length) for clade in tree.find_clades() if clade.branch_length]
sorted_branches = sorted(branches, key=lambda x: x[1], reverse=True)

print("\nTop 5 Longest Branches:")
for name, length in sorted_branches[:5]:
    print(f"{name}: {length}")

# Optional: Save a textual representation of the tree
TREE_OUTPUT = "tree_analysis_output.txt"
with open(TREE_OUTPUT, "w") as f:
    Phylo.draw_ascii(tree, file=f)

print(f"\nTree analysis complete. Results saved in {TREE_OUTPUT}")
