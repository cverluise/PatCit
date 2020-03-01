#!/bin/bash

#gsutil cp "gs://patstat_2018b/Patstat 2018b/data_PATSTAT_Global_2018_Autumn_09/tls214*" "./"
#gsutil cp "gs://patstat_2018b/Patstat 2018b/data_PATSTAT_Global_2018_Autumn_10/tls214*" "./"

find "$1"/*.zip | parallel unzip -o
echo "UNZIP: DONE"
mkdir -p "$1"/small_chunks
parallel split -l100000 "$1/tls214_part0{}.txt" "$1/small_chunks/tls214_part0{}.txt.sub-" ::: 1 2 3 4 5
echo "SPLIT: DONE"
python3 ./bin/rename-tls214.py "$1"/small_chunks/
echo "RENAME: DONE"
for file in $(find "$1"/small_chunks/*aa.txt); do
  sed -i '' 1d "$file"  # remove header(only *aa have one)
done
echo "REMOVE HEADER: DONE"
find "$1"/small_chunks/*.txt | parallel gzip
echo "GZIP: DONE"
find "$1"/*.txt | parallel rm
echo "CLEAN: DONE"
