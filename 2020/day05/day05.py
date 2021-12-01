#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

FNAME = "input.txt"

def main():
    """Main function."""
    part1()
    part2()

def part1():
    """Solution to day 5, part 1."""
    data = load_input()
    max_id = 0
    for specifier in data:
        bp = BoardingPass(specifier)
        max_id = bp.seat_id if bp.seat_id > max_id else max_id

    print(f"The highest seat ID is {max_id}")
    
def part2():
    """Solution to day 5, part 2."""
    data = load_input()
    seat_ids = []
    for spec in data:
        seat_ids.append(BoardingPass(spec).seat_id)

    # Sort the ids, then get the two seats that are not adjacent.
    # My seat is in between them. One needs to add 2 because the first
    # seat is ignored (+1) and because we don't want my neighbour's
    # seat id (+1).
    seat_ids = np.sort(seat_ids)
    idx = np.where(seat_ids[2:] - seat_ids[:-2] != 2)[0][0]
    my_seat_id = seat_ids[idx] + 2
    print(f"My seat ID is {my_seat_id}.")

def load_input():
    """Read in the data, return as a list."""
    with open(FNAME, "r") as f:
        data = f.readlines()
    data = [d.strip("\n") for d in data]
    return data

class BoardingPass:
    def __init__(self, specifier):
        self.specifier = specifier
        self.row, self.column = self.get_position()
        self.seat_id = self.get_id()
    
    def get_position(self, specifier=None):
        """Get the row and column from the specifier."""
        if specifier is None:
            specifier = self.specifier

        row = self.get_row(specifier[:7])
        column = self.get_column(specifier[-3:])
        
        return row, column

    def get_row(self, specifier):
        """Get the row number.

        Represent the specifier as binary number, then convert to
        decimal base.
        """
        row = specifier.replace("F", "0").replace("B", "1")
        row = int(row, 2)

        return row

    def get_column(self, specifier):
        """Get the column number.

        Represent the specifier as binary number, then convert to
        decimal base.
        """
        column = specifier.replace("L", "0").replace("R", "1")
        column = int(column, 2)

        return column

    def get_id(self):
        return self.row*8 + self.column


if __name__=="__main__":
    main()
