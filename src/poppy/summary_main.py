from pathlib import Path

def summary_main(mode: str, indir: Path, outfile: Path, suffix: str):

    if mode == "flag":
        from poppy.summary_flag import flag_summary
        print("\tSummarizing flag stats...")
        flag_summary(indir, outfile, suffix)

    if mode == "bam":
        from poppy.summary_mapping import mapping_summary
        print("\tSummarizing mapping stats...")
        mapping_summary(indir, outfile, suffix)

    if mode == "vcf":
        from poppy.summary_vcf import vcf_summary
        print("\tSummarizing VCF stats...")
        vcf_summary(indir, outfile, suffix)
