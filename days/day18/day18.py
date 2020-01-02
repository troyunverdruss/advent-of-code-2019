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
class SearchState:
    loc: Point
    required_keys: list
    other_keys: set
    # collected_keys: list
    steps: int
    doors: set
    collected_order: list

    def __str__(self):
        return f"{self.loc} {self.steps} {len(self.required_keys)}:{self.required_keys} {len(self.other_keys)}:{self.other_keys}"

    def __hash__(self):
        # s = f"{len(self.required_keys)} {len(self.other_keys)} {self.steps}"
        # s = f"{self.collected_order[-1]} {len(self.collected_order)}  {self.steps}"
        s = f"{self.collected_order[-1]} {len(self.collected_order)}"
        return hash(s)

    def __eq__(self, other):
        # return sorted(self.collected_order) == sorted(other.collected_order) \
        #        and (len(self.collected_order) != 0 and len(other.collected_order) != 0
        #             and self.collected_order[-1] == other.collected_order[-1]) \
        #        and self.steps == other.steps
        #
        return len(self.required_keys) == len(other.required_keys) \
               and (len(self.collected_order) != 0 and len(other.collected_order) != 0
                    and self.collected_order[-1] == other.collected_order[-1]) \
               and len(self.other_keys) == len(other.other_keys) \
               # and self.steps == other.steps
        # return self.loc == other.loc \
        #        and self.steps == other.steps \
        #        and self.remaining_doors() == other.remaining_doors() \
        #        and self.other_keys_count() == other.other_keys_count()

    def collected_key_count(self):
        return len(self.required_keys) + len(self.other_keys)

    def collected_keys(self):
        return self.required_keys + list(self.other_keys)

    def contains(self, key):
        return key in self.required_keys or key in self.other_keys

    def add_key(self, key):
        if key not in self.collected_order:
            self.collected_order.append(key)

        if key.upper() in self.doors:
            self.required_keys.append(key)
        else:
            self.other_keys.add(key)

    # def remaining_doors(self):
    #     return set(set(map(lambda d: d.lower(), self.doors)) - set(self.collected_keys))
    #
    # def other_keys_count(self):
    #     return len(set(self.collected_keys) - set(map(lambda d: d.lower(), self.doors)))
    #
    # def sorted_keys(self):
    #     return list(sorted(self.collected_keys))

    def sort_key(self):
        return (
            # This is the only sorting solution that HAS EVER worked for all the tests
            # So don't delete it without thinking
            -len(self.required_keys),
            self.steps,
            # End of ever-working list

            # len(self.doors) - len(self.required_keys),
            # self.steps,
            # self.collected_key_count()

            # -len(self.collected_keys())
            # len(self.required_keys) * 20 + len(self.other_keys) * 5 - self.steps
            # self.steps,
            # -len(self.required_keys),

        )


@dataclass
class SavedState:
    graph: nx.Graph
    grid: Dict
    start: Point
    keys: Dict
    target_key: str
    path_to_key: list
    total_distance: int

steps_by_collected_cache = {}

def part1_v2(_lines):
    grid, start, available_keys, required_doors = parse_map_to_grid(_lines)

    open = deque()
    shortest_path = sys.maxsize
    closed = deque()

    open.append(SearchState(start, [], set(), 0, required_doors, []))

    cycle = 0
    while len(open) > 0:
        cycle += 1
        if (cycle % 1000) == 0:
            print(f"Cycle: {cycle}, remaining open: {len(open)}")

        current: SearchState = open.popleft()  # list(sorted(open, key=lambda s: s.sort_key()))[0]
        # open.remove(current)
        closed.append(current)
        # print(f"Current: {current}")

        # If we ever get to a place where we're already longer than the best, bail on this path
        if current.steps >= shortest_path or current.steps > steps_by_collected_cache[current.__hash__()]:
            continue

        destinations = explore_map(grid, current)
        for d in sorted(destinations, key=lambda es: es.sort_key()):
            s = SearchState(d.loc, current.required_keys[:], set(current.other_keys), d.steps, required_doors,
                            current.collected_order[:])

            if grid[d.loc] in ascii_lowercase and not s.contains(grid[d.loc]):
                s.add_key(grid[d.loc])
            # print(f"Reached {s}")

            lookup_key = s.__hash__()
            if s.collected_key_count() == len(available_keys):
                # print(f"Final destination: {s}")
                if s.steps <= shortest_path:
                    shortest_path = s.steps
                    print(f"Shortest path so far: {shortest_path} via {s.collected_order}. Remaining open: {len(open)}")
                # Optionally append the solution
            elif s not in open and s not in closed:
                open.append(s)
            else:
                # lookup_key = (s.collected_order[-1], str(sorted(s.collected_order)))
                if s.steps < steps_by_collected_cache[lookup_key]:
                    open.append(s)
                # Then store the steps for this collected set, with final key
            # else:
            #     print(f"Not appending: {s}")
            steps_by_collected_cache[lookup_key] = s.steps
    return shortest_path


# def in_closed(closed, candidate):
#     filter(lambda ss: ss., closed)

@dataclass
class ExploreState:
    loc: Point
    steps: int
    door_key: bool = False

    def __hash__(self):
        return hash(str(f"{self.loc}"))

    def __eq__(self, other):
        return self.loc == other.loc

    def sort_key(self):
        return (
            self.steps,
            not self.door_key
        )


exploration_cache = {}


def explore_map(grid: Dict, state: SearchState):
    open = deque()
    closed = set()
    destinations = set()
    cached_destinations = set()

    lookup_key = (Point(state.loc.x, state.loc.y), ''.join(list(sorted(state.collected_keys()))))

    if lookup_key in exploration_cache:
        # print(f"Cache hit: {lookup_key}, value: {exploration_cache[lookup_key]}")
        dests = set()
        for cd in exploration_cache[lookup_key]:
            dests.add(ExploreState(cd.loc, cd.steps + state.steps))

        return dests

    open.append(ExploreState(state.loc, state.steps))

    while len(open) > 0:
        current = open.popleft()
        closed.add(current)

        for n in find_valid_neighbors(grid, current.loc, state.collected_keys()):
            s = ExploreState(n, current.steps + 1)

            if grid[s.loc] in ascii_lowercase and grid[s.loc] not in state.collected_keys():
                cached_state = ExploreState(n, current.steps + 1 - state.steps)
                if grid[s.loc] in ascii_uppercase:
                    s.door_key = True
                    cached_state.door_key = True

                cached_destinations.add(cached_state)
                destinations.add(s)

            elif s not in open and s not in closed:
                open.append(s)

    # # print(f"Possible destinations: {destinations}")
    # if lookup_key in exploration_cache and exploration_cache[lookup_key] != destinations:
    #     print(f"Cache has:       {exploration_cache[lookup_key]}")
    #     print(f"Really returned: {destinations}")

    exploration_cache[lookup_key] = set(cached_destinations)
    # return exploration_cache[lookup_key]
    return destinations


def find_valid_neighbors(grid: Dict[Point, str], loc: Point, collected_keys: List):
    neighbors = []

    for d in dirs.values():
        # If it's a wall
        if grid[loc + d] == '#':
            continue

        # or a door we don't have the key for
        if grid[loc + d] in ascii_uppercase and grid[loc + d].lower() not in collected_keys:
            continue

        # Or a key we already collected
        # if grid[loc + d] in collected_keys:
        #     continue

        neighbors.append(loc + d)

    # print(f"Valid neighbors {neighbors}")
    return neighbors


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


def parse_map_to_grid(_lines):
    grid = defaultdict(lambda: '#')
    starts = list()
    keys = set()
    doors = set()

    for y in range(len(_lines)):
        for x in range(len(_lines[y])):
            grid[Point(x, y)] = _lines[y][x]
            if _lines[y][x] == '@':
                starts.append(Point(x, y))
            elif _lines[y][x] in ascii_lowercase:
                keys.add(_lines[y][x])
            elif _lines[y][x] in ascii_uppercase:
                doors.add(_lines[y][x])

    return grid, starts, list(sorted(keys)), doors


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
    r1 = part1_v2(lines)
    print(r1)
    pass
# too high 3822
