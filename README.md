# POPPY

A personal python scripts for population genomics


## Installation

Initiate virtual environment and install into the venv:

```sh
cd /path/to/your/proj
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install git+https://github.com/ymat2/poppy
poppy --help
# deactivate
```

Alternatively, it can be installed via [uv](https://docs.astral.sh/uv/):

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

See also `poppy --help` / `poppy help <command>`.
