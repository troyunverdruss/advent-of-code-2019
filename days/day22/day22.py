from collections import deque
from dataclasses import dataclass
from typing import List
from helpers import read_raw_entries
from sympy import mod_inverse


def part1(lines, cards_count, target_card, cycles, reverse=False, initial_starting_order_list=None):
    ordered_lines = lines[:]
    if reverse:
        ordered_lines = ordered_lines.reverse()

    deck = deque()
    if initial_starting_order_list is None:
        deck.extend(range(cards_count))
    else:
        deck.extend(initial_starting_order_list)

    # print(f"Cycle: {0}. Card at position 2020: {deck[2020]}")
    for cycle in range(cycles):
        print(f"Cycle {cycle}: {deck}")
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
        print(f"Cycle {cycle}: {pos_target}")
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


def part1_linear_functions(lines, cards_count, target_card):
    # a, b, as in y = ax + b
    # 1, 0 => exact same positions as it started/was
    a, b = 1, 0

    for step in lines:
        if "deal with increment" in step:
            inc = int(step.split(" ")[3])
            temp_a = inc
            temp_b = 0
        elif "deal into new stack" in step:
            temp_a = -1
            temp_b = cards_count - 1
        elif "cut" in step:
            cut = int(step.split(" ")[1])
            temp_a = 1
            temp_b = -cut
        else:
            raise Exception("Unknown command: ", step)
        # Combine the values from this step with the running tallies
        a = (a * temp_a) % cards_count
        b = (temp_a * b + temp_b) % cards_count

    return (a * target_card + b) % cards_count


def part1_linear_functions_reverse(lines, cards_count, target_card):
    a, b = compute_coefficients_reverse(cards_count, lines)

    return (a * target_card + b) % cards_count


def compute_coefficients_reverse(cards_count, lines):
    # a, b, as in y = ax + b
    # 1, 0 => exact same positions as it started/was
    a, b = 1, 0
    reversed_lines = lines[:]
    reversed_lines.reverse()
    for step in reversed_lines:
        if "deal with increment" in step:
            inc = int(step.split(" ")[3])
            temp_a = modinv(inc, cards_count)
            temp_b = 0
        elif "deal into new stack" in step:
            temp_a = -1
            temp_b = cards_count - 1
        elif "cut" in step:
            cut = int(step.split(" ")[1])
            temp_a = 1
            temp_b = cut
        else:
            raise Exception("Unknown command: ", step)
        # Combine the values from this step with the running tallies
        a = (a * temp_a) % cards_count
        b = (temp_a * b + temp_b) % cards_count
    return a, b


def exponentiate_polynomial(a, b, power, mod):
    if power == 0:
        return 1, 0

    if power % 2 == 0:
        # a*(ax+b) + b
        return exponentiate_polynomial(a * a % mod, a * b + b % mod, power // 2, mod)

    c, d = exponentiate_polynomial(a, b, power - 1, mod)
    return a * c % mod, (a * d + b) % mod


CARDS_COUNT = 119315717514047
REPEATS_COUNT = 101741582076661


def part2_linear_functions(lines, cards_count, repeat_count, target_card):
    a, b = compute_coefficients_reverse(cards_count, lines)
    a, b = exponentiate_polynomial(a, b, repeat_count, cards_count)
    return (a * target_card + b) % cards_count


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

    pos_target_cycle = {}

    for cycle in range(cycles):
        if cycle % 1_000_000 == 0:
            print("Cycle ", cycle)
        # print(f"Cycle: {cycle}")
        # if pos_target in pos_target_cycle.keys():
        #     print(f"Repeat found on cycle {cycle}")
        #     cycles_before_repeat = cycles
        #     period = cycles - pos_target_cycle[pos_target]
        #     remainder = (cycles - cycles_before_repeat) % period
        #     print(f"Period: {period}")
        #     print(f"Accoutns for all but last {remainder}")
        #     # return pos_on_cycle[remainder]
        #
        #
        # pos_target_cycle[pos_target] = cycle
        # # pos_on_cycle[cycle] = pos_target

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
            else:
                raise Exception("Unknown command: ", step)
            # print(f"Cycle {cycle + 1}, After step: {step}, target card at position: {pos_target}")
        # print(f"Cycle: {cycle}. Position: {pos_target}")
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

    new_target = pos_target * modinv(count, cards_count) % cards_count

    leading = new_target
    tailing = cards_count - new_target - 1
    return leading, new_target, tailing


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

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

    # r11 = part1(_lines, 10007, 2019, 10007)
    # print(r11)

    # r1 = part2(_lines, 119315717514047, 2020, 17574135437386)
    # print(r1)

    # r2 = part2(_lines, 119315717514047, 2020, 101741582076661)
    # print(r2)

    pos = 2019
    r1 = part1_efficient(_lines, 10007, pos, 1)
    print(r1)

    r2 = part2_linear_functions(_lines, 10007, 1, 7860)
    print(r2)

    r2 = part2_linear_functions(_lines, CARDS_COUNT, REPEATS_COUNT, 2020)
    print(r2)

    # too high 195593846987374290
    #              61256063148970
    # too low      41159822405911 << oops used 2019
