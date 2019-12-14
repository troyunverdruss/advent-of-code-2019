import sys
from dataclasses import dataclass
from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


class Arcade:
    def __init__(self, inst):
        self.ic = IntcodeComputer(inst)

    def run(self):
        self.ic.run()
        return self.ic.waiting


def part1(instructions):
    arcade = Arcade(instructions)
    arcade.run()

    blocks = set()

    while len(arcade.ic.outputs) > 0:
        x = arcade.ic.outputs.popleft()
        y = arcade.ic.outputs.popleft()
        t = arcade.ic.outputs.popleft()

        if t == 2:
            blocks.add((x, y))

    return len(blocks)


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash(str(self))


def part2(instructions):
    arcade = Arcade(instructions)
    arcade.ic.memory[0] = 2
    # arcade.ic.inputs.append(1)
    # arcade.ic.enable_stdout = True

    buffer = {}
    item_lookup = {0: ' ', 1: '|', 2: '#', 3: '_', 4: 'o'}
    score = 0
    paddle = Point(0, 0)
    ball = Point(0, 0)

    while arcade.run():

        score = read_output_to_buffer(arcade, buffer, item_lookup, paddle, score)

        draw_buffer(buffer)
        # print(f"Score: {score}")
        # print("")

        arcade.ic.waiting = False
    score = read_output_to_buffer(arcade, buffer, item_lookup, paddle, score)
    print(f"Score: {score}")
    return score

def draw_buffer(buffer):
    _max_x = _max_y = -sys.maxsize
    _min_x = _min_y = sys.maxsize
    for key in buffer.keys():
        _max_x = max(_max_x, key.x)
        _min_x = min(_min_x, key.x)
        _max_y = max(_max_y, key.y)
        _min_y = min(_min_y, key.y)
    # print_buffer_to_console(Point(0,0), _max_x - _min_x, _max_y - _min_y, buffer)


def read_output_to_buffer(arcade, buffer, item_lookup, paddle, score):
    while len(arcade.ic.outputs) > 0:
        x = arcade.ic.outputs.popleft()
        y = arcade.ic.outputs.popleft()
        t = arcade.ic.outputs.popleft()

        if x == -1 and y == 0:
            score = t
        # else:
        #     buffer[Point(x, y)] = item_lookup[t]

        if t == 3:
            paddle = Point(x, y)
            # print(f"Paddle: {paddle}")
        if t == 4:
            ball = Point(x, y)
            # print(f"Ball: {ball}")
            if ball.x > paddle.x:
                arcade.ic.inputs.append(1)
            elif ball.x < paddle.x:
                arcade.ic.inputs.append(-1)
            else:
                arcade.ic.inputs.append(0)
    return score


def print_buffer_to_console(origin, wide, tall, buffer):
    for y in range(tall + 1):
        # print(f"{y}", end="")
        for x in range(wide + 1):
            print(buffer[Point(origin.x + x, origin.y + y)], end="")
            print(" ", end="")
        print("")


if __name__ == "__main__":
    raw_instructions = list(map(int, read_raw_entries("input13.txt")[0].split(",")))
    part1 = part1(raw_instructions[:])
    print(f"Part 1: {part1}")

    part2 = part2(raw_instructions[:])
    print(f"Part 2: {part2}")
