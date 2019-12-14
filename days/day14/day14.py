import math
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict
from helpers import read_raw_entries


@dataclass
class ReactionElement:
    quantity: int
    element: str

    def __hash__(self):
        return hash(str(self))


@dataclass
class ReactionStep:
    reaction_out: ReactionElement
    reaction_in: List[ReactionElement]


def parse_lines(_lines):
    # indexed on element string, is list of options
    elements = defaultdict(lambda: [])
    # indexed on thing you get, values are things you need
    reaction_steps = {}
    ore_producers = {}

    for l in _lines:
        print(l)
        inputs, outputs = l.split(" => ")

        needed_in = []
        for _in in inputs.split(","):
            q, e = _in.lstrip().rstrip().split(" ")

            in_el = ReactionElement(int(q), e)
            elements[e].append(in_el)
            needed_in.append(in_el)

        q, e = outputs.split(" ")
        out_el = ReactionElement(int(q), e)
        elements[e].append(out_el)

        if out_el.element in reaction_steps:
            raise Exception("blarg, repeat key", out_el)

        reaction_step = ReactionStep(out_el, needed_in)
        reaction_steps[out_el.element] = reaction_step

        if len(needed_in) == 1 and "ORE" == needed_in[0].element:
            ore_producers[out_el.element] = reaction_step

    for e in reaction_steps.keys():
        print(f"{reaction_steps[e].reaction_in} => {reaction_steps[e].reaction_out}")
    i = 0

    return reaction_steps, ore_producers


def part1(lines):
    reaction_steps, ore_producers = parse_lines(lines)
    needed_inputs = find_inputs(reaction_steps, ore_producers, "FUEL", 1)

    print(needed_inputs)

    ore = 0
    for k in needed_inputs.keys():
        multiplier = 1
        while ore_producers[k].reaction_out.quantity * multiplier < needed_inputs[k] :
            multiplier += 1
        # multiplier = int(math.ceil(float(needed_inputs[k])/float(ore_producers[k].reaction_in[0].quantity)))

        ore += multiplier * ore_producers[k].reaction_in[0].quantity

    print(ore)
    return ore
    # 16302 too low
    # 201606 too low
    # 4867716 too high



def find_inputs(reaction_steps: Dict[str, ReactionStep], ore_producers: Dict[str, ReactionStep], required_element: str,
                quantity: int, indent=0):
    print(f"{'  '* indent}Seeking {quantity} of element: {required_element}")
    # base case is ORE?
    # base case is maybe elements that can be created directly from ORE?
    if required_element in ore_producers:
        print(f"{'  '* indent}Required element is produced from ORE {required_element}: {quantity}")
        return {required_element: quantity}

    if required_element == "ORE":
        print(f"{'  '* indent}Required element is ORE")
        return {}

    # This will be a running tally
    required_in = defaultdict(lambda: 0)

    reaction = reaction_steps[required_element]

    # multiplier = int(math.ceil(float(reaction.reaction_out.quantity)/float(quantity)))

    multiplier = 1
    while reaction.reaction_out.quantity * multiplier < quantity:
        multiplier += 1


    for el_in in reaction.reaction_in:
        found_required = find_inputs(reaction_steps, ore_producers, el_in.element, multiplier * el_in.quantity, indent + 1)
        for k in found_required:
            print(f"{'  '* indent}Will be provided by {found_required[k]} {k}")
            required_in[k] += found_required[k]

    return required_in


if __name__ == "__main__":
    _lines = read_raw_entries("input14.txt")
    part1(_lines)
    pass
