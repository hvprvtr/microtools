#!/usr/bin/python3

import sys
import re
import argparse
import os

DICT_PATH = "/usr/share/seclists/Passwords/common_corporate_passwords.lst"

MARKER_COMPANY = "<COMPANY>"
MARKER_DEPARTMENT = "<DEPARTMENT>"
MARKER_COUNTRY = "<LOCATION>"
MARKER_CITY = "<ADDRESS>"
MARKER_HOBBY = "<SPORTS_TEAM/HOBBY>"


def mutate(s):
    mutations = []
    mutations.append(s)
    if re.match('^[A-Z]{1}[a-z0-9]+', s):
        mutations.append(s.lower())
    if s.islower():
        mutations.append(s[0:1].upper() + s[1:])
    return mutations


def print_mutations(source_line, marker, mutations):
    for mutation in mutations:
        line = source_line.replace(marker, mutation)
        print(line)


if not os.path.exists(DICT_PATH):
    print("Corporate dict not exists in " + DICT_PATH)
    print("Install seclists")
    exit(0)


parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('--company', help='Company name', required=True)
parser.add_argument('--department', help='Dept name', required=False, default='')
parser.add_argument('--country', help='Country', required=False, default='')
parser.add_argument('--city', help='City', required=False, default='')
parser.add_argument('--hobby', help='Hobby word (sport team may be)', required=False, default='')
args = parser.parse_args()

for line in open(DICT_PATH):
    line = line.strip()
    if not len(line):
        continue

    if MARKER_DEPARTMENT in line and not len(args.department):
        continue
    if MARKER_COUNTRY in line and not len(args.country):
        continue
    if MARKER_CITY in line and not len(args.city):
        continue
    if MARKER_HOBBY in line and not len(args.hobby):
        continue

    if MARKER_COMPANY in line:
        mutations = mutate(args.company)
        print_mutations(line, MARKER_COMPANY, mutations)

    if MARKER_DEPARTMENT in line:
        mutations = mutate(args.department)
        print_mutations(line, MARKER_DEPARTMENT, mutations)

    if MARKER_COUNTRY in line:
        mutations = mutate(args.country)
        print_mutations(line, MARKER_COUNTRY, mutations)

    if MARKER_CITY in line:
        mutations = mutate(args.city)
        print_mutations(line, MARKER_CITY, mutations)

    if MARKER_HOBBY in line:
        mutations = mutate(args.hobby)
        print_mutations(line, MARKER_HOBBY, mutations)

