# POPPY

A personal python scripts for population genomics


## Installation

```sh
python3 -m pip install git+https://github.com/ymat2/poppy
poppy --help
```

Alternatively, it can be installed via uv:

```sh
uv tool install git+https://github.com/ymat2/poppy
poppy --help
```


## Usage

Example usages:

1. Count number of variants per variant type in single-sample VCF.

```sh
poppy vcfkit --mode count -i <VCF>
```

2. Extract partial sequence from FASTA.

```sh
poppy faskit --mode exract --fasta <fasta> --chrom <chromosome> --pos <position> --range 50
```

3. Remove invariant sites from alignment.

```sh
poppy alnkit --mode trim -i <alignment> -o <outfile> --format fasta
```

See also `poppy help <command>`.
