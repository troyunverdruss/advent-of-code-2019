from collections import defaultdict
from dataclasses import dataclass
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


def map_to_graph(grid: Dict):
    graph = nx.Graph()
    portals = defaultdict(lambda: [])
    start = None
    end = None
    map_locs = list(grid.keys())
    for key in map_locs:
        val = grid[key]
        loc = key
        if val == '.':
            for d in dirs.values():
                neighbor = grid[loc + d]
                if neighbor == '.':
                    graph.add_edge(loc, loc+d)
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
                    if portal == 'AA':
                        start = _up
                    elif portal == 'ZZ':
                        end = _up
                    else:
                        portals[portal].append(_up)
                elif grid[_down] == '.':
                    if portal == 'AA':
                        start = _down
                    elif  portal == 'ZZ':
                        end = _down
                    else:
                        portals[portal].append(_down)
                else:
                    raise Exception("problem with finding adjacent up/down square")

            elif right in ascii_uppercase:
                portal += right
                _left = loc + dirs["LT"]
                _right = loc + dirs["RT"] + dirs["RT"]
                if grid[_left] == '.':
                    if portal == 'AA':
                        start = _left
                    elif  portal == 'ZZ':
                        end=_left
                    else:
                        portals[portal].append(_left)
                elif grid[_right] == '.':
                    if portal == 'AA':
                        start = _right
                    elif portal == 'ZZ':
                        end = _right
                    else:
                        portals[portal].append(_right)
                else:
                    raise Exception("problem with finding adjacent left/right square")
    for key in portals.keys():
        assert len(portals[key]) == 2
        graph.add_edge(portals[key][0], portals[key][1])

    return graph, start, end


def part1(lines):
    grid = parse_map(lines)
    graph, start, end = map_to_graph(grid)

    path = nx.dijkstra_path(graph, start, end)
    print(path)
    return len(path)-1

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

# 4788 too high
