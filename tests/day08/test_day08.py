from unittest import TestCase

from days.day08.day08 import part1, part2_read_into_buffer, write_buffer_to_image


class TestDay08(TestCase):
    def test_part_1(self):
        _input = list(map(int, "121212789012"))
        self.assertEqual(9, part1(3, 2, _input))

    def test_part_2(self):
        _input = list(map(int, "0222112222120000"))
        buffer = part2_read_into_buffer(2, 2, _input)
        self.assertEqual(0, buffer[(0, 0)])
        self.assertEqual(1, buffer[(1, 0)])
        self.assertEqual(1, buffer[(0, 1)])
        self.assertEqual(0, buffer[(1, 1)])

    def test_write_image(self):
        buffer = {
            (0, 0): 0,
            (1, 0): 1,
            (2, 0): 2,
            (0, 1): 2,
            (1, 1): 0,
            (2, 1): 1,
        }
        write_buffer_to_image(3, 2, buffer, "day08/test_image.png")
