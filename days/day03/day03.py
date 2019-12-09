from collections import defaultdict
from typing import Dict, List

from PIL import Image, ImageDraw

from helpers import Point, manhattan_distance, read_raw_entries

# For each key, what does it mean in coordinate space
dirs = {"U": Point(0, 1), "L": Point(-1, 0), "R": Point(1, 0), "D": Point(0, -1)}


# Since both solutions require laying out the entire path for line A and
# then laying out path B on top of it, solve for both at once.
# Returns a tuple:
# [distance to closest to origin, sum of distances of wire to first collision]
def solve_by_gridding(_line_a, _line_b):
    # Set up some defaults, use a defaultdict so we always have a value if we reference it
    grid = defaultdict(lambda: "_")
    origin = Point(0, 0)
    position = Point(0, 0)
    grid[origin] = "o"

    # Lay out all of line A, marking each coordinate with "A###" in order
    # ie: A1, A2, A3, etc. If line A collides with itself, keep the previous entry
    step_count_a = 0
    for direction in _line_a:
        _dir = direction[:1]
        num = int(direction[1:])

        for _ in range(num):
            step_count_a += 1
            position = position + dirs[_dir]

            if grid[position].startswith("A"):
                pass
            else:
                grid[position] = f"A{step_count_a}"

    # tuple: point, sum of points intersection
    collisions = []
    # Reset out srarting position
    position = Point(0, 0)

    # Here we'll lay out line B just like line A, however, in addition
    # to the above rules, if we run into a collision with line A, we'll
    # record the position of it as well as the sum of the distances so
    # that we can find the solutions afterwards
    step_count_b = 0
    for direction in _line_b:
        _dir = direction[:1]
        num = int(direction[1:])

        for _ in range(num):
            step_count_b += 1
            position = position + dirs[_dir]

            if grid[position].startswith("A"):
                collisions.append(
                    # tuple: point, sum of points intersection
                    (
                        Point(position.x, position.y),
                        step_count_b + int(grid[position][1:]),
                    )
                )
                grid[position] = "X"
            elif grid[position].startswith("B"):
                pass
            else:
                grid[position] = f"B{step_count_b}"

    # map over the collisions and get the distances to each point tuple index 0, the find the min
    closest_to_origin = min(
        map(lambda _tuple: manhattan_distance(origin, _tuple[0]), collisions)
    )

    # map over the answers collisions and get the lowest sum from the tuple's index 1 position
    shortest_distance_by_wire = min(map(lambda _tuple: _tuple[1], collisions))

    # Return the answers!
    return closest_to_origin, shortest_distance_by_wire


# This is a helper method to take a list of the inputs and place them
# into a dict with points as keys, and distance from origin as values.
# Used elsewhere to simplify setup
def gen_path_map(_line: List[int]) -> Dict[Point, int]:
    position = Point(0, 0)
    path = {}

    step_count = 0
    for direction in _line:
        _dir = direction[:1]
        num = int(direction[1:])

        for _ in range(num):
            step_count += 1
            position = position + dirs[_dir]
            if position not in path:
                path[position] = step_count
    return path


# Woke up with this much simpler solution, so hacked it out. Instead
# of tracing the lines during mapping and recording the collisions,
# just get the entire paths and then get the set intersection. Those
# are all the possible collisions, then it's just a matter of finding
# the closest to origin and the shortest distance by wire
def solve_with_sets(_line_a, _line_b):
    a_map = gen_path_map(_line_a)
    b_map = gen_path_map(_line_b)

    intersection = set(a_map.keys()).intersection(set(b_map.keys()))
    closest_to_origin = min(
        map(lambda x: manhattan_distance(Point(0, 0), x), (p for p in intersection))
    )

    shortest_distance_by_wire = min((a_map[p] + b_map[p] for p in intersection))

    return closest_to_origin, shortest_distance_by_wire


# Playing around with some visualization here, basically just taking
# the paths and writing them one-to-one into a giant image canvas. Not
# exactly efficient ... but easy! Then since the resulting file is gigantic,
# I scale it down by a factor of 4 before writing it out
def write_image_of_wires(_line_a: List[int], _line_b: List[int]):
    a_map = gen_path_map(_line_a)
    b_map = gen_path_map(_line_b)

    # Get the bounds of the wires
    min_x = min(a_map.keys() | b_map.keys(), key=lambda p: p.x).x
    max_x = max(a_map.keys() | b_map.keys(), key=lambda p: p.x).x
    min_y = min(a_map.keys() | b_map.keys(), key=lambda p: p.y).y
    max_y = max(a_map.keys() | b_map.keys(), key=lambda p: p.y).y

    # Figure out where the origin should be, this will be where we
    # reference all the other points. Doing it this way makes it so we
    # don't have the origin centered and with a heavily skewed drawing
    # to one quadrant of the axes
    image_origin = Point(50 + abs(min_x), 50 + abs(min_y))

    # Set up our image canvas
    image = Image.new("RGBA", (abs(min_x) + abs(max_x) + 100, abs(min_y) + abs(max_y) + 100), "black")
    image_draw = ImageDraw.Draw(image)

    # Configurable, needs to be multiple of 2
    line_width = 8

    # Draw line A points
    for p in a_map.keys():
        image_draw.rectangle((image_origin.x + p.x - line_width / 2, image_origin.y + p.y - line_width / 2,
                              image_origin.x + p.x + line_width / 2, image_origin.y + p.y + line_width / 2),
                             fill="blue")
    # Draw line B points
    for p in b_map.keys():
        image_draw.rectangle((image_origin.x + p.x - line_width / 2, image_origin.y + p.y - line_width / 2,
                              image_origin.x + p.x + line_width / 2, image_origin.y + p.y + line_width / 2),
                             fill="orange")
    # Draw collision points
    for p in a_map.keys() & b_map.keys():
        image_draw.rectangle((image_origin.x + p.x - line_width, image_origin.y + p.y - line_width,
                              image_origin.x + p.x + line_width, image_origin.y + p.y + line_width),
                             fill="purple")
    # Draw the origin
    image_draw.rectangle((image_origin.x - line_width * 2, image_origin.y - line_width * 2,
                          image_origin.x + line_width * 2, image_origin.y + line_width * 2), fill="white")

    # Resize + save
    small_image = image.resize((image.size[0] // 4, image.size[1] // 4))
    small_image.save("wire_map.png")


def parse_input(line):
    return line.split(",")


if __name__ == "__main__":
    lines = read_raw_entries("input03.txt")
    line_a = parse_input(lines[0])
    line_b = parse_input(lines[1])

    part1, part2 = solve_by_gridding(line_a, line_b)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    write_image_of_wires(line_a, line_b)
