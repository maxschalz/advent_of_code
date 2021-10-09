#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
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
    """Solution to day 13, part 1."""
    earliest_timestamp = float(data[0])
    bus_ids = np.array(data[1].replace("x", "nan").split(","), dtype=float)

    departures_after_earliest_timestamp = ((earliest_timestamp // bus_ids + 1)
                                           * bus_ids)
    waiting_time = departures_after_earliest_timestamp - earliest_timestamp
    earliest_bus_idx = np.nanargmin(waiting_time)

    result = waiting_time[earliest_bus_idx] * bus_ids[earliest_bus_idx]
    print(f"The result is {result:.0f}.")

    return result

def load_input(fname):
    """Read in the data, return as a list."""
    with open(fname, "r") as f:
        data = f.readlines()
    return data


class TestMethods(unittest.TestCase):
    def setUp(self):
        self.data = load_input(TEST_FNAME)

    def test_part1(self):
        value = part1(self.data)
        self.assertEqual(value, 295)


if __name__=="__main__":
    main()
