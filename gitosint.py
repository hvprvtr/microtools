#!/usr/bin/python3

import csv
import json
import subprocess
import os
import sys
from pprint import pprint

KNOWN_KEYS = ['metadata', 'location']

GITOSINT_BIN = "/usr/local/bin/gitosint"
if not os.path.exists(GITOSINT_BIN):
    print("Install gitosint first! It must be here: " + GITOSINT_BIN)
    exit(1)

repos = set()
paths = sys.argv[1:]
for path in paths:
    if not path.endswith("/"):
        path += "/"
    for r in os.listdir(path):
        repos.add(path + r)

users = {}
stdout = subprocess.check_output([GITOSINT_BIN, "git", "--repos", ",".join(repos)])
stdout = stdout.decode("utf8")
for line in stdout.split("\n"):
    line = line.strip()
    if not len(line):
        continue
    data = json.loads(line)['repository']

    repo_keys = data.keys()
    for repo_key in repo_keys:
        if repo_key not in KNOWN_KEYS:
            print(line)
            print("Unknown key! " + repo_key)
            exit(0)

    if 'metadata' not in data.keys():
        continue

    users.update(data['metadata'])

subprocess.check_output(["rm", "-rf", "/tmp/gitrecon*"])


with open('gitosint-users.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

    for email in users:
        if 'noreply@github.com' in email:
            continue
        user = users[email]
        csvwriter.writerow([email, ",".join(user)])
print("Wrote {0} users into csv".format(len(users)))