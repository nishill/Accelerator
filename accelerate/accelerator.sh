
main() {

    hal_path=$1
    ref=$2
    annotation_path=$3
    genomes=$4
    single_copy_cutoff=$5

    hal4dExtract "${hal_path}" "${ref}" "${annotation_path}" 4d_sites.bed

    hal2maf --refGenome "${ref}" --targetGenomes "${genomes}" --noDupes --noAncestors --unique --refTargets 4d_sites.bed $hal_path 4d_sites.maf
    
    # get phylogenetic tree from MAF file
    phylo_tree=`head 4d_sites.maf | grep ^"# hal" | tr -d '# hal '`

    sed -i -e 2d 4d_sites_primates.maf
    
    phyloFit --tree $phylo_tree --subst-mod SSREV --sym-freqs --out-root primate_neutral --msa-format MAF 4d_sites_primates.maf

    base_comp=`halStats --baseComp "${ref},1"`

    modFreqs primate_neutral.mod $base_comp > primate_neutral.modFreqs.mod

    hal2maf $hal_path --refGenome "hg19" --targetGenomes $genomes --onlyOrthologs --noAncestors --refSequence "chr8" "chr8_primates.maf"

    phastCons --target-coverage 0.3 --expected-length 45 --gc 0.409446 --estimate-trees "primate" --msa-format MAF "chr8_primates.maf" primate_neutral.modFreqs.mod --most-conserved primate_cons.bed --no-post-probs

    python ./scripts/multi_single_copy.py < primate_cons.bed > primate.cons.chr8.single.bed

    python ./scripts/find_accelerated_regions.py --hal $hal_path --ref_genome "hg19" --conserved_bed $cons_bed_path --conserved_model primate.cons.mod --non_conserved_model primate.noncons.mod --out_bed accelerated.bed --target_genomes $genomes --accelerated_genomes "hg19" --single_copy_percent_cutoff 0.95

    python ./scripts/check_regions < accelerated.bed

}

main $1 $2 $3 $4 $5
