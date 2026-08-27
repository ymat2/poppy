# POPPY

Miscellaneous python scripts for genomic data


## Installation

Python3 (>=3.12) is required.

```sh
cd /path/to/your/proj
git clone https://github.com/ymat2/poppy.git
```


## Scripts

See `python3 ***.py -h/--help` for each scripts.

### `extract_subseq.py`

Extract partial sequence from FASTA.

```sh
~$ python3 extract_subseq.py -f tests/data/sample.ref.fa -c chr2 -p 10 -r 5
# Chromosome: chr2
# Position: from 5 to 15
ACGTCGCTTGC
-----*-----
```

### `plink2treemix.py`

Convert plink freq file into input file for treemix analysis.

### `remove_invariant_sites.py`

Remove invariant sites from multiple alignment.

```sh
~$ python3 remove_invariant_sites.py -i tests/data/sample.aln.phy -o tests/data/sample.varsites.fa --format fasta

MSA has 30 sites.
25/30 variants are retained after filtering.
```
