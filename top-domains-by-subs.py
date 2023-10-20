#!/usr/bin/python3

import sys

from tld import get_tld


def get_top_level_domain(domain):
    tld = get_tld("http://" + domain)
    level_two = domain[:-len(tld)-1].split('.')[-1]
    return level_two + "." + tld


tops = set()
for line in open(sys.argv[1]):
    line = line.strip()
    if not len(line):
        continue

    domain = get_top_level_domain(line)
    tops.add(domain)

print("\n".join(tops))