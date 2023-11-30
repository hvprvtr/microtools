#!/usr/bin/python3

import sys
import csv
import dns.resolver
import re


def is_domain_alive(domain):
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4']
    try:
        answer = my_resolver.resolve(domain, tcp=True)
        ips = re.findall("IN A (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", answer.response.to_text())
        return ips
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers,
            dns.resolver.LifetimeTimeout) as e:
        return None


stat = {}
for line in open(sys.argv[1]):
    line = line.strip()
    if not len(line):
        continue
    ips = is_domain_alive(line)
    print("{0}\t{1}".format(line, ",".join(ips) if ips is not None else "unknown"))
    if ips is None:
        ips = ['Not Found']

    for ip in ips:
        if ip not in stat.keys():
            stat[ip] = []
        stat[ip].append(line)

with open('domains-to-ips.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

    for ip in stat.keys():
        writer.writerow([ip, ",".join(stat[ip])])
