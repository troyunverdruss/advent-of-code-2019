from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries

class Arcade:
    def __init__(self, inst):
        self.ic = IntcodeComputer(inst)

    def run(self):
        self.ic.run()


if __name__ == "__main__":
    raw_instructions = map(int, read_raw_entries("input13.txt")[0].split(","))
    arcade = Arcade(raw_instructions)
    arcade.run()

    blocks = set()

    while len(arcade.ic.outputs) > 0:
        x = arcade.ic.outputs.popleft()
        y = arcade.ic.outputs.popleft()
        t = arcade.ic.outputs.popleft()

        if t == 2:
            blocks.add((x,y))

    print(f"Part 1: {len(blocks)}")

    # for index in range(0, arcade.ic.outputs, 3):
    #     if arcade.ic.outputs[index] ==
    # pass
