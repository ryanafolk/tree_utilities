#! /usr/bin/env python3

# Run like:
# python3 enumerate_robinsonfoulds.py simulated_tree_set.tre out_simulated.csv empirical_tree.tre out_empirical.csv


import dendropy
from dendropy import TreeList
from dendropy.calculate import treecompare
import sys
import csv
import itertools

# Process arguments
fin = sys.argv[1]
fout = sys.argv[2]
chloroplast_tree = sys.argv[3]
cp_out = sys.argv[4]


#######
# Simulated trees
###### 	   	

f=open(fin, "r")

sp_tree_str = ""
for l in f:
    sp_tree_str += l
f.close()

sp_tree_str = "[&R] " + sp_tree_str

# Import the tree; note that we have to work with node labels rather than taxon labels due to the presence of taxon label duplicates
print("Loading simulation tree file.\n")
tns = dendropy.TaxonNamespace()
sp_tree = dendropy.TreeList.get_from_string(sp_tree_str, "newick", preserve_underscores = True, suppress_internal_node_taxa = True, suppress_leaf_node_taxa = False, taxon_namespace=tns)
# sp_tree = sp_tree[1:5] # For testing


        
print("Number of trees:")
print(len(sp_tree))

print("\nGenerating tree pairs.\n")
pairs = list(itertools.combinations(sp_tree,2)) # Combinations for unordered pair enumeration
pairs = [list(x) for x in pairs]
print("Number of tree pairs:")
print(len(pairs))

print("\nGenerating simulated distances.\n")
for x in pairs:
	b1 = x[0].encode_bipartitions()
	b2 = x[1].encode_bipartitions()

output = [treecompare.symmetric_difference(x[0], x[1]) for x in pairs]
#print(output)

with open(fout, "w") as f:
    writer = csv.writer(f)
    for x in output:
    	writer.writerow([x])
   
#######
# Chloroplast
###### 	
    	
f=open(chloroplast_tree, "r")

cp_tree_str = ""
for l in f:
    cp_tree_str += l
f.close()

cp_tree_str = "[&R] " + cp_tree_str

print("Loading chloroplast tree file.\n")
cp_tree = dendropy.Tree.get_from_string(cp_tree_str, "newick", preserve_underscores = True, suppress_internal_node_taxa = True, suppress_leaf_node_taxa = False, taxon_namespace=tns)
b_cp = cp_tree.encode_bipartitions()

print("Generating empirical distances.\n")
output = []
for tree in sp_tree:
	output.append(treecompare.symmetric_difference(tree, cp_tree))

with open(cp_out, "w") as f:
    writer = csv.writer(f)
    for x in output:
    	writer.writerow([x])

