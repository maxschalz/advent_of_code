#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

FNAME = "input.txt"
TEST_FNAME = "test_input.txt"

N_ITER_MAX = int(1e4)

def main():
    """Main function."""
    data = load_input(FNAME)
    part1(data)
    part2(data)

    print("\nUnittests")
    unittest.main()

def part1(data):
    """Solution to day 7, part 1."""
    prog = Program(data)
    acc = prog.identify_inf_loop()
    
    return acc

def part2(data):
    """Solution to day 7, part 2."""
    prog = Program(data)
    acc = prog.fix_code()
    
    return acc

def load_input(fname):
    """Read in the data, return as a list."""
    with open(fname, "r") as f:
        data = f.readlines()
    data = [x.strip("\n") for x in data]

    return data

class Program:
    def __init__(self, instructions):
        self.instructions = self.get_instructions(instructions)
        self.n_instructions = len(self.instructions)
        self.accumulator = 0
        self.current_line = 0
        self.program_ended = False

    def get_instructions(self, instructions):
        inst_list = []
        for line in instructions:
            inst, val = line.split(" ")
            val = int(val)
            inst_list.append(Instruction(inst, val, self))

        return inst_list

    def update_current_line(self, line_diff):
        self.current_line += line_diff
        if self.current_line >= self.n_instructions:
            self.program_ended = True

    def reset_program(self):
        self.accumulator = 0
        self.current_line = 0
        self.program_ended = False
        
        for inst in self.instructions:
            inst.instruction_executed = False

    def run_program(self):
        current_inst = self.instructions[self.current_line]
        n_iter = 0
        while not current_inst.instruction_executed:
            current_inst.do_inst()
            if self.program_ended:
                break
            current_inst = self.instructions[self.current_line]
            n_iter += 1
            if n_iter > N_ITER_MAX:
                raise RuntimeError("Too many iterations!")

        if self.program_ended:
            return True
        if current_inst.instruction_executed:
            return False

    def identify_inf_loop(self):
        exit_successfully = self.run_program()

        if not exit_successfully:
            print(f"Stopped at line {self.current_line} with "
                  f"accumulator at {self.accumulator}")
            return self.accumulator
        else:
            raise RuntimeError()

    def fix_code(self):
        for inst in self.instructions:
            swap_successful = inst.swap_inst()
            if not swap_successful:
                # The instruction was 'acc' and no swapping was done.
                continue
            exit_successful = self.run_program()
            if exit_successful:
                print(f"Ran program successfully! Value of the "
                      f"accumulator: {self.accumulator}")
                break
            self.reset_program()
            inst.swap_inst()

        return self.accumulator

class Instruction:
    def __init__(self, inst, val, program):
        """Initialise an instruction object.

        Parameters
        ----------
        inst : str
            The operation, has to be either `acc` or `jmp` or `nop`.
        val : int
            The value associated to the operation.
        prog : Program
            The program which the instruction is a part of.
        """
        if inst not in ("acc", "jmp", "nop"):
            msg = "`inst` has to be one of `acc` or `jmp` or `nop`."
            raise ValueError(msg)
        self.inst = inst
        self.val = val
        self.program = program
        self.instruction_executed = False

    def __repr__(self):
        return f"{self.inst} {self.val:+}"

    def do_inst(self):
        """Perform this instruction in the program."""
        if self.instruction_executed:
            raise RuntimeError("Instruction already executed!")

        if self.inst == "nop":
            self.program.update_current_line(1)
        elif self.inst == "acc":
            self.program.accumulator += self.val
            self.program.update_current_line(1)
        elif self.inst == "jmp":
            self.program.update_current_line(self.val)
        self.instruction_executed = True

    def swap_inst(self):
        if self.inst == "acc":
            return False
        elif self.inst == "nop":
            self.inst = "jmp"
        elif self.inst == "jmp":
            self.inst = "nop"
        return True

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.data = load_input(TEST_FNAME)

    def test_part1(self):
        acc = part1(self.data)
        self.assertEqual(acc, 5)

    def test_part2(self):
        acc = part2(self.data)
        self.assertEqual(acc, 8)

if __name__=="__main__":
    main()
