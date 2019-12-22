from collections import deque
from typing import List
from helpers import read_raw_entries


def part1(lines, cards_count, target_card, cycles):
    deck = deque()
    deck.extend(range(cards_count))

    for cycle in range(cycles):
        for step in lines:
            if "deal with increment" in step:
                count = int(step.split(" ")[3])
                tmp = []
                for _ in range(cards_count):
                    tmp.append(None)

                pos = 0
                while len(deck) > 0:
                    c = deck.popleft()
                    tmp[pos] = c
                    pos = (pos + count) % cards_count

                deck.extend(tmp)
                # print(deck.index(2019))
            elif "deal into new stack" in step:
                deck.reverse()
            elif "cut" in step:
                count = int(step.split(" ")[1])
                deck.rotate(-1 * count)
            else:
                raise Exception("Unknown command: ", step)

    return deck.index(target_card)


def part2(lines, cards_count, target_card, cycles):
    leading = target_card
    pos_target = target_card
    tailing = cards_count - target_card - 1

    for cycle in range(cycles):
        for step in lines:
            if "deal with increment" in step:
                count = int(step.split(" ")[3])
                pos_target = pos_target * count % cards_count
                leading = pos_target
                tailing = cards_count - pos_target -1
            elif "deal into new stack" in step:
                leading, tailing = tailing, leading
                pos_target = leading
            elif "cut" in step:
                count = int(step.split(" ")[1])
                # if count >= 0:
                leading = (leading - count) % cards_count
                tailing = (tailing + count) % cards_count
                pos_target = leading
                # else:
                #     leading = (leading + -1*count) % cards_count
                #     tailing = (tailing - -1*count) % cards_count
                #     pos_target = leading
            else:
                raise Exception("Unknown command: ", step)

    return pos_target


if __name__ == "__main__":
    _lines = read_raw_entries("input22.txt")

    r11 = part1(_lines, 10007, 2019, 1)
    print(r11)
    r1 = part2(_lines, 10007, 2019, 1)
    print(r1)

    r2 = part2(_lines, 119315717514047, 2020, 101741582076661)
    print(r2)
