from unittest import TestCase
from ddt import data, ddt, unpack
from helpers import read_raw_entries
from sympy import mod_inverse

from days.day22.day22 import part1_efficient, part2, _reverse_deal_with_inc, _deal_with_inc, modinv, \
    part1_linear_functions, part1_linear_functions_reverse


class TestDay22(TestCase):
    def test_part_2_ex_1_deal_into_new_stack(self):
        inst = [
            "deal into new stack"
        ]
        pos1 = part1_efficient(inst, 10, 9, 1)
        pos2 = part1_efficient(inst, 10, 2, 1)
        self.assertEqual(0, pos1)
        self.assertEqual(7, pos2)

        # pos3 = part2(inst, 10, 2, 1)
        # self.assertEqual(7, pos3)

    def test_part_2_ex_1_deal_with_inc(self):
        inst = [
            "deal with increment 3"
        ]
        pos1 = part1_efficient(inst, 10, 9, 1)
        pos2 = part1_efficient(inst, 10, 2, 1)
        self.assertEqual(7, pos1)
        self.assertEqual(6, pos2)

        # pos3 = part2(inst, 10, 2, 1)
        # self.assertEqual(4, pos3)

    def test_part_2_ex_1_deal_with_pos_cut(self):
        inst = [
            "cut 3 cards"
        ]
        pos1 = part1_efficient(inst, 10, 9, 1)
        pos2 = part1_efficient(inst, 10, 2, 1)
        self.assertEqual(6, pos1)
        self.assertEqual(9, pos2)

        # pos3 = part2(inst, 10, 2, 1)
        # self.assertEqual(5, pos3)

    def test_part_2_ex_1_deal_with_neg_cut(self):
        inst = [
            "cut -4 cards"
        ]
        pos1 = part1_efficient(inst, 10, 9, 1)
        pos2 = part1_efficient(inst, 10, 2, 1)
        self.assertEqual(3, pos1)
        self.assertEqual(6, pos2)

        # pos3 = part2(inst, 10, 2, 1)
        # self.assertEqual(8, pos3)

    def test_ex_1(self):
        inst = [
            "deal with increment 7",
            "deal into new stack",
            "deal into new stack",
            # Result: 0 3 6 9 2 5 8 1 4 7
        ]
        pos = part1_efficient(inst, 10, 6, 1)
        self.assertEqual(2, pos)

        # pos2 = part2(inst, 10, 6, 1)
        # self.assertEqual(8, pos2)

    def test_ex_2(self):
        inst = [
            "cut 6",
            "deal with increment 7",
            "deal into new stack",
            # Result: 3 0 7 4 1 8 5 2 9 6
        ]
        pos = part1_efficient(inst, 10, 6, 1)
        self.assertEqual(9, pos)

        # pos2 = part2(inst, 10, 6, 1)
        # self.assertEqual(5, pos2)

    def test_ex_3(self):
        inst = [
            "deal with increment 7",
            "deal with increment 9",
            "cut -2",
            # Result: 6 3 0 7 4 1 8 5 2 9
        ]
        pos = part1_efficient(inst, 10, 6, 1)
        self.assertEqual(0, pos)

        # pos2 = part2(inst, 10, 0, 1)
        # self.assertEqual(6, pos2)

    def test_ex_4(self):
        inst = [
            "deal into new stack",
            "cut -2",
            "deal with increment 7",
            "cut 8",
            "cut -4",
            "deal with increment 7",
            "cut 3",
            "deal with increment 9",
            "deal with increment 3",
            "cut -1",
            # Result: 9 2 5 8 1 4 7 0 3 6
        ]
        pos = part1_efficient(inst, 10, 6, 1)
        self.assertEqual(9, pos)

        # pos2 = part2(inst, 10, 6, 1)
        # self.assertEqual(7, pos2)

    def test_cycle_repeat(self):
        inst = [
            "cut 1"
        ]
        pos1 = part1_efficient(inst, 10, 6, 3)
        self.assertEqual(3, pos1)

        pos2 = part1_efficient(inst, 10, 6, 8)
        self.assertEqual(8, pos2)

    def test_reverse_inc_7(self):
        step = "deal with increment 7"
        f_leading, f_pos_target, f_tailing = _deal_with_inc(11, 3, step)
        print(f_leading, f_pos_target, f_tailing)

        leading, pos_target, tailing = _reverse_deal_with_inc(11, f_pos_target, step)
        self.assertEqual(3, leading)
        self.assertEqual(3, pos_target)
        self.assertEqual(7, tailing)

    def test_reverse_inc_2(self):
        step = "deal with increment 3"
        f_leading, f_pos_target, f_tailing = _deal_with_inc(11, 7, step)

        leading, pos_target, tailing = _reverse_deal_with_inc(11, f_pos_target, step)
        self.assertEqual(7, leading)
        self.assertEqual(7, pos_target)
        self.assertEqual(3, tailing)

    def test_reverse_part1(self):
        lines = read_raw_entries("test_input22.txt")
        position_of_2019 = part1_efficient(lines[:], 10007, 2019, 1)
        print(position_of_2019)

        reversed_position = part2(lines[:], 10007, position_of_2019, 1)
        self.assertEqual(2019, reversed_position)

    def test_mod_inverse(self):
        # current pos_target * deal by inc count % total cards_count
        # 8, 4, 11
        new_position = 8 * 4 % 11
        original_position = mod_inverse(4, 11)
        i = 0


class TestDay22LinearFunctions(TestCase):
    def test_part_1_nothing(self):
        inst = []
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)
        self.assertEqual(9, pos1)
        self.assertEqual(2, pos2)

    def test_part_1_nothing_rev(self):
        inst = []
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)

        r1 = part1_linear_functions_reverse(inst, 11, pos1)
        r2 = part1_linear_functions_reverse(inst, 11, pos2)
        self.assertEqual(9, r1)
        self.assertEqual(2, r2)

    def test_part_1_deal_new_stack(self):
        inst = [
            "deal into new stack"
        ]
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)
        self.assertEqual(1, pos1)
        self.assertEqual(8, pos2)

    def test_part_1_deal_new_stack_rev(self):
        inst = [
            "deal into new stack"
        ]
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)

        r1 = part1_linear_functions_reverse(inst, 11, pos1)
        r2 = part1_linear_functions_reverse(inst, 11, pos2)
        self.assertEqual(9, r1)
        self.assertEqual(2, r2)

    def test_part_1_deal_with_inc(self):
        inst = [
            "deal with increment 3"
        ]
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)
        self.assertEqual(5, pos1)
        self.assertEqual(6, pos2)

    def test_part_1_deal_with_inc_rev(self):
        inst = [
            "deal with increment 3"
        ]
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)

        r1 = part1_linear_functions_reverse(inst, 11, pos1)
        r2 = part1_linear_functions_reverse(inst, 11, pos2)
        self.assertEqual(9, r1)
        self.assertEqual(2, r2)

    def test_part_1_cut(self):
        inst = [
            "cut 3 cards"
        ]
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)
        self.assertEqual(6, pos1)
        self.assertEqual(10, pos2)

    def test_part_1_cut_rev(self):
        inst = [
            "cut 3 cards"
        ]
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)

        r1 = part1_linear_functions_reverse(inst, 11, pos1)
        r2 = part1_linear_functions_reverse(inst, 11, pos2)
        self.assertEqual(9, r1)
        self.assertEqual(2, r2)

    def test_part_1_neg_cut(self):
        inst = [
            "cut -4 cards"
        ]
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)
        self.assertEqual(2, pos1)
        self.assertEqual(6, pos2)

    def test_part_1_neg_cut(self):
        inst = [
            "cut -4 cards"
        ]
        pos1 = part1_linear_functions(inst, 11, 9)
        pos2 = part1_linear_functions(inst, 11, 2)

        r1 = part1_linear_functions_reverse(inst, 11, pos1)
        r2 = part1_linear_functions_reverse(inst, 11, pos2)
        self.assertEqual(9, r1)
        self.assertEqual(2, r2)

    def test_run_part_1(self):
        lines = read_raw_entries("test_input22.txt")
        r = part1_linear_functions(lines, 10007, 2019)
        self.assertEqual(7860, r)

    def test_run_part_1_rev(self):
        lines = read_raw_entries("test_input22.txt")
        pos1 = part1_linear_functions(lines, 10007, 2019)
        self.assertEqual(7860, pos1)

        r = part1_linear_functions_reverse(lines, 10007, pos1)
        self.assertEqual(2019, r)

    # def test_run_part_1_(self):
    #     lines = read_raw_entries("test_input22.txt")
    #     r = part1_linear_functions(lines, 10007, 2019)
    #     self.assertEqual(7860, r)
    #
    # def test_run_part_1_rev(self):
    #     lines = read_raw_entries("test_input22.txt")
    #     pos1 = part1_linear_functions(lines, 10007, 2019)
    #     self.assertEqual(7860, pos1)
    #
    #     r = part1_linear_functions_reverse(lines, 10007, pos1)
    #     self.assertEqual(2019, r)
