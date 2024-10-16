def remove_invariant_site(infile, outfile, format):

    f = read_phylip(infile)
    f = remove_invariant_sites(f)

    #if args.output:
    #    outfile = args.output
    #else:
    #    outfile = ".".join(args.input.split(".")[:-1])
    #    outfile = outfile + ".varsites"

    write_phylip(f, outfile, format)


def read_phylip(file):
    seq_dict = dict()
    with open(file) as f:
        next(f)
        for line in f:
            [taxa, seq] = line.rstrip("\n").split()
            seq_dict[taxa] = seq
    return seq_dict


def write_phylip(seq_dict, file, format):
    num_sp = len(seq_dict.keys())
    seq_length = get_value_length(seq_dict)
    if format == "phylip":
        with open(file, "w") as f:
            f.write(str(num_sp)+"\t"+str(seq_length)+"\n")
            for k,v in seq_dict.items():
                f.write(k+"\t"+v+"\n")
    elif format == "fasta":
        with open(file, "w") as f:
            for k,v in seq_dict.items():
                f.write(">"+k+"\n"+v+"\n")


def remove_invariant_sites(dct):
    varsites = {k: [] for k in dct.keys()}
    l = get_value_length(dct)
    lv = 0
    print("\nMSA has", l, "sites.")
    for i in range(l):
        if i == 10000:
            print("\t10000 sites are validated.")
        if i in range(100000, 10000001, 100000):
            print(f"\t{i} sites are validated.")
        if is_varsite(dct, i):
            lv += 1
            for k,v in dct.items():
                varsites[k].append(v[i])
    for k in varsites.keys():
        varsites[k] = ''.join(varsites[k])
    print(str(lv)+"/"+str(l)+" variants are retained after filtering.")
    return varsites


def get_value_length(dct):
    l = [len(v) for v in dct.values()]
    if len(set(l)) == 1:
        return l[0]
    else:
        print("Warning: different length in alignmnet")
        return l[0]


def is_varsite(dct, i):
    l = [v[i] for v in dct.values()]
    return len(set(l)) != 1
