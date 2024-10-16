import glob
from pathlib import Path

def flag_summary(indir, outfile):

    samples = glob.glob(indir+"/*")
    with open(outfile, "w") as f:
        _header = "sample\tnum_reads\tprop_mapped\n"
        f.write(_header)
        for sample in samples:
            sample = sample.split("/")[-1]
            flag_stat_file = indir+"/"+sample+"/"+sample+".stat"
            print("\t", flag_stat_file)
            stats = get_mapped_reads_info(flag_stat_file)
            f.write(sample+"\t"+"\t".join(stats)+"\n")

    print("\tFinish summarising stats.")


def get_mapped_reads_info(file: Path) -> list:
    num_total_mapped_reads = 0
    prop_properly_mapped = 0
    pattern_total = "total"
    pattern_prop_mapped = "properly paired %"

    with open(file) as f:
        for line in f:
            if pattern_total in line:
                num = line.split("\t")[0]
                num_total_mapped_reads = num
            if pattern_prop_mapped in line:
                num = line.split("\t")[0].rstrip("%")
                prop_properly_mapped = num

    return([str(num_total_mapped_reads), str(prop_properly_mapped)])
