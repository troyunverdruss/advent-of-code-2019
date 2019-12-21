from unittest import TestCase
from ddt import data, ddt, unpack

from days.day20.day20 import part1
from helpers import read_raw_entries


class TestDay20(TestCase):
    def test_part_1(self):
        _lines = read_raw_entries("ex1_input.txt", strip=False)
        r1 = part1(_lines)
        self.assertEqual(23, r1)
