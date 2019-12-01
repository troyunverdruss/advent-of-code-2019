from typing import List

from helpers import read_numeric_entries


# This is the formula for computing fuel requirements based on mass
def compute_fuel(m: int) -> int:
    req = m // 3 - 2
    if req < 0:
        return 0
    else:
        return req


# Iterate over all the entries to compute a sum
def part1(lines: List[int]) -> int:
    return sum(map(lambda m: compute_fuel(m), lines))


# Slightly more complicated since we have to account for fuel's mass
# Keep going until it results in 0 fuel required, then sum it all up
def part2(lines: List[int]) -> int:
    total = 0

    for m in lines:
        _sum = 0
        _remaining = m
        while _remaining > 0:
            _remaining = compute_fuel(_remaining)
            _sum += _remaining
        total += _sum

    return total


if __name__ == "__main__":
    input_numbers = read_numeric_entries("input01.txt")
    print(f"Part 1, Fuel required: {part1(input_numbers)}")
    print(f"Part 2, Fuel required: {part2(input_numbers)}")
