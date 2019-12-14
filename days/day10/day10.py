from collections import deque
from typing import List, Tuple, Dict
from helpers import read_raw_entries
import math


# We need the asteroid with the most asteroids visible from it
def part1(starmap: Dict[Tuple[float, float], bool]):
    # Filter the grid for True so we have only asteroid locations
    asteroids = list(map(lambda e: e[0], filter(lambda e: e[1], starmap.items())))

    # This hash will be where we store the results as we go
    visible_from_asteroid = {}

    # Now let's just do a nested loop and try it all ...
    for start in asteroids:
        # Track angles we've seen
        seen = set()

        # For every possible destination, going in sorted order for kinda no reason
        for end in sorted(asteroids, key=lambda e: distance(start, e)):
            # Don't count the start by accident
            if start == end:
                continue

            # Get the rounded radians value and store it
            rounded_rad = get_rounded_radians(start, end)
            seen.add(rounded_rad)

        # Since seen is a set, it will automatically filter out dupes. Save the count here
        visible_from_asteroid[start] = len(seen)

    # Sort the list by number seen and get the first item, which should be the best
    best_data = sorted(visible_from_asteroid.items(), key=lambda p: p[1], reverse=True)[0]

    return best_data[0], best_data[1]


def get_rounded_radians(start, end, offset=0.0):
    # Multiple by 1000 and cast to int, so we return an int "rounded" to 4 decimal places
    # Just in case floating point math were to round weirdly or screw us.
    return int((math.atan2(end[1] - start[1], end[0] - start[0]) + offset) * 1000)


# In this one, we need to find all the asteroids in order of destruction and
# return the info about the requested target index
def part2(starmap: Dict[Tuple[float, float], bool], best: Tuple[float, float], destroyed_asteroid_target_index):
    # Find all the asteroids
    asteroids = list(map(lambda e: e[0], filter(lambda e: e[1], starmap.items())))

    # This list of destroyed asteroids will be in order of destruction
    destroyed = []

    # This outer loop is because each time through the inner loop, we probably won't
    # nuke everything, so
    while len(destroyed) < len(asteroids):
        # We don't want to repeat any angles because we only want to destroy the closest ones in the first wave
        # IOW nothing that is blocked should be destroyed in each wave
        seen = {}

        # Now every possible end is a valid target. Sorting here really matters because
        # blocked asteroids will be destroyed in a later wave and 200th is very specific
        for end in sorted(asteroids, key=lambda e: distance(best, e)):
            # Always skip ourselves
            if best == end:
                continue

            # Get the angle to the potential destination
            rounded_rad = get_rounded_radians(best, end, math.pi/2)

            # If we've seen this angle on this iteration, then that means it was
            # blocked from destruction. Keep going. We'll get it in another wave.
            if rounded_rad in seen.values():
                continue

            # Update the sets to track angles we've seen and points we've seen
            seen[end] = rounded_rad

        recently_destroyed = recently_destroyed()
        recently_destroyed.extend(sorted(seen.items(), key=lambda e: e[1]))

        while recently_destroyed[0][1] < 0:
            recently_destroyed.rotate(-1)

        destroyed.extend(recently_destroyed)

    point, _ = destroyed[destroyed_asteroid_target_index]
    return int(point[0] * 100 + point[1])


def distance(a: Tuple[float, float], b: Tuple[float, float]):
    return math.sqrt(abs(a[0] - b[0]) + abs(a[1] - b[1]))


# This might be overkill, but I didn't quite think about it, so I just mapped
# it all to a grid right away
def build_grid(lines: List[str]) -> Dict[Tuple[float, float], bool]:
    starmap = {}
    lookup = {"#": True, ".": False}
    for y, line in enumerate(lines):
        for x, char in enumerate(list(line)):
            # Be sure to use floats, because everything is gonna be fractions of angles
            starmap[(float(x), float(y))] = lookup[char]

    return starmap


if __name__ == "__main__":
    raw_lines = list(filter(lambda l: l != "", read_raw_entries("input10.txt")))

    _map = build_grid(raw_lines)

    _best, _max = part1(_map)
    print(f"Part 1: {_best} can see {_max}")

    part2 = part2(_map, _best, 199)
    print(f"Part 2: {part2}")
