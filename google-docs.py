#!/usr/bin/python3

import sys

FILETYPES = [
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
]

domains_file = sys.argv[1]
for line in open(domains_file):
    domain = line.strip()
    if not len(domain):
        continue

    for ftype in FILETYPES:
        print("site:{0} filetype:{1}".format(domain, ftype))