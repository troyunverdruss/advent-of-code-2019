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

    def __hash__(self):
        h = f"{self.loc} {self.last_key()} {sorted(self.collected_keys_in_order)}"
        return hash(h)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def add_key(self, key):
        if key not in self.collected_keys_in_order:
            self.collected_keys_in_order.append(key)

    def last_key(self):
        if len(self.collected_keys_in_order) > 0:
            return self.collected_keys_in_order[-1]

        return None

    def sort_key(self):
        return (
            self.steps
        )


def part1(lines):
    grid, start, available_keys, doors = parse_map_to_grid(lines)

    _open = deque()
    _closed = set()

    _open.append(SearchState(start, [], 0))

    shortest_path = sys.maxsize
    while len(_open) > 0:
        current = list(sorted(_open, key=lambda ss: ss.sort_key()))[0]
        _open.remove(current)
        _closed.add(current)

        if len(current.collected_keys_in_order) == len(available_keys) and current.steps < shortest_path:
            shortest_path = current.steps
            continue

        for n in find_neighbors(grid, doors, current):
            next_state = SearchState(n, current.collected_keys_in_order[:], current.steps + 1)
            if grid[n] in ascii_lowercase:
                next_state.add_key(grid[n])

            if next_state not in _closed and next_state not in _open:
                _open.append(next_state)

    return shortest_path


dirs = {"U": Point(0, 1), "L": Point(-1, 0), "R": Point(1, 0), "D": Point(0, -1)}


def find_neighbors(grid: Dict[Point, str], doors: List, state: SearchState):
    neighbors = []

    for d in dirs.values():
        test_loc = state.loc + d
        if grid[test_loc] == '#':
            continue
        if grid[test_loc] in doors and grid[test_loc].lower() not in state.collected_keys_in_order:
            continue

        neighbors.append(test_loc)

    return neighbors


if __name__ == "__main__":
    _lines = read_raw_entries("input18.txt")
    r1 = part1(_lines)
    print(r1)
    pass
# too high 3822
