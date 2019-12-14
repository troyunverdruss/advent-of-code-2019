from itertools import permutations
from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


# We're just gonna brute force try all the possible phases
def part1(instructions):
    max_output = 0
    for permutation in permutations(range(5)):
        output = run_part1_with_permutation(instructions, permutation)

        if output > max_output:
            max_output = output

    return max_output


# Try each permutation
def run_part1_with_permutation(instructions, permutation):
    input_value = 0
    for phase_setting in permutation:
        ic = IntcodeComputer(instructions)
        ic.set_inputs([phase_setting, input_value])
        ic.run()
        input_value = ic.get_outputs()[0]
    return input_value


# Same deal, just brute forcing it
def part2(instructions):
    max_output = 0
    for permutation in permutations(range(5, 10)):
        # print(f"trying {permutation}")

        output = run_part2_with_permutation(instructions, permutation)

        if output > max_output:
            max_output = output

    return max_output


# A little trickier on part 2, need to keep trying until they all halt
def run_part2_with_permutation(instructions, permutation):
    # Set up an IC for each letter in a list
    ics = []
    for index, _id in enumerate(list("ABCDE")):
        ic = IntcodeComputer(instructions, _id)
        ic.set_inputs([permutation[index]])
        ics.append(ic)

    # Seed A with 0
    ics[0].inputs.append(0)

    # We need to know what the final output is
    last_output = 0

    # I don't want to over-complicate the logic to get *into* the loop the
    # first time, or put all the checks at the end
    start = True

    # Running has a specific meaning here, and that is that it hasn't *halted*. A
    # computer can be paused waiting for input, but it since it has not halted, it is
    # still "running". So as long as any of the ics are running, keep churning through.
    # An ic in a "paused" state won't proceed to do anything until it has received input
    # so you can call run() on it as many times as you want
    while start or any(map(lambda c: c.running, ics)):
        # You can only start once
        start = False

        # Run every ic. Paused ics will just skip quickly,
        # unpaused ones will run, produce output, then we'll
        # stuff it into the next one's input for it to consume
        # when it runs again
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
