#!/bin/bash

# Python Offensive PenTesting: - All rights reserved Nathan W Jones nathan.jones@arcadeusops.com

# don't forget to chmod 755 dnszone.sh
# usgage is ./dnszone.sh target.com


# Simple Zone Transfer Bash Script
# $1 is the first argument given after the bash script
# Check if argument was given, if not, print usage

if [ -z "$1" ]; then
echo "[*] Simple Zone transfer script"
echo "[*] Usage : $0 <domain name> "
exit 0
fi

# if argument was given, identify the DNS servers for the domain
for server in $(host -t ns $1 |cut -d" " -f4);do

# For each of these servers, attempt a zone transfer
host -l $1 $server |grep "has address"
done