#!/bin/bash

if [[ -z "$1" ]]; then
  echo "Provide a day as argument, like ./setup_day.sh 01"
  exit
fi

mkdir -p days/day"$1" tests/day"$1"
touch tests/day"$1"/__init__.py

cat << EOF > ./days/day"$1"/day"$1".py
from typing import List
from helpers import read_raw_entries
if __name__ == "__main__":
    pass
EOF

cat << EOF > ./tests/day"$1"/test_day"$1".py
from unittest import TestCase
from ddt import data, ddt, unpack

@ddt
class TestDay$1(TestCase):
    @data(
        []
    )
    @unpack
    def test_part_1(self, test_input, expected):
        self.assertEqual(expected, 0)
EOF

