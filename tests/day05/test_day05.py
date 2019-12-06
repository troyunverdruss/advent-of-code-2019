from unittest import TestCase
from ddt import data, ddt, unpack

from days.day02.intcode_computer import IntcodeComputer


@ddt
class TestDay05(TestCase):

    def test_example_program_1(self):
        ic = IntcodeComputer([3, 0, 4, 0, 99])
        # ic.enable_stdout = True
        ic.set_inputs([1234])
        ic.run()

    def test_first_diagnostic_program(self):
        ic = IntcodeComputer(
            [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 99, 65, 39, 225, 2, 14, 169, 224, 101, -2340, 224, 224, 4,
             224, 1002, 223, 8, 223, 101, 7, 224, 224, 1, 224, 223, 223, 1001, 144, 70, 224, 101, -96, 224, 224, 4, 224,
             1002, 223, 8, 223, 1001, 224, 2, 224, 1, 223, 224, 223, 1101, 92, 65, 225, 1102, 42, 8, 225, 1002, 61, 84,
             224, 101, -7728, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 5, 224, 1, 223, 224, 223, 1102, 67, 73,
             224, 1001, 224, -4891, 224, 4, 224, 102, 8, 223, 223, 101, 4, 224, 224, 1, 224, 223, 223, 1102, 54, 12,
             225, 102, 67, 114, 224, 101, -804, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 3, 224, 1, 224, 223, 223,
             1101, 19, 79, 225, 1101, 62, 26, 225, 101, 57, 139, 224, 1001, 224, -76, 224, 4, 224, 1002, 223, 8, 223,
             1001, 224, 2, 224, 1, 224, 223, 223, 1102, 60, 47, 225, 1101, 20, 62, 225, 1101, 47, 44, 224, 1001, 224,
             -91, 224, 4, 224, 1002, 223, 8, 223, 101, 2, 224, 224, 1, 224, 223, 223, 1, 66, 174, 224, 101, -70, 224,
             224, 4, 224, 102, 8, 223, 223, 1001, 224, 6, 224, 1, 223, 224, 223, 4, 223, 99, 0, 0, 0, 677])
        # ic.enable_stdout = True
        ic.set_inputs([1])
        ic.run()

    @data(
        [[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 10, 0],
        [[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1],
        [[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, 1],
        [[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0],
    )
    @unpack
    def test_part_2_position_mode_examples(self, instructions, input_value, expected):
        ic = IntcodeComputer(instructions)
        ic.set_inputs([input_value])
        # ic.enable_stdout = True
        ic.run()
        self.assertEqual(expected, ic.get_outputs()[0])

    @data(
        [[3, 3, 1108, -1, 8, 3, 4, 3, 99], 10, 0],
        [[3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1],
        [[3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, 1],
        [[3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, 0],
    )
    @unpack
    def test_part_2_immediate_mode_examples(self, instructions, input_value, expected):
        ic = IntcodeComputer(instructions)
        ic.set_inputs([input_value])
        # ic.enable_stdout = True
        ic.run()
        self.assertEqual(expected, ic.get_outputs()[0])

    @data(
        [[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0],
        [[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 2, 1],
    )
    @unpack
    def test_part_2_jump_test_position_mode_examples(self, instructions, input_value, expected):
        ic = IntcodeComputer(instructions)
        ic.set_inputs([input_value])
        # ic.enable_stdout = True
        ic.run()
        self.assertEqual(expected, ic.get_outputs()[0])

    @data(
        [[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0],
        [[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 2, 1],
    )
    @unpack
    def test_part_2_jump_test_immediate_mode_examples(self, instructions, input_value, expected):
        ic = IntcodeComputer(instructions)
        ic.set_inputs([input_value])
        # ic.enable_stdout = True
        ic.run()
        self.assertEqual(expected, ic.get_outputs()[0])
