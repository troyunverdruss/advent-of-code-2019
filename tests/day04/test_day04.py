from unittest import TestCase
from ddt import data, ddt, unpack

from days.day04.day04 import convert_num_to_digits, valid_part1, valid_part2


@ddt
class TestDay04(TestCase):
    @data([111111, True], [223450, False], [123789, False])
    @unpack
    def test_part1_examples(self, test_input, is_valid):
        self.assertEqual(is_valid, valid_part1(convert_num_to_digits(test_input)))

    @data([112233, True], [123444, False], [111122, True])
    @unpack
    def test_part2_examples(self, test_input, is_valid):
        self.assertEqual(is_valid, valid_part2(convert_num_to_digits(test_input)))
