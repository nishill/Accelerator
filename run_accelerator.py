import argparse
import subprocess

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--hal', help='HAL alignment file.', required=True) 
    parser.add_argument('--ref-genome', help='Reference genome to test acceleration on.', required=True)
    parser.add_argument('--annotations', help='Gene annotations for your reference genome.', required=True)
    parser.add_argument('--target-genomes', nargs='+', required=True, help='target genomes')
    parser.add_argument('--single-copy-cutoff', default=0.95, type=float,
                        help='Percent of region that must be single copy before we test it for acceleration')
 
    return vars(parser.parse_args())

def main():

    args = parse_args()

    cmd = "./accelerate/accelerator.sh {} {} {} {} {}"
    cmd = cmd.format(args["hal"],args["ref-genome"],args["annotations"],args["target-genomes"], args["single-copy-cutoff"])

    subprocess.check_call(cmd, shelll=True)

if __name__=="__main__":
	
    main()
