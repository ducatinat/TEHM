#!/bin/bash
# usage ./ruffo.sh > tests.txt and dont forget to change target
whois arcadeusops.com  
nslookup -type=any arcadeusops.com
host arcadeusops.com
host -t ns arcadeusops.com
host -l ns1.arcadeusops.com
host -t mx arcadeusops.com
dig target.com
