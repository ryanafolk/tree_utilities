#! /usr/bin/env python3

# Run like:
# python3 enumerate_clade_frequencies.py simulated_tree_set.tre clade_frequencies.csv


import dendropy
from dendropy import TreeList
import sys
import csv

# Process arguments
fin = sys.argv[1]
fout= sys.argv[2]

f=open(fin, "r")

sp_tree_str = ""
for l in f:
    sp_tree_str += l
f.close()

sp_tree_str = "[&R] " + sp_tree_str

# Import the tree; note that we have to work with node labels rather than taxon labels due to the presence of taxon label duplicates
sp_tree = dendropy.TreeList.get_from_string(sp_tree_str, "newick", preserve_underscores = True, suppress_internal_node_taxa=True, suppress_leaf_node_taxa=True)

# Define list of taxa from a node; working with leaf node labels rather than taxa simplifies things
def list_taxa(node):
	taxa = []
	for i in node.leaf_iter():
		taxa.append(i.label)
	return(taxa)
	

print("Number of trees:")
print(len(sp_tree))

taxa = [list_taxa(tree) for tree in sp_tree] # Count taxa by making a list of taxon lists for each taxon in tree
taxa = len(list(set(sum(taxa, [])))) # Collapse list of lists to list of unique elements, then count
print("Number of taxa observed across all trees:")
print(taxa)

print("Enumerating clades.\n")
internal = lambda x: True if len(x.child_nodes()) > 0 else False
complete_clade_list = []
unique_clade_list = []
for tree in sp_tree: # Iterate over trees in file
	#print("On tree:") # State which tree we are on
	#print(sp_tree.index(tree))
	for node in tree.postorder_node_iter(internal): # iterate over internal nodes
		taxa = set(list_taxa(node)) # Clade members as a set so it is unordered
		complete_clade_list.append(taxa)
		if taxa not in unique_clade_list: # Only add unique clades
			unique_clade_list.append(taxa)


print("Number of clades observed across all trees:")
print(len(complete_clade_list))

print("Number of unique clades observed across all trees:")
print(len(unique_clade_list))

# Generate counts
print("Generating clade counts.\n")
output = [["clade_number", "clade_frequency"]]
for clade in unique_clade_list:
	output.append([unique_clade_list.index(clade), complete_clade_list.count(clade)/len(complete_clade_list)])

with open(fout, "w") as f:
    writer = csv.writer(f)
    writer.writerows(output)
