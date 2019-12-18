from unittest import TestCase
from ddt import data, ddt, unpack

from days.day16.day16 import take_n_skip_n


class TestDay16(TestCase):
    def test_ex_1(self):
        _initial_signal = list(map(int, list("12345678")))
        take_n_skip_n(_initial_signal, 4)
