from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


def part1(instructions, _inputs=[]):
    ic = IntcodeComputer(instructions)
    ic.set_inputs(_inputs)
    # ic.enable_stdout = True
    ic.run()
    print(ic.outputs)
    return ic.outputs


if __name__ == "__main__":
    raw_instructions = list(map(int, read_raw_entries("input09.txt")[0].split(",")))
    part1(raw_instructions, [1])
    part1(raw_instructions, [2])
