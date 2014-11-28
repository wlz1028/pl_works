import sys

last = None
pg = 0
alpha = 0.8
N = 4
counter = 0

for line in sys.stdin:
    data = line.strip().split('\t')
    node,value = data[0],data[1]
    #If new link detect, print previous link pg
    if last != None and node != last:
        pg = alpha * pg + (1 - alpha) / N
        print '%s\t%s\t%s' % (last,str(pg),outlinks)
        pg =0
    #save outlink info for current node
    if value == "outlinks":
        outlinks = "\t".join(data[2:])
        last = node
        continue
    #Acc values
    pg += float(value)
    last = node
    counter += 1

pg = alpha * pg + (1 - alpha) / N
print '%s\t%s\t%s' % (last,str(pg),outlinks)
