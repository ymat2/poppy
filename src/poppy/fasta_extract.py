from pathlib import Path


def main(args):

    start_position = args.pos - args.range
    end_position = args.pos + args.range

    if args.ref and args.alt:
        variant = "[" + args.ref + "/" + args.alt + "]"
        symbol = "-" * args.range + variant + "-" * args.range
        seq = get_seq(args.fasta, args.chrom, start_position, end_position)
        seq = seq[0:args.range] + variant + seq[args.range+1:]
        # if seq[args.range] != args.ref:
        #     import warnings
        #     warn_msg = "REF allele is not equal to allele position" + str(args.pos)
        #     warnings.warn(warn_msg)
    else:
        symbol = "-" * args.range + "*" + "-" * args.range
        seq = get_seq(args.fasta, args.chrom, start_position, end_position)

    print("# Chromosome:", args.chrom)
    print("# Position: from", start_position, "to", end_position)
    print(seq)
    print(symbol)


def get_alleles(csv: Path, chr: str, pos: int) -> str:
    _ref, _alt = "NA", "NA"
    with open(csv) as f:
        for line in f:
            CHR, POS, REF, ALT = line.split(",")[0:4]
            if CHR == chr and POS == str(pos):
                _ref, _alt = REF, ALT
                break
            else:
                continue
    return (_ref, _alt)


def get_seq(fa: Path, chr: str, start: int, end: int) -> str:
    seq_chr = fasta2chr(fa, chr)
    seq_to_return = seq_chr[start-1:end]
    return seq_to_return


def fasta2chr(fa: Path, chr: str) -> str:
    seq = []
    tmp_header = ""
    with open(fa) as f:
        for l in f:
            if l[0] == ">":
                hdr = l.split()[0][1:]
                tmp_header = hdr
            elif tmp_header == chr:
                seq.append(l.rstrip("\n"))
            else:
                continue
    seq = "".join(seq)
    return seq


if __name__ == "__main__":
    main()
