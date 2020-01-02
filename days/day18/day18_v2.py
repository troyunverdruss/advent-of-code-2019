import heapq
import itertools
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, Dict, Iterable, Set

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
    current_key: str
    collected_keys_in_order: list
    steps: int

    def __str__(self):
        return f"{self.last_key()} {self.steps} {sorted(self.collected_keys_in_order)}"

    def __hash__(self):
        h = f"{self.last_key()} {''.join(sorted(self.collected_keys_in_order))}"
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
            # if key.upper() in self.doors:
            #     self.door_keys_in_order.append(key)

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
            len(self.collected_keys_in_order)
            # self.steps,
            # -len(self.collected_keys_in_order),
            # self.steps_per_key()
        )


@dataclass
class TraversalData:
    start: str
    end: str
    steps: int
    required_keys: set

    def is_open(self, collected_keys: Iterable[str]):
        return len(self.required_keys - set(collected_keys)) == 0


@dataclass
class TraversalSearchState:
    loc: Point
    doors: set
    keys: set
    steps: int

    def __hash__(self):
        h = f"{self.loc}"
        return hash(h)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        return self.sort_key() < other.sort_key()

    def sort_key(self):
        return (
            self.steps
        )


def build_traversal_data(grid: Dict[Point, str], keys: List[str]):
    traversal_data = defaultdict(lambda: {})
    key_to_loc = {}
    door_to_loc = {}

    for _loc, _val in list(grid.items()):
        if _val in ascii_lowercase:
            key_to_loc[_val] = _loc
        elif _val in ascii_uppercase:
            door_to_loc[_val] = _loc
        elif _val == '@':
            key_to_loc['_'] = _loc

    for start_key in ['_'] + keys:
        _open = []
        _closed = {}

        heapq.heapify(_open)

        _open.append(TraversalSearchState(key_to_loc[start_key], set(), set(), 0))

        found_ends = 0
        while len(_open) > 0 and found_ends < len(keys):
            current = heapq.heappop(_open)

            if grid[current.loc] in ascii_lowercase and start_key != grid[current.loc]:
                end_key = grid[current.loc]
                required_keys = set(map(lambda d: d.lower(), current.doors))
                traversal_data[start_key][end_key] = TraversalData(start_key, end_key, current.steps, required_keys)
                if start_key != '_':
                    traversal_data[end_key][start_key] = TraversalData(end_key, start_key, current.steps, required_keys)
                found_ends += 1

            _closed[current] = current

            for d in dirs.values():
                if grid[current.loc + d] == '#':
                    continue
                doors = set(current.doors)
                if grid[current.loc + d] in ascii_uppercase:
                    doors.add(grid[current.loc + d])
                _keys = set(current.keys)
                if grid[current.loc + d] in ascii_lowercase:
                    _keys.add(grid[current.loc + d])

                next_state = TraversalSearchState(current.loc + d, doors, _keys, current.steps + 1)
                if next_state not in _open and next_state not in _closed:
                    _open.append(next_state)

    return traversal_data


@dataclass
class DijkstraSearchNode:
    last_key: str
    visited: set
    distance: int

    def __hash__(self):
        h = f"{self.last_key} {sorted(self.visited)}"
        return hash(h)

    def __eq__(self, other):
        return hash(self) == hash(other)


def part1(lines):
    grid, start, available_keys, doors = parse_map_to_grid(lines)
    traversal_data = build_traversal_data(grid, available_keys)

    return distance_to_collect_keys(available_keys, traversal_data, '_', set(available_keys), {})


def distance_to_collect_keys(all_keys: List[str],
                             traversal_data: Dict[str, Dict[str, TraversalData]],
                             current_key: str,
                             keys: Set[str],
                             cache: Dict):
    if len(keys) == 0:
        return 0

    cache_key = (current_key, str(sorted(keys)))
    if cache_key in cache:
        return cache[cache_key]

    result = sys.maxsize
    collected_keys = set(all_keys) - set(keys)
    reachable_keys = set()
    for lookup_key in traversal_data[current_key].keys():
        if traversal_data[current_key][lookup_key].is_open(collected_keys):
            reachable_keys.add(lookup_key)

    for key in reachable_keys & keys:
        d = traversal_data[current_key][key].steps \
            + distance_to_collect_keys(all_keys, traversal_data, key, keys - set(key), cache)
        result = min(d, result)

    cache[cache_key] = result
    return result


def part1x(lines):
    grid, start, available_keys, doors = parse_map_to_grid(lines)

    traversal_data = build_traversal_data(grid, available_keys)

    cache = {}
    start = DijkstraSearchNode('_', set('_'), 0)
    cache[start] = start

    last_visited = []
    last_visited.append(start)
    current_unvisited = []
    next_unvisited = []

    for _ in range(len(available_keys)):
        # Set up my initial "next" nodes
        for node in last_visited:
            for k in sorted(available_keys):
                if node.last_key == k:
                    continue

                if traversal_data[node.last_key][k].is_open(node.visited):
                    n = DijkstraSearchNode(k, node.visited, node.distance + traversal_data[node.last_key][k].distance)
                    if n in cache:
                        continue

                    next_unvisited.append(n)
                    cache[n] = n

        last_visited.clear()
        for unvisited in current_unvisited:
            unvisited.distance = traversal_data[node.last_key][unvisited.last_key]
            last_visited.append(
                unvisited
            )


# def thing():
#     _queue = []
#     _open = {}
#     _closed = {}
#     _cache = {}
#
#     heapq.heapify(_queue)
#     first_state = SearchState(['_'], 0, doors, [])
#     _queue.append(first_state)
#     _open[first_state] = first_state
#
#     shortest_path = sys.maxsize
#     cycles = 0
#     while len(_queue) > 0:
#         print_cycle_debug_info(_closed, _queue, cycles, shortest_path)
#
#         # Get the next item
#         current = heapq.heappop(_queue)
#         del _open[current]
#         _closed[current] = current
#
#         # Check if it's actually a solution
#         if len(current.collected_keys_in_order) == len(available_keys) + 1 and current.steps < shortest_path:
#             shortest_path = current.steps
#             print(f"Shortest path: {shortest_path}")
#             continue
#
#         visited = {}
#         unvisited = []
#         for u in get_available_targets(traversal_data, current):
#             unvisited.append(SearchState(
#
#             ))
#         for dest in
#
#         for dest in get_available_targets(traversal_data, current):
#             next_state = SearchState(
#                 current.collected_keys_in_order[:],
#                 current.steps + dest.steps,
#                 doors,
#                 current.door_keys_in_order[:])
#             next_state.add_key(dest.end)
#
#             if next_state not in _queue and next_state not in _closed:
#                 _queue.append(next_state)
#                 _open[next_state] = next_state
#             elif next_state in _open and next_state.steps < _open[next_state].steps:
#                 _open[next_state].steps = next_state.steps
#             elif next_state in _closed and next_state.steps < _closed[next_state].steps:
#                 del _closed[next_state]
#                 _queue.append(next_state)
#                 _open[next_state] = next_state
#
#         # for n in  find_neighbors(grid, doors, current):
#         #     next_state = SearchState(n, current.collected_keys_in_order[:], current.steps + 1, doors,
#         #                              current.door_keys_in_order[:])
#         #     if grid[n] in ascii_lowercase:
#         #         next_state.add_key(grid[n])
#         #
#         #     if next_state not in _closed and next_state not in _open:
#         #         _open.append(next_state)
#
#     return shortest_path


def print_cycle_debug_info(_closed, _queue, cycles, shortest_path):
    cycles += 1
    if cycles % 100 == 0:
        print(
            f"Cycle: {cycles}, open: {len(_queue)}, closed: {len(_closed)}, current shortest path: {shortest_path}")


def get_available_targets(traversal_data: Dict[str, Dict[str, TraversalData]], state: SearchState):
    available_targets = list(filter(
        lambda td: td.is_open(state.collected_keys_in_order) and td.end not in state.collected_keys_in_order,
        traversal_data[state.last_key()].values()
    ))
    sorted_targets = list(sorted(
        available_targets,
        key=lambda td: td.steps
    ))
    return sorted_targets


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
