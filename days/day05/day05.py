from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


def part1(instructions):
    ic = IntcodeComputer(instructions)
    ic.set_inputs([1])
    ic.run()
    outputs = ic.get_outputs()
    return outputs[-1]


def part2(instructions):
    ic = IntcodeComputer(instructions)
    ic.set_inputs([5])
    ic.run()
    outputs = ic.get_outputs()
    return outputs[-1]


if __name__ == "__main__":
    lines = read_raw_entries("input05.txt")
    raw_instructions = list(map(lambda x: int(x), lines[0].split(",")))

    part1 = part1(raw_instructions)
    print(f"Part 1: {part1}")

    part2 = part2(raw_instructions)
    print(f"Part 2: {part2}")
