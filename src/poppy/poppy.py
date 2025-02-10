import argparse
import time

from importlib import metadata


__version__ = metadata.version("poppy")

parser = argparse.ArgumentParser(
    description = "Miscellaneous python scripts for population genomics.",
    usage = "poppy <commands> [-h/--help] [Options]"
)
parser.add_argument("-V", "--version", action = "version", version = __version__,
                    help = "Show the version number")
subparsers = parser.add_subparsers(title = "Commands", metavar = "")


def command_summary(args):
    print("Command poppy::summary starts.")
    start = time.time()
    from poppy.summary_main import summary_main
    summary_main(args.mode, args.indir, args.outfile, args.suffix)
    print("Command poppy::summary ends. Time elapsed: {:,} sec.".format(int(time.time() - start)))


def command_vcfkit(args):
    print("Command poppy::vcfkit starts.")
    start = time.time()
    from poppy.vcfkit import vcfkit
    vcfkit(args.mode, args)
    print("Command poppy::vcfkit ends. Time elapsed: {:,} sec.".format(int(time.time() - start)))


def command_alnkit(args):
    print("Command poppy::alnkit starts.")
    start = time.time()
    from poppy.alnkit import alnkit
    print("\tRemoving invariant sites...")
    alnkit(args.mode, args.aln, args.outfile, args.format)
    print("Command poppy::alnkit ends. Time elapsed: {:,} sec.".format(int(time.time() - start)))


def command_faskit(args):
    from poppy.faskit import faskit
    faskit(args.mode, args)


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
    parser_summary.add_argument("-m", "--mode", choices = ["flag", "bam", "vcf"],
                                help = "Output filetype to summarize.")
    parser_summary.add_argument("-i", "--indir",
                                help = "PATH to directory that contains stat files.")
    parser_summary.add_argument("-o", "--outfile",
                                help = "PATH to output file.")
    parser_summary.add_argument("--suffix",
                                help = "Suffix of files to summary. (e.g. vcf.stat, cov, etc.)")
    parser_summary.set_defaults(handler = command_summary)

    # vcfkit
    help_txt = "Handle single VCF file."
    help_txt += " See `poppy vcfkit -h`."
    parser_vcfkit = subparsers.add_parser("vcfkit", help = help_txt)
    parser_vcfkit.add_argument("-m", "--mode", choices = ["count", "select"],
                               help = "Count number of each genotype.")
    parser_vcfkit.add_argument("-i", "--infile", dest = "vcf",
                               help = "Input VCF file name. Can be gzipped.")
    parser_vcfkit.add_argument("-r", "--region",
                               help = "Position to select (format: `Chromosome:Position`).")
    parser_vcfkit.add_argument("-o", "--outfile",
                               help = "PATH to output file (default: stdout).")
    parser_vcfkit.set_defaults(handler = command_vcfkit)

    # alnkit
    help_txt = "Handle an alignment file."
    help_txt += " See `poppy alnkit -h`."
    parser_alnkit = subparsers.add_parser("alnkit", help = help_txt)
    parser_alnkit.add_argument("-m", "--mode", choices = ["trim"],
                               help = "Remove invariant sites.")
    parser_alnkit.add_argument("-i", "--infile", dest = "aln",
                               help = "PATH to input alignment file. PHYLIP from vcf2phylip is assumed.")
    parser_alnkit.add_argument("-o", "--outfile",
                               help = "PATH to output alignment file.")
    parser_alnkit.add_argument("--format", choices = ["fasta", "phylip"],
                               help = "Format of output alignment.")
    parser_alnkit.set_defaults(handler = command_alnkit)

    # faskit
    help_txt = "Handle a FASTA file."
    help_txt += " See `poppy faskit -h`."
    parser_faskit = subparsers.add_parser("faskit", help = help_txt)
    parser_faskit.add_argument("-m", "--mode", choices = ["extract"],
                               help = "Extract partial sequence from FASTA file.")
    parser_faskit.add_argument("-f", "--fasta",
                               help  = "PATH to FASTA file of genome sequence.")
    parser_faskit.add_argument("-c", "--chrom",
                               help = "Chromosome or contig name.")
    parser_faskit.add_argument("-p", "--pos", type = int,
                               help = "Position of variant.")
    parser_faskit.add_argument("-r", "--range", type = int,
                               help = "Range of sequences too show around variant.")
    parser_faskit.add_argument("--ref", help = "Reference nucleotide.")
    parser_faskit.add_argument("--alt", help = "Alternative variant.")
    parser_faskit.set_defaults(handler = command_faskit)

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
