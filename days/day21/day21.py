aoc17() if 'aoc17' in dir() else None
# from dataclasses import dataclass, field
from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


def part1(instructions):
    ic = IntcodeComputer(instructions)
    ic.run()
    ic.outputs.clear()

    # # If A is empty, jump
    ic.inputs.extend(map(ord, list("NOT A J\n")))

    # If C is empty but D isn't, jump
    ic.inputs.extend(map(ord, list("NOT C T\n")))
    ic.inputs.extend(map(ord, list("OR T J\n")))
    ic.inputs.extend(map(ord, list("AND D J\n")))

    ic.inputs.extend(map(ord, list("WALK\n")))

    ic.waiting = False
    ic.run()

    for c in ic.outputs:
        try:
            to_print = chr(c)
        except:
            return c
        print(to_print, end="")


def part2(instructions):
    ic = IntcodeComputer(instructions)
    ic.run()
    ic.outputs.clear()

    # # If C is empty but D isn't, jump
    ic.inputs.extend(map(ord, list("NOT C T\n")))
    ic.inputs.extend(map(ord, list("OR T J\n")))

    # if H is blank, delay jumping
    ic.inputs.extend(map(ord, list("AND H J\n")))

    # if E is not blank, go ahead and jump
    ic.inputs.extend(map(ord, list("NOT E T\n")))
    ic.inputs.extend(map(ord, list("NOT T T\n")))
    ic.inputs.extend(map(ord, list("OR T J\n")))

    # If B is a hole
    ic.inputs.extend(map(ord, list("NOT B T\n")))
    ic.inputs.extend(map(ord, list("OR T J\n")))

    # Failsafe, jump if A is empty ...
    # # # If A is empty, jump
    ic.inputs.extend(map(ord, list("NOT A T\n")))
    ic.inputs.extend(map(ord, list("OR T J\n")))

    # ... but don't jump if D is empty
    ic.inputs.extend(map(ord, list("AND D J\n")))

    ic.inputs.extend(map(ord, list("RUN\n")))

    ic.waiting = False
    ic.run()

    for c in ic.outputs:
        try:
            to_print = chr(c)
        except:
            return c
        print(to_print, end="")


if __name__ == "__main__":
    _inst = list(map(int, read_raw_entries("input21.txt")[0].split(",")))
    r1 = part1(_inst[:])
    print(f"Part 1: {r1}")
    r2 = part2(_inst[:])
    print(f"Part 2: {r2}")
