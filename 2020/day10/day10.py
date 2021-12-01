#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import unittest

FNAME = "input.txt"
TEST_FNAME = "test_input.txt"

def main():
    """Main function."""
    data = load_input(FNAME)
    part1(data)
    part2(data)

    print("\nUnittests")
    unittest.main()

def part1(data):
    """Solution to day 10, part 1."""
    # Add the charging outlet.
    data.append(0)
    data = np.sort(data)
    diff = data[1:] - data[:-1]
    hist, _ = np.histogram(diff, bins=[0,1,2,3,4], density=False)

    # +1 because the last step, from adapter to device is +3 jolts.
    result = hist[1] * (hist[3] + 1)

    print("The product of number of 1 and three jolt differences is "
          f"{result}.")
    return result
    
def part2(data):
    """Solution to day 10, part 2."""
    return

def load_input(fname):
    """Read in the data, return as a list."""
    with open(fname, "r") as f:
        data = f.readlines()
    data = [int(x) for x in data]

    return data

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.data = load_input(TEST_FNAME)

    def test_part1(self):
        value = part1(self.data)
        n_one_jolt = 22
        n_three_jolts = 10
        expected_val = n_one_jolt * n_three_jolts
        self.assertEqual(value, expected_val)

    """
    def test_part2(self):
        value = part2(self.data, self.len_preamble)
        self.assertEqual(value, 62)
"""
if __name__=="__main__":
    main()
