import re
from collections import defaultdict
from copy import deepcopy

N_BITS = 36


class Initialiser:
    def __init__(self, fname):
        self.mask = N_BITS * " "
        self.memory = defaultdict(int)

        with open(fname, "r") as input_data:
            self.program = input_data.readlines()

    @staticmethod
    def get_mem_address(query):
        expr = re.compile("\[(\d+)\]")
        return expr.search(query).group(1)

    def run_initialisation(self, version="v1"):
        for line_number, operation in enumerate(self.program):
            print(f"In line {line_number}")
            operation = operation.strip()
            lhs, rhs = operation.split(" = ", maxsplit=1)
            if lhs.startswith("mas"):
                self.mask = rhs
            elif lhs.startswith("mem"):
                mem_address = Initialiser.get_mem_address(lhs)
                if version == "v1":
                    self.store_value_v1(rhs, mem_address)
                else:
                    self.store_value_v2(rhs, mem_address)
            else:
                raise ValueError(f"Operation not correct. Operation: {operation}")

    def store_value_v1(self, value, mem_address):
        binary_repr = list(bin(int(value))[2:].zfill(N_BITS))
        for position, masked_bit in enumerate(self.mask):
            if masked_bit == "X":
                continue
            binary_repr[position] = masked_bit

        updated_value = int("".join(binary_repr), 2)
        self.memory[mem_address] = updated_value

    def store_value_v2(self, value, mem_address):
        pass

    def get_sum(self):
        sum_ = sum(self.memory.values())
        print(f"Sum is {sum_}.")


if __name__ == "__main__":
    FNAME = "input.txt"
    for version in ("v1", "v2"):
        init = Initialiser(FNAME)
        init.run_initialisation(version=version)
        init.get_sum()
