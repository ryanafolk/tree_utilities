#! /usr/bin/env python3

# Run like:
# ./sampled_ancestornodes_to_branches.py fagales.treesample.subset.tre fagales.treesample.subset.zerobranchancestors.tre


import dendropy
from dendropy import TreeList
import sys

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

# Define list of taxa, working with leaf node labels rather than taxa to simplify adding new taxa below
def list_taxa(tree):
	taxa = []
	for node in tree.leaf_node_iter():
		taxa.append(node.label)
	return(taxa)

print("Number of trees:")
print(len(sp_tree))

taxa = [list_taxa(tree) for tree in sp_tree] # Count taxa by making a list of taxon lists for each taxon in tree
taxa = len(list(set(sum(taxa, [])))) # Collapse list of lists to list of unique elements, then count
print("Number of taxa observed across all trees:")
print(taxa)

internal = lambda x: True if len(x.child_nodes()) > 0 else False
for tree in sp_tree: # Iterate over trees in file
	print("On tree:") # State which tree we are on
	print(sp_tree.index(tree))
	print("Taxon number before:") # State how many taxa are in the original file (sampled ancestors not represented as leaves yet, so not included)
	print(len(list_taxa(tree)))
	print("Internal nodes are:")
	for node in tree.postorder_node_iter(internal): # iterate over internal nodes
		if node.label is not None: # Skip nodes with no label, i.e., not sampled ancestors
			print(node.label)
			new_node = node.new_child() # Give the node a new child node
			new_node.edge_length = 1e-6 # Assign very short branch to subtending edge of new child node
			new_node.label = node.label # Assign node label to the new child node, which is now a leaf representing the sampled ancestor
	print("Taxon number after:") # State how many taxa are in the original file (sampled ancestors converted to leaves, so now included!)
	print(len(list_taxa(tree)))



sp_tree.write_to_path(fout, 'newick', suppress_leaf_node_labels = False, unquoted_underscores = True) # Use this version if not importing taxon names per above
