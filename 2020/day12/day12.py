#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import numpy as np
import unittest

CARDINAL_DIRECTIONS = ("N", "E", "S", "W")
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
    """Solution to day 12, part 1."""
    ship = Ship()
    for instruction in data:
        ship.action(instruction)

    distance = ship.manhattan_distance()
    print(f"The Manhattan distance is {distance}.")

    return distance

def part2(data):
    """Solution to day 12, part 2."""
    ship = ShipWithWaypoint()
    for instruction in data:
        ship.action(instruction)

    distance = ship.manhattan_distance()
    print(f"The Manhattan distance is {distance}.")

    return distance

def load_input(fname):
    """Read in the data, return as a list."""
    with open(fname, "r") as f:
        data = f.readlines()
    return data


class FloatingObject(metaclass=ABCMeta):
    """An object in a two-dimensional space.

    The following convention for position is used: north (N) and east (E) are
    assigned to positive values, south (S) and west (W) to negative values.
    Following typical conventions, we formulate the coordinates as a (latitude,
    longitude) pair.

    Example
    -------
    Initial position: (0, 0)
    Moving N10 results in a new position (10, 0).
    Following this, moving S20 results in a new position (-10, 0).
    """
    def __init__(self, initial_position):
        """Create an object with an initial position."""
        # Call np.asarray twice to create two deepcopys.
        self.initial_position = np.asarray(initial_position)
        self.current_position = np.asarray(initial_position)

    def update_position(self, direction, value):
        """Update the object's position."""
        if direction == "N":
            self.current_position[0] += value
            return
        if direction == "S":
            self.current_position[0] -= value
            return
        if direction == "E":
            self.current_position[1] += value
            return
        if direction == "W":
            self.current_position[1] -= value
            return
        
        msg = "No valid direction indicated!"
        raise ValueError(msg)


class Ship(FloatingObject):
    """A ship moving in a two-dimensional space."""
    def __init__(self, initial_direction="E", initial_position=[0,0]):
        super().__init__(initial_position)
        self.current_direction_idx = CARDINAL_DIRECTIONS.index(initial_direction)

    def action(self, instruction):
        """Perform an action, which can either be a movement or a rotation."""
        direction = instruction[0]
        value = int(instruction[1:])
        if direction in ("L", "R"):
            self.update_direction(direction, value)
        else:
            self.update_position(direction, value)

    def update_position(self, direction, value): 
        """Update the position of the ship."""
        if direction == "F":
            direction = CARDINAL_DIRECTIONS[self.current_direction_idx]
        super().update_position(direction, value)

    def update_direction(self, direction, degrees):
        """Update the direction by rotating X degrees to the left or right.

        Note that currently, 'degrees' must be a multiple of 90.
        """
        if abs(degrees) % 90 != 0:
            msg = f"'degrees' is not a multiple of 90. degrees is: {degrees}"
            raise ValueError(msg)
        if direction not in ("L", "R"):
            msg = "'direction' must be 'L' or 'R'."
            raise ValueError(msg)

        degrees = -1 * degrees if direction == "L" else degrees
        self.current_direction_idx += degrees // 90
        self.current_direction_idx %= len(CARDINAL_DIRECTIONS)

    def manhattan_distance(self):
        """Return the sum of the absolute values of E/W and N/S position."""
        distance = np.abs(self.current_position - self.initial_position).sum()
        return distance


class Waypoint(FloatingObject):
    def __init__(self, initial_position):
        super().__init__(initial_position)

    def rotate_waypoint(self, direction, value):
        """Rotate the waypoint around the ship."""
        value = -1 * value if direction == "L" else value
        value = np.radians(value)
        rotation_matrix = np.array([[np.cos(value), -np.sin(value)],
                                    [np.sin(value), np.cos(value)]])
        self.current_position = np.matmul(rotation_matrix,
                                          self.current_position)


class ShipWithWaypoint(Ship):
    def __init__(self, initial_direction="E", initial_position=[0,0],
                 waypoint_initial_position=[1, 10]):
        super().__init__(initial_direction, initial_position)
        self.waypoint = Waypoint(waypoint_initial_position)

    def action(self, instruction):
        direction = instruction[0]
        value = int(instruction[1:])
        if direction == "F":
            self.current_position = (self.current_position +
                                     self.waypoint.current_position*value)
        elif direction in CARDINAL_DIRECTIONS:
            self.waypoint.update_position(direction, value)
        elif direction in ("L", "R"):
            self.waypoint.rotate_waypoint(direction, value)    
        

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.data = load_input(TEST_FNAME)

    def test_part1(self):
        value = part1(self.data)
        self.assertEqual(value, 25)

    def test_part2(self):
        value = part2(self.data)
        self.assertEqual(value, 286)


if __name__=="__main__":
    main()
