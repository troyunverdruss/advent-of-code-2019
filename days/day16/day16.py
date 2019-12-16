from dataclasses import dataclass
from typing import List
from helpers import read_raw_entries


@dataclass
class SignalGenerator:
    n: int
    base_pattern: List[int]
    first: bool = True
    index: int = 0
    count: int = 0

    def __init__(self):
        self.base_pattern = [0, 1, 0, -1]

    def next(self):

        if self.first:
            self.first = False
            if self.n == 1:
                self.index += 1
            else:
                self.count += 1

        value = self.base_pattern[self.index]
        self.count += 1
        if self.count >= self.n:
            self.index = (self.index + 1) % len(self.base_pattern)
            self.count = 0

        yield value


def part1(initial_signal, count=100):
    phase_input = initial_signal[:]
    for count_id in range(count):
        print(count_id)
        phase_output = []
        for i in range(1, len(phase_input) + 1):
            sg = SignalGenerator()
            sg.n = i
            running_sum = 0
            for d in phase_input:
                running_sum += d * next(sg.next())
            phase_output.append(int(str(running_sum)[-1]))
        # print(phase_output)
        phase_input = phase_output[:]
    return ''.join(map(str, phase_input[0:8]))


if __name__ == "__main__":
    _initial_signal = list(map(int, list(read_raw_entries("input16.txt")[0])))
    part1res = part1(_initial_signal)
    print(part1res)

    # s = read_raw_entries("input16.txt")[0]
    # s1 = s * 10000
    # part2 = part1(list(map(int, list(s1))))
    # _in = list(map(int, list("80871224585914546619083218645595")))
    # part1(_in, 100)
    # sg = SignalGenerator()
    # sg.n = 8
    pass
