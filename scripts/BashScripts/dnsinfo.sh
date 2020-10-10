#!/bin/bash

# Python Offensive PenTesting: - All rights reserved Nathan W Jones nathan.jones@arcadeusops.com

# don't forget to chmod 755 dnsinfo.sh
# usage is ./dnsinfo.sh

host -t ns arcadeusops.com # change to your target

host -t mx arcadeusops.com # change to your target