import heapq
from collections import deque
from dataclasses import dataclass
from typing import List
import networkx as nx

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def dir_to(self, other):
        p = Point(other.x - self.x, other.y - self.y)
        return list(filter(lambda d: d.point == p, dirs.values()))[0]

    def __hash__(self):
        return hash(str(self))


@dataclass
class Direction:
    command: int
    point: Point


@dataclass
class MapNode:
    point: Point
    type: str


dirs = {
    "north": Direction(1, Point(0, 1)),
    "south": Direction(2, Point(0, -1)),
    "west": Direction(3, Point(-1, 0)),
    "east": Direction(4, Point(1, 0)),
}

responses = {
    0: '#',
    1: '.',
    2: 'o',
}


class Robot:
    def __init__(self, inst):
        self.instructions = inst[:]
        self.ic = IntcodeComputer(inst)
        self.loc = Point(0, 0)

    def follow(self, path: List[Point]):
        _path = path[:]
        final_step = False
        while len(_path) > 0:
            if len(_path) == 1:
                final_step = True

            p = _path.pop(0)

            if p == self.loc:
                continue

            d = self.loc.dir_to(p)

            self.ic.inputs.append(d.command)
            self.ic.waiting = False
            self.ic.run()

            out = self.ic.outputs.popleft()

            if final_step:
                if out == 1:
                    self.loc += d.point
                return responses[out]
            else:
                if out != 1:
                    raise Exception("Ran into wall!")
                self.loc += d.point


def part1(inst):
    graph = nx.Graph()
    graph.add_node(Point(0, 0))
    grid = {Point(0, 0): '.'}

    robot = Robot(inst)

    oxygen_tank = find_oxygen_tank(graph, grid, robot)
    return len(nx.dijkstra_path(graph, Point(0, 0), oxygen_tank))


def find_oxygen_tank(graph: nx.Graph, grid, robot):
    _open = deque()
    _closed = set()
    _closed.add(Point(0, 0))

    initial_neighbors = neighbor_coords(robot.loc)
    _open.extend(initial_neighbors)
    for init_n in initial_neighbors:
        graph.add_edge(robot.loc, init_n)

    oxygen_location = None
    while oxygen_location is None:
        # Get a destination
        loc = _open.popleft()
        _closed.add(loc)
        if loc in grid and grid[loc] == '#':
            continue

        # Find a path to it
        path = nx.dijkstra_path(graph, robot.loc, loc)
        result = robot.follow(path)
        grid[loc] = result
        if result == '#':
            graph.remove_node(loc)
            continue
        elif result == 'o':
            oxygen_location = robot.loc

        neighbors = neighbor_coords(loc)
        for n in neighbors:
            if n not in _open and n not in _closed:
                _open.appendleft(n)
                graph.add_edge(loc, n)

    return oxygen_location


def neighbor_coords(loc: Point):
    return [loc + d.point for d in dirs.values()]


if __name__ == "__main__":
    raw_instructions = list(map(int, read_raw_entries("input15.txt")[0].split(",")))
    part1 = part1(raw_instructions)
    print(f"Part 1: {part1}")
