import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from os import read
from typing import List, Iterable

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


dirs = {"north": Point(0, -1), "south": Point(0, 1), "west": Point(-1, 0), "east": Point(1, 0)}
dir_opposites = {"north": "south", "south": "north", "west": "east", "east": "west"}


@dataclass
class Room:
    name: str
    desc: str
    loc: Point
    doors: list
    items: list
    path = []

    def __hash__(self):
        h = f"{self.name}"
        return hash(h)

    def __eq__(self, other):
        return hash(self) == hash(other)


def part1(inst):
    rooms = search_map(inst)
    for room in rooms.values():
        print(room.name)
        print(room.desc)
        print(room.items)
        print(room.loc)
        print(room.path)
        print()

    items_to_collect = find_collectable_items(inst, rooms.values())

    grid = defaultdict(lambda: '#')
    loc = Point(0, 0)
    grid[loc] = '@'

    ic = IntcodeComputer(inst)
    collect_items(ic, items_to_collect)

    # At this point, you've collected everything you can and need to
    # go to the security checkpoint amnd try to get past. This might mean
    # dropping and picking up things until you are the correct weight
    # and might take a lot of guesses ... items in inventory:
    #
    # - space law space brochure
    # - fixed point
    # - candy cane
    # - sand
    # - ornament
    # - fuel cell
    # - spool of cat6
    # - wreath

    last_loc = loc
    while True:
        ic.waiting = False
        ic.run()
        for line in print_outputs(ic):
            if line == '- north' and grid[loc + dirs["north"]] == '#':
                grid[loc + dirs["north"]] = '?'
            elif line == '- south' and grid[loc + dirs["south"]] == '#':
                grid[loc + dirs["south"]] = '?'
            elif line == '- west' and grid[loc + dirs["west"]] == '#':
                grid[loc + dirs["west"]] = '?'
            elif line == '- east' and grid[loc + dirs["east"]] == '#':
                grid[loc + dirs["east"]] = '?'

        print_buffer_to_console(grid, loc)

        if not ic.running:
            break

        cmd = input()
        while cmd[0] == 'x':
            if cmd == 'xback':
                loc = last_loc
                print(f"Corrected to {loc}")
                print_buffer_to_console(grid, loc)
            cmd = input()

        if cmd in dirs.keys():
            grid[loc] = 'O'
            loc += dirs[cmd]
            grid[loc] = 'x'

        ic.inputs.extend(map(ord, list(cmd) + ['\n']))
def collect_items(ic, items):
    for item, room in items.items():
        max_index = len(room.path) - 1
        for index, step in enumerate(room.path):
            ic.set_ascii_cmd(step)
            ic.waiting = False
            ic.run()

            if index == max_index:
                ic.set_ascii_cmd("take " + room.items[0])
                ic.waiting = False
                ic.run()
                # output_data = ''.join(map(lambda c: chr(c), ic.outputs))
                ic.outputs.clear()
                # print(output_data)
            else:
                ic.outputs.clear()

        for index, step in enumerate(reversed(room.path)):
            ic.set_ascii_cmd(dir_opposites[step])
            ic.waiting = False
            ic.run()

            if index == max_index:
                output_data = ''.join(map(lambda c: chr(c), ic.outputs)).split(('\n'))
                should_be_home = process_output_data(Point(0, 0), output_data)
                assert should_be_home.name == '== Hull Breach =='
            else:
                ic.outputs.clear()


def find_collectable_items(inst, rooms: Iterable[Room]):
    items = {}

    for room in rooms:
        if len(room.items) > 0:
            if "infinite loop" in room.items:
                continue

            ic = IntcodeComputer(inst)
            ic.run()
            ic.outputs.clear()

            max_index = len(room.path) - 1
            for index, step in enumerate(room.path):
                ic.set_ascii_cmd(step)
                ic.waiting = False
                ic.run()

                if index == max_index:
                    ic.set_ascii_cmd("take " + room.items[0])
                    ic.waiting = False
                    ic.run()
                    output_data = ''.join(map(lambda c: chr(c), ic.outputs))
                    ic.outputs.clear()
                    print(output_data)
                else:
                    ic.outputs.clear()

            for index, step in enumerate(reversed(room.path)):
                ic.set_ascii_cmd(dir_opposites[step])
                ic.waiting = False
                ic.run()

                if index == max_index:
                    output_data = ''.join(map(lambda c: chr(c), ic.outputs)).split(('\n'))
                    should_be_home = process_output_data(Point(0, 0), output_data)
                    if should_be_home.name == '== Hull Breach ==':
                        items[room.items[0]] = room
                else:
                    ic.outputs.clear()

    return items


@dataclass
class SearchState:
    loc: Point
    next_step: str
    ic: IntcodeComputer


def search_map(inst):
    to_visit = deque()
    rooms = {}
    to_visit.append([])

    while to_visit:

        loc = Point(0, 0)
        path = to_visit.popleft()

        ic = IntcodeComputer(inst)
        ic.run()
        if len(path) == 0:

            output_data = ''.join(map(lambda c: chr(c), ic.outputs)).split('\n')
            ic.outputs.clear()
            room = process_output_data(loc, output_data)
            room.loc = loc
            rooms[room.name] = room

            for door in set(room.doors):
                to_visit.append(path[:] + [door])
        else:
            ic.outputs.clear()

        current_path = []
        for step in path:
            current_path.append(step)
            loc += dirs[step]
            ic.set_ascii_cmd(step)
            ic.waiting = False
            ic.run()

            output_data = ''.join(map(lambda c: chr(c), ic.outputs)).split('\n')
            ic.outputs.clear()
            room = process_output_data(loc, output_data)

            if room not in rooms.values():
                room.path = current_path[:]
                rooms[room.name] = room

                for door in (set(room.doors) - {dir_opposites[step]}):
                    to_visit.append(path[:] + [door])

    return rooms


def process_output_data(loc, output_data):
    name = ''
    desc = ''
    doors = []
    items = []
    while len(output_data) > 0:
        line = output_data.pop(0)

        if line.startswith('=='):
            name = line
            desc = output_data.pop(0)
        elif line in ['- north', '- south', '- west', '- east']:
            doors.append(line.replace('- ', ''))
        elif line.startswith('- '):
            items.append(line.replace('- ', ''))
    return Room(name, desc, loc, doors, items)


def print_buffer_to_console(buffer, loc):
    _max_x = _max_y = -sys.maxsize
    _min_x = _min_y = sys.maxsize

    for key in buffer.keys():
        _max_x = max(_max_x, key.x)
        _min_x = min(_min_x, key.x)
        _max_y = max(_max_y, key.y)
        _min_y = min(_min_y, key.y)

    leading_zeros = 3
    col_spacer = ' '
    # Print x headers
    x_headers = {}
    for x in range(_min_x, _max_x + 1):
        for y in range(leading_zeros):
            x_headers[Point(x, y)] = list(str(x).zfill(leading_zeros))[y]

    for y in range(leading_zeros):
        print(' ' * leading_zeros, end="")
        print(col_spacer, end="")
        for x in range(_min_x, _max_x + 1):
            print(x_headers[Point(x, y)], end="")
            print(col_spacer, end="")
        print("")

    for y in range(_min_y, _max_y + 1):
        print(f"{str(y).zfill(leading_zeros)}", end="")
        for x in range(_min_x, _max_x + 1):

            # Now print the horizontal spacer
            if x + dirs["west"].x >= _min_x and buffer[Point(x, y) + dirs["west"]] != '#':
                print("-", end="")
            else:
                print(col_spacer, end="")

            # if Point(x, y) == Point(0, 0) and loc == Point(0, 0):
            #     print("O", end="")
            # #     print(" ", end="")
            # else:
            print(buffer[Point(x, y)], end="")

        # Now print the vertical spacer
        # print("")
        # print(" " * leading_zeros, end="")
        # for x in range(_min_x, _max_x+1):
        #     if buffer[Point(x,y)] != '#' and buffer[Point(x,y) + dirs["south"]] != '#':
        #         print("|", end="")
        #     else:
        #         print("#", end="")
        print("")


def print_outputs(ic: IntcodeComputer):
    too_large = list(filter(lambda v: v > 255, ic.outputs))
    for n in too_large:
        ic.outputs.remove(n)
    output_data = ''.join(map(lambda c: chr(c), ic.outputs))
    print(output_data)

    if len(too_large) > 0:
        print(f'Too large: {too_large}')

    ic.outputs.clear()
    return output_data.split('\n')


if __name__ == "__main__":
    _instructions = list(map(int, read_raw_entries("input25.txt")[0].split(',')))
    part1(_instructions)
    pass
