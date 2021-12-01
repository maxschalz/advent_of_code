#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    """Solution to day 6, part 1."""
    counts = 0
    for answer in data:
        declaration = CustomsDeclaration(answer)
        counts += declaration.any_yes

    print(f"The sum is {counts}.")
    return counts

def part2(data):
    """Solution to day 6, part 2."""
    counts = 0
    for answer in data:
        declaration = CustomsDeclaration(answer)
        counts += declaration.all_yes

    print(f"The sum is {counts}.")
    return counts

def load_input(fname):
    """Read in the data, return as a list."""
    data = [""]
    with open(fname, "r") as f:
        for line in f.readlines():
            if line.strip("\n"):
                data[-1] += line.strip("\n") + " "
            else:
                data[-1] = data[-1].strip(" ")
                data.append("")
    data [-1] = data[-1].strip(" ")

    return data

class CustomsDeclaration:
    def __init__(self, answers):
        self.answers = answers
        self.any_yes = self.get_any_yes()
        self.all_yes = self.get_all_yes()

    def get_any_yes(self, answers=None):
        """Get the number of yes-answers by at least one person."""
        if answers is None:
            answers = self.answers

        n_any_yes = len(set(answers.replace(" ", "")))
        return n_any_yes
    
    def get_all_yes(self, answers=None):
        """Get the number of yes-answers by all persons in the group."""
        if answers is None:
            answers = self.answers

        if len(answers.split()) == 1:
            return len(set(answers))

        answer_person = set(answers.split()[0])
        for answer in answers.split():
            answer_person = answer_person.intersection(set(answer))

        n_all_yes = len(answer_person)
        return n_all_yes

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.data = load_input(TEST_FNAME)

    def test_part1(self):
        counts = part1(self.data)
        self.assertEqual(counts, 11)

    def test_part2(self):
        counts = part2(self.data)
        self.assertEqual(counts, 6)

if __name__=="__main__":
    main()
