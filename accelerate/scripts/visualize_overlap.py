import matplotlib.pyplot as plt
from matplotlib_venn import venn2

def main():

	nicks = []
	with open("constraint_primate_subs_1000_scc_accelerated_chr8.sorted.merged.bed", 'rb+') as nick:
    #with open("1000_scc_accelerated_chr8p.bed", 'rb+') as nick:	
	#with open("1000_scc_accelerated_chr8.bed", 'rb+') as nick:	
	#with open("chromosome8_accelerated_regions.bed", 'rb+') as nick:

		for line in nick:

			line = line.strip().split()	
			start, end = int(line[1]), int(line[2])
			pos = range(start,end)
			nicks.extend(pos)

		
	katies = []
	with open("hg19_accelerated_regions_chr8p.bed", 'rb+') as katie:
	
		for line in katie:
	
			line = line.strip().split()
			start, end = int(line[1]), int(line[2])
			pos = range(start,end)
			katies.extend(pos)	

	nicks = set(nicks)
	katies = set(katies)
	nick_and_katie = nicks.intersection(katies)
	nicks = nicks - nick_and_katie 
	katies = katies - nick_and_katie
	s = ( len(nicks), len(katies), len(nick_and_katie) )
	print (s)
	venn2(subsets=s, set_labels=('Nick', 'Katie'))
	plt.title("Genomic Positions in Nicks-HARs intersected with Katies-HARs") 
	plt.show()

if __name__=="__main__":
	main()
