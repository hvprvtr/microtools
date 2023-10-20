#!/usr/bin/python3

import sys
import json

data = json.loads(open(sys.argv[1]).read())
for r in data['results']:
    if r['status'] == 403 and r['content-type'] == 'text/html':
        continue
    if r['status'] == 500 and ".." in r['url']:
        continue
    if "#" in r['url']:
        continue
    print("{0} ".format(r['status']) + r['url'])
