import os
from pathlib import Path


sbdirs = [
    "src",
    "bam",
    "out",
    "vcf"
]


def initialize_proj(proj: Path) -> None:
    if not os.path.exists(proj):
        os.mkdir(proj)

    for sbdir in sbdirs:
        dirpath = os.path.join(proj.rstrip("/"), sbdir)
        os.makedirs(dirpath)
