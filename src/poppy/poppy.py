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

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
