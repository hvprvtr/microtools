#!/usr/bin/python3

import sys
import codecs

dict_path = sys.argv[1]
min_len = int(sys.argv[2])

with codecs.open(dict_path, encoding="utf8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if len(line) < min_len:
            continue
        print(line)