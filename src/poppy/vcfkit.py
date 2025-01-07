from pathlib import Path

def vcfkit(args):

    if args.count:
        from poppy.vcf_count import get_count_variant
        d = get_count_variant(args.vcf)
        output = args.vcf+"\t"
        output += "\t".join([str(k)+":"+str(v) for k,v in d.items()])
        if args.outfile:
            with open(args.outfile, "w") as f:
                f.write(output+"\n")
        else:
            print(output)
