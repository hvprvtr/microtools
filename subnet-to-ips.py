#!/usr/bin/python3

import ipaddress
import sys

for ip in ipaddress.IPv4Network(sys.argv[1]):
    print(str(ip))