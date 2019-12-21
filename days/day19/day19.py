import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
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

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y)


def part1(instructions):
    grid = defaultdict(lambda: '.')
    for y in range(50):
        for x in range(50):
            # print(x,y)
            res = test_point(instructions, x, y)
            grid[Point(x, y)] = res

    print_buffer_to_console(grid)

    find_sqaure_in_beam(grid, 2)
    find_sqaure_in_beam(grid, 3)
    point_n4 = find_sqaure_in_beam(grid, 4)
    find_sqaure_in_beam(grid, 5)

    return len(list(filter(lambda v: v == '#', grid.values()))), point_n4


dirs = {"U": Point(0, 1), "L": Point(-1, 0), "R": Point(1, 0), "D": Point(0, -1)}


def find_sqaure_in_beam(grid, n):
    _max_x = _max_y = -sys.maxsize
    _min_x = _min_y = sys.maxsize

    for key in grid.keys():
        _max_x = max(_max_x, key.x)
        _min_x = min(_min_x, key.x)
        _max_y = max(_max_y, key.y)
        _min_y = min(_min_y, key.y)

    for y in range(_min_y, _max_y):
        for x in range(_min_x, _max_x):
            if grid[Point(x, y)] != '#':
                continue

            _pass = True
            for test in get_test_coords(Point(x, y), n):
                if grid[test] != '#':
                    _pass = False
                    break

            if _pass:
                print(f"Found {n}x{n} square at ({x}, {y})")
                return Point(x, y)


def get_test_coords(origin, n):
    xs = []
    ys = []
    # for x in range(n):
    xs.append(origin.x)
    xs.append(origin.x + n - 1)
    ys.append(origin.y)
    ys.append(origin.y + n - 1)
    return [Point(x, y) for x, y in itertools.product(xs, ys)]


def test_point(instructions, x, y):
    ic = IntcodeComputer(instructions)
    ic.inputs.append(x)
    ic.inputs.append(y)
    ic.waiting = False
    ic.run()
    pulled = ic.outputs.popleft()
    # print(f"pulled: {pulled}")
    if pulled == 0:
        return '.'
    elif pulled == 1:
        return '#'
    else:
        raise Exception("bad response from drone")


def part2(instructions, known_point: Point, size=100):
    res = test_point(instructions, known_point.x, known_point.y)
    if res != '#':
        raise Exception("Need to start from a known good point")

    step = size
    closest_point = None
    to_test_x = known_point.x * step
    to_test_y = known_point.y * step
    while step > 0:

        r = test_point(instructions, to_test_x, to_test_y)
        if r != '#':
            raise Exception(f"Assumed slope is consistent, but ({to_test_x}, {to_test_x}) is not in funnel")

        min_x, max_x = find_width_at_xy(instructions, to_test_x, to_test_y)
        min_y, max_y = find_height_at_xy(instructions, to_test_x, to_test_y)
        # if max_x - min_x < size:
        #     step *= 2
        #     continue

        fits = test_for_square_starting_at(instructions, max_x - size, to_test_y, size)
        if fits:
            closest_point = Point(max_x - step, to_test_y)
            to_test_x = max_x - ((max_x - min_x) // 2) - size
            to_test_y = max
        else:
            step //= 2
            to_test_x += known_point.x * step
            to_test_y += known_point.y * step
    return closest_point.x * 10000 + closest_point.y

    # grid = defaultdict(lambda: '.')
    # for y in range(750, 1250, 10):
    #     for x in range(750, 1250, 10):
    #         res = test_point(instructions, x, y)
    #         grid[Point(x, y)] = res
    # print_buffer_to_console(grid)


def test_for_square_starting_at(instructions, x, y, n):
    for test in get_test_coords(Point(x, y), n):
        if test.x < 0 or test.y < 0:
            return False

        if test_point(instructions, test.x, test.y) == '.':
            return False

    return True


def find_width_at_xy(instructions, x, y):
    _x = x
    if test_point(instructions, _x, y) != '#':
        raise Exception("Expected xy to be in funnel")

    results = {Point(x, y): '#'}

    # Find min x
    test_width = 50
    while test_width > 0:
        res = test_point(instructions, _x - test_width, y)
        results[Point(_x - test_width, y)] = res
        if res == '#':
            _x -= test_width
            continue
        else:
            test_width //= 2

    # Find max x
    test_width = 50
    _x = x
    while test_width > 0:
        res = test_point(instructions, _x + test_width, y)
        results[Point(_x + test_width, y)] = res
        if res == '#':
            _x += test_width
            continue
        else:
            test_width //= 2
    print(list(filter(lambda i: i[1] == '#', results.items())))
    _min_x = min(map(lambda p: p[0].x, filter(lambda pair: pair[1] == '#', results.items())))
    _max_x = max(map(lambda p: p[0].x, filter(lambda pair: pair[1] == '#', results.items())))
    return _min_x, _max_x


def find_height_at_xy(instructions, x, y):
    _y = y
    if test_point(instructions, x, _y) != '#':
        raise Exception("Expected xy to be in funnel")

    results = {Point(x, y): '#'}

    # Find min y
    test_height = 50
    while test_height > 0:
        res = test_point(instructions, x, _y - test_height)
        results[Point(x, _y - test_height)] = res
        if res == '#':
            _y -= test_height
            continue
        else:
            test_height //= 2

    # Find max y
    test_height = 50
    _y = y
    while test_height > 0:
        res = test_point(instructions, x, _y + test_height)
        results[Point(x, _y + test_height)] = res
        if res == '#':
            _y += test_height
            continue
        else:
            test_height //= 2

    print(list(filter(lambda i: i[1] == '#', results.items())))
    _min_y = min(map(lambda p: p[0].y, filter(lambda pair: pair[1] == '#', results.items())))
    _max_y = max(map(lambda p: p[0].y, filter(lambda pair: pair[1] == '#', results.items())))
    return _min_y, _max_y


def search_for_n_square(instructions, n, seed):
    guess_x = seed.x
    guess_y = seed.y


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
            if buffer[Point(x, y)] == '.':
                print(" ", end="")
            else:
                print(buffer[Point(x, y)], end="")
            # print(" ", end="")
        print("")


if __name__ == "__main__":
    _inst = list(map(int, read_raw_entries("input19.txt")[0].split(",")))
    # res1, known_good_n4 = part1(_inst)
    # print(res1)
    #
    res2 = part2(_inst, Point(28, 35), size=5)
    print(res2)

    # minx, maxx = find_width_at_xy(_inst, 19, 24)
    # print(minx, maxx)

    pass
