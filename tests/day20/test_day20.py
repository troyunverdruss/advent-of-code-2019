from unittest import TestCase
from ddt import data, ddt, unpack

from days.day20.day20 import part1, part2
from helpers import read_raw_entries


class TestDay20(TestCase):
    def test_part_1_ex_1(self):
        _lines = read_raw_entries("ex1_input.txt", strip=False)
        r1 = part1(_lines)
        self.assertEqual(23, r1)

    def test_part_2_ex_1(self):
        _lines = read_raw_entries("ex1_input.txt", strip=False)
        r = part2(_lines)
        self.assertEqual(26, r)

    def test_part_2_ex_2(self):
        _lines = read_raw_entries("ex3_input.txt", strip=False)
        r = part2(_lines)
        self.assertEqual(396, r)
