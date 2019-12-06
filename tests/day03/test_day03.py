from unittest import TestCase
from ddt import data, ddt, unpack

from days.day03.day03 import solve_by_gridding, parse_input, solve_with_sets


@ddt
class TestDay03(TestCase):
    @data(
        ["R8,U5,L5,D3", "U7,R6,D4,L4", 6],
        ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159],
        ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135]
    )
    @unpack
    def test_part_1(self, line_a, line_b, expected_distance):
        parsed_a = parse_input(line_a)
        parsed_b = parse_input(line_b)
        self.assertEqual(expected_distance, solve_by_gridding(parsed_a, parsed_b)[0])
        self.assertEqual(expected_distance, solve_with_sets(parsed_a, parsed_b)[0])

    @data(
        ["R8,U5,L5,D3", "U7,R6,D4,L4", 30],
        ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 610],
        ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 410]
    )
    @unpack
    def test_part_2(self, line_a, line_b, expected_distance):
        parsed_a = parse_input(line_a)
        parsed_b = parse_input(line_b)
        self.assertEqual(expected_distance, solve_by_gridding(parsed_a, parsed_b)[1])
