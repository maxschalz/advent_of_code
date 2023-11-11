from collections import deque

N_TURN = 30000000


def main():
    for fname in ("test_input.txt", "input.txt"):
        print(f"Using file {fname}:")
        part1(fname)


def part1(fname):
    with open(fname, "r", encoding="utf-8") as file:
        starting_numbers = [int(i) for i in file.readline().split(",")]

    numbers = {}
    for turn, starting_number in enumerate(starting_numbers, start=1):
        numbers[starting_number] = deque((turn,), maxlen=2)

    # Turn after the last starting number
    last_number_spoken = starting_numbers[-1]
    for turn in range(len(starting_numbers) + 1, N_TURN + 1):
        if turn % 1000000 == 0:
            print(f"\tTurn {turn:10d} / {N_TURN}")
        try:
            second_to_last_time, last_time = numbers[last_number_spoken]
        except ValueError:
            this_number = 0
        else:
            this_number = last_time - second_to_last_time
        try:
            numbers[this_number].append(turn)
        except KeyError:
            numbers[this_number] = deque((turn,), maxlen=2)

        last_number_spoken = this_number

    print(f"\tLast number spoken: {last_number_spoken}")


if __name__ == "__main__":
    main()
