from unittest import TestCase
from ddt import data, ddt, unpack

from days.day10.day10 import part1, build_grid, part2


class TestDay10(TestCase):
    def test_part_2_example_1(self):
        _input = [
        ".#....#####...#..",
        "##...##.#####..##",
        "##...#...#.#####.",
        "..#.....#...###..",
        "..#.#.....#....##",
            ]


        _map = build_grid(_input)
        _best, _max = part1(_map)
        part2(_map, (8.0, 3.0))

        # self.assertEqual(expected, 0)
