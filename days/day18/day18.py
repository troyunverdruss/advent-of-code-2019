import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, Dict
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
class SavedState:
    graph: nx.Graph
    grid: Dict
    start: Point
    keys: Dict
    target_key: str
    path_to_key: list
    total_distance: int


def part1(_lines):
    graph, grid, start, keys, doors = parse_map(_lines)

    to_test = deque()
    # seen = set()
    to_test_best_keys_to_distance = {}
    
    best_path_distance = sys.maxsize
    targets = reachable(graph, start, keys)
    for k, p in sorted(targets.items(), key=lambda p: len(p[1])):
        print(k, p)
        to_search_state = SavedState(graph.copy(), deepcopy(grid), deepcopy(start), deepcopy(keys), k, p, 0)
        to_test.append(to_search_state)
        # seen.add(hash(to_search_state))

    while len(to_test) > 0:
        state: SavedState = to_test.popleft()
        while len(state.keys.keys()) > 0:
            state.total_distance += len(state.path_to_key) - 1
            if state.total_distance > best_path_distance:
                # Can't get shorter
                break

            unlock_door(state.graph, state.grid, doors, state.target_key)
            del state.keys[state.target_key]
            state.start = state.path_to_key[-1]

            targets = reachable(state.graph, state.start, state.keys)
            if len(targets.keys()) == 0:
                # No targets, so just bail
                break

            first = True
            for k, p in sorted(targets.items(), key=lambda p: len(p[1])):
                if first:
                    first = False
                    state.target_key = k
                    state.path_to_key = p
                else:
                    to_search_state = SavedState(state.graph.copy(), deepcopy(state.grid), deepcopy(state.start),
                                             deepcopy(state.keys), k, p, state.total_distance)
                    # seen.add(hash(to_search_state))
                    to_test.append(
                        to_search_state
                    )
        if len(state.keys) == 0:
            print(f"New best: {state.total_distance}")
            best_path_distance = state.total_distance
    return best_path_distance

    # while len(keys) > 0:
    #     results = find_best(graph, grid, start, keys, doors)
    #     best = sorted(results, key=lambda r: (r.keys_captured, r.distance))[0]
    #     unlock_door(graph, grid, doors, best.next_key)
    #     del keys[best.next_key]


@dataclass
class SearchResult:
    next_key: str
    keys_captured: int
    distance: int


def find_best(graph: nx.Graph, grid: Dict, start: Point, keys: Dict, doors: Dict, depth=2) -> List[SearchResult]:
    if depth == 0 or len(keys) == 0:
        return [SearchResult('', 0, 0)]

    destinations = reachable(graph, start, keys)

    results = []
    for dst_key in destinations.keys():
        _graph = graph.copy()
        _start = deepcopy(start)
        _keys = deepcopy(keys)

        result = SearchResult(dst_key, 1, len(destinations[dst_key]) - 1)

        del _keys[dst_key]
        unlock_door(_graph, grid, doors, dst_key)

        to_merge = find_best(_graph, grid, destinations[dst_key][-1], _keys, doors, depth - 1)

        i = 0
    return best


def reachable(graph, start, keys):
    res = {}
    for key in keys:
        try:
            path = nx.dijkstra_path(graph, start, keys[key])
            res[key] = path
        except Exception as e:
            pass
    return res


dirs = {"U": Point(0, 1), "L": Point(-1, 0), "R": Point(1, 0), "D": Point(0, -1)}


def unlock_door(graph, grid, doors, key: str):
    if key.upper() in doors:
        # print(f"Unlocking door: {key.upper()}")
        door_loc = doors[key.upper()]
        grid[door_loc] = '.'
        for d in dirs.values():
            if grid[door_loc + d] == '.' or grid[door_loc + d] in ascii_lowercase:
                graph.add_edge(door_loc, door_loc + d)


def parse_map(_lines):
    graph = nx.Graph()
    start = None
    keys = {}
    doors = {}

    grid = defaultdict(lambda: '#')
    for y in range(len(_lines)):
        for x in range(len(_lines[y])):
            grid[Point(x, y)] = _lines[y][x]
    for y in range(len(_lines)):
        for x in range(len(_lines[y])):
            if grid[Point(x, y)] == '#':
                continue
            if grid[Point(x, y)] in ascii_uppercase:
                doors[grid[Point(x, y)]] = Point(x, y)
                continue

            for d in dirs.values():
                if grid[Point(x, y) + d] == '.' or grid[Point(x, y) + d] in ascii_lowercase \
                        or grid[Point(x, y) + d] == '@':
                    graph.add_edge(Point(x, y), Point(x, y) + d)
            if grid[Point(x, y)] in ascii_lowercase:
                keys[grid[Point(x, y)]] = Point(x, y)
            if grid[Point(x, y)] == '@':
                start = Point(x, y)

    return graph, grid, start, keys, doors


if __name__ == "__main__":
    lines = read_raw_entries("input18.txt")
    part1(lines)
    pass
