from unittest import TestCase
from ddt import data, ddt, unpack

from days.day12.day12 import parse_input, part2


class TestDay12(TestCase):
    def test_part_2_ex_1(self):
        lines = [
            "<x=-1, y=0, z=2>",
            "<x=2, y=-10, z=-7>",
            "<x=4, y=-8, z=8>",
            "<x=3, y=5, z=-1>",
        ]
        moons = parse_input(lines)
        result = part2(moons)
        self.assertEqual(2772, result)

    def test_part_2_ex_2(self):
        lines = [
            "<x=-8, y=-10, z=0>",
            "<x=5, y=5, z=10>",
            "<x=2, y=-7, z=3>",
            "<x=9, y=-8, z=-3>",
        ]
        moons = parse_input(lines)
        result = part2(moons)
        self.assertEqual(4686774924, result)
