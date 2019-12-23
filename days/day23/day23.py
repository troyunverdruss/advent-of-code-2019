from dataclasses import dataclass
from typing import List

from days.day02.intcode_computer import IntcodeComputer
from helpers import read_raw_entries


@dataclass
class Nat:
    x: int
    y: int


def part1(instructions):
    computers = []

    # Boot up
    for i in range(50):
        computers.append(IntcodeComputer(instructions))
        computers[i].run()
        computers[i].inputs.append(i)

    y_for_255 = None

    while y_for_255 is None:
        for i in range(50):
            computers[i].waiting = False
            computers[i].run()

            while len(computers[i].outputs) % 3 == 0 and len(computers[i].outputs) != 0:
                a = computers[i].outputs.popleft()
                x = computers[i].outputs.popleft()
                y = computers[i].outputs.popleft()

                if a == 255:
                    y_for_255 = y
                    break

                computers[a].inputs.append(x)
                computers[a].inputs.append(y)
            if len(computers[i].inputs) == 0 and computers[i].waiting is True:
                computers[i].inputs.append(-1)
    return y_for_255


def part2(instructions):
    computers = []

    # Boot up
    last_delivered = []
    for i in range(50):
        computers.append(IntcodeComputer(instructions))
        computers[i].run()
        computers[i].inputs.append(i)
        last_delivered.append(0)

    nat = Nat(0, 0)
    last_delivered_y = None

    cycle = 0
    searching = True
    while searching:
        cycle += 1
        for i in range(50):
            computers[i].waiting = False
            computers[i].run()

            while len(computers[i].outputs) % 3 == 0 and len(computers[i].outputs) != 0:
                a = computers[i].outputs.popleft()
                x = computers[i].outputs.popleft()
                y = computers[i].outputs.popleft()

                if a == 255:
                    nat.x = x
                    nat.y = y

                else:
                    computers[a].inputs.append(x)
                    computers[a].inputs.append(y)
            if len(computers[i].inputs) == 0 and computers[i].waiting is True:
                computers[i].inputs.append(-1)

        idle = len(list(filter(lambda c: len(c.inputs) == 0 or (len(c.inputs) == 1 and c.inputs[0] == -1), computers)))
        if idle == len(computers) and cycle != 1:
            computers[0].inputs.append(nat.x)
            computers[0].inputs.append(nat.y)

            if last_delivered_y == nat.y:
                searching = False

            last_delivered_y = nat.y

    print(last_delivered_y)
    return last_delivered_y


if __name__ == "__main__":
    _inst = list(map(int, read_raw_entries("input23.txt")[0].split(",")))
    r1 = part1(_inst)
    print(r1)

    r2 = part2(_inst)
    print(r2)
    pass
