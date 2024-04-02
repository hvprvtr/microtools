#!/usr/bin/python3

import sys
import re

report = sys.argv[1]

data = open(report).read()
for row in data.split("\n\n"):
    row = row.strip()
    if not len(row):
        continue

    try:
        ip = re.findall("Nmap scan report for (.+)", row)[0]
    except IndexError:
        print("IndexError")
        print(row)
        exit()
    ports = re.findall("(\d+/tcp .+)", row)
    print(ip)
    print("\n".join(ports))
    print("")


