from unittest import TestCase

from days.day06.day06 import part1, part2_with_search, part2_with_sets


class TestDay06(TestCase):
    def test_part_1(self):
        lines = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L",
        ]

        self.assertEqual(part1(lines), 42)

    def test_part1_simple(self):
        lines = [
            "AAA)BBB",
            "COM)AAA"
        ]

        self.assertEqual(part1(lines), 3)

    def test_part2_with_search(self):
        lines = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L",
            "K)YOU",
            "I)SAN"
        ]

        self.assertEqual(part2_with_search(lines), 4)

    def test_part2_with_sets(self):
        lines = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L",
            "K)YOU",
            "I)SAN"
        ]

        self.assertEqual(part2_with_sets(lines), 4)
