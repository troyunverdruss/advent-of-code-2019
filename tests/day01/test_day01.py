from unittest import TestCase

from ddt import unpack, data, ddt

from days.day01.day01 import part1, part2


@ddt
class TestDay01(TestCase):
    @data([12, 2], [14, 2], [1969, 654], [100756, 33583])
    @unpack
    def test_part_1(self, mass, expected):
        self.assertEqual(expected, part1([mass]))

    @data([14, 2], [1969, 966], [100756, 50346])
    @unpack
    def test_part_2(self, mass, expected):
        self.assertEqual(expected, part2([mass]))
