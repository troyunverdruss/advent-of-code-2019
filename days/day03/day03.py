from collections import defaultdict

from helpers import Point, manhattan_distance, read_raw_entries

# For each key, what does it mean in coordinate space
dirs = {
    "U": Point(0, 1),
    "L": Point(-1, 0),
    "R": Point(1, 0),
    "D": Point(0, -1)
}


# Since both solutions require laying out the entire path for line A and
# then laying out path B on top of it, solve for both at once.
# Returns a tuple:
# [distance to closest to origin, sum of distances of wire to first collision]
def solve(_line_a, _line_b):
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
                    (Point(position.x, position.y), step_count_b + int(grid[position][1:]))
                )
                grid[position] = "X"
            elif grid[position].startswith("B"):
                pass
            else:
                grid[position] = f"B{step_count_b}"

    # map over the collisions and get the distances to each point tuple index 0, the find the min
    closest_to_origin = min(map(lambda _tuple: manhattan_distance(origin, _tuple[0]), collisions))

    # map over the answers collisions and get the lowest sum from the tuple's index 1 position
    shortest_distance_by_wire = min(map(lambda _tuple: _tuple[1], collisions))

    # Return the answers!
    return closest_to_origin, shortest_distance_by_wire


def parse_input(line):
    return line.split(",")


if __name__ == "__main__":
    lines = read_raw_entries("input03.txt")
    line_a = parse_input(lines[0])
    line_b = parse_input(lines[1])

    part1, part2 = solve(line_a, line_b)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
