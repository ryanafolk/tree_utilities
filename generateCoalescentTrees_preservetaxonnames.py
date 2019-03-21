#! /usr/bin/env python

#####
# This script was adapted from simulation tools developed by S. Mirarab for the paper: 
# Mirarab et al. 2014. Statistical binning enables an accurate coalescent-based estimation of the avian tree. Science 346(6215):1250463.

import dendropy
from dendropy import treesim
from dendropy import TreeList
import sys

fin = sys.argv[1]
num = int(sys.argv[2])
fout= sys.argv[3]

f=open(fin, "r")

sp_tree_str = ""
for l in f:
    sp_tree_str += l
f.close()


sp_tree_str = "[&R] " + sp_tree_str

sp_tree = dendropy.Tree.get_from_string(sp_tree_str, "newick", unquoted_underscores = False)
gene_to_species_map = dendropy.TaxonSetMapping.create_contained_taxon_mapping(
        containing_taxon_set=sp_tree.taxon_set,
        num_contained=1)

gene_tree_list = TreeList()

for i in range(num):
    gene_tree = treesim.contained_coalescent(containing_tree=sp_tree,
    gene_to_containing_taxon_map=gene_to_species_map)
    for t in gene_tree.leaf_nodes():
        t.taxon.label = t.taxon.label.split( )[0]
    gene_tree_list.append(gene_tree)


gene_tree_list.write_to_path(fout, 'newick')

