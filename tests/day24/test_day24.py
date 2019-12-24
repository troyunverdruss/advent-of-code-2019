from unittest import TestCase
from ddt import data, ddt, unpack

from days.day24.day24 import part1, part2


class TestDay24(TestCase):
    def test_part_1(self):
        lines = [
            "....#",
            "#..#.",
            "#..##",
            "..#..",
            "#....",
        ]

        r1 = part1(lines)

        self.assertEqual(2129920, r1)

    def test_part_2(self):
        lines = [
            "....#",
            "#..#.",
            "#..##",
            "..#..",
            "#....",
        ]

        r2 = part2(lines, 10)
        self.assertEqual(99, r2)
