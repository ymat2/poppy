from pathlib import Path

def summary_main(indir: Path, outfile: Path, type: str, suffix: str):

    if type == "flag":
        from poppy.summary_flag import flag_summary
        print("\tSummarizing flag stats...")
        flag_summary(indir, outfile, suffix)

    if type == "bam":
        from poppy.summary_mapping import mapping_summary
        print("\tSummarizing mapping stats...")
        mapping_summary(indir, outfile, suffix)

    if type == "vcf":
        from poppy.summary_vcf import vcf_summary
        print("\tSummarizing VCF stats...")
        vcf_summary(indir, outfile, suffix)
