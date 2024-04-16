#!/usr/bin/python3

import sys
import argparse
import os

DICT_PATH = "/usr/share/seclists/Passwords/common_corporate_passwords.lst"

MARKER_COMPANY = "<COMPANY>"
MARKER_DEPARTMENT = "<DEPARTMENT>"
MARKER_COUNTRY = "<LOCATION>"
MARKER_CITY = "<ADDRESS>"
MARKER_HOBBY = "<SPORTS_TEAM/HOBBY>"

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
        line = line.replace(MARKER_COMPANY, args.company)

    if MARKER_DEPARTMENT in line:
        line = line.replace(MARKER_DEPARTMENT, args.department)

    if MARKER_COUNTRY in line:
        line = line.replace(MARKER_COUNTRY, args.country)

    if MARKER_CITY in line:
        line = line.replace(MARKER_CITY, args.city)

    if MARKER_HOBBY in line:
        line = line.replace(MARKER_HOBBY, args.hobby)

    print(line)