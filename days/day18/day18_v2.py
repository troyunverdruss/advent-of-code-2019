import heapq
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, Dict

from days.day18.day18 import parse_map_to_grid
from helpers import read_raw_entries
from string import ascii_lowercase, ascii_uppercase
from copy import deepcopy
import networkx as nx


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


@dataclass
class SearchState:
    loc: Point
    collected_keys_in_order: list
    steps: int
    doors: set
    door_keys_in_order: list

    def __str__(self):
        return f"{self.loc} {self.steps} {self.last_key()} {sorted(self.collected_keys_in_order)}"

    def __hash__(self):
        h = f"{self.loc} {self.last_key()} {len(self.door_keys_in_order)} {len(self.collected_keys_in_order)}"
        return hash(h)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        # if self.sort_key() == other.sort_key():
        #     return 0
        # if self == list(sorted([self.sort_key(), other.sort_key]))[0]
        #     return -1
        # return 1
        return self.sort_key() < other.sort_key()

    def add_key(self, key):
        if key not in self.collected_keys_in_order:
            self.collected_keys_in_order.append(key)
            if key.upper() in self.doors:
                self.door_keys_in_order.append(key)

    def last_key(self):
        if len(self.collected_keys_in_order) > 0:
            return self.collected_keys_in_order[-1]

        return None

    def steps_per_key(self):
        if len(self.collected_keys_in_order) > 0:
            return self.steps / len(self.collected_keys_in_order)
        return sys.maxsize

    def sort_key(self):
        return (
            self.steps,
            # -len(self.collected_keys_in_order),
            # self.steps_per_key()
        )


def part1(lines):
    grid, start, available_keys, doors = parse_map_to_grid(lines)

    _open = []
    _closed = set()

    heapq.heapify(_open)
    first_state = SearchState(start, [], 0, doors, [])
    _open.append(first_state)

    shortest_path = sys.maxsize
    cycles = 0
    while len(_open) > 0:
        cycles += 1
        current = heapq.heappop(_open)  # list(sorted(_open, key=lambda ss: ss.sort_key()))[0]
        # _open.remove(current)
        _closed.add(current)

        if len(current.collected_keys_in_order) == len(available_keys) and current.steps < shortest_path:
            shortest_path = current.steps
            print(f"Shortest path: {shortest_path}")
            continue

        for n in find_neighbors(grid, doors, current):
            next_state = SearchState(n, current.collected_keys_in_order[:], current.steps + 1, doors, current.door_keys_in_order[:])
            if grid[n] in ascii_lowercase:
                next_state.add_key(grid[n])

            if next_state not in _closed and next_state not in _open:
                _open.append(next_state)

    return shortest_path


dirs = {"U": Point(0, 1), "L": Point(-1, 0), "R": Point(1, 0), "D": Point(0, -1)}

neighbor_cache = {}
def find_neighbors(grid: Dict[Point, str], doors: List, state: SearchState):
    neighbors = []

    lookup_key = (state.loc, str(sorted(state.door_keys_in_order)))
    # if lookup_key in neighbor_cache:
    #     return neighbor_cache[lookup_key]

    for d in dirs.values():
        test_loc = state.loc + d
        if grid[test_loc] == '#':
            continue
        if grid[test_loc] in doors and grid[test_loc].lower() not in state.door_keys_in_order:
            continue

        neighbors.append(test_loc)

    neighbor_cache[lookup_key] = neighbors[:]
    return neighbors


if __name__ == "__main__":
    _lines = read_raw_entries("input18.txt")
    r1 = part1(_lines)
    print(r1)
    pass
# too high 3802
