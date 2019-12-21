from unittest import TestCase
from ddt import data, ddt, unpack

from days.day16.day16 import take_n_skip_n, part1_v2, part2, process_for_digit_n


class TestDay16(TestCase):
    def test_part1_ex_1(self):
        _initial_signal = list(map(int, list("12345678")))
        result = part1_v2(_initial_signal, 4)
        self.assertEqual("01029498", result)

    def test_part1_ex_2(self):
        _initial_signal = list(map(int, list("80871224585914546619083218645595")))
        result = part1_v2(_initial_signal, 100)
        self.assertEqual("24176176", result)

    def test_part1_ex_3(self):
        _initial_signal = list(map(int, list("19617804207202209144916044189917")))
        result = part1_v2(_initial_signal, 100)
        self.assertEqual("73745418", result)

    def test_part1_ex_4(self):
        _initial_signal = list(map(int, list("69317163492948606335995924319873")))
        result = part1_v2(_initial_signal, 100)
        self.assertEqual("52432133", result)

    def test_part2_ex_1(self):
        _initial_signal = list(map(int, list("03036732577212944063491565474664")))
        result = part2(_initial_signal, 100)
        self.assertEqual("84462026", result)

    def test_part2_ex_2(self):
        _initial_signal = list(map(int, list("02935109699940807407585447034323")))
        result = part2(_initial_signal, 100)
        self.assertEqual("78725270", result)

    def test_part2_ex_3(self):
        _initial_signal = list(map(int, list("03081770884921959731165446850517")))
        result = part2(_initial_signal, 100)
        self.assertEqual("53553731", result)


@ddt
class TestDay16Ddt(TestCase):
    @data(

            [2, 1],
            [4, 2],
            [4, 3],
            [2, 4],
            [6, 5],
            [0, 6],
            [4, 7],
            [8, 8],
            [7, 9],
            [1, 10],
            [8, 11],
            [8, 12],
            [2, 13],
            [7, 14],
            [1, 15],
            [4, 16],
            [6, 17],
            [5, 18],
            [3, 19],
            [0, 20],
            [6, 21],
            [1, 22],
            [5, 23],
            [8, 24],


    )
    @unpack
    def test_part2_intermediate_states(self, expected_output, n):
        _in = list(map(int, list("12345678"))) * 3
        _out = _in[:]

        process_for_digit_n(n, 8, _in, 24, _out)
        # res = process_for_digit_n([1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8], 1)
        # print(res)

        print(_out[n - 1])

        self.assertEqual(expected_output, _out[n - 1])
