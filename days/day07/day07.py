from itertools import permutations
from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


def part1(instructions):
    max_output = 0
    for permutation in permutations(range(5)):
        output = run_part1_with_permutation(instructions, permutation)

        if output > max_output:
            max_output = output

    return max_output


def run_part1_with_permutation(instructions, permutation):
    input_value = 0
    for phase_setting in permutation:
        ic = IntcodeComputer(instructions)
        ic.set_inputs([phase_setting, input_value])
        ic.run()
        input_value = ic.get_outputs()[0]
    return input_value


def part2(instructions):
    max_output = 0
    for permutation in permutations(range(5, 10)):
        # print(f"trying {permutation}")

        output = run_part2_with_permutation(instructions, permutation)

        if output > max_output:
            max_output = output

    return max_output


def run_part2_with_permutation(instructions, permutation):
    ics = []
    for index, _id in enumerate(list("ABCDE")):
        ic = IntcodeComputer(instructions, _id)
        ic.set_inputs([permutation[index]])
        ics.append(ic)

    ics[0].inputs.append(0)

    last_output = 0
    start = True

    while start or any(map(lambda c: c.is_running(), ics)):
        start = False
        for index, ic in enumerate(ics):
            ic.run()
            output = ic.get_outputs().pop()

            next_index = (index + 1) % len(ics)
            ics[next_index].inputs.append(output)
            ics[next_index].waiting = False

            last_output = output

    # print(f" => last output {last_output}")

    return last_output


if __name__ == "__main__":
    raw_instructions = list(map(int, read_raw_entries("input07.txt")[0].split(",")))
    part1 = part1(raw_instructions)
    print(f"Part 1: {part1}")

    part2 = part2(raw_instructions)
    print(f"Part 2: {part2}")
