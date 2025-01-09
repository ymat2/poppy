from pathlib import Path

def vcfkit(mode: str, vcf: Path, outfile: Path):

    if mode == "count":
        from poppy.vcf_count import get_count_variant
        d = get_count_variant(vcf)
        output = vcf+"\t"
        output += "\t".join([str(k)+":"+str(v) for k,v in d.items()])
        if outfile:
            with open(outfile, "w") as f:
                f.write(output+"\n")
        else:
            print(output)
