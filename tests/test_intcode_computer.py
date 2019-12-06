from unittest import TestCase

from days.day02.intcode_computer import IntcodeComputer, Modes


class TestIntcodeComputer(TestCase):
    def test_parse_instruction(self):
        ic = IntcodeComputer([101, -1, 0, 99])
        instruction = ic.parse_instruction(101)
        self.assertEqual(instruction.instruction, 1)
        self.assertEqual(instruction.get_parameter_mode(0), Modes.IMMEDIATE)
