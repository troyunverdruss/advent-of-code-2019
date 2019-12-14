import enum
import math
import sys
from collections import defaultdict, namedtuple, deque
from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries

Point = namedtuple('Point', ['x', 'y'])


class Color(enum.Enum):
    BLACK = 0
    WHITE = 1


class Dir(enum.Enum):
    UP = Point(0, 1)
    DN = Point(0, -1)
    LT = Point(-1, 0)
    RT = Point(1, 0)


class PaintingRobot:
    color_lookup = {Color.BLACK: 0, Color.WHITE: 1}
    color_reverse_lookup = {0: Color.BLACK, 1: Color.WHITE}
    rotate_lookup = {
        Dir.UP: {0: Dir.LT, 1: Dir.RT},
        Dir.DN: {0: Dir.RT, 1: Dir.LT},
        Dir.LT: {0: Dir.DN, 1: Dir.UP},
        Dir.RT: {0: Dir.UP, 1: Dir.DN}
    }

    def __init__(self, instructions, hull):
        self.ic = IntcodeComputer(instructions)
        self.loc = Point(0, 0)
        self.dir = Dir.UP
        self.hull = hull
        self.painted = set()

        self.testing = False
        self.test_outputs = deque()

    def run(self):
        start = True
        while start or self.ic.running:
            start = False
            self.step()

    def step(self):
        color = self.hull[self.loc]
        # print(color)
        # print(self.color_lookup[color])
        self.ic.inputs.append(PaintingRobot.color_lookup[color])

        if not self.testing:
            self.ic.waiting = False
            self.ic.run()

        if self.testing:
            new_color = self.test_outputs.popleft()
            new_dir = self.test_outputs.popleft()
        else:
            new_color = self.ic.outputs.popleft()
            new_dir = self.ic.outputs.popleft()

        self.hull[self.loc] = PaintingRobot.color_reverse_lookup[new_color]

        # Track painted squares
        self.painted.add(self.loc)

        self.dir = self.rotate_lookup[self.dir][new_dir]

        self.loc = Point(self.loc.x + self.dir.value.x, self.loc.y + self.dir.value.y)


def part1(instructions):
    hull = defaultdict(lambda: Color.BLACK)

    robot = PaintingRobot(instructions, hull)
    robot.run()
    return len(robot.painted)


def part2(instructions):
    hull = defaultdict(lambda: Color.BLACK)
    hull[Point(0, 0)] = Color.WHITE

    robot = PaintingRobot(instructions, hull)
    robot.run()

    _max_x = _max_y = -sys.maxsize
    _min_x = _min_y = sys.maxsize

    for key in hull.keys():
        _max_x = max(_max_x, key.x)
        _min_x = min(_min_x, key.x)
        _max_y = max(_max_y, key.y)
        _min_y = min(_min_y, key.y)

    # _min_x = min(map(lambda k: k.x, hull.keys()))
    # _max_x = max(map(lambda k: k.x, hull.keys()))
    # _min_y = min(map(lambda k: k.y, hull.keys()))
    # _max_y = max(map(lambda k: k.y, hull.keys()))

    print_buffer_to_console(Point(_min_x, _min_y), _max_x - _min_x, _max_y - _min_y, hull)


def print_buffer_to_console(origin, wide, tall, buffer):
    color_lookup = {Color.BLACK: " ", Color.WHITE: "#"}

    for y in range(tall, -1, -1):
        print(f"{y}", end="")
        for x in range(wide + 1):
            print(color_lookup[buffer[Point(origin.x + x, origin.y + y)]], end="")
            print(" ", end="")
        print("")


if __name__ == "__main__":
    raw_instructions = list(map(int, read_raw_entries("input11.txt")[0].split(",")))
    part1 = part1(raw_instructions[:])
    print(part1)

    part2(raw_instructions[:])
