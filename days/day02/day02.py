from typing import List

from helpers import read_raw_entries


class IntcodeComputer:
    def __init__(self, instructions: List[int]):
        self.initial_memory = instructions[:]
        self.memory = instructions[:]  # memory
        self.instruction_pointer = 0

    def run(self):
        while self.step():
            pass

    def reset(self):
        self.instruction_pointer = 0
        self.memory = self.initial_memory[:]

    def get_zero(self) -> int:
        return self.memory[0]

    def step(self) -> bool:
        cur = self.memory[self.instruction_pointer]
        if cur == 1:
            a = self.memory[self.instruction_pointer + 1]
            b = self.memory[self.instruction_pointer + 2]
            target = self.memory[self.instruction_pointer + 3]
            self.memory[target] = self.memory[a] + self.memory[b]
            self.instruction_pointer += 4
            return True
        elif cur == 2:
            a = self.memory[self.instruction_pointer + 1]
            b = self.memory[self.instruction_pointer + 2]
            target = self.memory[self.instruction_pointer + 3]
            self.memory[target] = self.memory[a] * self.memory[b]
            self.instruction_pointer += 4
            return True
        elif cur == 99:
            return False
        else:
            raise Exception(f"Oops, bad instruction {cur} at index {self.instruction_pointer}")


def part1(instructions):
    instructions[1] = 12
    instructions[2] = 2
    ic = IntcodeComputer(instructions)
    ic.run()
    print(f"Part 1: 1202 => {ic.get_zero()}")


def part2(instructions):
    ic = IntcodeComputer(instructions)

    for one in range(0, 100):
        for two in range(0, 100):
            ic.reset()
            ic.memory[1] = one
            ic.memory[2] = two
            ic.run()
            if ic.get_zero() == 19690720:
                print(f"Part 2: {one}{two} => 19690720")
                return


if __name__ == "__main__":
    lines = read_raw_entries("input02.txt")
    raw_instructions = list(map(lambda x: int(x), lines[0].split(",")))
    part1(raw_instructions[:])
    part2(raw_instructions[:])
