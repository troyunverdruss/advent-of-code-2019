from collections import deque
from unittest import TestCase

from days.day02.intcode_computer import IntcodeComputer


class TestDay09(TestCase):
    def test_part_1(self):
        inst = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        ic = IntcodeComputer(inst)
        ic.run()
        expected = deque()
        expected.extend(inst)
        self.assertEqual(expected, ic.outputs)

    def test_part_1_2(self):
        inst = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
        ic = IntcodeComputer(inst)
        ic.run()

        self.assertEqual(16, len(str(ic.outputs[0])))

    def test_part_1_3(self):
        inst = [104, 1125899906842624, 99]
        ic = IntcodeComputer(inst)
        ic.run()

        self.assertEqual(1125899906842624, ic.outputs[0])

    def test_part_1_4(self):
        # For example, if the relative base is 2000,
        # then after the instruction 109,19, the relative base would be 2019.
        # If the next instruction were 204,-34, then the value at address 1985 would be output.

        ic = IntcodeComputer([109, 19, 204, -34, 99])
        ic.relative_base = 2000
        ic.memory[1985] = 123456
        ic.enable_stdout = True
        ic.run()

        self.assertEqual(123456, ic.get_outputs()[0])

    def test_part_1_5(self):
        # For example, if the relative base is 2000,
        # then after the instruction 109,19, the relative base would be 2019.
        # If the next instruction were 204,-34, then the value at address 1985 would be output.

        ic = IntcodeComputer([203, 0, 99, 10, 20])
        ic.set_inputs([123456])
        ic.relative_base = 4

        ic.enable_stdout = True
        ic.run()
        self.assertEqual(123456, ic.memory[4])

    def test_inst_3(self):
        ic = IntcodeComputer([3, 0, 99])
        ic.set_inputs([123456])
        ic.run()

        self.assertEqual({0: 123456, 2: 99}, ic.get_all_non_zero_memory())

    def test_inst_203_1(self):
        ic = IntcodeComputer([203, 0, 99])
        ic.set_inputs([123456])
        ic.run()

        self.assertEqual({0: 123456, 2: 99}, ic.get_all_non_zero_memory())

    def test_inst_203_2(self):
        ic = IntcodeComputer([203, 0, 99])
        ic.relative_base = 10
        ic.set_inputs([123456])
        ic.run()

        self.assertEqual({0: 203, 2: 99, 10: 123456}, ic.get_all_non_zero_memory())

    def test_inst_203_3(self):
        ic = IntcodeComputer([203, 0, 99])
        ic.enable_stdout = True
        ic.relative_base = 10
        ic.set_inputs([123456])
        ic.run()

        self.assertEqual({0: 203, 2: 99, 10: 123456}, ic.get_all_non_zero_memory())
