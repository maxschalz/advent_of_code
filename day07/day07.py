#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import unittest

COLOR = "shiny gold"
FNAME = "input.txt"
N_ITER = 1e7
TEST_FNAME = "test_input.txt"

def main():
    """Main function."""
    data = load_input(FNAME)    
    part1(data)
    part2(data)

    print("\nUnittests")
    unittest.main()

def part1(data):
    """Solution to day 7, part 1."""
    for rule in data:
        Bag(rule)

    n_bags = Bag.n_bags_containing_specific_bag(COLOR)
    print(f"{n_bags} bags can contain at least one {COLOR} bag.")

    return n_bags

def part2(data):
    """Solution to day 7, part 2."""
    for rule in data:
        Bag(rule)

    n_bags = Bag.n_bags_inside(COLOR)
    print(f"One {COLOR} bag contains {n_bags} other bags.")

    return n_bags

def load_input(fname):
    """Read in the data, return as a list."""
    with open(fname, "r") as f:
        data = f.readlines()
    data = [x.strip("\n") for x in data]

    return data

class Bag:
    all_bags = {}
    def __init__(self, rule):
        self.color, self.descendants = self.init_bag(rule)
        self.no_descendants = not bool(self.descendants)

        Bag.all_bags[self.color] = self

    def init_bag(self, rule):
        """Get the color of the bag and its descendants.

        Parameters
        ----------
        rule : str
            Contains the rule defining the bag, e.g.:
            shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        Returns
        -------
        color : str
            The color of the bag, e.g., `dark olive`
        descendants_dict : dict
            A dictionary with the keys being the colors of the bags
            contained in this bag and the values being the corresponding
            amount of bags of the color.
        """
        color, descendants = rule.split(" bags contain ")
        descendants_dict = {}
        for desc in descendants.split(","):
            match = re.match(r"(\d+) ([a-z]+ [a-z]+) bags?",
                             desc.strip())
            if match is None:
                return color, None
            else:
                amount = int(match.group(1))
                descendant_color = match.group(2)
                descendants_dict[descendant_color] = amount

        return color, descendants_dict

    def bag_in_descendants(self, bag_color, n_iter):
        """Check if bag_color is in this bag or in its descendants.

        This function recursively looks for the bag in question. There
        surely are more efficient ways to do this but I think this is
        quite intuitive and understandable.
        """
        # Prevent an infinite loop.
        if n_iter > N_ITER:
            raise RuntimeError("Exceeded maximum number of iterations!")
        if self.color==bag_color:
            return True
        if self.no_descendants:
            return False

        for descendant_bag_color in self.descendants.keys():
            descendant_bag = Bag.all_bags[descendant_bag_color]
            if descendant_bag.bag_in_descendants(bag_color, n_iter+1):
                return True

        return False

    def n_bags_in_descendants(self, n_iter):
        """Return the number of bags in the descendants of this bag.

        Note
        ----
        This includes the bag itself, e.g., consider one red bag
        containing four green bags. In that case, the function would
        return 5 (and not 4).
        """
        # Prevent an infinite loop.
        if n_iter > N_ITER:
            raise RuntimeError("Exceeded maximum number of iterations!")
        if self.no_descendants:
            return 0

        n_iter += 1
        bags_inside = 0
        for descendant_color, descendant_num in self.descendants.items():
            descendant_bag = Bag.all_bags[descendant_color]
            if descendant_bag.no_descendants:
                bags_inside += descendant_num
            else:
                bags_inside += (
                    descendant_num
                    * descendant_bag.n_bags_in_descendants(n_iter))
        bags_inside += 1

        return bags_inside

    @classmethod
    def n_bags_containing_specific_bag(cls, bag_color):
        """Return the number of bags containing the bag `bag_color`"""
        n_bags = 0
        for bag in Bag.all_bags.values():
            if bag is Bag.all_bags[COLOR]:
                continue
            n_bags += int(bag.bag_in_descendants(COLOR, 0))
        
        return n_bags

    @classmethod
    def n_bags_inside(self, bag_color):
        """Return the number of bags inside the bag `bag_color`."""
        n_bags = Bag.all_bags[bag_color].n_bags_in_descendants(0)
        n_bags -= 1  # Substract the bag itself.

        return n_bags


class TestMethods(unittest.TestCase):
    def setUp(self):
        Bag.all_bags = {}
        self.data = load_input(TEST_FNAME)

    def test_part1(self):
        counts = part1(self.data)
        self.assertEqual(counts, 4)

    def test_part2(self):
        counts = part2(self.data)
        self.assertEqual(counts, 32)

if __name__=="__main__":
    main()
