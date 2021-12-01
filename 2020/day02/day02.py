#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import re

FNAME = "input.txt"

def main():
    """Main function."""
    part1()
    part2()

def part1():
    """Solution to day 2, part 1."""
    data = load_input()

    valid = 0
    for pwd in data:
        password = PasswordPart1(pwd)
        valid += int(password.valid)

    print(f"{valid} passwords are valid!")

def part2():
    """Solution to day 2, part 2."""
    data = load_input()

    valid = 0
    for pwd in data:
        password = PasswordPart2(pwd)
        valid += int(password.valid)

    print(f"{valid} passwords are valid!")

def load_input():
    """Read in the passwords, return as a list."""
    with open(FNAME, "r") as f:
        entries = f.readlines()
    return entries


class Password(metaclass=ABCMeta):
    def __init__(self, line):
        self.password = self.get_password(line)

        self.policy_min = -1
        self.policy_max = -1
        self.policy_letter = ""
        self.get_policy(line)

        self.valid = self.is_valid()
    
    def get_password(self, line):
        """Get the password from a string."""
        password = line.replace(" ", "").split(":")[1]
        return password

    def get_policy(self, line):
        """Get the policy from a string."""
        policy = line.replace(" ", "").split(":")[0]

        policy_numbers = re.compile("\d+-\d+")
        match_object = policy_numbers.match(policy)
        if match_object is None:
            msg = ("Could not determine policy, no valid input given! "
                   + f"Input: {line}")
            raise RuntimeError(msg)
        
        minimum, maximum = match_object.group().split("-")
        self.policy_min = int(minimum)
        self.policy_max = int(maximum)

        self.policy_letter = policy[-1]

    @abstractmethod
    def is_valid(self):
        pass

class PasswordPart1(Password):
    def is_valid(self):
        """Check if the password follows the policy."""
        occurences = self.password.count(self.policy_letter)
        
        return (occurences >= self.policy_min
                and occurences <= self.policy_max)

class PasswordPart2(Password):
    def letter_matches_password(self, idx):
        """Check if the letter at idx equals the policy letter."""
        return self.password[idx] == self.policy_letter
        
    def is_valid(self):
        """Implement the policy from part 2.

        Note that the variable naming may make a bit less sense than in
        part 1, but it should still be understandable if you have read
        the exercise/the README.
        """
        position1 = self.letter_matches_password(self.policy_min - 1)
        position2 = self.letter_matches_password(self.policy_max - 1)

        return position1 ^ position2


if __name__=="__main__":
    main()
