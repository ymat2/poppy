import gzip
from pathlib import Path

from poppy.vcf_count import FIELDS


def select(vcf: Path, chrom: str, pos: str) -> str:
    selected_line = ""
    if vcf.lower().endswith(".gz"):
        handler = gzip.open
    else:
        handler = open

    with handler(vcf, "rt") as f:
        CHUNK_SIZE = 50000
        while 1:
            vcf_chunk = f.readlines(CHUNK_SIZE)
            if not vcf_chunk:
                break
            for line in vcf_chunk:
                line = line.rstrip("\n")
                if line and not line.startswith("#"):
                    record = dict(zip(FIELDS, line.split()))
                    if record["CHROM"] == chrom and record["POS"] == pos:
                        selected_line =  line
                        break
    return selected_line
