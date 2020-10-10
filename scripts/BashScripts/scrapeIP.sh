#!/bin/bash

wget www.savills.com.hk

cat index.html | grep -o 'http://[^"]*' | cut -d "/" -f 3 | sort -u > list.txt

for url in $(cat list.txt); do host $url; done | grep "has address" | cut -d " " -f 4 | sort -u