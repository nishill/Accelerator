import sys
from multiprocessing import *

def worker(conserved_length, conserved_range, start, end):

	with open("single_copy_regions_chr8.bed", 'r') as single_copies:

		copied = 0
		for line2 in single_copies:

			line2 = line2.strip().split()	
			chrom2, start2, end2 = line2[0],line2[1],line2[2]
	
			scc_range = set(range(int(start2),int(end2)) )     

			intersecting_positions = scc_range.intersection(conserved_range) 
			
			copied += len(intersecting_positions)

	score = float(copied)/float(conserved_length)
	region = "{}\t{}\t{}\t{}"
	print region.format(chrom2,start, end,score)

		
def find_single_copy_percentage():

	while True:

		line = sys.stdin.readline().strip().split()
		if not line: 

			break

		chrom, start, end = line[0], line[1], line[2]
		conserved_length = int(end) - int(start)
		conserved_range = set(range(int(start),int(end)))

		p = Process(target=worker, args=(conserved_length, conserved_range, start, end) )
		p.start()
		p.join()

def main():

	find_single_copy_percentage()

if __name__=="__main__":
	main()
