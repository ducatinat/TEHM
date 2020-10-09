#!/bin/bash
# Forward DNS Lookup Script chmod 755
# change line 5 xxxxxxxxxx.com to target
# list.txt add another possible domain names
for ip in $(cat list.txt);do host $ip.megacorpone.com;done

# Reverse Look UP BruteForce PTR) 
for ip in $(seq 155 190);do host 50.7.67.$ip;done |grep -v "not found”