from collections import deque
from dataclasses import dataclass
from typing import List
from helpers import read_raw_entries


def part1(lines, cards_count, target_card, cycles, reverse=False, initial_starting_order_list=None):
    ordered_lines = lines[:]
    if reverse:
        ordered_lines = ordered_lines.reverse()

    deck = deque()
    if initial_starting_order_list is None:
        deck.extend(range(cards_count))
    else:
        deck.extend(initial_starting_order_list)

    print(f"Cycle: {0}. Card at position 2020: {deck[2020]}")
    for cycle in range(cycles):
        for step in ordered_lines:
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
        print(f"Cycle: {cycle + 1}. Card at position 2020: {deck[2020]}")
    return deck.index(target_card)


def part1_efficient(lines, cards_count, target_card, cycles):
    leading = target_card
    pos_target = target_card
    tailing = cards_count - target_card - 1

    for cycle in range(cycles):
        for step in lines:
            if "deal with increment" in step:
                leading, pos_target, tailing = _deal_with_inc(cards_count, pos_target, step)
            elif "deal into new stack" in step:
                leading, tailing = tailing, leading
                pos_target = leading
            elif "cut" in step:
                count = int(step.split(" ")[1])
                # if count >= 0:
                leading = (leading - count) % cards_count
                tailing = (tailing + count) % cards_count
                pos_target = leading
            else:
                raise Exception("Unknown command: ", step)
            print(f"Cycle {cycle + 1}, After step: {step}, target card at position: {pos_target}")
    return pos_target


def _deal_with_inc(cards_count, pos_target, step):
    count = int(step.split(" ")[3])
    pos_target = pos_target * count % cards_count
    leading = pos_target
    tailing = cards_count - pos_target - 1
    return leading, pos_target, tailing


# Going to run this in reverse?
def part2(lines, cards_count, final_target, cycles):
    ordered_lines = lines[:]
    ordered_lines.reverse()

    leading = final_target
    pos_target = final_target
    tailing = cards_count - final_target - 1

    for cycle in range(cycles):
        # if pos_target in pos_target_cycle.keys():
        #     print(f"Repeat found on cycle {cycle}")
        #     cycles_before_repeat = cycles
        #     period = cycles - pos_target_cycle[pos_target]
        #     remainder = (cycles - cycles_before_repeat) % period
        #     return pos_on_cycle[remainder]
        #
        # pos_target_cycle[pos_target] = cycle
        # pos_on_cycle[cycle] = pos_target

        for step in ordered_lines:
            if "deal with increment" in step:
                leading, pos_target, tailing = _reverse_deal_with_inc(cards_count, pos_target, step)
            elif "deal into new stack" in step:
                leading, tailing = tailing, leading
                pos_target = leading
            elif "cut" in step:
                count = int(step.split(" ")[1])
                # if count >= 0:
                leading = (leading + count) % cards_count
                tailing = (tailing - count) % cards_count
                pos_target = leading
                # else:
                #     leading = (leading + -1*count) % cards_count
                #     tailing = (tailing - -1*count) % cards_count
                #     pos_target = leading
            else:
                raise Exception("Unknown command: ", step)
            print(f"Cycle {cycle + 1}, After step: {step}, target card at position: {pos_target}")
        print(f"Cycle: {cycle}. Position: {pos_target}")
    return pos_target


@dataclass
class Multiples:
    n: int
    c: int = 0

    def get(self):
        val = self.c * self.n
        self.c += 1
        yield val, self.c


def _reverse_deal_with_inc(cards_count, pos_target, step):
    count = int(step.split(" ")[3])


    f_lead = f_pos = f_tail = -1
    possible_target = -1
    while f_pos != pos_target:
        possible_target += 1
        f_lead, f_pos, f_tail = _deal_with_inc(cards_count, possible_target, step)

    leading = pos_target
    tailing = cards_count - possible_target - 1
    return leading, possible_target, tailing


    #
    # # Find the inverse mod
    # multiples = Multiples(cards_count)
    # while True:
    #     mul, new_n = next(multiples.get())
    #     div_f = (mul + pos_target) / count
    #     if div_f == int(div_f):
    #         pos_target = new_n
    #         break
    #
    # leading = pos_target
    # tailing = cards_count - pos_target - 1
    # return leading, pos_target, tailing


if __name__ == "__main__":
    _lines = read_raw_entries("input22.txt")

    r11 = part1(_lines, 10007, 2019, 10)
    print(r11)
    # r1 = part2(_lines, 10007, 2019, 1)
    # print(r1)

    # r2 = part2(_lines, 119315717514047, 2020, 10)
    # print(r2)
