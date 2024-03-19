#!/usr/bin/python3

import sys
import json
from pprint import pprint


data = json.loads(open(sys.argv[1]).read())
for r in data['results']:
    # if "helpdesk" in r['url'] and r['words'] == 2:
    #     continue
    # if r['words'] in [2298, 113, 5760,]:
    #     continue
    # if r['length'] in [162]:
    #     continue
    if r['status'] == 403 and r['content-type'] == 'text/html':
        continue
    if r['status'] == 500 and ".." in r['url']:
        continue
    if "#" in r['url']:
        continue
    print("{0}\t{1}\t{2}\t{3}".format(r['status'], r['url'], r['length'], r['words']))
