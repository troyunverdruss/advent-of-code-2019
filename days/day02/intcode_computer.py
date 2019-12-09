import enum
from collections import deque, defaultdict
from typing import List


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
# ic.get_zero()
# ic.reset()
class IntcodeComputer:
    def __init__(self, instructions: List[int], _id=""):
        self.id = _id
        self.initial_memory = instructions[:]
        self.memory = defaultdict(lambda: 0)
        for index, v in enumerate(instructions):
            self.memory[index] = v

        # instructions[:]  # memory
        self.instruction_pointer = 0
        self.inputs = deque()
        self.outputs = deque()
        self.enable_stdout = False
        self.running = False
        self.waiting = False
        self.relative_base = 0

    def __str__(self):
        return f"ID: {self.id} Running: {self.running} Waiting: {self.waiting} " \
               f"Inputs: {self.inputs} Outputs: {self.outputs}"

    def run(self):
        self.running = True
        count = 0
        while self.step() and not self.waiting:
            count += 1
            if self.enable_stdout:
                print(f"iteration: {count}. {self.instruction_pointer}. {self.memory[self.instruction_pointer]} {self.memory[self.instruction_pointer+1]} {self.memory[self.instruction_pointer+2]} {self.memory[self.instruction_pointer+3]}")
                # print(f"mem: {map(lambda i: "{i[0]}: {i[1]}", sorted(self.memory.items(), key=lambda i: i[0])}")
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
        if self.enable_stdout:
            print(f"{instruction}")

        # add
        if instruction.instruction == 1:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)

            # if instruction.get_parameter_mode(2) == Modes.POSITION:
            target = self.get_parameter_value(2, instruction, True)# self.memory[self.instruction_pointer + 3]
            # else:
            #     target = self.memory[self.instruction_pointer + 3] + self.relative_base #self.memory[self.instruction_pointer + 3]

            self.memory[target] = param_1 + param_2
            if self.enable_stdout:
                print(f"{raw_instruction_value} {instruction}. add. mem[{target}] = {param_1} + {param_2}")
            self.instruction_pointer += 4
            return True

        # multiply
        elif instruction.instruction == 2:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.get_parameter_value(2, instruction, True)
            self.memory[target] = param_1 * param_2
            if self.enable_stdout:
                print(f"{raw_instruction_value} {instruction}. mul.  mem[{target}] = {param_1} * {param_2}")
            self.instruction_pointer += 4
            return True

        # input
        elif instruction.instruction == 3:
            if len(self.inputs) == 0:
                self.waiting = True
                if self.enable_stdout:
                    print(f"{self.id} Started waiting")
            else:
                _input = self.inputs.popleft()
                # param_1 = self.memory[self.instruction_pointer + 1]
                target = self.get_parameter_value(0, instruction, True)
                # param_1 = self.get_parameter_value(0, instruction) # self.memory[self.instruction_pointer + 1]
                self.memory[target] = _input
                # if instruction.get_parameter_mode(0) == Modes.POSITION:
                #     self.memory[param_1] = _input
                # elif instruction.get_parameter_mode(0) == Modes.RELATIVE:
                #     self.memory[param_1 + self.relative_base] = _input
                # else:
                #     raise Exception("Bad mode for input instruction")

                if self.enable_stdout:
                    print(f"{raw_instruction_value} {instruction}. in. mem[{target}] = from input: {_input}")
                self.instruction_pointer += 2
            return True

        # output
        elif instruction.instruction == 4:
            param_1 = self.get_parameter_value(0, instruction)
            # value_at_param_1 = self.memory[param_1]
            self.outputs.append(param_1)
            if self.enable_stdout:
                print(f"{raw_instruction_value} {self.id} Output: {param_1}")
            self.instruction_pointer += 2
            return True

        # jump-if-true
        elif instruction.instruction == 5:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)

            if param_1 != 0:
                self.instruction_pointer = param_2
                if self.enable_stdout:
                    print(f"{raw_instruction_value} {instruction}. jit. inst_pointer = {param_1}!=0 => {param_2}")
            else:
                if self.enable_stdout:
                    print(f"{raw_instruction_value} {instruction}. jit. not jumping = {param_1}==0 => {param_2}")
                self.instruction_pointer += 3
            return True

        # jump-if-false
        elif instruction.instruction == 6:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)

            if param_1 == 0:
                self.instruction_pointer = param_2
                if self.enable_stdout:
                    print(f"{raw_instruction_value} {instruction}. jif. inst_pointer = {param_1}==0 => {param_2}")
            else:
                if self.enable_stdout:
                    print(f"{raw_instruction_value} {instruction}. jif. not jumping = {param_1}!=0 => {param_2}")
                self.instruction_pointer += 3
            return True

        # less than
        elif instruction.instruction == 7:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.get_parameter_value(2, instruction, True)

            if param_1 < param_2:
                self.memory[target] = 1
                if self.enable_stdout:
                    print(f"{raw_instruction_value} {instruction}. lt. mem[{target}] = 1")
            else:
                self.memory[target] = 0
                if self.enable_stdout:
                    print(f"{raw_instruction_value} {instruction}. lt. mem[{target}] = 0")

            self.instruction_pointer += 4
            return True

        # equals
        elif instruction.instruction == 8:
            param_1 = self.get_parameter_value(0, instruction)
            param_2 = self.get_parameter_value(1, instruction)
            target = self.get_parameter_value(2, instruction, True)

            if param_1 == param_2:
                self.memory[target] = 1
                if self.enable_stdout:
                    print(f"{raw_instruction_value} {instruction}. eq. mem[{target}] = 1")
            else:
                self.memory[target] = 0
                if self.enable_stdout:
                    print(f"{raw_instruction_value} {instruction}. eq. mem[{target}] = 0")

            self.instruction_pointer += 4
            return True

        # modify relative base
        elif instruction.instruction == 9:
            param_1 = self.get_parameter_value(0, instruction)

            self.relative_base += param_1
            if self.enable_stdout:
                print(f"{raw_instruction_value} {instruction}. rel_base = {param_1}")

            self.instruction_pointer += 2
            return True
        # exit / halt
        elif instruction.instruction == 99:
            if self.enable_stdout:
                print(f"{raw_instruction_value} {instruction}. halt")
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
            elif c == 2:
                data.parameter_modes.append(Modes.RELATIVE)

        return data

    def get_parameter_value(self, param_id, instruction, target_mode=False):
        mode = instruction.get_parameter_mode(param_id)
        v = self.memory[self.instruction_pointer + 1 + param_id]

        if target_mode:
            if mode == Modes.POSITION:
                return v
            elif mode == Modes.IMMEDIATE:
                raise Exception("immediate mode is unsupported for target mode ")
            elif mode == Modes.RELATIVE:
                return v + self.relative_base

        if mode == Modes.POSITION:
            return self.memory[v]
        elif mode == Modes.IMMEDIATE:
            return v
        elif mode == Modes.RELATIVE:
            return self.memory[self.relative_base + v]
