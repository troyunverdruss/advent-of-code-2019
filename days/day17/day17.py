import itertools
import sys
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import List, Dict, Set, Union, Deque

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries
from string import ascii_uppercase


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


dirs = {"U": Point(0, -1), "L": Point(-1, 0), "R": Point(1, 0), "D": Point(0, 1)}
dirs_by_robot = {"v": "D", "<": "L", ">": "R", "^": "U"}
dir_to_straight = {"D": "D", "U": "U", "L": "L", "R": "R"}
dir_to_left = {"D": "R", "U": "L", "L": "D", "R": "U"}
dir_to_right = {"D": "L", "U": "R", "L": "U", "R": "D"}


def part1():
    inst = list(map(int, read_raw_entries("input17.txt")[0].split(',')))
    vr = VacuumRobot(inst)
    vr.ic.run()

    grid = defaultdict(lambda: '.')
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
    return grid


@dataclass
class State:
    dir: str
    loc: Point
    path: List
    covered: Set

    def __hash__(self):
        return hash(str(self.path))


@dataclass()
class Node:
    loc: Point
    neighbors: Dict


@dataclass
class Rover:
    dir: str
    loc: Point
    path: List


@dataclass
class PathLink:
    dir: str
    loc: Point


@dataclass
class HashableList:
    l: List

    def __hash__(self):
        return hash(str(self.l))


def part2(grid: Dict[Point, str]):
    # Let's build a new graph
    node_grid = {}
    grid_keys = set(grid.keys())
    for k in grid_keys:
        if grid[k] != '.':
            node_grid[k] = Node(k, {})

    for k in node_grid.keys():
        for direction, vector in dirs.items():
            if k + vector in node_grid.keys():
                node_grid[k].neighbors[direction] = node_grid[k + vector]

    start_loc, start_dir = list(filter(lambda i: i[1] in list("^v<>"), grid.items()))[0]
    rover = Rover(dirs_by_robot[start_dir], start_loc, [])

    searching = True
    while searching:
        straight = dir_to_straight[rover.dir]
        if rover.loc + dirs[straight] in node_grid.keys():
            rover.path.append(PathLink("S", rover.loc + dirs[straight]))
            rover.loc += dirs[straight]
            continue

        left = dir_to_left[rover.dir]
        if rover.loc + dirs[left] in node_grid.keys():
            rover.path.append(PathLink("L", rover.loc + dirs[left]))
            rover.loc += dirs[left]
            rover.dir = dir_to_left[rover.dir]
            continue

        right = dir_to_right[rover.dir]
        if rover.loc + dirs[right] in node_grid.keys():
            rover.path.append(PathLink("R", rover.loc + dirs[right]))
            rover.loc += dirs[right]
            rover.dir = dir_to_right[rover.dir]
            continue

        searching = False

    simplified_path = []
    length = 0
    for link in rover.path:
        if link.dir != 'S':
            simplified_path.append(length)
            length = 1
            simplified_path.append(link.dir)
        else:
            length += 1

    simplified_path.append(length)

    if simplified_path[0] == 0:
        simplified_path.remove(0)

    algorithms = {}
    tmp_algorithms = {}
    tmp_algorithms['A'] = {}
    # Find A
    a = tmp_algorithms['A']
    for i in range(10):
        candidate = HashableList(simplified_path[:i + 1])
        a[candidate] = 0
        for j in range(len(simplified_path)):
            if candidate.l == simplified_path[j:j + len(candidate.l)]:
                a[candidate] += 1

    tmp_algorithms['B'] = {}
    b = tmp_algorithms['B']
    for i in range(len(simplified_path) - 10, len(simplified_path)):
        candidate = HashableList(simplified_path[i:])
        b[candidate] = 0
        for j in range(len(simplified_path)):
            if candidate.l == simplified_path[j:j + len(candidate.l)]:
                b[candidate] += 1

    # Solve for the best combo
    a_candidates = list(
        map(lambda i: i[0].l, sorted(tmp_algorithms['A'].items(), key=lambda item: item[1], reverse=True)))
    b_candidates = list(
        map(lambda i: i[0].l, sorted(tmp_algorithms['B'].items(), key=lambda item: item[1], reverse=True)))
    working_combos = []
    for a, b in itertools.permutations(range(10), 2):
        if len(a_candidates[a]) > 10:
            continue
        if len(b_candidates[b]) > 10:
            continue

        candidate_a = ','.join(map(str, a_candidates[a]))
        candidate_b = ','.join(map(str, b_candidates[b]))
        target = ','.join(map(str, simplified_path))

        compressed_remainder = target.replace(candidate_a, '').replace(candidate_b, '')
        target_remainder = target.replace(candidate_a, 'A').replace(candidate_b, 'B')

        while ',,' in compressed_remainder:
            compressed_remainder = compressed_remainder.replace(',,', ',')
        if compressed_remainder[0] == ',':
            compressed_remainder = compressed_remainder[1:]
        if compressed_remainder[-1] == ',':
            compressed_remainder = compressed_remainder[:-1]

        remainder_list = compressed_remainder.split(',')
        for i in range(11):
            sublist = remainder_list[0:i]
            candidate_c = ','.join(map(str, sublist))

            if len(target_remainder) == target_remainder.replace(candidate_c, ''):
                break

            test_with_c = target_remainder.replace(candidate_c, 'C')
            is_empty = test_with_c.replace('A', '').replace('B', '').replace('C', '').replace(',', '')

            if len(is_empty) == 0:
                working_combos.append([test_with_c, candidate_a, candidate_b, candidate_c])

    if len(working_combos) == 0:
        raise Exception("Found 0 solutions")

    main = working_combos[0][0].split(',')
    routine_a = working_combos[0][1].split(',')
    routine_b = working_combos[0][2].split(',')
    routine_c = working_combos[0][3].split(',')

    inst = list(map(int, read_raw_entries("input17.txt")[0].split(',')))
    vr = VacuumRobot(inst)
    assert vr.ic.memory[0] == 1
    vr.ic.memory[0] = 2
    vr.ic.run()

    print_outputs(vr)

    feed_routine(vr, main)
    vr.ic.waiting = False
    vr.ic.run()
    print_outputs(vr)

    feed_routine(vr, routine_a)
    vr.ic.waiting = False
    vr.ic.run()
    print_outputs(vr)

    feed_routine(vr, routine_b)
    vr.ic.waiting = False
    vr.ic.run()
    print_outputs(vr)

    feed_routine(vr, routine_c)
    vr.ic.waiting = False
    vr.ic.run()
    print_outputs(vr)

    vr.ic.inputs.extend([ord('n'), ord('\n')])
    vr.ic.waiting = False
    vr.ic.run()
    print_outputs(vr)


def feed_routine(vr: VacuumRobot, routine: List):
    first = True
    for e in routine:
        if first:
            first = False
        else:
            vr.ic.inputs.append(ord(','))

        if e in ascii_uppercase:
            vr.ic.inputs.append(ord(e))
        else:
            for c in list(e):
                vr.ic.inputs.append(ord(c))

    vr.ic.inputs.append(ord('\n'))


def print_outputs(vr: VacuumRobot):
    too_large = list(filter(lambda v: v > 255, vr.ic.outputs))
    for n in too_large:
        vr.ic.outputs.remove(n)
    print(''.join(map(lambda c: chr(c), vr.ic.outputs)))

    if len(too_large) > 0:
        print(too_large)

    vr.ic.outputs.clear()


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
    _grid = part1()
    part2(_grid)
