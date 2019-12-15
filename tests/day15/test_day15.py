from unittest import TestCase
from ddt import data, ddt, unpack

@ddt
class TestDay15(TestCase):
    @data(
        []
    )
    @unpack
    def test_part_1(self, test_input, expected):
        self.assertEqual(expected, 0)
