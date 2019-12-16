import heapq
import sys
from collections import deque, defaultdict
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
        past_positions = [Point(self.loc.x, self.loc.y)]
        while len(_path) > 0:
            if len(_path) == 1:
                final_step = True

            p = _path.pop(0)

            if p == self.loc:
                # print("Starting at ", self.loc)
                continue

            d = self.loc.dir_to(p)

            self.ic.inputs.append(d.command)
            self.ic.waiting = False
            self.ic.run()

            out = self.ic.outputs.popleft()
            # if out == 2:
            #     print("reached o2", self.loc + d.point, end="")

            if final_step:
                if out == 1 or out == 2:
                    self.loc += d.point
                    past_positions.append(Point(self.loc.x, self.loc.y))
                # print("END1")
                return responses[out]
            else:
                if out == 0:
                    msg = f"Ran into wall at {p}, result: {out}!"
                    print(msg)
                    raise Exception(msg)
                self.loc += d.point
                past_positions.append(Point(self.loc.x, self.loc.y))
            # print(self.loc, end="")
            # print(" -> ", end="")
        # print("END2")


def part1(inst):
    graph, oxygen_tank = get_oxygen_tank_location(inst)
    # sub 1 because we want steps between, not all points
    return len(nx.dijkstra_path(graph, Point(0, 0), oxygen_tank)) - 1


def get_oxygen_tank_location(inst):
    graph = nx.Graph()
    graph.add_node(Point(0, 0))

    grid = defaultdict(lambda: ' ')
    grid[Point(0, 0)] = '.'

    robot = Robot(inst)
    oxygen_tank = find_oxygen_tank(graph, grid, robot)
    return graph, oxygen_tank


def part2(inst):
    _, oxygen_tank = get_oxygen_tank_location(inst)
    print(f"o2 tank: {oxygen_tank}")

    graph = nx.Graph()
    graph.add_node(Point(0, 0))
    grid = defaultdict(lambda: ' ')
    grid[Point(0, 0)] = '.'
    robot = Robot(inst)

    # try:
    explore_everything(graph, grid, robot)
    # except Exception as e:
    #     print(e)
    #     print_buffer_to_console(grid)

    longest_path = 0
    for p in map(lambda p: p[0], filter(lambda p: p[1] in list('.o'), grid.items())):
        #     path = nx.dijkstra_path(graph, oxygen_tank, p[0])
        #     nx.all_pairs_dijkstra_path()
        if p == oxygen_tank:
            continue

        path = nx.dijkstra_path(graph, oxygen_tank, p)
        longest_path = max(len(path) - 1, longest_path)

    return longest_path


def explore_everything(graph: nx.Graph, grid, robot):
    _open = deque()
    _closed = set()
    _closed.add(Point(0, 0))

    initial_neighbors = neighbor_coords(robot.loc)
    _open.extend(initial_neighbors)

    oxygen_tank = None

    while len(_open) > 0:
        # Get a destination
        loc = _open.popleft()
        _closed.add(loc)
        if loc in grid and grid[loc] == '#':
            continue

        # Find a neighbor of our destination that we know we can get to
        destination = None
        for n in neighbor_coords(loc):
            if n in graph and grid[n] in list('.o'):
                destination = n
                break

        if destination is None:
            raise Exception("Couldn't find neighbor for " + loc)

        path = nx.dijkstra_path(graph, robot.loc, destination)
        result = robot.follow(path + [loc])
        if loc in grid and grid[loc] != ' ':
            raise Exception("We've already visited this point?" + loc)
        grid[loc] = result
        if result == 'o':
            oxygen_tank = loc
            # grid[loc] = '.'

        if result != '#':
            graph.add_edge(destination, loc)
        else:
            continue

        neighbors = neighbor_coords(loc)
        for n in neighbors:
            if n not in _open and n not in _closed:
                _open.append(n)

        print_buffer_to_console(grid, robot.loc, oxygen_tank)
        # print("----------------------------")

    # all_pairs = nx.all_pairs_dijkstra_path(graph)


def print_buffer_to_console(buffer, robot_loc, oxygen_tank):
    _max_x = _max_y = -sys.maxsize
    _min_x = _min_y = sys.maxsize

    for key in buffer.keys():
        _max_x = max(_max_x, key.x)
        _min_x = min(_min_x, key.x)
        _max_y = max(_max_y, key.y)
        _min_y = min(_min_y, key.y)

    print("Robot is supposed to be at: ", robot_loc)
    print("Oxygen tank is supposed to be at: ", oxygen_tank)

    for y in range(_min_y, _max_y + 1):
        print(f"{str(y).zfill(3)}", end="")
        for x in range(_min_x, _max_x + 1):
            if Point(x, y) == Point(0, 0):
                print("X", end="")
            elif Point(x, y) == robot_loc:
                print("R", end="")
            else:
                print(buffer[Point(x, y)], end="")
            # print(" ", end="")
        print("")


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
    part1 = part1(raw_instructions[:])
    print(f"Part 1: {part1}")

    part2 = part2(raw_instructions[:])
    print(f"Part 2: {part2}")
