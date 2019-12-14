from collections import defaultdict
from unittest import TestCase
from ddt import data, ddt, unpack

# @ddt
from days.day11.day11 import PaintingRobot, Color


class TestDay11(TestCase):
    # @data(
    #     []
    # )
    # @unpack
    def test_part_1(self):
        hull = defaultdict(lambda: Color.BLACK)
        robot = PaintingRobot([], hull)
        robot.testing = True
        robot.test_outputs.extend(
            [
                1, 0,
                0, 0,
                1, 0,
                1, 0,
                0, 1,
                1, 0,
                1, 0
            ])

        robot.step()
        robot.step()
        robot.step()
        robot.step()
        robot.step()
        robot.step()
        robot.step()
