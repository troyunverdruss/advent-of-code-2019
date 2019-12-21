import math
from collections import deque
from dataclasses import dataclass
from typing import List, Iterable
from helpers import read_raw_entries
from itertools import combinations, islice
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


@dataclass
class Point:
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __hash__(self):
        return hash(str(self))


@dataclass
class Moon:
    loc: Point
    vel: Point = Point()
    id: str = ""

    def move(self):
        self.loc.x += self.vel.x
        self.loc.y += self.vel.y
        self.loc.z += self.vel.z

    def energy(self):
        potential = abs(self.loc.x) + abs(self.loc.y) + abs(self.loc.z)
        kinetic = abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)
        return potential * kinetic

    def __hash__(self):
        return hash(str(self))

    def hash_by_axis(self, axis):
        if axis == 'x':
            return f"{self.loc.x} {self.vel.x}"
        elif axis == 'y':
            return f"{self.loc.y} {self.vel.y}"
        elif axis == 'z':
            return f"{self.loc.z} {self.vel.z}"
        else:
            raise Exception("unexpected axis: " + axis)


@dataclass
class Changeset:
    m1: Moon
    m1_vel: Point
    m2: Moon
    m2_vel: Point


def compute_changeset(m1: Moon, m2: Moon):
    m1_vel = Point()
    m2_vel = Point()

    if m1.loc.x > m2.loc.x:
        m1_vel.x -= 1
        m2_vel.x += 1
    elif m1.loc.x < m2.loc.x:
        m1_vel.x += 1
        m2_vel.x -= 1
    if m1.loc.y > m2.loc.y:
        m1_vel.y -= 1
        m2_vel.y += 1
    elif m1.loc.y < m2.loc.y:
        m1_vel.y += 1
        m2_vel.y -= 1
    if m1.loc.z > m2.loc.z:
        m1_vel.z -= 1
        m2_vel.z += 1
    elif m1.loc.z < m2.loc.z:
        m1_vel.z += 1
        m2_vel.z -= 1

    return Changeset(m1, m1_vel, m2, m2_vel)


def part1(moons, steps):
    for _ in range(steps):
        do_step(moons)

    return sum(map(lambda m: m.energy(), moons))


def do_step(moons):
    changesets: List[Changeset] = []
    for combo in combinations(moons, 2):
        changesets.append(compute_changeset(combo[0], combo[1]))

    for changeset in changesets:
        changeset.m1.vel += changeset.m1_vel
        changeset.m2.vel += changeset.m2_vel

    for moon in moons:
        moon.move()


def part2(moons):
    iter_start = time.time()

    sets_of_seen_by_axis = {}
    seeking_by_axis = {}

    _id = 0
    for m in moons:
        m.id = f"Moon {_id}"
        _id += 1

    for axis in list('xyz'):
        sets_of_seen_by_axis[axis] = set()
        seeking_by_axis[axis] = True

    while any(seeking_by_axis.values()):
        do_step(moons)

        for axis in list('xyz'):
            all_moons_one_axis_hash = hash(str(list(map(lambda m: m.hash_by_axis(axis), moons))))
            if all_moons_one_axis_hash in sets_of_seen_by_axis[axis]:
                seeking_by_axis[axis] = False
            else:
                sets_of_seen_by_axis[axis].add(all_moons_one_axis_hash)
    lengths = list(map(lambda x: len(x), sets_of_seen_by_axis.values()))
    return lcm(lengths)


def lcm(numbers: List[int]) -> int:
    _lcm = numbers[0]
    for n in numbers[1:]:
        _lcm = _lcm * n / math.gcd(_lcm, n)
        _lcm = int(_lcm)
    return _lcm


def parse_input(lines: List[str]):
    moons = []
    for line in lines:
        coord_tokens = line.replace("<", "").replace(">", "").replace(",", "").split(" ")
        x, y, z = map(lambda ct: int(ct.split("=")[1]), coord_tokens)
        moons.append(Moon(Point(x, y, z)))
    return moons


if __name__ == "__main__":
    raw_lines = read_raw_entries("input12.txt")
    _moons = parse_input(raw_lines)
    part1 = part1(_moons, 1000)
    print(f"Part 1: {part1}")

    _moons_2 = parse_input(raw_lines)
    part2 = part2(_moons_2)
    print(f"Part 2: {part2}")

# 307_043_147_758_488
