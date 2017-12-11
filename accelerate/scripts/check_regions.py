import sys
import os

def main():

	if os.path.isdir("./beds"):

		os.system("rm -r beds")

	if os.path.isdir("./models"):

		os.system("rm -r models")
	
	if os.path.isdir("./mafs"):

		os.system("rm -r mafs")

	os.system("mkdir beds")
	os.system("mkdir models")
	os.system("mkdir mafs")


	#genomes = "C57B6J,Pahari_EiJ,hg19,panTro4,ponAbe2,canFam3,gorGor3,rheMac3,oryCun2,Rattus,oviAri3,bosTau8,felCat8,loxAfr3"
	#conserved_model = "/mnt/nishill/fall/conserv/0.3-45/estimate/whole.cons.mod"
	#non_conserved_model = "/mnt/nishill/fall/conserv/0.3-45/estimate/whole.noncons.mod"
	genomes = "hg19,panTro4,ponAbe2,gorGor3,rheMac3"
	conserved_model = "/mnt/nishill/fall/conserv/0.3-45/convert/primate.cons.mod"
	non_conserved_model = "/mnt/nishill/fall/conserv/0.3-45/convert/primate.noncons.mod"


	while True:
		
		line = sys.stdin.readline().strip().split()		
		if not line: break

		chrom,start,stop = str(line[0]), str(line[1]), str(line[2])

		length = int(stop) - int(start)

		region = chrom + ':' + start + '-' + stop
		with open("{}.bed".format(region), 'w' ) as bed:
	
			bed.write(chrom+'\t'+start+'\t'+stop)
			
		os.system("mv {}.bed beds".format(region))

		print 
		print "input region: " + region
		print 

		print "Running hal2maf..."
		#hal2maf = "hal2maf --noAncestors --targetGenomes {} --refGenome rheMac3 --refSequence {} --start {} --length {} /mnt/nishill/data/1509_outgroups.hal mafs/{}.maf"
		hal2maf = "hal2maf --noAncestors --targetGenomes {} --refGenome hg19 --refSequence {} --start {} --length {} /mnt/nishill/data/1509_outgroups.hal mafs/{}.maf"
		os.system( hal2maf.format( genomes, chrom, start, length, region) )

		print "Running phyloFit..."
		#os.system("phyloFit --init-model {} --scale-subtree rheMac3:loss --out-root {} ./mafs/{}.maf".format(conserved_model, region, region ) )
		os.system("phyloFit --init-model {} --scale-subtree hg19:loss --out-root {} ./mafs/{}.maf".format(conserved_model, region, region ) )

		os.system("mv {}.mod ./models".format(region))

		print "Running phastOdds..."
		phastOdds = "phastOdds --output-bed --features ./beds/{}.bed --background-mods {} --feature-mods ./models/{}.mod ./mafs/{}.maf"
		os.system(phastOdds.format(region, conserved_model, region, region) )

		print 

if __name__=="__main__":
	main()
