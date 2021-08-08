#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

FNAME = "input.txt"
NORTH_POLE_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
PASSPORT_FIELDS = NORTH_POLE_FIELDS + ["cid"]

def main():
    """Main function."""
    part1_and_2()

def part1_and_2():
    """Solution to day 4, part 1."""
    data = load_input()

    n_valid_fields = 0
    n_valid_values = 0
    for d in data:
        passport = Passport(d)
        if passport.valid_keys():
            n_valid_fields += 1
            n_valid_values += int(passport.valid_values())

    print(f"{n_valid_fields} passports have valid fields.")
    print(f"{n_valid_values} passports have valid values.")


def load_input():
    """Read in the data, return as a list."""
    with open(FNAME, "r") as f:
        # [:-1] because Python adds a newline to the end of the file.
        data = f.read()
        if data.endswith("\n"):
            data = data[:-1]
    entries = data.split("\n\n")
    entries = [x.replace("\n", " ") for x in entries]

    return entries

class Passport:
    def __init__(self, passport_str):
        self.attributes = {}
        self.initialise_vals(passport_str) 
    
    def initialise_vals(self, passport_str):
        """Load the attributes into the dictionary."""
        vals = passport_str.split(" ")
        for val in vals:
            key, value = val.split(":")
            if key in self.attributes:
                raise RuntimeError(f"Key {key} occured twice in one passport!")
            
            if value.endswith("\n"):
                value = value[:-1]
            self.attributes[key] = value

    def valid_keys(self):
        """Check if all the keys (except for cid) are present."""
        for north_pole_key in NORTH_POLE_FIELDS:
            if north_pole_key not in self.attributes:
                return False
        return True

    def valid_values(self):
        """Check the passport entries for validity."""
        # Last value in range is *excluded*.
        byr = lambda x: int(x) in range(1920, 2003)
        iyr = lambda x: int(x) in range(2010, 2021)
        eyr = lambda x: int(x) in range(2020, 2031)
        hgt_cm = lambda x: int(x) in range(150, 194) 
        hgt_in = lambda x: int(x) in range(59, 77) 
        def hgt(x):
            if "cm" in x:
                return hgt_cm(x[:-2])
            elif "in" in x:
                return hgt_in(x[:-2])
            return False
        ecl = lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl",
                              "oth"]

        def hcl(x):
            pattern = re.compile("#[0-9a-f]{6}")
            return bool(pattern.match(x))
        def pid(x):
            pattern = re.compile("\d{9}$")
            return bool(pattern.match(x))
        cid = lambda x: True
        checks = {"byr": byr, "iyr": iyr, "eyr": eyr, "hgt": hgt,
                  "hcl": hcl, "ecl": ecl, "pid": pid, "cid": cid}

        for key, val in self.attributes.items():
            if not checks[key](val):
                return False
        return True

if __name__=="__main__":
    main()
