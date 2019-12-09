import enum
from collections import deque
from typing import List


class Modes(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1


class InstructionData:
    def __init__(self):
        # This will be numeric
        self.instruction = None

        # This will be a list of modes, indexed for each parameter
        self.parameter_modes = []

    def get_parameter_mode(self, param_index):
        if len(self.parameter_modes) > param_index:
            return self.parameter_modes[param_index]
        else:
            return Modes.POSITION

    def __str__(self):
        return f"{self.instruction}, {self.parameter_modes}"


# This computer takes a sequence of integers as initial instructions
# and then starting at index 0, reads the values for 0, 1, 2, 3.
# 0 is the opcode, 1 and 2 are the parameters, and 3 is the destination place in memory
# for the result
#
# For different opcodes, it does different things:
# 1 = add
# 2 = multiply
# 3 = input
# 4 = output
# 5 =
# 99 = exit
#
# Use it like so:
# ic = IntcodeComputer([your instructions as ints])
# ic.run()
# ic.get_zero()
# ic.reset()
class IntcodeComputer:
    def __init__(self, instructions: List[int], _id=""):
        self.id = _id
        self.initial_memory = instructions[:]
        self.memory = instructions[:]  # memory
        self.instruction_pointer = 0
        self.inputs = deque()
        self.outputs = deque()
        self.enable_stdout = False
        self.running = False
        self.waiting = False

    def __str__(self):
        return f"ID: {self.id} Running: {self.running} Waiting: {self.waiting} " \
               f"Inputs: {self.inputs} Outputs: {self.outputs}"

    def run(self):
        self.running = True
        while self.step() and not self.waiting:
            pass

    def is_running(self):
        return self.running

    def is_waiting(self):
        return self.waiting

    def reset(self):
        self.instruction_pointer = 0
        self.memory = self.initial_memory[:]

    def set_noun(self, noun):
        self.memory[1] = noun

    def set_verb(self, verb):
        self.memory[2] = verb

    def set_inputs(self, _inputs):
        self.inputs.extend(_inputs)

    def get_zero(self) -> int:
        return self.memory[0]

    def get_outputs(self):
        return self.outputs

    def step(self) -> bool:
        raw_instruction_value = self.memory[self.instruction_pointer]
        instruction = self.parse_instruction(raw_instruction_value)

        if instruction.instruction == 1:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.memory[self.instruction_pointer + 3]
            self.memory[target] = param_1 + param_2
            self.instruction_pointer += 4
            return True
        elif instruction.instruction == 2:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.memory[self.instruction_pointer + 3]
            self.memory[target] = param_1 * param_2
            self.instruction_pointer += 4
            return True
        elif instruction.instruction == 3:
            if len(self.inputs) == 0:
                self.waiting = True
                if self.enable_stdout:
                    print(f"{self.id} Started waiting")
            else:
                _input = self.inputs.popleft()
                param_1 = self.memory[self.instruction_pointer + 1]
                self.memory[param_1] = _input
                self.instruction_pointer += 2
            return True
        elif instruction.instruction == 4:
            param_1 = self.memory[self.instruction_pointer + 1]
            value_at_param_1 = self.memory[param_1]
            self.outputs.append(value_at_param_1)
            if self.enable_stdout:
                print(f"{self.id} Output: {value_at_param_1}")
            self.instruction_pointer += 2
            return True
        elif instruction.instruction == 5:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)

            if param_1 != 0:
                self.instruction_pointer = param_2
            else:
                self.instruction_pointer += 3
            return True
        elif instruction.instruction == 6:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)

            if param_1 == 0:
                self.instruction_pointer = param_2
            else:
                self.instruction_pointer += 3
            return True
        elif instruction.instruction == 7:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.memory[self.instruction_pointer + 3]

            if param_1 < param_2:
                self.memory[target] = 1
            else:
                self.memory[target] = 0

            self.instruction_pointer += 4
            return True
        elif instruction.instruction == 8:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.memory[self.instruction_pointer + 3]

            if param_1 == param_2:
                self.memory[target] = 1
            else:
                self.memory[target] = 0

            self.instruction_pointer += 4
            return True

        elif instruction.instruction == 99:
            self.running = False
            return False
        else:
            raise Exception(
                f"Oops, bad instruction {raw_instruction_value} at index {self.instruction_pointer}"
            )

    def parse_instruction(self, raw_value) -> InstructionData:
        chars = list(str(raw_value))
        data = InstructionData()

        if len(chars) == 1:
            data.instruction = int(chars[0])
            return data

        data.instruction = int("".join(chars[-2:]))
        # Remove the chars for the instruction
        chars.pop()
        chars.pop()

        # Now lets find the parameter modes
        while len(chars) > 0:
            c = int(chars.pop())
            if c == 0:
                data.parameter_modes.append(Modes.POSITION)
            elif c == 1:
                data.parameter_modes.append(Modes.IMMEDIATE)

        return data

    def get_parameter_value(self, param_id, instruction):
        mode = instruction.get_parameter_mode(param_id)
        v = self.memory[self.instruction_pointer + 1 + param_id]

        if mode == Modes.POSITION:
            return self.memory[v]
        elif mode == Modes.IMMEDIATE:
            return v
