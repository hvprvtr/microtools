#!/usr/bin/python3

import sys
import re
import dns.resolver
from randstr import randstr


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

    domain = line
    stat[domain] = set()
    wildcard_cnt = 0
    for _ in range(10):
        subdomain = randstr(12) + "." + domain
        ips = is_domain_alive(subdomain)
        if ips is None and wildcard_cnt == 0:
            break

        if ips is not None:
            stat[domain].update(ips)
            wildcard_cnt += 1

    if wildcard_cnt > 5:
        print("*." + domain + "\t" + ",".join(stat[domain]))

