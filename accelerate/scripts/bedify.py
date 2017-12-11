with open("human_specific_for_nick.chr8.tsv") as andrews:

    for line in andrews:
    
        line = line.strip().split()
    
        print line[3].replace(':','\t').replace('-','\t')

