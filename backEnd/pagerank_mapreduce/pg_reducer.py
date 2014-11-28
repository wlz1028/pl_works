import sys

last = None
pg = 0
beta = 0.8
N = 4
counter = 0

for line in sys.stdin:
    data = line.strip().split('\t')
    page_id,value = data[0],data[1]
    #If new page_id detect, print previous page pagerank followed by outlinks
    if last != None and page_id != last:
        pg = beta * pg + (1 - beta) / N
        print '%s\t%s\t%s' % (last,str(pg),outlinks)
        pg =0
    #save outlinks info for current page
    if value == "outlinks":
        outlinks = "\t".join(data[2:])
        last = page_id
        continue
    #Acc values
    pg += float(value)
    last = page_id
    counter += 1

#Print last line
pg = beta * pg + (1 - beta) / N
print '%s\t%s\t%s' % (last,str(pg),outlinks)
