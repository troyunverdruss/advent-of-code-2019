# from dataclasses import dataclass
from typing import List
# from helpers import read_raw_entries
import time

# @dataclass
from days.day12.day12 import lcm
from helpers import read_raw_entries


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
            modifiers = []
            new_digits = []
            for d in phase_input:
                modifier = next(sg.next())
                modifiers.append(modifier)
                running_sum += d * modifier
                new_digits.append(d * modifier)
            # print(''.join(map(lambda x: str(x).rjust(3), phase_input)), "  ->",
            # print(''.join(map(lambda x: str(x).rjust(3), new_digits)), "   -> ", int(str(running_sum)[-1]))
            # print(''.join(map(lambda x: str(x).rjust(3), modifiers)))
            # print("")

            # print(''.join(map(lambda x: str(x).rjust(3), phase_input)), "  ->",
            #       ''.join(map(lambda x: str(x).rjust(3), phase_output)))
            phase_output.append(int(str(running_sum)[-1]))

        phase_input = phase_output[:]
    return ' '.join(map(str, phase_input[0:8]))


def part1_v2(initial_signal, iter_count=100):
    signal_len = len(initial_signal)

    phases = [None, None]
    phases[0] = initial_signal[:]
    phases[1] = initial_signal[:]

    for count_id in range(iter_count):
        src = count_id % 2
        dst = (count_id + 1) % 2

        take_n_skip_n(phases[src], phases[dst], repeat_length=signal_len)
        # print("   mid:", ' '.join(map(str, phases[dst])))

    final_dst = iter_count % 2
    # print("answer:", ' '.join(map(str, phases[final_dst][0:8])))
    # print("answer:", ' '.join(map(str, phases[final_dst])))
    return ''.join(map(str, phases[0][0:8]))


def part2(initial_signal, iter_count=100, repeat_count=10_000):
    offset = int(''.join(map(str, initial_signal[0:7])))

    repeated_signal = initial_signal * repeat_count
    signal_len = len(initial_signal)

    if offset < signal_len / 2:
        raise Exception("I hope you have time to kill ...")

    for count_id in range(iter_count):
        total = 0
        start = len(repeated_signal) - 1
        for d in range(start, offset-1, -1):
            total += repeated_signal[d]
            repeated_signal[d] = abs(total) % 10
    # print("answer:", ''.join(map(str, repeated_signal[offset:offset + 8])))
    # print("")
    return ''.join(map(str, repeated_signal[offset:offset + 8]))
    # 5747284 is too low
    # 57472847 is too high
    # phases = [None, None]
    # phases[0] = repeated_signal[:]
    # phases[1] = repeated_signal[:]
    #
    # for count_id in range(iter_count):
    #     print(f"iteration count: {count_id}")
    #     src = count_id % 2
    #     dst = (count_id + 1) % 2
    #
    #
    #     take_n_skip_n(phases[src], phases[dst], repeat_length=signal_len)
    #
    # final_dst = iter_count % 2
    # print("answer:", ' '.join(map(str, phases[final_dst][offset:offset + 8])))
    # print("")
    # return ''.join(map(str, phases[0][offset:offset + 8]))


def take_n_skip_n(signal_in, signal_out, repeat_length):
    signal_len = len(signal_in)

    for n in range(1, signal_len + 1):
        process_for_digit_n(n, repeat_length, signal_in, signal_len, signal_out)
        # print(f"count: {count_id}, n={n}")
        # print(signal_out[n - 1], end="")
    # print("")
    # print(phases[0])
    # print(phases[1])


def process_for_digit_n(n, repeat_length, signal_in, signal_len, signal_out):
    iter_max = signal_len
    if repeat_length != signal_len:
        iter_max = lcm([repeat_length, 4 * n, n])
    # print(f"{n}.", end="")
    # if n % 1000 ==0:
    #     print("")
    total = 0
    add = False
    for index in range(n - 1, iter_max, 2 * n):
        # print(f"  index: {index}")
        add = not add
        if add:
            total += sum(signal_in[index:min(index + n, signal_len)])
        else:
            total -= sum(signal_in[index:min(index + n, signal_len)])
        # print(f"  subtotal: {total}")
    if repeat_length != signal_len:
        even_repeats = signal_len // iter_max
        total *= even_repeats
        leftover_len = signal_len - (iter_max * even_repeats)

        if leftover_len > 0:
            to_process = signal_in[-1 * leftover_len:]

            # let's go through what's left here ...
            add = False
            for index in range(0, leftover_len, 2 * n):
                # print(f"  index: {index}")
                add = not add
                if add:
                    total += sum(to_process[index + n - 1:min(index + n + n - 1, signal_len)])
                else:
                    total -= sum(to_process[index + n - 1:min(index + n + n - 1, signal_len)])

        signal_out[n - 1] = abs(total) % 10
    else:
        signal_out[n - 1] = abs(total) % 10
    # print("n=" + str(n), abs(total) % 10)


# print("1:     ", ' '.join(map(str, phases[1][0:8])))
# print("answer:", ' '.join(map(str, phases[last_dst][0:8])))
# return ''.join(map(str, phases[0][0:8]))


if __name__ == "__main__":
    # # lines="59772698208671263608240764571860866740121164692713197043172876418614411671204569068438371694198033241854293277505547521082227127768000396875825588514931816469636073669086528579846568167984238468847424310692809356588283194938312247006770713872391449523616600709476337381408155057994717671310487116607321731472193054148383351831456193884046899113727301389297433553956552888308567897333657138353770191097676986516493304731239036959591922009371079393026332649558536888902303554797360691183681625604439250088062481052510016157472847289467410561025668637527408406615316940050060474260802000437356279910335624476330375485351373298491579364732029523664108987"
    # _initial_signal = list(map(int, list(lines)))
    _initial_signal = list(map(int, list(read_raw_entries("input16.txt")[0])))
    # # part1res = part1(_initial_signal)
    # # print(part1res)
    res = part1_v2(_initial_signal)
    print(res)

    p2 = part2(_initial_signal)
    print(p2)


    # # part1res2 = take_n_skip_n(_initial_signal)
    # # print(part1res2)
    #
    # # offset=_initial_signal[:8]
    # # part2res = take_n_skip_n(_initial_signal*10000)
    # # print(part2res[offset:offset+8])
    #
    # # s = read_raw_entries("input16.txt")[0]
    # # s = '1234567890' * 65 * 10000
    # # s1 = list(map(int, list(s)))
    # # print(len(s1))
    # # s1 = s * 10000
    # # sm = sum(s1)
    # # print(sm)
    # # part2 = part1(list(map(int, list(s1))))
    # repeat=1
    # #s =  "00000000000000000100"
    # s='10'.zfill(100)
    # _in = list(map(int, list(s))) * 1
    # print("input :", ' '.join(map(str, _in)))
    # part1_v2(_in, repeat)
    # s = "0000" +"0000" + "0100"
    # _in = list(map(int, list(s))) * 1
    # print("input :", ' '.join(map(str, _in)))
    # part1_v2(_in, repeat)
    # _in = list(map(int, list(s))) * 4
    # print("input :", ' '.join(map(str, _in)))
    # part1_v2(_in, repeat)
    # _in = list(map(int, list(s))) * 6
    # print("input :", ' '.join(map(str, _in)))
    # part1_v2(_in, repeat)
    # _in = list(map(int, list(s))) * 8
    # print("input :", ' '.join(map(str, _in)))
    # part1_v2(_in, repeat)
    # part2(_in, iter_count=1, repeat_count=3)
    # print(part1(_in, 1))
    # sg = SignalGenerator()
    # sg.n = 8
    pass
