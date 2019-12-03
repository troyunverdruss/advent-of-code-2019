from typing import List


# This computer takes a sequence of integers as initial instructions
# and then starting at index 0, reads the values for 0, 1, 2, 3.
# 0 is the opcode, 1 and 2 are the parameters, and 3 is the destination place in memory
# for the result
#
# For different opcodes, it does different things:
# 1 = add
# 2 = multiply
# 99 = exit
#
# Use it like so:
# ic = IntcodeComputer([your instructions as ints])
# ic.run()
# ic.get_zero()
# ic.reset()
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

    def set_noun(self, noun):
        self.memory[1] = noun

    def set_verb(self, verb):
        self.memory[2] = verb

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
