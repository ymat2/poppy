import glob
import pandas as pd


def mapping_summary(indir, outfile):

    samples = glob.glob(indir+"/*")
    with open(outfile, "w") as f:

        _header = "sample\tmeandp\tmeancov\tmeandp_nc\tmeancov_nc\tmeandp_nw\tmeancov_nw\n"
        f.write(_header)

        for sample in samples:
            sample = sample.split("/")[-1]
            cov_file = indir+"/"+sample+"/"+sample+".cov"
            stats = summarize_stat(cov_file)
            f.write(sample+"\t"+"\t".join(stats)+"\n")
            print("\t", cov_file)

    print("\tFinish summarising stats.")


def summarize_stat(path):

    df = pd.read_csv(path, sep = "\t")
    df = df[df["numreads"] != 0]

    total_depth = (df["covbases"]*df["meandepth"]).sum()
    total_coverage = (df["covbases"]*df["coverage"]).sum()
    total_covbase = df["covbases"].sum()
    mean_depth = total_depth/total_covbase
    mean_coverage = total_coverage/total_covbase

    df_nc = df[df["#rname"].str.startswith("NC_")]
    total_depth_nc = (df_nc["covbases"]*df_nc["meandepth"]).sum()
    total_coverage_nc = (df_nc["covbases"]*df_nc["coverage"]).sum()
    total_covbase_nc = df_nc["covbases"].sum()
    mean_depth_nc = total_depth_nc/total_covbase_nc
    mean_coverage_nc = total_coverage_nc/total_covbase_nc

    df_nw = df[df["#rname"].str.startswith("NW_")]
    total_depth_nw = (df_nw["covbases"]*df_nw["meandepth"]).sum()
    total_coverage_nw = (df_nw["covbases"]*df_nw["coverage"]).sum()
    total_covbase_nw = df_nw["covbases"].sum()
    mean_depth_nw = total_depth_nw/total_covbase_nw
    mean_coverage_nw = total_coverage_nw/total_covbase_nw

    stats = [mean_depth, mean_coverage, mean_depth_nc, mean_coverage_nc, mean_depth_nw, mean_coverage_nw]
    stats = list(map(str, stats))

    return stats
