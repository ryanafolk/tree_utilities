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
sp_tree = dendropy.Tree.get_from_string(sp_tree_str, "newick", preserve_underscores = True, suppress_internal_node_taxa=True, suppress_leaf_node_taxa=True)

# Define list of taxa 
# Note we must work with node labels instead of taxon labels due to taxon label duplicates
def list_taxa(tree):
	taxa = []
	for node in tree.leaf_node_iter():
		taxa.append(node.label)
	return(taxa)

taxa = list_taxa(sp_tree)

print("List of duplicate taxa:")
print(list(set([x for i, x in enumerate(taxa) if taxa.count(x) > 1])))

taxonremoved = 0
# Main loop, work until the tree taxon number is the same as the unique number of taxon labels
while len(list_taxa(sp_tree)) > len(list(set(list_taxa(sp_tree)))):
	taxa = list_taxa(sp_tree)
	print("Remaining taxa:")
	print(len(taxa))
	duplicate_list = list(set([x for i, x in enumerate(taxa) if taxa.count(x) > 1])) # List comprehension method to get duplicates
	print("Number of duplicates left:")
	print(len(list_taxa(sp_tree)) - len(list(set(list_taxa(sp_tree)))))
	for i in duplicate_list:
		for node in sp_tree.leaf_node_iter(): # Iterate over leaves (can't iterate over taxa per above)
			if taxonremoved == 1: # Switch variable we use to prune only the first duplicate
				taxonremoved = 0
				duplicate_list.remove(i)
				break
			elif node.label == i: # If switch is off we prune the node
				#print(i)
				node.edge.tail_node.remove_child(node, suppress_unifurcations = True) # Suppress unifurcations, which can arise if leaves are trimmed but leave behind orphan nodes
				taxonremoved = 1 # Turn switch on
			else: 
				pass

taxa_reduced = []
for node in sp_tree.leaf_node_iter():
	taxa_reduced.append(node.label)
	
print("After:")
print(len(taxa_reduced))

sp_tree.write_to_path(fout, 'newick', suppress_leaf_node_labels = False, unquoted_underscores = True) # Use this version if not importing taxon names per above

