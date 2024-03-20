#!/usr/bin/python3

import sys
import os
import json
import requests


if len(sys.argv) != 3:
    print("USAGE: {0} TOKEN user_or_filewusers".format(sys.argv[0]))
    exit()

token = sys.argv[1]
source = sys.argv[2]

targets = set()
if os.path.exists(source):
    for line in open(source):
        line = line.strip()
        if not len(line):
            continue
        targets.add(line)
else:
    targets.add(source)

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer ' + token,
    'X-GitHub-Api-Version': '2022-11-28',
}

errors = {}
for target in targets:
    resp = requests.get(
        "https://api.github.com/users/{target}/repos".format(target=target),
        headers=headers,
        timeout=10,
    )
    data = json.loads(resp.text)

    if isinstance(data, dict):
        errors[target] = data["message"]
        continue

    for repo in data:
        if repo['fork'] is True:
            continue
        print(repo['html_url'])

if len(errors) > 0:
    print("Errors:")
    for target in errors.keys():
        print("{0} => {1}".format(target, errors[target]))