#!/usr/bin/python3

import csv
import json
import subprocess
import os
import sys
from pprint import pprint

GITOSINT_BIN = "/usr/local/bin/gitleaks"
if not os.path.exists(GITOSINT_BIN):
    print("Install gitleaks first! It must be here: " + GITOSINT_BIN)
    exit(1)

repos = set()
paths = sys.argv[1:]
for path in paths:
    if not path.endswith("/"):
        path += "/"
    for r in os.listdir(path):
        repos.add(path + r)

for repo in repos:
    print("Scan repo: " + repo)
    p = subprocess.Popen(["gitleaks", "detect", "--source", repo, "-v"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    print(stdout.decode("utf8"))
    print(stderr.decode("utf8"))