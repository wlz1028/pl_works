import sys

for line in sys.stdin:
    data = line.strip().split('\t')
    page_id, pg, outlinks = data[0], float(data[1]), data[2:]
    #output each outlink page id and its probability
    for outlink in outlinks:
        print '%s\t%s' % (str(outlink), str(pg/len(outlinks)))
    #out put outlinks ids for each page for reducer
    print page_id + "\toutlinks\t" + "\t".join(outlinks)
