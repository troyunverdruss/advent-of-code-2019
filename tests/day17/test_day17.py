from unittest import TestCase
from ddt import data, ddt, unpack

from days.day16.day16 import process_for_digit_n


@ddt
class TestDay17(TestCase):
    @data(
        []
    )
    @unpack
    def test_part_1(self, test_input, expected):
        self.assertEqual(expected, 0)
