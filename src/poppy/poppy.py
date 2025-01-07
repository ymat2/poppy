import argparse
import time
import os


parser = argparse.ArgumentParser(
    description = "Miscellaneous python scripts for population genomics.",
    usage = "poppy <commands> [-h/--help] [Options]"
)
subparsers = parser.add_subparsers(title = "Commands", metavar = "")


def command_summary(args):
    print("Command poppy::summary starts.")
    start = time.time()
    from poppy.summary_main import summary_main
    summary_main(args.indir, args.outfile, args.type, args.suffix)
    print("Command poppy::summary ends. Time elapsed: {:,} sec.".format(int(time.time() - start)))


def command_vcfkit(args):
    print("Command poppy::vcfkit starts.")
    start = time.time()
    from poppy.vcfkit import vcfkit
    vcfkit(args)
    print("Command poppy::vcfkit ends. Time elapsed: {:,} sec.".format(int(time.time() - start)))


def command_remove_invariant_site(args):
    print("Command poppy::remove_invariant_site starts.")
    start = time.time()
    from poppy.remove_invariant_site import remove_invariant_site
    print("\tRemoving invariant sites...")
    remove_invariant_site(args.infile, args.outfile, args.format)
    print("Command poppy::remove_invariant_site ends. Time elapsed: {:,} sec.".format(int(time.time() - start)))


def command_extract_seq(args):
    from poppy.extract_seq import main
    main(args)


def command_help(args):
    if args.command == "self":
        parser.print_help()
    else:
        print(parser.parse_args([args.command, '--help']))


def main():

    # summary
    help_txt = "Scan directory to summarize stat files."
    help_txt += " See `poppy summary -h`."
    parser_summary = subparsers.add_parser("summary", help = help_txt)
    parser_summary.add_argument("-i", "--indir",
                                help = "PATH to directory that contains stat files.")
    parser_summary.add_argument("-o", "--outfile",
                                help = "PATH to output file.")
    parser_summary.add_argument("-t", "--type", choices = ["flag", "bam", "vcf"],
                                help = "Output filetype to summarize.")
    parser_summary.add_argument("--suffix",
                                help = "Suffix of files to summary. (e.g. vcf.stat, cov, etc.)")
    parser_summary.set_defaults(handler = command_summary)

    # vcfkit
    help_txt = "Handle single VCF file."
    help_txt += " See `poppy vcflit -h`."
    parser_vcfkit = subparsers.add_parser("vcfkit", help = help_txt)
    parser_vcfkit.add_argument("-i", "--infile", dest = "vcf",
                               help = "Input VCF file name. Can be gzipped.")
    parser_vcfkit.add_argument("-o", "--outfile",
                               help = "PATH to output file (stdout by default).")
    parser_vcfkit.add_argument("--count", action = "store_true",
                               help = "Count number of each genotype.")
    parser_vcfkit.set_defaults(handler = command_vcfkit)

    # remove_invariant_site
    help_txt = "Remove invariant sites from alignment."
    help_txt += " See `poppy remove_invariant_site -h`."
    parser_ris = subparsers.add_parser("remove_invariant_site", help = help_txt)
    parser_ris.add_argument("-i", "--infile",
                            help = "PATH to input alignment file. PHYLIP from vcf2phylip is assumed.")
    parser_ris.add_argument("-o", "--outfile",
                            help = "PATH to output alignment file.")
    parser_ris.add_argument("--format", choices = ["fasta", "phylip"],
                            help = "Format of output alignment.")
    parser_ris.set_defaults(handler = command_remove_invariant_site)

    # extract_seq
    help_txt = "Extract partial sequence around variant."
    help_txt += " See `poppy extract_seq -h`."
    parser_exs = subparsers.add_parser("extract_seq", help = help_txt)
    parser_exs.add_argument("-f", "--fasta",
                            help  = "PATH to FASTA file of genome sequence.")
    parser_exs.add_argument("-c", "--chrom",
                            help = "Chromosome or contig name.")
    parser_exs.add_argument("-p", "--pos", type = int,
                            help = "Position of variant.")
    parser_exs.add_argument("-r", "--range", type = int,
                            help = "Range of sequences too show around variant.")
    parser_exs.add_argument("--ref", help = "Reference nucleotide.")
    parser_exs.add_argument("--alt", help = "Alternative variant.")
    parser_exs.set_defaults(handler = command_extract_seq)

    # help
    help_txt = "Show help for commands."
    help_txt += " e.g. `poppy help summary`."
    parser_help = subparsers.add_parser("help", help = help_txt)
    parser_help.add_argument("command", nargs = "?", default = "self",
                             help = "Command to show help message.")
    parser_help.set_defaults(handler = command_help)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
