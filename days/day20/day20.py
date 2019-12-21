import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import List, Dict
from string import ascii_uppercase

import networkx as nx

from helpers import read_raw_entries


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y)


dirs = {"DN": Point(0, 1), "UP": Point(0, -1), "RT": Point(1, 0), "LT": Point(-1, 0)}


@dataclass
class GraphNode:
    loc: Point
    neighbors: list
    portal_dest_lookup: Dict
    portal: bool = False


def map_to_graph(grid: Dict):
    part1_graph = nx.Graph()
    part2_graph = {}

    portals = defaultdict(lambda: [])
    # Need to save this off bc default dict can create new keys and blow up looping
    map_locs = list(grid.keys())

    for key in map_locs:
        val = grid[key]
        loc = key
        if val == '.':
            for d in dirs.values():
                neighbor = grid[loc + d]
                if neighbor == '.':
                    part1_graph.add_edge(loc, loc + d)
        elif val in ascii_uppercase:
            # based on traversal order
            # topmost first
            # leftmost first
            down = grid[loc + Point(0, 1)]
            right = grid[loc + Point(1, 0)]
            portal = val
            if down in ascii_uppercase:
                portal += down
                _up = loc + dirs["UP"]
                _down = loc + dirs["DN"] + dirs["DN"]
                if grid[_up] == '.':
                    portals[portal].append(_up)
                elif grid[_down] == '.':
                    portals[portal].append(_down)
                else:
                    raise Exception("problem with finding adjacent up/down square")

            elif right in ascii_uppercase:
                portal += right
                _left = loc + dirs["LT"]
                _right = loc + dirs["RT"] + dirs["RT"]
                if grid[_left] == '.':
                    portals[portal].append(_left)
                elif grid[_right] == '.':
                    portals[portal].append(_right)
                else:
                    raise Exception("problem with finding adjacent left/right square")

    start = portals['AA'][0]
    end = portals['ZZ'][0]
    del portals['AA']
    del portals['ZZ']

    for point in part1_graph:
        neighbors = list(nx.neighbors(part1_graph, point))
        part2_graph[point] = GraphNode(point, neighbors, {})

    for key in portals.keys():
        assert len(portals[key]) == 2
        part1_graph.add_edge(portals[key][0], portals[key][1])
        p = GraphNode(Point(-1, -1),
                      portals[key],
                      {portals[key][0]: portals[key][1], portals[key][1]: portals[key][0]},
                      True)
        part2_graph[key] = p
        for n in portals[key]:
            part2_graph[n].neighbors.append(key)

    return part1_graph, part2_graph, start, end


def part1(lines):
    grid = parse_map(lines)
    graph, _, start, end = map_to_graph(grid)

    path = nx.dijkstra_path(graph, start, end)
    print(path)
    return len(path) - 1


@dataclass
class SearchState:
    level: int
    loc: Point
    steps: int

    def __hash__(self):
        return hash(f"{self.level} {self.loc}")

    def __eq__(self, other):
        return self.level == other.level and self.loc == other.loc


def part2(lines):
    grid = parse_map(lines)
    _, graph, start, end = map_to_graph(grid)
    _open = deque()
    _closed = set()

    _open.append(SearchState(0, start, 0))
    final = SearchState(0, end, 0)

    # Figure out which portals are on the "outer" ring
    _max_x = _max_y = -sys.maxsize
    _min_x = _min_y = sys.maxsize
    for key in graph.keys():
        if type(key) is Point:
            _max_x = max(_max_x, key.x)
            _min_x = min(_min_x, key.x)
            _max_y = max(_max_y, key.y)
            _min_y = min(_min_y, key.y)

    searching = True
    steps = -1
    while len(_open) > 0 and searching:
        here = _open.popleft()
        _closed.add(here)

        # Are we done?
        if here == final:
            steps = here.steps
            searching = False

        for neighbor in graph[here.loc].neighbors:
            # Deal with normal neighbors
            if type(neighbor) is Point:
                ss = SearchState(here.level, neighbor, here.steps + 1)
                if ss == final:
                    steps = ss.steps
                    searching = False

                if ss not in _open and ss not in _closed:
                    _open.append(ss)

            # And now deal with portal neighbors
            else:
                assert graph[neighbor].portal
                # outer ring
                if here.loc.x in [_min_x, _max_x] or here.loc.y in [_min_y, _max_y]:
                    if here.level == 0:
                        # Outer level means they're walls
                        continue
                    else:
                        ss = SearchState(here.level - 1, graph[neighbor].portal_dest_lookup[here.loc], here.steps + 1)
                # inner ring
                else:
                    ss = SearchState(here.level + 1, graph[neighbor].portal_dest_lookup[here.loc], here.steps + 1)

                if ss not in _open and ss not in _closed:
                    _open.append(ss)
    return steps


def parse_map(lines):
    grid = defaultdict(lambda: ' ')
    for y, line in enumerate(lines):
        for x, val in enumerate(list(line)):
            grid[Point(x, y)] = val
    return grid


if __name__ == "__main__":
    _lines = read_raw_entries("input20.txt", strip=False)
    r1 = part1(_lines)
    print(r1)

    r2 = part2(_lines)
    print(r2)

# 4788 too high
