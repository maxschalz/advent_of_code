import re
from dataclasses import dataclass


@dataclass
class Rule:
    name: str
    ranges: list

    def valid_value(self, value):
        return any(lower <= value <= upper for (lower, upper) in self.ranges)


class AllTickets:
    def __init__(self):
        self.tickets = []
        self.rules = []

    def __repr__(self):
        return str(self.tickets) + "\n" + str(self.rules)

    def add_ticket(self, ticket):
        self.tickets.append(ticket)

    def add_rule(self, name, ranges):
        self.rules.append(Rule(name, ranges))

    def scanning_error_rate(self, discard_invalid_tickets=False):
        rate = 0
        if discard_invalid_tickets:
            discard_idx = []
        for idx, ticket in enumerate(self.tickets):
            for value in ticket:
                is_valid = any(rule.valid_value(value) for rule in self.rules)
                if not is_valid:
                    rate += value
                    if discard_invalid_tickets:
                        discard_idx.append(idx)

        # I think this is super inefficient but anyway
        if discard_invalid_tickets:
            valid_tickets = []
            for idx, ticket in enumerate(self.tickets):
                if idx not in discard_idx:
                    valid_tickets.append(ticket)

            self.tickets = valid_tickets

        print(f"Ticket scanning error rate: {rate}")


def main():
    for fname in ("input.txt",):  # "input.txt"):
        tickets = AllTickets()
        status = "rules"
        with open(fname, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                if line == "your ticket:":
                    status = "your ticket"
                    continue
                if line == "nearby tickets:":
                    status = "nearby tickets"
                    continue

                if status == "rules":
                    name, rules = line.split(":", maxsplit=1)
                    pattern = re.compile(r"\d+-\d+")
                    string_ranges = pattern.findall(rules)
                    ranges = []
                    for range_ in string_ranges:
                        lower, upper = range_.split("-", maxsplit=1)
                        ranges.append((int(lower), int(upper)))

                    tickets.add_rule(name, ranges)
                elif status == "nearby tickets":
                    values = [int(val) for val in line.split(",")]
                    tickets.add_ticket(values)
                elif status == "your ticket":
                    print(line)

        tickets.scanning_error_rate(discard_invalid_tickets=True)


if __name__ == "__main__":
    main()
