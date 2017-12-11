import subprocess

def format_ratio(num, denom):

	return float(num)/float(denom)

def get_bases(f):
    
		c = 0
		for l in open(f):
			l = l.split()
			c += int(l[2]) - int(l[1])

		return c

chr8_size = 146364022

subprocess.check_call("bedtools bed12tobed6 -i appris_human_gencodeV27lift37_cds.sorted_chr8.bed > appris_human_gencodeV27lift37_cds.sorted_chr8.flat.bed", shell=True)
subprocess.check_call("sort -k1,1 -k2,2n appris_human_gencodeV27lift37_cds.sorted_chr8.flat.bed > sorted.bed", shell=True)
subprocess.check_call("bedtools merge -d 0 -i sorted.bed > merged_overlap_sorted.bed", shell= True )
subprocess.check_call("bedtools merge -d 50 -i whole_conserved.bed > chr8_conserved_merged.bed", shell=True)
subprocess.check_call("bedtools intersect -a chr8_conserved_merged.bed -b merged_overlap_sorted.bed > overlap_conserved.bed", shell=True)

chr8_conserved_bases = get_bases('chr8_conserved_merged.bed')
chr8_coding_bases = get_bases('merged_overlap_sorted.bed')
cons_bases = get_bases('overlap_conserved.bed')


print "Overall chromosome 8 coverage= {}%".format(format_ratio(chr8_conserved_bases, chr8_size)*100)
print "CDS chromosome 8 coverage= {}%".format(format_ratio(cons_bases, chr8_coding_bases)*100)
