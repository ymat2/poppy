import glob


def vcf_summary(indir, outfile):

    samples = glob.glob(indir+"/*")
    with open(outfile, "w") as f:

        _header = "sample\tn_record\tn_snp\tn_mnp\tn_indel\tn_other\tts\ttv\ttstv_ratio\tdp_min\tdp_max\n"
        f.write(_header)

        for sample in samples:
            sample = sample.split("/")[-1]
            vcfstat = indir+"/"+sample+"/"+sample+".q.vcf.stat"  # should be specified as argument
            stats = summarize_vcfstat(vcfstat)
            f.write(sample+"\t"+"\t".join(stats)+"\n")
            print("\t", vcfstat)

    print("\tFinish summarising VCF stats.")


def summarize_vcfstat(path):

    with open(path) as f:
        sn = dict()
        dps = list()
        for line in f:
            if line.startswith("SN"):
                tabs = line.rstrip("\n").split("\t")
                sn[tabs[-2]] = tabs[-1]

            if line.startswith("TSTV"):
                tabs = line.rstrip("\n").split("\t")
                ts, tv, tstv_ratio = tabs[2], tabs[3], tabs[4]

            if line.startswith("DP"):
                dp = line.rstrip("\n").split("\t")[2]
                dps.append(int(dp.lstrip(">")))  # in case of >500

        #print(sn)
        n_record = sn["number of records:"]
        n_snp = sn["number of SNPs:"]
        n_mnp = sn["number of MNPs:"]
        n_indel = sn["number of indels:"]
        n_other = sn["number of others:"]
        dp_min, dp_max = min(dps), max(dps)

    stats = [n_record, n_snp, n_mnp, n_indel, n_other, ts, tv, tstv_ratio, dp_min, dp_max]
    stats = list(map(str, stats))

    return stats
