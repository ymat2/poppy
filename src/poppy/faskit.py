
def faskit(mode: str, args):

    if mode == "extract":
        from poppy.fasta_extract import main
        main(args)
