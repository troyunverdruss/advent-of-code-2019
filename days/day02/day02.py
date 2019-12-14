import itertools
from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


# Here we just run the IntcodeComputer until it quits,
# then read the value in the zero index in memory
def part1(instructions: List[int]):
    ic = IntcodeComputer(instructions)
    ic.set_noun(12)
    ic.set_verb(2)
    ic.run()
    return ic.memory[0]


# Here we're gonna try every combo of numbers from 0 to 99
# and after each run of the ic completes, check if the zero
# index in memory holds the magic target number. When it does,
# return that value
def part2(instructions: List[int]):

    for noun, verb in itertools.product(range(100), repeat=2):
        ic = IntcodeComputer(instructions)
        ic.set_noun(noun)
        ic.set_verb(verb)
        ic.run()
        if ic.memory[0] == 19690720:
            return noun * 100 + verb


if __name__ == "__main__":
    lines = read_raw_entries("input02.txt")
    raw_instructions = list(map(lambda x: int(x), lines[0].split(",")))

    part1 = part1(raw_instructions[:])
    print(f"Part 1: 1202 => {part1}")

    part2 = part2(raw_instructions[:])
    print(f"Part 2: {part2} => 19690720")
