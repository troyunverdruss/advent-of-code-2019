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

    funnel_width_at_kp = find_width_at_xy(instructions, known_point.x, known_point.y)
    multiplier = size // (funnel_width_at_kp[1] - funnel_width_at_kp[0])

    to_test_x = known_point.x * multiplier
    to_test_y = known_point.y * multiplier

    get_starting_point = True
    while get_starting_point:
        # We're not even *wide* enough here, let's jump again
        min_x, max_x = find_width_at_xy(instructions, to_test_x, to_test_y)
        if max_x - min_x < size:
            to_test_x += known_point.x * 2
            to_test_y += known_point.y * 2
            continue

        # We're not even *tall* enough here, let's jump again
        min_y, max_y = find_height_at_xy(instructions, to_test_x, to_test_y)
        if max_y - min_y < size:
            to_test_x += known_point.x * 2
            to_test_y += known_point.y * 2
            continue

        # Alright, height + width fit, finally
        get_starting_point = False

    closest_score = sys.maxsize
    step = 10
    fits = False

    # Start out with finding a place in the funnel where the ship FITS
    while not fits:
        print(f"Testing ({to_test_x}, {to_test_y})")
        r = test_point(instructions, to_test_x, to_test_y)
        if r != '#':
            raise Exception(f"Assumed slope is consistent, but ({to_test_x}, {to_test_x}) is not in funnel")

        min_x, max_x = find_width_at_xy(instructions, to_test_x, to_test_y)

        fits = test_for_square_starting_at(instructions, max_x - size, to_test_y, size)
        if fits:
            to_test_x = max_x-size
        else:
            print(f"!Fits: ({to_test_x}, {to_test_y})")
            to_test_x = max_x
            to_test_y += step

    # Ok, we found a place where the ship fits, let's start trying to find the
    # closest point while walking backwards
    best_x = to_test_x
    best_y = to_test_y
    searching = True
    while searching:
        if test_for_square_starting_at(instructions, best_x - 1, best_y - 1, size):
            best_x -= 1
            best_y -= 1
        elif test_for_square_starting_at(instructions, best_x - 1, best_y, size):
            best_x -= 1
        elif test_for_square_starting_at(instructions, best_x, best_y - 1, size):
            best_y -= 1
        else:
            searching = False

    return point_to_score(Point(best_x, best_y))
    # grid = defaultdict(lambda: '.')
    # for y in range(750, 1250, 10):
    #     for x in range(750, 1250, 10):
    #         res = test_point(instructions, x, y)
    #         grid[Point(x, y)] = res
    # print_buffer_to_console(grid)


def point_to_score(point: Point):
    return point.x * 10000 + point.y


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
    res2 = part2(_inst, Point(28, 35), size=100)
    print(res2)

    # minx, maxx = find_width_at_xy(_inst, 19, 24)
    # print(minx, maxx)

    pass
