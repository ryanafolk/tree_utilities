# Tree utilities

## simulate_gene_trees.py

Simulate gene trees given a newick species tree with branch lengths in coalescent units via a simple wrapper for Dendropy functions. The script takes three arguments: an input file name, a desired number of trees, and an output name. This script requires Dendropy and is based on supplemental methods from Mirarab et al. 2014 in Science: [http://science.sciencemag.org/content/346/6215/1250463.figures-only].

This script is representative of methods used for characterizing ILS expectations in:

Folk, R.A., J.R. Mandel, and J.V. Freudenstein. 2017. Ancestral gene flow and parallel organellar genome capture result in extreme phylogenomic discord in a lineage of angiosperms. Systematic Biology 66(3): 320–337.

García, N., R.A. Folk, A.W. Meerow, S. Chamala, M.A. Gitzendanner, R.S de Oliveira, D.E. Soltis, and P.S. Soltis. 2017. Deep reticulation and incomplete lineage sorting obscure the diploid phylogeny of rain-lilies and allies (Amaryllidaceae tribe Hippeastreae). Molecular Phylogenetics and Evolution 111: 231-247.

The file `astral_example_hippeastrum.tre` is from the aTRAM-ASTRAL analysis in García et al. 2017 and may be run like so:

```
./generateCoalescentTrees_preservetaxonnames.py astral_example_hippeastrum.tre 1000 example_gene_trees.tre
```
