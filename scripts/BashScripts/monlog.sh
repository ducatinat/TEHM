#!/bin/bash 
 
# Python Offensive PenTesting: - All rights reserved Nathan W Jones nathan.jones@arcadeusops.com

# don't forget to chmod 755 monlog.sh. This script monitors logs and send it to your email.
# usgage is ./monlog.sh google.com yahoo.com 192.168.1.2 mylinuxbox N2100
 
LOG=/tmp/mylog.log 
SECONDS=3600 

EMAIL=my@email.address 
 
for i in $@; do 
	echo "$i-UP!" > $LOG.$i 

done 
 
while true; do 
	for i in $@; do 

ping -c 1 $i > /dev/null 
if [ $? -ne 0 ]; then 
	STATUS=$(cat $LOG.$i) 
 		if [ $STATUS != "$i-DOWN!" ]; then 
 			echo "`date`: ping failed, $i host is down!" | 
			mail -s "$i host is down!" $EMAIL 

 		fi 
	echo "$i-DOWN!" > $LOG.$i 

else 
	STATUS=$(cat $LOG.$i)
 		if [ $STATUS != "$i-UP!" ]; then 
 			echo "`date`: ping OK, $i host is up!" | 
			mail -s "$i host is up!" $EMAIL

 		fi 
	echo "$i-UP!" > $LOG.$i 
fi 
done 

sleep $SECONDS 
done