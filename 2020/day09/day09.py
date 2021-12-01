#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from math import factorial
import unittest

FNAME = "input.txt"
TEST_FNAME = "test_input.txt"

def main():
    """Main function."""
    data = load_input(FNAME)
    len_preamble = 25
    part1(data, len_preamble)
    part2(data, len_preamble)

    print("\nUnittests")
    unittest.main()

def part1(data, len_preamble):
    """Solution to day 9, part 1."""
    cipher = Cipher(data, len_preamble)
    number = cipher.wrong_number()
    print(f"First false value is {number}.")

    return number
    
def part2(data, len_preamble):
    """Solution to day 9, part 2."""
    cipher = Cipher(data, len_preamble)
    result = cipher.find_weakness()
    if result is None:
        print("No solution found!")
    else:
        print(f"The encryption weakness is {result}.")

    return result

def load_input(fname):
    """Read in the data, return as a list."""
    with open(fname, "r") as f:
        data = f.readlines()
    data = [int(x) for x in data]

    return data

class Cipher:
    def __init__(self, cipher, len_preamble):
        self.cipher = cipher
        self.preamble = cipher[:len_preamble]
        self.len_preamble = len_preamble
        self.possible_vals = self.init_possible_vals()

    def init_possible_vals(self):
        # Use deque which allows for efficient FIFO operations.
        vals = deque()
        for i, x in enumerate(self.preamble[:-1]):
            for y in self.preamble[i+1:]:
                vals.append(x + y)
        return vals

    def wrong_number(self):
        """Part 1, find number which is not the sum of previous ones."""
        for idx in range(self.len_preamble, len(self.cipher)):
            if self.cipher[idx] not in self.possible_vals:
                break
            self.update_possible_vals(idx)
            idx += 1

        return self.cipher[idx]

    def update_possible_vals(self, idx):
        for _ in range(1, self.len_preamble):
            self.possible_vals.popleft()
        insert_idx = 0
        for i in range(self.len_preamble-1, 0, -1):
            insert_idx += i
            val = self.cipher[idx] + self.cipher[idx-i]
            self.possible_vals.insert(insert_idx-1, val)

    def find_weakness(self):
        """Part 2. Brute-forced because why not"""
        target_val = self.wrong_number()
        
        for i, x in enumerate(self.cipher):
            sum_ = x
            for j, y in enumerate(self.cipher[i+1:]):
                sum_ += y
                if sum_ == target_val:
                    min_val = min(self.cipher[i:i+j+1])
                    max_val = max(self.cipher[i:i+j+1])
                    return min_val + max_val
                elif sum_ > target_val:
                    break

        return None

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.data = load_input(TEST_FNAME)
        self.len_preamble = 5

    def test_part1(self):
        value = part1(self.data, self.len_preamble)
        self.assertEqual(value, 127)

    def test_part2(self):
        value = part2(self.data, self.len_preamble)
        self.assertEqual(value, 62)

if __name__=="__main__":
    main()
