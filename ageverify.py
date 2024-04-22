#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ----------------------------------------------------------------------------
# ------------------------ GERMAN ID AGE VERIFICATION ------------------------
# ageverify.py
# Version: 0.2.0
# 2024-04-21
#
# ----------------------------------------------------------------------------
# This script allows to verify someones age based on the ID, birth date, expiry date,
# and checksums of the german ID (Personalausweis) as well as to generate valid random
# sets of those data point for testing purposes

import argparse
import datetime as dt
import random as rd
import string

VERSION = "0.2.0"
VERSION_DATE = "2023-03-21"
DESCRIPTION = """TBD"""

# Base Config
DEFAULT_MIN_AGE = 18
DEFAULT_MAX_AGE = 99
ALLOWED_CHARS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "C", "F", "G", "H", "J", "K", "L", "M", "N", "P", "R", "T", "V", "W", "X", "Y", "Z"]

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('-V', '--version', help='Print the version information', action='store_true')
parser.add_argument('-v', '--verbose', help='Enable verbose mode', action='store_true')
parser.add_argument('-g', '--generate', help='Generate new age verification data', action='store_true')
parser.add_argument('--verify', nargs=4, metavar=('ID','BD','ED','CS'), help='Verify a given set of data')

# Parse command line
args = parser.parse_args()
debug_mode = args.verbose

# Print version info and quit
def print_version():
    print(f"Version: {VERSION} ({VERSION_DATE})")
    exit()

# Verify a given set of ID, birth date, and expiry date
def verify_age(full_id, full_birth_date, full_expiry_date, check_sum):

    # parse dates
    birth_date = dt.datetime.strptime(full_birth_date[:-1], "%y%m%d")
    expiry_date = dt.datetime.strptime(full_expiry_date[:-1], "%y%m%d")

    if expiry_date < dt.datetime.today():
        print(f"The passport has expired at {expiry_date.isoformat()}")
        exit(1)
    else:
        age = int((dt.datetime.today() - birth_date).days / 365)
        if age < 0:
            age = 99 + age

    # Check date checksums
    if calc_check_sum(full_birth_date[:-1]) != int(full_birth_date[-1:]):
        print(f"The checksum for the birth date is invalid")
        exit(1)
    elif calc_check_sum(full_expiry_date[:-1]) != int(full_expiry_date[-1:]):
        print(f"The checksum for the expiry date is invalid")
        exit(1)

    # Check whether the ID contains invalid characters
    if (set(full_id) - set(ALLOWED_CHARS) != set()):
        invalid_chars = set(full_id) - set(ALLOWED_CHARS)
        print(f"The ID string contains the following invalid characters: {', '.join(invalid_chars)}")
        exit(1)
    elif calc_check_sum(full_id[:-1]) != int(full_id[-1:]):
        print(f"The checksum for the passport ID is invalid")
        exit(1)
    elif calc_check_sum(full_id + full_birth_date + full_expiry_date) != int(check_sum):
        print("The overall checksum is not valid, ID does not match birth or expiry date")
        exit(1)
    else:
        print(f"The passport ID seems to be valid, the person is {age} years old")



# Generate a random, valid ID, birth date, and expiry date
def generate_data(min_age = DEFAULT_MIN_AGE, max_age = DEFAULT_MAX_AGE):
    id = create_id()
    bd = create_birth_date(min_age, max_age)
    ed = create_expiry_date()
    checksum_total = calc_check_sum(id + bd[0] + ed[0])
    print(id, bd[0], ed[0], checksum_total)
    print(f"Ausweisnummer: {id}")
    print(f"Geburtsdatum: {bd[0]} ({bd[1]})")
    print(f"Ablaufdatum: {ed[0]} ({ed[1]})")
    print(f"Prüfsumme: {checksum_total}")

def create_id():
    first_chars = ["L","M", "N", "P", "R", "T", "V", "W", "X", "Y"]
    allowed_chars = ALLOWED_CHARS
    id_num = first_chars[rd.randint(0,len(first_chars) - 1)]
    id_num += "".join([allowed_chars[rd.randint(0,len(allowed_chars) - 1)] for x in range(8)])
    ret_id = id_num + str(calc_check_sum(id_num))
    return ret_id

def create_birth_date(min_age: int, max_age: int = 0):
    if max_age == 0:
        birth_year = (dt.date.today() - dt.timedelta(days=min_age * 365)).year
    else:
        birth_year = (dt.date.today() - dt.timedelta(days=rd.randint(min_age, max_age) * 365)).year
    birth_day = rd.randint(1, 365)
    birth_date = dt.date(birth_year,1,1) + dt.timedelta(days=birth_day)
    ret_bd = birth_date.strftime("%y%m%d")
    ret_bd += str(calc_check_sum(ret_bd))
    return (ret_bd, birth_date.isoformat())

def create_expiry_date():
    max_days = 365 * 5
    expires_in = rd.randint(100,max_days)
    today = dt.date.today()
    expiry_date = today + dt.timedelta(days=expires_in)
    ret_ed = expiry_date.strftime("%y%m%d")
    ret_ed += str(calc_check_sum(ret_ed))
    return (ret_ed, expiry_date.isoformat())

# Calculate a checksum over any valid input string
def calc_check_sum(str):
    arr = [char for char in str]
    sum = 0
    for i in range(len(arr)):
        char = arr[i]
        if char.isnumeric():
            num = int(char)
        else:
            num = list(string.ascii_uppercase).index(char) + 10
        pos = i % 3
        if pos == 0:
            res = (num * 7) % 10
        elif pos == 1:
            res = (num * 3) % 10
        elif pos == 2:
            res = (num * 1) % 10
        sum += res
    return sum % 10


# ----- SCRIPT ACTIONS -----

def main():
    if args.version:
        print_version()
    elif args.generate:
        generate_data()
    elif args.verify:
        verify_age(args.verify[0], args.verify[1], args.verify[2], args.verify[3])

if __name__ == "__main__":
    main()