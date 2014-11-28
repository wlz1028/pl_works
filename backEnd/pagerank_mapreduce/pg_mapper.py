import sys

for line in sys.stdin:
    data = line.strip().split('\t')
    node, pg, outlinks = data[0], float(data[1]), data[2:]
    #output each node
    for outlink in outlinks:
        print '%s\t%s' % (str(outlink), str(pg/len(outlinks)))
    #out put outlinks for reduce purposes
    print node + "\toutlinks\t" + "\t".join(outlinks)
