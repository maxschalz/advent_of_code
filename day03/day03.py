#!/usr/bin/env python3
# -*- coding: utf-8 -*-

FNAME = "input.txt"

def main():
    """Main function."""
    part1()
    part2()

def part1():
    """Solution to day 3, part 1."""
    data = load_input()
    moves = (3, 1)
    initial_position = (0, 0)

    tobbogan = Tobbogan(data, moves, initial_position)
    n_trees = tobbogan.unhappy_encounters()
    print(f"{n_trees} trees were encountered.")

def part2():
    """Solution to day 3, part 2."""
    data = load_input()
    n_trees_product = 1
    moves = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    initial_position = (0, 0)

    for move in moves:
        tobbogan = Tobbogan(data, move, initial_position)
        n_trees = tobbogan.unhappy_encounters()
        n_trees_product *= n_trees
        print(f"{n_trees} trees were encountered.")

    print(f"The solution is {n_trees_product}.")

def load_input():
    """Read in the grid, return as a list."""
    with open(FNAME, "r") as f:
        entries = f.read().splitlines()
    
    return entries

class Tobbogan:
    def __init__(self, grid, move, initial_position):
        self.grid = self.get_grid(grid)
        self.grid_x = len(self.grid[0])
        self.grid_y = len(self.grid)

        self.x = initial_position[0]
        self.y = initial_position[1]

        self.move_x = move[0]
        self.move_y = move[1]

    def get_grid(self, grid):
        """Preprocess grid.

        Replace all trees with '1', all open locations with '0'.
        """
        new_grid = []
        for line in grid:
            new_grid.append(line.replace(".", "0").replace("#", "1"))

        return new_grid
            
    def unhappy_encounters(self):
        """Count the number of times you hit a tree on the way down."""
        trees = 0
        while self.y < self.grid_y:
            # Check if the current position is a tree or not.
            trees += int(self.grid[self.y][self.x])

            # Move to the new position.
            self.x = (self.x+self.move_x) % self.grid_x
            self.y += self.move_y

        return trees

if __name__=="__main__":
    main()
