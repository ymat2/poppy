import sys

def vcfkit(mode: str, args):

    vcf = args.vcf
    outfile = args.outfile

    if mode == "count":
        from poppy.vcf_count import get_count_variant
        d = get_count_variant(vcf)
        output = args.vcf+"\t"
        output += "\t".join([str(k)+":"+str(v) for k,v in d.items()])
        if outfile:
            with open(outfile, "w") as f:
                f.write(output+"\n")
        else:
            print(output)

    if mode == "select":
        from poppy.vcf_select import select
        if not args.region:
            sys.exit("error: Provide --region to use vcfkit::select.")
        else:
            chrom, pos = args.region.split(":")
            output = select(vcf, chrom, pos)
        if outfile:
            with open(outfile, "w") as f:
                f.write(output+"\n")
        else:
            print(output)
