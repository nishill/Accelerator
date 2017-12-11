

with open("human_specific_for_nick.tsv") as human:

    for line in human:
    
        line = line.strip().split()
        if line[3].startswith('chr8:'):
        
            print '\t'.join(i for i in line)
