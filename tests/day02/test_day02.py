from typing import List
from unittest import TestCase

from ddt import data, ddt, unpack

from days.day02.intcode_computer import IntcodeComputer


@ddt
class TestDay02(TestCase):
    @data(
        [3500,
         [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
         [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]],
        [2,
         [1, 0, 0, 0, 99],
         [2, 0, 0, 0, 99]],
        [2,
         [2, 3, 0, 3, 99],
         [2, 3, 0, 6, 99]],
        [30,
         [1, 1, 1, 4, 99, 5, 6, 0, 99],
         [30, 1, 1, 4, 2, 5, 6, 0, 99]]
    )
    @unpack
    def test_part_1(self, expected_in_zero: int, instructions: List[int], final_memory: List[int]):
        ic = IntcodeComputer(instructions)
        ic.run()
        self.assertEqual(expected_in_zero, ic.get_zero())
        self.assertEqual(final_memory, ic.memory)
