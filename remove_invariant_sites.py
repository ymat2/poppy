import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help = "PATH to input alignment file. PHYLIP from vcf2phylip is assumed.")
    parser.add_argument("-o", "--output", help = "PATH to output alignment file.")
    parser.add_argument("--format", choices = ["fasta", "phylip"], default = "phylip", help = "Format of output alignment.")
    args = parser.parse_args()

    f = read_phylip(args.input)
    f = remove_invariant_sites(f)
    write_phylip(f, args.output, args.format)


def read_phylip(file: Path):
    seq_dict = {}
    with open(file) as f:
        next(f)
        for line in f:
            [taxa, seq] = line.rstrip("\n").split()
            seq_dict[taxa] = seq
    return seq_dict


def write_phylip(seq_dict: dict, file: Path, format: str):
    num_sp = len(seq_dict.keys())
    seq_length = get_value_length(seq_dict)
    if format == "phylip":
        with open(file, "w") as f:
            f.write(str(num_sp)+"\t"+str(seq_length)+"\n")
            f.writelines(k+"\t"+v+"\n" for k,v in seq_dict.items())
    elif format == "fasta":
        with open(file, "w") as f:
            f.writelines(">"+k+"\n"+v+"\n" for k,v in seq_dict.items())


def remove_invariant_sites(dct: dict):
    varsites = {k: [] for k in dct}
    l = get_value_length(dct)
    lv = 0
    print("\nMSA has", l, "sites.")
    for i in range(l):
        if i>0 and i % 50000 == 0:
            print(f"\t{i:d} sites are validated.")
        if is_varsite(dct, i):
            lv += 1
            for k,v in dct.items():
                varsites[k].append(v[i])
    for k in varsites:
        varsites[k] = ''.join(varsites[k])
    print(str(lv)+"/"+str(l)+" variants are retained after filtering.")
    return varsites


def get_value_length(dct: dict):
    l = [len(v) for v in dct.values()]
    if len(set(l)) == 1:
        return l[0]
    else:
        print("Warning: different length in alignmnet")
        return l[0]


def is_varsite(dct: dict, i: int):
    l = [v[i] for v in dct.values()]
    return len(set(l)) != 1


if __name__ == "__main__":
    main()
