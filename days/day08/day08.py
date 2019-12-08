from collections import Counter, defaultdict
from typing import List
from helpers import read_raw_entries


def part1(wide, tall, input_bits):
    layers = []
    for offset in range(0, len(input_bits), wide * tall):
        layer = input_bits[offset:wide * tall + offset]
        counts = Counter(layer)
        layers.append((counts[0], counts[1] * counts[2]))

    min_entry = min(layers, key=lambda v: v[0])
    return min_entry[1]


def part2_read_into_buffer(wide, tall, input_bits):
    buffer = defaultdict(lambda: 2)
    for offset in range(0, len(input_bits), wide * tall):
        layer = input_bits[offset:wide * tall + offset]
        for y in range(tall):
            for x in range(wide):
                if buffer[(x, y)] == 2:
                    buffer[(x, y)] = layer[y * wide + x]
    return buffer


def print_buffer(wide, tall, buffer):
    # 0: Black, 1: White
    color_lookup = {0: " ", 1: "#"}

    for y in range(tall):
        for x in range(wide):
            print(color_lookup[buffer[(x, y)]], end="")
            print(" ", end="")
        print("")


if __name__ == "__main__":
    line = read_raw_entries("input08.txt")[0]
    bits = list(map(int, line))
    part1 = part1(25, 6, bits)
    print(f"Part 1: {part1}")

    part2_buffer = part2_read_into_buffer(25, 6, bits)
    print("Part 2:")
    print_buffer(25, 6, part2_buffer)
