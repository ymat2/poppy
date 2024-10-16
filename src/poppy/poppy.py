import argparse
import time


def command_summary(args):
    print("Command poppy::summary starts.")
    start = time.time()
    if args.type == "flag":
        from poppy.flag_summary import flag_summary
        print("\tSummarizing flag stats...")
        flag_summary(args.indir, args.outfile)
    if args.type == "bam":
        from poppy.mapping_summary import mapping_summary
        print("\tSummarizing mapping stats...")
        mapping_summary(args.indir, args.outfile)
    if args.type == "vcf":
        from poppy.vcf_summary import vcf_summary
        print("\tSummarizing VCF stats...")
        vcf_summary(args.indir, args.outfile)
    print("Command poppy::summary ends. Time elapsed: {:,} sec.".format(int(time.time() - start)))


def command_remove_invariant_site(args):
    print("Command poppy::remove_invariant_site starts.")
    start = time.time()
    from poppy.remove_invariant_site import remove_invariant_site
    print("\tRemoving invariant sites...")
    remove_invariant_site(args.infile, args.outfile, args.format)
    print("Command poppy::remove_invariant_site ends. Time elapsed: {:,} sec.".format(int(time.time() - start)))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # summary
    help_txt = "Summary stat files to generate tsv."
    help_txt += " See `poppy summary -h`"
    parser_summary = subparsers.add_parser("summary", help = help_txt)
    parser_summary.add_argument("-i", "--indir",
                                help = "PATH to directory that contains stat files.")
    parser_summary.add_argument("-o", "--outfile",
                                help = "PATH to output file.")
    parser_summary.add_argument("-t", "--type", choices = ["flag", "bam", "vcf"],
                                help = "Output filetype to summarize.")
    parser_summary.set_defaults(handler = command_summary)

    # remove_invariant_site
    help_txt = "Remove invariant sites from alignment."
    help_txt += " See `poppy remove_invariant_site -h`"
    parser_ris = subparsers.add_parser("remove_invariant_site", help = help_txt)
    parser_ris.add_argument("-i", "--infile",
                            help = "PATH to input alignment file. PHYLIP from vcf2phylip is assumed.")
    parser_ris.add_argument("-o", "--outfile",
                            help = "PATH to output alignment file.")
    parser_ris.add_argument("--format", choices = ["fasta", "phylip"],
                            help = "Format of output alignment.")
    parser_ris.set_defaults(handler = command_remove_invariant_site)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
