from collections import deque
from dataclasses import dataclass
from typing import List
from helpers import read_raw_entries
from itertools import combinations
import time


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

    cycles_to_repeat = {}
    seeking_repeat = {}
    sets_of_seen = {}
    states_of_seen = {}
    _id = 0
    for m in moons:
        m.id = f"Moon {_id}"
        _id += 1
        sets_of_seen[m.id] = set()
        states_of_seen[m.id] = deque()
        sets_of_seen[m.id].add(hash(m))
        seeking_repeat[m.id] = True
        states_of_seen[m.id].append(str(m))

    seen = set()
    seeking = True
    repeat = 0
    seen.add(hash(tuple(map(lambda m: hash(m), moons))))

    count = 0
    while any(map(lambda m: seeking_repeat[m.id], moons)) or seeking:
        count += 1
        if count % 1_000_000 == 0:
            now = time.time()
            print(f"Iteration {count}. Took {now - iter_start} seconds since last mark")
            iter_start = now
        do_step(moons)

        for m in moons:
            h = hash(m)
            if h in sets_of_seen[m.id]:
                seeking_repeat[m.id] = False
                cycles_to_repeat[m.id] = count
            elif seeking_repeat[m.id]:
                sets_of_seen[m.id].add(h)
                states_of_seen[m.id].append(str(m))

        state = hash(tuple(map(lambda m: hash(m), moons)))
        if state in seen:
            seeking = False
            repeat = count
        seen.add(state)

    print(cycles_to_repeat)
    for m in moons:
        print(m)

    return repeat


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
