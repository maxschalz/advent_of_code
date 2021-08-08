#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import combinations

FNAME = "input.txt"
TARGET_VAL = 2020

def main():
    """Main function."""
    part1()
    part2()

def part1():
    """Solution to day 1, part 1."""
    result = find_sum(TARGET_VAL, 2)

    if result is None:
        print("No possible combination found!")
    else:
        x, y = result
        product = x * y
        print(f"Solution found for\nx = {x},\ny = {y},\n"
              f"x * y = {product}")

def part2():
    """Solution to day 1, part 2."""
    result = find_sum(TARGET_VAL, 3)

    if result is None:
        print("No possible combination found!")
    else:
        x, y, z= result
        product = x * y * z
        print(f"Solution found for\nx = {x},\ny = {y},\nz = {z}\n"
              f"x * y * z = {product}")

def load_input():
    """Read in the values, return as a list."""
    with open(FNAME, "r") as f:
        entries = [int(val) for val in f.readlines()]
    return entries

def find_sum(sum_, n_tuple):
    """Find the two entries that sum to `sum_`."""
    data = load_input() 
    combinations_ = combinations(data, n_tuple)

    for combination in combinations_:
        if sum(combination) == sum_:
            return combination
    return None

if __name__=="__main__":
    main()
