import sys
import bx.align.maf
import os
from multiprocessing import *
from collections import *
import json 

def weak_or_strong(ref_base, tgt_base):
    """Is this substitution weak->strong, strong->weak, weak->weak, strong->strong?"""
    if ref_base in ['A', 'T'] and tgt_base in ['G', 'C']:
        return 'weak_to_strong'
    elif ref_base in ['G', 'C'] and tgt_base in ['A', 'T']:
        return 'strong_to_weak'
    elif (ref_base == 'A' and tgt_base == 'T') or (ref_base == 'T' and tgt_base == 'A'):
        return 'weak_to_weak'
    else:
        return 'strong_to_strong'


def parse_maf(maf, chrom, start, stop):
    """
    Report the % identity found from the reference in this MAF to every other species.
    """
    maf_reader = bx.align.maf.Reader(open(maf))
    result_dict = defaultdict(lambda: Counter())  # keep track of mismatches -- weak or strong?
    # result_dict is of the form genome -> {'weak_to_strong': #, 'strong_to_weak': #,
    # 'strong_to_strong': #, 'weak_to_weak': #}
    first_comp = None
    ref_base_counter = 0  # keep track of total ref bases evaluated
    for m in maf_reader:
        # maintain mapping of components to genomes
        species_map = {i: c.src.split('.')[0] for i, c in enumerate(m.components)}
        for column in m.column_iter():
            ref_base = column[0].upper()  # human is always the first
            if ref_base == '-':
                continue
            ref_base_counter += 1
            for i in xrange(1, len(column)):
                tgt_base = column[i].upper()
                if tgt_base == '-':
                    continue
                if ref_base == tgt_base:
                    continue
                species = species_map[i]
                r = weak_or_strong(ref_base, tgt_base)
                result_dict[species][r] += 1
    overall_mismatch_rate = {x: 1.0 * sum(y.values()) / ref_base_counter for x, y in result_dict.iteritems()}
    return result_dict, overall_mismatch_rate

def main():

  #maf_file = "/mnt/nishill/fall/conserv/0.3-45/convert/chr8.maf"
  #cand_hars = "/home/nishill/scripts/chromosome8_accelerated_regions.bed"

  if os.path.isdir("./mafs"):
    os.system("rm -r mafs")

  os.system("mkdir mafs")

  genomes = "panTro4,C57B6J,Pahari_EiJ,hg19,ponAbe2,canFam3,gorGor3,rheMac3,oryCun2,Rattus,oviAri3,bosTau8,felCat8,loxAfr3"
  conserved_model = "/mnt/nishill/fall/conserv/0.3-45/estimate/whole.cons.mod"
  non_conserved_model = "/mnt/nishill/fall/conserv/0.3-45/estimate/whole.noncons.mod"
  #genomes = "hg19,panTro4,ponAbe2,gorGor3,rheMac3"
  #conserved_model = "/mnt/nishill/fall/conserv/0.3-45/convert/primate.cons.mod"
  #non_conserved_model = "/mnt/nishill/fall/conserv/0.3-45/convert/primate.noncons.mod"

  iterator = 0
  mismatch_rates = {}
  #while iterator < 50:
  while True:

    line = sys.stdin.readline().strip().split()
    if not line: break

    chrom,start,stop = str(line[0]), str(line[1]), str(line[2])
    length = int(stop) - int(start)

    region = chrom + ':' + start + '-' + stop

    hal2maf = "hal2maf --noAncestors --targetGenomes {} --refGenome hg19 --refSequence {} --start {} --length {} /mnt/nishill/data/1509_outgroups.hal mafs/{}.maf"
    os.system( hal2maf.format( genomes, chrom, start, length, region) )

    result_dict, overall_mismatch_rate = parse_maf("mafs/{}.maf".format(region), chrom, int(start), int(stop))
    #p = Process(target=parse_maf, args=("mafs/{}.maf".format(region), int(start), int(stop)) )
    #p.start()
    #p.join()
    
    #if overall_mismatch_rate != None and "panTro4" in overall_mismatch_rate:
    #if overall_mismatch_rate != None and "panTro4" in overall_mismatch_rate and "ponAbe2" in overall_mismatch_rate and "gorGor3" in overall_mismatch_rate and "rheMac3" in overall_mismatch_rate:
    if overall_mismatch_rate != None and "panTro4" in overall_mismatch_rate and "ponAbe2" in overall_mismatch_rate and "gorGor3" in overall_mismatch_rate and "rheMac3" in overall_mismatch_rate and "Rattus" in overall_mismatch_rate and "Pahari_EiJ" in overall_mismatch_rate and "canFam3" in overall_mismatch_rate and "felCat8" in overall_mismatch_rate and "C57B6J" in overall_mismatch_rate and "oviAri3" in overall_mismatch_rate and "bosTau8" in overall_mismatch_rate:
      mismatch_rates[region] = overall_mismatch_rate
      print "chr8\t{}\t{}\t{}".format(start,stop,overall_mismatch_rate["panTro4"], result_dict["panTro4"]["strong_to_weak"])


    iterator += 1

  with open('species.data.json', 'w') as fp:
    json.dump(mismatch_rates, fp)

  with open('species_subs.data.json', 'w') as fp:
    json.dump(result_dict, fp)

if __name__=="__main__":
  main()

