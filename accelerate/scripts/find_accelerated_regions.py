"""
Run acceleration tests on each region in the conserved_bed.
"""

import os
import argparse
import itertools
from ete3 import Tree
from collections import OrderedDict
#from jobTree.scriptTree.target import Target
#from jobTree.scriptTree.stack import Stack
from sonLib.bioio import system, TempFileTree, popenCatch, setLoggingFromOptions, logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hal', help='HAL alignment file.', required=True) 
    parser.add_argument('--ref_genome', help='Reference genome.', required=True)
    parser.add_argument('--conserved_bed', help='Conserved BED file.', required=True)
    parser.add_argument('--conserved_model', help='Original conserved model', required=True)
    parser.add_argument('--non_conserved_model', help='Original nonconserved model.', required=True)
    parser.add_argument('--out_bed', help='output BED', required=True)
    parser.add_argument('--target_genomes', nargs='+', required=True, help='target genomes')
    parser.add_argument('--accelerated_genomes', nargs='+', required=True, help='target genomes')
    parser.add_argument('--single_copy_percent_cutoff', default=0.98, type=float,
                        help='Percent of region that must be single copy before we test it for acceleration')
    
    return vars(parser.parse_args())

def conserved_model_contains_sufficient_outgroups(model, accelerated_genomes, outgroup_genomes, percent_outgroups=0.5):
    """makes sure that this region, when extracted, has at least percent_outgroups present"""
    lines = open(model).readlines()
    t = Tree(lines[-1].split('TREE: ')[1], format=1)
    outgroup_nodes = set(t.get_leaf_names()) - set(accelerated_genomes)
    return format_ratio(len(outgroup_nodes), len(outgroup_genomes)) >= percent_outgroups


def extract_conserved_region(args, chrom, start, stop):
		
		"""extract maf for a specific region and the target genomes"""
		
		maf_path = os.path.join('extracted-mafs', chrom.strip()+ ":"+start+"-"+stop+'.maf')
		size = int(stop) - int(start)
		cmd = 'hal2maf --noAncestors --targetGenomes {} --refGenome {} --refSequence {} --start {} --length {} {} {}'
		cmd = cmd.format(','.join(args["target_genomes"]), args["ref_genome"], chrom, start, size, args["hal"], maf_path)
		system(cmd)
		with open("log",'a') as log: 
			log.write('extracted MAF for region {}:{}-{}\n'.format(chrom, start, stop))

		return maf_path

def get_region_specific_model( conserved_model, accelerated_genomes, maf_path):

    cmd = 'phyloFit --init-model {} --scale-subtree {}:loss --out-root tmp {}'
    cmd = cmd.format(conserved_model,accelerated_genomes[0],maf_path )
    print ("running phyloFit: " + cmd )
    system(cmd)

def get_rescaled_model(maf_path):

    cmd = 'phyloFit --init-model tmp.mod --scale-only --out-root rescaled_conserved_region {}'
    cmd = cmd.format(maf_path)
    print ("running phyloFit: " + cmd)
    system(cmd)

def get_output_bed(conserved_bed, rescaled_model, conserved_model, maf_path):

	arg_bed = "temp-beds/temp-"+maf_path.replace("extracted-mafs/","").replace(".maf",".bed")
	with open( arg_bed, 'a') as tempbed:
		
		tempbed.write(conserved_bed)
  
	cmd = 'phastOdds --output-bed --features {} --background-mods {} --feature-mods {} {} > ' + "beds/"+maf_path.replace("extracted-mafs/","").replace(".maf",".bed")
	#cmd = 'phastOdds --output-bed --features {} --background-mods {} --feature-mods rescaled_conserved_region.mod {} > ' + "beds/"+maf_path.replace("extracted-mafs/","").replace(".maf",".bed")
	cmd = cmd.format(arg_bed,rescaled_model,conserved_model,maf_path )
	print ( "running phastOdds: " + cmd )
	system(cmd)


def main():

	args = parse_args()

	with open(args["conserved_bed"]) as bedfile:
		
		for line in bedfile:
			
			data = line.strip().split()
			chrom,start,stop,score = data[0],data[1],data[2],data[3]
			
			# do not test a region if it is not at least single_copy_percent_cutoff
			if float(score) <= args["single_copy_percent_cutoff"]:
				
				with open("log",'a') as log:
					log.write('locus {}:{}-{} has insufficient single copy percentage {}\n'.format(chrom, start, stop, score))
				
				continue
			
			# extract region MAF
			maf_path = extract_conserved_region(args, chrom, start, stop)
			# get region specific conserved model 
			get_region_specific_model(args["conserved_model"],args["accelerated_genomes"],maf_path )
			# should we continue? If the region specific model was generated then yes, otherwise no
			if os.path.exists("./tmp.mod"):
			
				# rescale the region specific conserved model
				get_rescaled_model(maf_path)	
				if os.path.exists("./rescaled_conserved_region.mod"):
        	# perform log odds and get output bed
					get_output_bed(line, "./rescaled_conserved_region.mod",args["conserved_model"], maf_path )
			
				system("rm ./rescaled_conserved_region.mod" )	
				system("rm ./tmp.mod")
			
			else:
				
				with open("log",'a') as log:
					log.write('locus {}:{}-{} has insufficient outgroups'.format(chrom, start, stop))



if __name__=="__main__":
	main()

