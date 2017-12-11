hal_path="/mnt/nishill/data/1509_outgroups.hal"
annotation_path="/mnt/nishill/fall/conserv/4DExtract/appris_human_gencodeV27lift37_cds.sorted.bed"

hal4dExtract $hal_path "hg19" $annotation_path 4d_sites.bed

phylo_tree="((((hg19:0.00642915,panTro4:0.00638042)1:0.00217637,gorGor3:0.00882142)1:0.00935116,ponAbe2:0.0185056)1:0.00440069,rheMac3:0.007);"

bed_path="/mnt/nishill/fall/conserv/0.3-45/4DExtract/4d_sites.bed"
genomes="hg19,panTro4,ponAbe2,gorGor3,rheMac3"

hal2maf --refGenome "hg19" --targetGenomes $genomes --noDupes --noAncestors --unique --refTargets $bed_path $hal_path 4d_sites_primates.maf

sed -i -e 2d 4d_sites_primates.maf

phyloFit --tree $phylo_tree --subst-mod SSREV --sym-freqs --out-root primate_neutral --msa-format MAF 4d_sites_primates.maf


modFreqs primate_neutral.mod 0.295089 0.204785 0.204661 0.295466 > primate_neutral.modFreqs.mod

hal2maf $hal_path --refGenome "hg19" --targetGenomes $genomes --onlyOrthologs --noAncestors --refSequence "chr8" "chr8_primates.maf"

phastCons --target-coverage 0.3 --expected-length 45 --gc 0.409446 --estimate-trees "primate" --msa-format MAF "chr8_primates.maf" primate_neutral.modFreqs.mod --most-conserved primate_cons.bed --no-post-probs

python multi_single_copy.py < primate_cons.bed > primate.cons.chr8.single.bed
