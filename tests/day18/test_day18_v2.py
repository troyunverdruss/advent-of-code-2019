from unittest import TestCase

from days.day18.day18_v2 import part1, part2


class TestDay18(TestCase):
    def test_part_1_ex_1(self):
        lines = [
            "#########",
            "#b.A.@.a#",
            "#########",
        ]
        self.assertEqual(8, part1(lines))

    def test_part_1_ex_2(self):
        lines = [
            "########################",
            "#f.D.E.e.C.b.A.@.a.B.c.#",
            "######################.#",
            "#d.....................#",
            "########################",
        ]
        self.assertEqual(86, part1(lines))

    def test_part_1_ex_3(self):
        lines = [
            "########################",
            "#...............b.C.D.f#",
            "#.######################",
            "#.....@.a.B.c.d.A.e.F.g#",
            "########################",
        ]
        self.assertEqual(132, part1(lines))

    def test_part_1_ex_4(self):
        lines = [
            "#################",
            "#i.G..c...e..H.p#",
            "########.########",
            "#j.A..b...f..D.o#",
            "########@########",
            "#k.E..a...g..B.n#",
            "########.########",
            "#l.F..d...h..C.m#",
            "#################",
        ]
        self.assertEqual(136, part1(lines))

    def test_part_1_ex_5(self):
        lines = [
            "########################",
            "#@..............ac.GI.b#",
            "###d#e#f################",
            "###A#B#C################",
            "###g#h#i################",
            "########################",
        ]
        self.assertEqual(81, part1(lines))

    def test_part_2_ex_1(self):
        lines = [
            "#######",
            "#a.#Cd#",
            "##@#@##",
            "#######",
            "##@#@##",
            "#cB#Ab#",
            "#######",
        ]
        self.assertEqual(8, part2(lines))
