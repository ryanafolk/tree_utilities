# Tree utilities

## drop_duplicates_tree.py

This script keeps only one taxon per tip name in the event of taxon name duplicates. I wrote this because there do not seem to be any good tools for managing multiple tips with the same name in standard tools. R and other environments cannot handle duplicate names, but they often arise in supermatrix construction. The first encountered duplicate is kept based on leaf_node_inter() in Dendropy.

Run like:
```
./drop_duplicates_tree.py intree.tre outtree.tre
```

## sampled_ancestornodes_to_branches.py

This script converts sampled ancestors notated as node labels (e.g., the native format in RevBayes output) to new tip taxa with a very short branch of 1e-6. The purpose is to easily use output with downstream tools such as BioGeoBEARS that expect sampled ancestors coded as leaves. It accepts lists of trees, e.g., MCMC output, and handles (but ignores in output) node metadata.

Run like:
```
 ./sampled_ancestornodes_to_branches.py fagales.treesample.subset.tre fagales.treesample.subset.zerobranchancestors.tre
```

## simulate_gene_trees.py

Simulate gene trees given a newick species tree with branch lengths in coalescent units via a simple wrapper for Dendropy functions. The script takes three arguments: an input file name, a desired number of trees, and an output name. This script requires Dendropy and is based on supplemental methods from Mirarab et al. 2014 in Science: [http://science.sciencemag.org/content/346/6215/1250463.figures-only].

This script is representative of methods used for characterizing ILS expectations in:

Folk, R.A., J.R. Mandel, and J.V. Freudenstein. 2017. Ancestral gene flow and parallel organellar genome capture result in extreme phylogenomic discord in a lineage of angiosperms. Systematic Biology 66(3): 320–337.

García, N., R.A. Folk, A.W. Meerow, S. Chamala, M.A. Gitzendanner, R.S de Oliveira, D.E. Soltis, and P.S. Soltis. 2017. Deep reticulation and incomplete lineage sorting obscure the diploid phylogeny of rain-lilies and allies (Amaryllidaceae tribe Hippeastreae). Molecular Phylogenetics and Evolution 111: 231-247.

The file `astral_example_hippeastrum.tre` is from the aTRAM-ASTRAL analysis in García et al. 2017 and may be run like so:

```
./simulate_gene_trees.py astral_example_hippeastrum.tre 1000 example_gene_trees.tre
```
