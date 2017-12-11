import sys
import bx.align.maf
import os
from multiprocessing import *

def format_ratio(num, denom):

	return float(num)/float(denom)

def parse_maf(maf, start, stop, window_size=50, step=1, identity_cutoff=0.9, merge_distance=5):
	"""
	Uses the bx python MAF parser to iterate over MAF columns, measuring identity in sliding windows.
	Nearby windows within merge_distance are merged after all windows are found.
	"""
	
	maf_reader = bx.align.maf.Reader(open(maf))
	matches = []
	# store first component to keep track of chromosome name and alignment start position
	# first component in a MAF is always the reference genome
	# we have to use this instead of the location in case the alignment doesn't start at the same place
	first_comp = None
	for m in maf_reader:
		comp = m.components[0]
		if first_comp is None:
			first_comp = comp
		# maintain mapping of components to genomes
		# this allows for discovery of duplicates in a genome to mask out
		species_map = {i: c.src.split('.')[0] for i, c in enumerate(m.components)}
		species = set(species_map.values())
		accelerated = 0
		for i, column in enumerate(m.column_iter()):
			# declare a dictionary of base index to base
			base_map = {i: x for i, x in enumerate(column)}
			# remove human from column
			column.pop(0)	
			# if this condition is met the region is accelerated
			if len(set(x.upper() for x in column)) == 1 and base_map[0] != base_map[1]:
					accelerated += 1
		
		if accelerated != 0:

			accel_score = float(accelerated) / (stop-start) 
		
			print "chr8\t{}\t{}\t{}".format(start,stop,accel_score)
			
def main():

	#maf_file = "/mnt/nishill/fall/conserv/0.3-45/convert/chr8.maf"
	#cand_hars = "/home/nishill/scripts/chromosome8_accelerated_regions.bed"

	if os.path.isdir("./beds"):
		os.system("rm -r beds")

	if os.path.isdir("./mafs"):
		os.system("rm -r mafs")

	os.system("mkdir beds")
	os.system("mkdir mafs")

	genomes = "panTro4,C57B6J,Pahari_EiJ,hg19,ponAbe2,canFam3,gorGor3,rheMac3,oryCun2,Rattus,oviAri3,bosTau8,felCat8,loxAfr3"
	conserved_model = "/mnt/nishill/fall/conserv/0.3-45/estimate/whole.cons.mod"
	non_conserved_model = "/mnt/nishill/fall/conserv/0.3-45/estimate/whole.noncons.mod"
	#genomes = "hg19,panTro4,ponAbe2,gorGor3,rheMac3"
	#conserved_model = "/mnt/nishill/fall/conserv/0.3-45/convert/primate.cons.mod"
	#non_conserved_model = "/mnt/nishill/fall/conserv/0.3-45/convert/primate.noncons.mod"

	while True:

		line = sys.stdin.readline().strip().split()
		if not line: break

		chrom,start,stop = str(line[0]), str(line[1]), str(line[2])
		length = int(stop) - int(start)

		region = chrom + ':' + start + '-' + stop
		with open("{}.bed".format(region), 'w' ) as bed:
  			bed.write(chrom+'\t'+start+'\t'+stop)
    
		os.system("mv {}.bed beds".format(region))

		hal2maf = "hal2maf --noAncestors --targetGenomes {} --refGenome hg19 --refSequence {} --start {} --length {} /mnt/nishill/data/1509_outgroups.hal mafs/{}.maf"
		os.system( hal2maf.format( genomes, chrom, start, length, region) )

		#parse_maf("mafs/{}.maf".format(region), int(start), int(stop))
		p = Process(target=parse_maf, args=("mafs/{}.maf".format(region), int(start), int(stop)) )
		p.start()
		p.join()

if __name__=="__main__":
	main()
