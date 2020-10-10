#!/bin/bash

# Python Offensive PenTesting: - All rights reserved Nathan W Jones nathan.jones@arcadeusops.com

# don't forget to chmod 755 subnet.sh
# usgage is ./subnet.sh 


is_alive_ping()
{
  ping -c 1 $1 > /dev/null
  [ $? -eq 0 ] && echo Node with IP: $i is up.
}

for i in 10.1.1.{1..255} 
do
is_alive_ping $i & disown
done