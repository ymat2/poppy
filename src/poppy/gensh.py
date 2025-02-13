from pathlib import Path


def generate_new_sh(outfile: Path, args):

    sh_args = []
    sh_args.append("#$ -S /bin/bash")
    sh_args.append("#$ -cwd")

    if args.memory:
        if args.memory.endswith("G") and int(args.memory.rstrip("G")) >= 64:
            sh_args.append("#$ -l medium")
        elif args.memory.endswith("T"):
            sh_args.append("#$ -l medium")
        sh_args.append("#$ -l s_vmem="+args.memory)
        sh_args.append("#$ -l mem_req="+args.memory)

    if args.time:
        sh_args.append("#$ -l d_rt="+args.time)
        sh_args.append("#$ -l s_rt="+args.time)

    sh_args.append("#$ -o /dev/null")
    sh_args.append("#$ -e /dev/null")

    with open(outfile, "w") as f:
        for arg in sh_args:
            f.write(arg+"\n")
