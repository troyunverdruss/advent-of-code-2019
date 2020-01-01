import sys
from collections import defaultdict
from dataclasses import dataclass
from os import read
from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


dirs = {"north": Point(0, -1), "south": Point(0, 1), "west": Point(-1, 0), "east": Point(1, 0)}


def part1(inst):
    grid = defaultdict(lambda: '#')
    loc = Point(0, 0)
    grid[loc] = '@'

    ic = IntcodeComputer(inst)

    last_loc = loc
    while True:
        ic.waiting = False
        ic.run()
        for line in print_outputs(ic):
            if line == '- north' and grid[loc + dirs["north"]] == '#':
                grid[loc + dirs["north"]] = '?'
            elif line == '- south' and grid[loc + dirs["south"]] == '#':
                grid[loc + dirs["south"]] = '?'
            elif line == '- west' and grid[loc + dirs["west"]] == '#':
                grid[loc + dirs["west"]] = '?'
            elif line == '- east' and grid[loc + dirs["east"]] == '#':
                grid[loc + dirs["east"]] = '?'

        print_buffer_to_console(grid, loc)

        if not ic.running:
            break

        cmd = input()
        while cmd[0] == 'x':
            if cmd == 'xback':
                loc = last_loc
                print(f"Corrected to {loc}")
                print_buffer_to_console(grid, loc)
            cmd = input()

        if cmd in dirs.keys():
            grid[loc] = 'O'
            loc += dirs[cmd]
            grid[loc] = 'x'

        ic.inputs.extend(map(ord, list(cmd) + ['\n']))


def print_buffer_to_console(buffer, loc):
    _max_x = _max_y = -sys.maxsize
    _min_x = _min_y = sys.maxsize

    for key in buffer.keys():
        _max_x = max(_max_x, key.x)
        _min_x = min(_min_x, key.x)
        _max_y = max(_max_y, key.y)
        _min_y = min(_min_y, key.y)

    leading_zeros = 3
    col_spacer = ' '
    # Print x headers
    x_headers = {}
    for x in range(_min_x, _max_x + 1):
        for y in range(leading_zeros):
            x_headers[Point(x, y)] = list(str(x).zfill(leading_zeros))[y]

    for y in range(leading_zeros):
        print(' ' * leading_zeros, end="")
        print(col_spacer, end="")
        for x in range(_min_x, _max_x + 1):
            print(x_headers[Point(x, y)], end="")
            print(col_spacer, end="")
        print("")

    for y in range(_min_y, _max_y + 1):
        print(f"{str(y).zfill(leading_zeros)}", end="")
        for x in range(_min_x, _max_x + 1):

            # Now print the horizontal spacer
            if x + dirs["west"].x >= _min_x and buffer[Point(x, y) + dirs["west"]] != '#':
                print("-", end="")
            else:
                print(col_spacer, end="")

            # if Point(x, y) == Point(0, 0) and loc == Point(0, 0):
            #     print("O", end="")
            # #     print(" ", end="")
            # else:
            print(buffer[Point(x, y)], end="")


        # Now print the vertical spacer
        # print("")
        # print(" " * leading_zeros, end="")
        # for x in range(_min_x, _max_x+1):
        #     if buffer[Point(x,y)] != '#' and buffer[Point(x,y) + dirs["south"]] != '#':
        #         print("|", end="")
        #     else:
        #         print("#", end="")
        print("")


def print_outputs(ic: IntcodeComputer):
    too_large = list(filter(lambda v: v > 255, ic.outputs))
    for n in too_large:
        ic.outputs.remove(n)
    output_data = ''.join(map(lambda c: chr(c), ic.outputs))
    print(output_data)

    if len(too_large) > 0:
        print(f'Too large: {too_large}')

    ic.outputs.clear()
    return output_data.split('\n')


if __name__ == "__main__":
    _instructions = map(int, read_raw_entries("input25.txt")[0].split(','))
    part1(_instructions)
    pass
