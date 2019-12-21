from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


def part1(instructions):
    ic = IntcodeComputer(instructions)
    ic.run()
    ic.outputs.clear()
    # ic.inputs.extend(map(ord, list("OR D T\n")))
    # ic.inputs.extend(map(ord, list("NOT A J\n")))
    # ic.inputs.extend(map(ord, list("NOT A J\n")))
    # ic.inputs.extend(map(ord, list("NOT B T\n")))
    # ic.inputs.extend(map(ord, list("AND T J\n")))
    # ic.inputs.extend(map(ord, list("NOT C T\n")))
    # ic.inputs.extend(map(ord, list("AND T J\n")))
    # ic.inputs.extend(map(ord, list("AND D J\n")))



    #     # If A and B are empty, jump
    # ic.inputs.extend(map(ord, list("NOT A J\n")))
    # ic.inputs.extend(map(ord, list("NOT B T\n")))
    # ic.inputs.extend(map(ord, list("AND J T\n")))
    #
    #
    # # If A is empty, jump
    ic.inputs.extend(map(ord, list("NOT A J\n")))

    # If C is empty but D isn't, jump
    ic.inputs.extend(map(ord, list("NOT C T\n")))
    ic.inputs.extend(map(ord, list("OR T J\n")))
    # ic.inputs.extend(map(ord, list("NOT J T\n")))
    # ic.inputs.extend(map(ord, list("OR J T\n")))
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






if __name__ == "__main__":
    _inst = map(int, read_raw_entries("input21.txt")[0].split(","))
    r1 = part1(_inst)
    print(r1)
    pass






