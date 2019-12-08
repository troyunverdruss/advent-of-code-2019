from collections import Counter


def valid_part1(digits):
    return sorted(digits) == digits and len(set(digits)) != len(digits)


def valid_part2(digits):
    return sorted(digits) == digits and 2 in Counter(digits).values()


def convert_num_to_digits(_digits):
    return list(map(int, list(str(_digits))))


def part1(low, high):
    possibles = 0
    for maybe in range(low, high + 1):
        if valid_part1(convert_num_to_digits(maybe)):
            possibles += 1
    return possibles


def part2(low, high):
    possibles = 0
    for maybe in range(low, high + 1):
        if valid_part2(convert_num_to_digits(maybe)):
            possibles += 1
    return possibles


def parse_input(input_str):
    return map(int, input_str.replace(" ", "").split("-"))


if __name__ == "__main__":
    _low, _high = parse_input("264360 - 746325")

    print(part1(_low, _high))
    print(part2(_low, _high))
