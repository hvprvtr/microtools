#!/usr/bin/python3

import csv
import sys
import ipaddress
import socket
from termcolor import colored

if len(sys.argv) != 3:
    print("USAGE: {0} subnets.txt domains.txt".format(sys.argv[0]))
    exit(0)

#TODO 'not in' mode

domains = set()
for domain in open(sys.argv[2]):
    domain = domain.strip()
    if not len(domain):
        continue
    domains.add(domain)

subnets = set()
for subnet in open(sys.argv[1]):
    subnet = subnet.strip()
    if not len(subnet):
        continue
    subnets.add(ipaddress.ip_network(subnet, False))

csvfile_in = open('in-subnets.csv', 'w')
csvfile_out = open('not-in-subnets.csv', 'w')

csv_writer_in = csv.writer(csvfile_in, quoting=csv.QUOTE_ALL)
csv_writer_out = csv.writer(csvfile_out, quoting=csv.QUOTE_ALL)

found_fh = open("in-subnets.txt", "w")
not_found_fh = open("not-in-subnets.txt", "w")
for domain in domains:
    found = False
    ip = "BLANK_IP"
    try:
        ip = socket.gethostbyname(domain)
        ip = ipaddress.ip_address(ip)
        for subnet in subnets:
            if ip in subnet:
                found = True
                csv_writer_in.writerow([domain, ip])
                print(colored("{0} in {1}".format(domain, subnet), "green"))
    except socket.gaierror:
        print(colored("{0} - not resolving".format(domain), "red"))
        continue

    if not found:
        csv_writer_out.writerow([domain, ip])
        print(colored("{0} ({1}) is not in subnets :( ".format(domain, ip), "red"))
        not_found_fh.write(domain + "\n")
    else:
        found_fh.write(domain + "\n")

# ipaddress.ip_address('192.168.0.1') in ipaddress.ip_network('192.168.0.0/24')