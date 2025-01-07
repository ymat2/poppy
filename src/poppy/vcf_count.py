import gzip
from pathlib import Path


FIELDS = [
    "CHROM",
    "POS",
    "ID",
    "REF",
    "ALT",
    "QUAL",
    "FILTER",
    "INFO",
    "FORMAT",
    "SAMPLE"
]

GT_BIN = {
    "./.":"?",
    ".|.":"?",
    "0/0":"0",
    "0|0":"0",
    "0/1":"1",
    "0|1":"1",
    "1/0":"1",
    "1|0":"1",
    "1/1":"2",
    "1|1":"2",
    "1/2":"3",
    "1|2":"3",
    "1/3":"3",
    "1|3":"3"
}


def is_snp(record: dict) -> bool:
    # <NON_REF> must be replaced by the REF in the ALT field for GVCFs from GATK
    REF = record["REF"]
    ALT = record["ALT"].replace("<NON_REF>", REF)
    return bool(len(REF) == 1 and all(len(alt) == 1 for alt in ALT.split(",")))


def is_mnp(record: dict) -> bool:
    # <NON_REF> must be replaced by the REF in the ALT field for GVCFs from GATK
    REF = record["REF"]
    ALT = record["ALT"].replace("<NON_REF>", REF)
    return bool(len(REF) > 1 and all(len(REF) == len(alt) for alt in ALT.split(",")))


def is_indel(record: dict) -> bool:
    # <NON_REF> must be replaced by the REF in the ALT field for GVCFs from GATK
    REF = record["REF"]
    ALT = record["ALT"].replace("<NON_REF>", REF)
    return bool(any(len(REF) != len(alt) for alt in ALT.split(",")))


def is_homo(record: dict) -> bool:
    GT = record["SAMPLE"].split(":")[0]
    return bool(GT_BIN[GT] == "0" or GT_BIN[GT] == "2")


def is_hetero(record: dict) -> bool:
    GT = record["SAMPLE"].split(":")[0]
    return bool(GT_BIN[GT] == "1")


def is_missing(record: dict) -> bool:
    GT = record["SAMPLE"].split(":")[0]
    return bool(GT_BIN[GT] == "?")


def is_multiallelic(record: dict) -> bool:
    GT = record["SAMPLE"].split(":")[0]
    return bool(GT_BIN[GT] == "3")


def get_count_variant(vcf: Path) -> dict:
    variant_count = {
        "snp": 0,
        "snp_hom": 0,
        "snp_het": 0,
        "mnp": 0,
        "indel": 0,
        "missing": 0,
        "multi": 0
    }

    if vcf.lower().endswith(".gz"):
        handler = gzip.open
    else:
        handler = open

    with handler(vcf, "rt") as f:
        total_variants = 0
        CHUNK_SIZE = 50000
        while 1:
            vcf_chunk = f.readlines(CHUNK_SIZE)
            if not vcf_chunk:
                break
            for line in vcf_chunk:
                total_variants += 1
                if total_variants % CHUNK_SIZE == 0:
                    print("{:d} lines processed.".format(total_variants))

                line = line.rstrip("\n")
                if line and not line.startswith("#"):
                    record = dict(zip(FIELDS, line.split("\t")))
                    if is_multiallelic(record):
                        variant_count["multi"] += 1
                        continue
                    if is_snp(record) & is_homo(record):
                        variant_count["snp"] += 1
                        variant_count["snp_hom"] += 1
                        continue
                    if is_snp(record) & is_hetero(record):
                        variant_count["snp"] += 1
                        variant_count["snp_het"] += 1
                        continue
                    if is_mnp(record):
                        variant_count["mnp"] += 1
                        continue
                    if is_indel(record):
                        variant_count["indel"] += 1
                        continue
                    if is_missing(record):
                        variant_count["missing"] += 1
                        continue

        print("Total {:d} lines processed.".format(total_variants))
    return variant_count
