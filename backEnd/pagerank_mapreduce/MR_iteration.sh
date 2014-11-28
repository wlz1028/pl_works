#! /bin/bash
total=30
echo "" > output.txt
for i in `seq 1 $total`
do
  echo $i >> output.txt
  cat pagerank.txt > tmp.txt
  cat tmp.txt  | python pg_mapper.py  | sort -k1n | python pg_reducer.py > pagerank.txt
  cat pagerank.txt | awk '{print $1 " " $2}' | tr -d '\n' ' '  >> output.txt
  echo "" >> output.txt
done

