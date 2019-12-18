import sys
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


class VacuumRobot:
    # lookup = {35: "#", 46: ".", 10: "\n", 60: }

    def __init__(self, inst):
        self.ic = IntcodeComputer(inst)


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def alignment_param(self):
        return self.x * self.y

dirs = {"U": Point(0, 1), "L": Point(-1, 0), "R": Point(1, 0), "D": Point(0, -1)}


def part1():
    inst = list(map(int, read_raw_entries("input17.txt")[0].split(',')))
    vr = VacuumRobot(inst)
    vr.ic.run()

    grid =defaultdict(lambda: '.')
    x = 0
    y = 0
    max_y = 0
    max_x = 0
    while len(vr.ic.outputs) > 0:
        out = vr.ic.outputs.popleft()

        if out == 10:
            y += 1
            x = 0
            max_y = max(max_y, y)
        else:
            grid[Point(x, y)] = chr(out)
            x += 1
            max_x = max(max_x, x)

    print_buffer_to_console(grid)

    intersections = deque()
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            here = Point(x, y)

            if grid[here] == '#':
                intersection = True
                for d in dirs.values():
                    if grid[here + d] != "#":
                        intersection = False
                        break
                if intersection:
                    intersections.append(here)

    total = sum(map(lambda i: i.alignment_param(), intersections))
    print(total)


def print_buffer_to_console(buffer):
    _max_x = _max_y = -sys.maxsize
    _min_x = _min_y = sys.maxsize

    for key in buffer.keys():
        _max_x = max(_max_x, key.x)
        _min_x = min(_min_x, key.x)
        _max_y = max(_max_y, key.y)
        _min_y = min(_min_y, key.y)

    for y in range(_min_y, _max_y + 1):
        print(f"{str(y).zfill(3)}", end="")
        for x in range(_min_x, _max_x + 1):
            if buffer[Point(x,y)] == '.':
                print(" ", end="")
            else:
                print(buffer[Point(x, y)], end="")
            print(" ", end="")
        print("")


if __name__ == "__main__":
    part1()
