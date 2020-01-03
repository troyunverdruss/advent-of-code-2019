import enum
from collections import deque, defaultdict
from typing import List, Dict


class Modes(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


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
# 5 = jump-if-true
# 6 = jump-if-false
# 7 = less than
# 8 = equals
# 99 = exit
#
# Use it like so:
# ic = IntcodeComputer([your instructions as ints])
# ic.run()
class IntcodeComputer:
    def __init__(self, instructions: List[int], _id: str = ""):
        self.id = _id
        self.memory = defaultdict(lambda: 0)
        for index, v in enumerate(instructions):
            self.memory[index] = v

        self.instruction_pointer = 0
        self.relative_base = 0

        self.inputs = deque()
        self.outputs = deque()

        self.running = False
        self.waiting = False
        self.enable_stdout = False

    def __str__(self):
        return f"ID: {self.id} Running: {self.running} Waiting: {self.waiting} " \
               f"Inputs: {self.inputs} Outputs: {self.outputs}"

    def clone(self):
        new_ic = IntcodeComputer([])
        new_ic.memory = self.memory.copy()
        new_ic.instruction_pointer = self.instruction_pointer
        new_ic.relative_base = self.relative_base
        new_ic.inputs.extend(self.inputs)
        new_ic.outputs.extend(self.outputs)
        new_ic.running = self.running
        new_ic.waiting = self.waiting
        new_ic.enable_stdout = self.enable_stdout
        return new_ic

    def run(self):
        self.running = True
        while self.step() and not self.waiting:
            pass

    def set_noun(self, noun: int):
        self.memory[1] = noun

    def set_verb(self, verb: int):
        self.memory[2] = verb

    def set_inputs(self, _inputs: List[int]):
        self.inputs.extend(_inputs)

    def set_ascii_cmd(self, command_string):
        self.inputs.extend(map(ord, list(command_string) + ['\n']))

    def get_outputs(self):
        return self.outputs

    def get_all_non_zero_memory(self) -> Dict[int, int]:
        return {k: v for k, v in filter(lambda e: e[1] != 0, self.memory.items())}

    def step(self) -> bool:
        raw_instruction_value = self.memory[self.instruction_pointer]
        instruction = self.parse_instruction(raw_instruction_value)
        if self.enable_stdout:
            print(f"{instruction}")

        # add
        if instruction.instruction == 1:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.get_target_value(2, instruction)

            self.memory[target] = param_1 + param_2

            self.instruction_pointer += 4
            return True

        # multiply
        elif instruction.instruction == 2:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.get_target_value(2, instruction)

            self.memory[target] = param_1 * param_2

            self.instruction_pointer += 4
            return True

        # input
        elif instruction.instruction == 3:
            if len(self.inputs) == 0:
                self.waiting = True

                if self.enable_stdout:
                    print(f"{self.id} Started waiting")
            else:
                target = self.get_target_value(0, instruction)

                self.memory[target] = self.inputs.popleft()

                self.instruction_pointer += 2
            return True

        # output
        elif instruction.instruction == 4:
            param_1 = self.get_parameter_value(0, instruction)

            self.outputs.append(param_1)

            self.instruction_pointer += 2
            return True

        # jump-if-true
        elif instruction.instruction == 5:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)

            if param_1 != 0:
                self.instruction_pointer = param_2
            else:
                self.instruction_pointer += 3
            return True

        # jump-if-false
        elif instruction.instruction == 6:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)

            if param_1 == 0:
                self.instruction_pointer = param_2
            else:
                self.instruction_pointer += 3
            return True

        # less than
        elif instruction.instruction == 7:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.get_target_value(2, instruction)

            if param_1 < param_2:
                self.memory[target] = 1
            else:
                self.memory[target] = 0

            self.instruction_pointer += 4
            return True

        # equals
        elif instruction.instruction == 8:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.get_target_value(2, instruction)

            if param_1 == param_2:
                self.memory[target] = 1
            else:
                self.memory[target] = 0

            self.instruction_pointer += 4
            return True

        # modify relative base
        elif instruction.instruction == 9:
            param_1 = self.get_parameter_value(0, instruction)

            self.relative_base += param_1

            self.instruction_pointer += 2
            return True

        # exit / halt
        elif instruction.instruction == 99:
            self.running = False
            return False

        # uh oh
        else:
            raise Exception(
                f"Oops, bad instruction {raw_instruction_value} at index {self.instruction_pointer}"
            )

    @staticmethod
    def parse_instruction(raw_value) -> InstructionData:
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
            elif c == 2:
                data.parameter_modes.append(Modes.RELATIVE)

        return data

    def get_parameter_value(self, param_id, instruction):
        mode = instruction.get_parameter_mode(param_id)
        v = self.memory[self.instruction_pointer + 1 + param_id]

        if mode == Modes.POSITION:
            return self.memory[v]
        elif mode == Modes.IMMEDIATE:
            return v
        elif mode == Modes.RELATIVE:
            return self.memory[self.relative_base + v]

    def get_target_value(self, param_id, instruction):
        mode = instruction.get_parameter_mode(param_id)
        v = self.memory[self.instruction_pointer + 1 + param_id]

        if mode == Modes.POSITION:
            return v
        elif mode == Modes.IMMEDIATE:
            raise Exception("IMMEDIATE mode is unsupported for getting target values")
        elif mode == Modes.RELATIVE:
            return v + self.relative_base
