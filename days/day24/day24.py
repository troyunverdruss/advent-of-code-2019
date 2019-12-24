import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import List

from days.day20.day20 import dirs
from helpers import read_raw_entries


@dataclass
class Point3d:
    x: int
    y: int
    z: int

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        return Point3d(self.x + other.x, self.y + other.y, self.z + other.y)


def part1(lines):
    total_x = 0
    total_y = 0

    grid = defaultdict(lambda: '_')
    for y, line in enumerate(lines):
        for x, val in enumerate(list(line)):
            grid[Point(x, y)] = val
            total_x = max(x, total_x)
            total_y = max(y, total_y)

    seen = set()

    next = {}
    for k, v in grid.items():
        next[k] = v

    first_repeat = False
    while not first_repeat:
        print_buffer_to_console(next)

        str_rep = ""

        for y in range(total_y + 1):
            for x in range(total_x + 1):
                bug_count = 0
                for d in dirs.values():
                    if grid[Point(x, y) + d] == '#':
                        bug_count += 1
                if grid[Point(x, y)] == '#' and not bug_count == 1:
                    next[Point(x, y)] = '.'
                    str_rep += '.'
                elif grid[Point(x, y)] == '.' and (bug_count == 1 or bug_count == 2):
                    next[Point(x, y)] = '#'
                    str_rep += '#'
                else:
                    next[Point(x, y)] = grid[Point(x, y)]
                    str_rep += grid[Point(x, y)]

        for k, v in next.items():
            grid[k] = v

        if str_rep in seen:
            first_repeat = True
        else:
            seen.add(str_rep)

    # Total up the score
    current_point_score = 1
    total_score = 0
    for y in range(total_y + 1):
        for x in range(total_x + 1):
            if grid[Point(x, y)] == '#':
                total_score += current_point_score
            current_point_score *= 2

    return total_score


def part2(lines, mins):
    total_x = 5
    total_y = 5
    z_min = -1
    z_max = 1

    grid = defaultdict(lambda: '.')
    for y, line in enumerate(lines):
        for x, val in enumerate(list(line)):
            grid[Point3d(x, y, 0)] = val
            total_x = max(x, total_x)
            total_y = max(y, total_y)
    setup_layer(grid, total_x, total_y, z_min)
    setup_layer(grid, total_x, total_y, z_max)

    next = {}
    for k, v in grid.items():
        next[k] = v

    for min in range(mins):
        print(f"After {min} mins")
        print_buffer_to_console_3d(grid, total_x, total_y, z_max - z_min)

        iter_values = list(filter(lambda kk: z_min <= kk[0].z <= z_max, grid.items()))
        # Need to filter only on z values that i care about?
        for point, value in iter_values:
            # The middle is never a simple square
            if point.x == 2 and point.y == 2:
                continue

            bug_count = 0
            neighbors = get_neighbors(point, total_x, total_y)
            for n in neighbors:
                if n.z < z_min:
                    z_min -= 1
                    setup_layer(grid, total_x, total_y, z_min)
                elif n.z > z_max:
                    z_max += 1
                    setup_layer(grid, total_x, total_y, z_max)

                if grid[n] == '#':
                    bug_count += 1

            if grid[point] == '#' and not bug_count == 1:
                next[point] = '.'
            elif grid[point] == '.' and (bug_count == 1 or bug_count == 2):
                next[point] = '#'
            else:
                next[point] = grid[point]

        for k, v in next.items():
            grid[k] = v

    print_buffer_to_console_3d(grid, total_x, total_y, z_max - z_min)
    return len(list(filter(lambda p: p == '#', list(grid.values()))))
    #
    # for z in range(0 - (total_z // 2), total_z - (total_z // 2)):
    #     # print(f"Level {z}")
    #     pass
    #
    #
    # for y in range(total_y):
    #     for x in range(total_x):
    #         total_z += 2
    #         for z in range(0 - (total_z // 2)-1, total_z - (total_z // 2)+1):
    #             pass # print(x,y,z)
    # return

    #             bug_count = 0
    #             for d in dirs.values():
    #                 if grid[Point(x, y) + d] == '#':
    #                     bug_count += 1
    #             if grid[Point(x, y)] == '#' and not bug_count == 1:
    #                 next[Point(x, y)] = '.'
    #                 str_rep += '.'
    #             elif grid[Point(x, y)] == '.' and (bug_count == 1 or bug_count == 2):
    #                 next[Point(x, y)] = '#'
    #                 str_rep += '#'
    #             else:
    #                 next[Point(x, y)] = grid[Point(x, y)]
    #                 str_rep += grid[Point(x, y)]
    #
    #     for k, v in next.items():
    #         grid[k] = v
    #
    #     if str_rep in seen:
    #         first_repeat = True
    #     else:
    #         seen.add(str_rep)
    #
    # # Total up the score
    # current_point_score = 1
    # total_score = 0
    # for y in range(total_y + 1):
    #     for x in range(total_x + 1):
    #         if grid[Point(x, y)] == '#':
    #             total_score += current_point_score
    #         current_point_score *= 2
    #
    # return total_score


def setup_layer(grid, total_x, total_y, z):
    for y in range(total_y):
        for x in range(total_x):
            grid[Point3d(x, y, z)] = '.'


def get_neighbors(point: Point3d, total_x, total_y):
    # lookup = {
    #     # starting point => (absolute x, absolute y, delta z)
    #     (0, 0): [(2, 1, -1), (1, 2, -1), (1, 0, 0), (0, 1, 0)],
    #     (1, 0): [(2, 1, -1), (0, 0, 0), (2, 0, 0), (1, 1, 0)],
    #     (2, 0): [(2, 1, -1), (1, 0, 0), (3, 0, 0), (2, 1, 0)],
    #     (3, 0): [(2, 1, -1), ],
    #     (4, 0): [(2, 1, -1)],
    # }

    neighbors = []
    # Go upwards
    if point.y == 0:
        neighbors.append(Point3d(2, 1, point.z - 1))
    elif point.y == 3 and point.x == 2:
        for x in range(total_x):
            neighbors.append(Point3d(x, 4, point.z + 1))
    else:
        neighbors.append(Point3d(point.x, point.y - 1, point.z))

    # Go leftwards
    if point.x == 0:
        neighbors.append(Point3d(1, 2, point.z - 1))
    elif point.x == 3 and point.y == 2:
        for y in range(total_y):
            neighbors.append(Point3d(4, y, point.z + 1))
    else:
        neighbors.append(Point3d(point.x - 1, point.y, point.z))

    # Go rightwards
    if point.x == 4:
        neighbors.append(Point3d(3, 2, point.z - 1))
    elif point.x == 1 and point.y == 2:
        for y in range(total_y):
            neighbors.append(Point3d(0, y, point.z + 1))
    else:
        neighbors.append(Point3d(point.x + 1, point.y, point.z))

    # Go downwards
    if point.y == 4:
        neighbors.append(Point3d(2, 3, point.z - 1))
    elif point.y == 1 and point.x == 2:
        for x in range(total_x):
            neighbors.append(Point3d(x, 0, point.z + 1))
    else:
        neighbors.append(Point3d(point.x, point.y + 1, point.z))

    return neighbors
    # # Going outwards
    # if point.y == 0:
    #     neighbors.append(Point3d(2, 1, point.z - 1))
    # else:
    #     neighbors.append(Point3d(point.x, point.y - 1, point.z))
    #
    # if point.x == 0:
    #     neighbors.append(Point3d(1, 2, point.z - 1))
    # else:
    #     neighbors.append(Point3d(point.x - 1, point.y, point.z))
    #
    # if point.y == 4:
    #     neighbors.append(Point3d(2, 3, point.z - 1))
    # else:
    #     neighbors.append(Point3d(point.x, point.y - 1, point.z))
    #
    # if point.x == 4:
    #     neighbors.append(Point3d(3, 2, point.z - 1))
    # else:
    #     neighbors.append(Point3d(point.x - 1, point.y, point.z))
    #
    # # Going inwards
    # if point.y == 1 and point.x == 2:
    #     for x in range(total_x):
    #         neighbors.append(Point3d(x, 0, point.z + 1))
    # if point.y == 3 and point.x == 2:
    #     for x in range(total_x):
    #         neighbors.append(Point3d(x, 4, point.z + 1))
    # if point.y == 2 and point.x == 1:
    #     for y in range(total_y):
    #         neighbors.append(Point3d(0, y, point.z + 1))
    # if point.y == 2 and point.x == 3:
    #     for y in range(total_y):
    #         neighbors.append(Point3d(4, y, point.z + 1))


def print_buffer_to_console(buffer):
    _max_x = _max_y = -sys.maxsize
    _min_x = _min_y = sys.maxsize

    for key in buffer.keys():
        _max_x = max(_max_x, key.x)
        _min_x = min(_min_x, key.x)
        _max_y = max(_max_y, key.y)
        _min_y = min(_min_y, key.y)

    for y in range(_min_y, _max_y + 1):
        print(f"{str(y).zfill(3)} ", end="")
        for x in range(_min_x, _max_x + 1):
            print(buffer[Point(x, y)], end="")
        print("")


def print_buffer_to_console_3d(buffer, total_x, total_y, total_z):
    if total_z == 0:
        total_z = 1

    for z in range(0 - (total_z // 2), total_z - (total_z // 2)):
        print(f"Layer {z}")
        for y in range(total_y):
            for x in range(total_x):
                if x == 2 and y == 2:
                    print("?", end="")
                else:
                    print(buffer[Point3d(x, y, z)], end="")
            print("")
    print("")


if __name__ == "__main__":
    _lines = read_raw_entries("input24.txt")
    # r1 = part1(_lines)
    # print(r1)
    # not right 16383, 49151, 33423359
    r2 = part2(_lines, 200)
    print(r2)
    pass
