#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import numpy as np
import unittest

FNAME = "input.txt"
TEST_FNAME = "test_input.txt"
N_ITER_MAX = 1000

def main():
    """Main function."""
    data = load_input(FNAME)
    part1(data)
    part2(data)

    print("\nUnittests")
    unittest.main()

def part1(data):
    """Solution to day 11, part 1."""
    grid = Grid(data)
    n_occupied = grid.get_n_occupied_seats(1)
    print(f"{n_occupied} seats are occupied.")

    return n_occupied
    
def part2(data):
    """Solution to day 11, part 2."""
    grid = Grid(data)
    n_occupied = grid.get_n_occupied_seats(2)
    print(f"{n_occupied} seats are occupied.")

    return n_occupied

def load_input(fname):
    """Read in the data, return as a list."""
    with open(fname, "r") as f:
        data = f.readlines()
    return data


class Grid:
    """A grid containing either seats or floor positions."""
    def __init__(self, grid_input):
        self.n_x, self.n_y, self.grid = self.generate_grid(grid_input)
        self.hashed_configuration = self.hash_configuration()

    def __repr__(self):
        msg = ""
        for row in self.grid:
            for pos in row:
                msg += pos.__repr__()
            msg += "\n"
        return msg

    def generate_grid(self, grid_input):
        """Determine size of grid and initialise it."""
        grid = []
        for i, row in enumerate(grid_input):
            grid.append([])
            for j, column in enumerate(row.replace("\n", "")):
                if column == ".":
                    grid[-1].append(Floor(self, j, i))
                elif column == "L":
                    grid[-1].append(Seat(self, j, i, True))
                elif column == "#":
                    grid[-1].append(Seat(self, j, i, False))
                else:
                    msg = f"'{column}' is not a valid input!" 
                    raise ValueError(msg)
        n_x = len(grid[0])
        n_y = len(grid)

        return n_x, n_y, grid

    def hash_configuration(self):
        """Hash the current seating configuration."""
        seating_configuration = ""
        for row in self.grid:
            for position in row:
                seating_configuration += str(position.is_empty)
        return hash(seating_configuration)

    def update_seats(self, exercise_part):
        # First determine if seats will be occupied or not.
        new_grid = []
        for row in self.grid:
            new_grid.append([])
            for position in row:
                new_grid[-1].append(
                    position.will_be_empty(exercise_part)
                )

        # Then update the their actual status.
        for i, row in enumerate(self.grid):
            for j, position in enumerate(row):
                position.is_empty = new_grid[i][j]

        return self.hash_configuration()

    def get_n_occupied_seats(self, exercise_part):
        next_configuration = self.update_seats(exercise_part)
        n_iter = 0
        while next_configuration != self.hashed_configuration:
            n_iter += 1
            self.hashed_configuration = next_configuration
            next_configuration = self.update_seats(exercise_part)

            if n_iter > N_ITER_MAX:
                msg = "Exceeded maximum number of iterations!"
                raise RuntimeError(msg)

        n_occupied = sum([int(not position.is_empty) \
                          for row in self.grid for position in row])
        return n_occupied


class Position(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, grid, x_position, y_position, is_empty):
        self.grid = grid
        self.x_position = x_position
        self.y_position = y_position
        self.is_empty = is_empty
    
    @abstractmethod
    def __repr__(self):
        """
        x_decimal_places = self.grid.n_x % 10
        y_decimal_places = self.grid.n_y % 10
        msg = (f"({self.x_position:x_decimal_places}, "
               f"{self.y_position:y_decimal_places}): "
               f"{self.is_empty:1}")
        """
        #msg = f"({self.x_position:1}, {self.y_position:1}): "
        #f"{self.is_empty:1}")
        pass

    @abstractmethod
    def will_be_empty(self, exercise_part):
        pass

    @abstractmethod
    def update(self):
        pass


class Floor(Position):
    def __init__(self, grid, x_position, y_position):
        super().__init__(grid, x_position, y_position, True)

    def __repr__(self):
        return "."

    def __str__(self):
        return f"Floor at {self.x_position}, {self.y_position}."

    def will_be_empty(self, exercise_part):
        return True

    def update(self):
        pass


class Seat(Position):
    def __init__(self, grid, x_position, y_position, is_empty=True):
        super().__init__(grid, x_position, y_position, is_empty)

    def __repr__(self):
        msg = "L" if self.is_empty else "#"
        return msg
        
    def __str__(self):
        msg = f"Seat at {self.x_position}, {self.y_position}: "
        msg = msg + "empty." if self.is_empty else msg + "occupied."
        return msg

    def will_be_empty(self, exercise_part):
        """Check if this seat will be occupied in the next round."""
        if exercise_part == 1:
            x_range = (max(0, self.x_position - 1),
                       min(self.x_position + 2, self.grid.n_x))
            y_range = (max(0, self.y_position - 1),
                       min(self.y_position + 2, self.grid.n_y))
            n_occupied = 0
            for x in range(x_range[0], x_range[1]):
                for y in range(y_range[0], y_range[1]):
                    n_occupied += int(not self.grid.grid[y][x].is_empty)

            n_occupied -= int(not self.is_empty)
            # Empty seats become occupied if adjacent ones are empty.
            if self.is_empty and n_occupied == 0:
                return False
            # Occupied seats become empty if at least four adjacent ones
            # are occupied, as well.
            if not self.is_empty and n_occupied >= 4:
                return True
            # Else, the state remains unchanged.
            return self.is_empty
        else:
            # Move along the 6 directions.
            movements = [(x, y) for x in range(-1, 2) \
                                for y in range(-1, 2) if x!=0 or y!=0]
            n_occupied = 0
            for movement in movements:
                query_position = np.array([self.x_position,
                                           self.y_position])
                while True:
                    query_position += movement
                    if np.any(query_position < 0):
                        break
                    try:
                        pos = self.grid.grid[query_position[1]][query_position[0]]
                    except IndexError:
                        break
                    if isinstance(pos, Floor):
                        continue
                    n_occupied += int(not pos.is_empty)
                    break
            # Empty seats become occupied if adjacent ones are empty.
            if self.is_empty and n_occupied == 0:
                return False
            # Occupied seats become empty if at least five adjacent ones
            # are occupied, as well.
            if not self.is_empty and n_occupied >= 5:
                return True
            # Else, the state remains unchanged.
            return self.is_empty


    def update(self):
        pass


class TestMethods(unittest.TestCase):
    def setUp(self):
        self.data = load_input(TEST_FNAME)

    def test_part1(self):
        value = part1(self.data)
        self.assertEqual(value, 37)

    def test_part2(self):
        value = part2(self.data)
        self.assertEqual(value, 26)


if __name__=="__main__":
    main()
