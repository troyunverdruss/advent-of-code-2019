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
        # print(l)
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

    # for e in reaction_steps.keys():
    #     print(f"{reaction_steps[e].reaction_in} => {reaction_steps[e].reaction_out}")
    # i = 0

    return reaction_steps, ore_producers


def part1(lines, fuel_count=None, leftover_pool=None):
    reaction_steps, ore_producers = parse_lines(lines)

    if leftover_pool is None and fuel_count is not None:
        raise Exception("Shouldn't have specified fuel count without providing reusable pool")

    # If we weren't passed one in, init it now
    if leftover_pool is None:
        leftover_pool = defaultdict(lambda: 0)

    if fuel_count is None:
        fuel_count = 1

    needed_inputs = find_inputs(
        reaction_steps, ore_producers, "FUEL", fuel_count, leftover_pool
    )

    print("leftover pool", leftover_pool)

    ore = 0
    unused_ore = 0
    for k in needed_inputs.keys():
        if leftover_pool[k] >= needed_inputs[k]:
            leftover_pool[k] -= needed_inputs[k]
            continue

        min_multiplier = needed_inputs[k] // ore_producers[k].reaction_out.quantity
        if min_multiplier * ore_producers[k].reaction_out.quantity < needed_inputs[k]:
            if min_multiplier * ore_producers[k].reaction_out.quantity + leftover_pool[k] >= needed_inputs[k]:
                # to_sub = quantity - (min_multiplier * reaction.reaction_out.quantity)
                # pool[reaction.reaction_out.element] -= to_sub
                pass
            else:
                min_multiplier += 1

        multiplier = min_multiplier
        # multiplier = 1
        # while (
        #         reaction.reaction_out.quantity * multiplier
        #         + pool[reaction.reaction_out.element]
        #         < quantity
        # ):
        #     multiplier += 1
        #
        # print(f"min_multiplier: {min_multiplier}, expected: {multiplier}")
        #
        # # take out of the pool as much as necessary
        to_create = ore_producers[k].reaction_out.quantity * multiplier
        if to_create > needed_inputs[k]:
            leftover_pool[ore_producers[k].reaction_out.element] += to_create - needed_inputs[k]
        else:
            to_sub = needed_inputs[k] - to_create
            leftover_pool[ore_producers[k].reaction_out.element] -= to_sub




        # multiplier = int(math.ceil(float(needed_inputs[k] / ore_producers[k].reaction_out.quantity)))
        # multiplier = 1
        # while ore_producers[k].reaction_out.quantity * multiplier < needed_inputs[k]:
        #     multiplier += 1
        # multiplier = int(math.ceil(float(needed_inputs[k])/float(ore_producers[k].reaction_in[0].quantity)))

        ore += multiplier * ore_producers[k].reaction_in[0].quantity
        leftover = (multiplier * ore_producers[k].reaction_out.quantity) - needed_inputs[k]
        leftover_pool[k] += leftover

    print(ore)
    return ore, unused_ore
    # 16302 too low
    # 201606 too low
    # 4867716 too high
    # 2486514


def part2(lines):
    trillion = 1_000_000_000_000
    approx_ore_per_one_fuel = part1(lines)[0]

    ore_remaining = trillion
    count = 0
    leftover_pool = defaultdict(lambda: 0)

    while ore_remaining // approx_ore_per_one_fuel > 100:
        fuel_to_create = ore_remaining // approx_ore_per_one_fuel
        ore_used, unused_ore = part1(lines, fuel_to_create, leftover_pool)
        if ore_used > ore_remaining:
            raise Exception()
        ore_remaining -= ore_used
        ore_remaining += unused_ore
        count += fuel_to_create

    while ore_remaining > 0:
        print(f"remaining: {ore_remaining}")
        _used, _unused = part1(lines, 1, leftover_pool)
        if _used > ore_remaining:
            break
        else:
            ore_remaining -= _used
            ore_remaining += _unused
            count += 1

    print(count)
    return count


def find_inputs_2(
        reaction_steps: Dict[str, ReactionStep],
        ore_producers: Dict[str, ReactionStep],
        required_element: str,
        quantity: int,
        pool: Dict[str, int],
        indent=0,
):
    if required_element in ore_producers:
        total_produced = math.ceil(float(quantity / ore_producers[required_element].reaction_out.quantity))
        extra = total_produced - quantity
        pool[required_element] += extra
        return {required_element: quantity}

    if required_element == "ORE":
        raise Exception("require ORE, mistake?")

    if pool[required_element] >= quantity:
        pool[required_element] -= quantity
        return {}


def find_inputs(
        reaction_steps: Dict[str, ReactionStep],
        ore_producers: Dict[str, ReactionStep],
        required_element: str,
        quantity: int,
        pool: Dict[str, int],
        indent=0,
):
    # print(f"{'  ' * indent}Seeking {quantity} of element: {required_element}")
    # base case is ORE?
    # base case is maybe elements that can be created directly from ORE?
    if required_element in ore_producers:
        # print(
        #     f"{'  ' * indent}Required element is produced from ORE {required_element}: {quantity}"
        # )
        return {required_element: quantity}

    if required_element == "ORE":
        # print(f"{'  ' * indent}Required element is ORE")
        raise Exception()
        return {}

    if pool[required_element] >= quantity:
        pool[required_element] -= quantity
        return {}

    # This will be a running tally
    required_in = defaultdict(lambda: 0)

    reaction = reaction_steps[required_element]

    # multiplier = int(math.ceil(float(reaction.reaction_out.quantity)/float(quantity)))
    min_multiplier = quantity // reaction.reaction_out.quantity
    if min_multiplier * reaction.reaction_out.quantity < quantity:
        if min_multiplier * reaction.reaction_out.quantity + pool[reaction.reaction_out.element] >= quantity:
            # to_sub = quantity - (min_multiplier * reaction.reaction_out.quantity)
            # pool[reaction.reaction_out.element] -= to_sub
            pass
        else:
            min_multiplier += 1

    multiplier = min_multiplier
    # multiplier = 1
    # while (
    #         reaction.reaction_out.quantity * multiplier
    #         + pool[reaction.reaction_out.element]
    #         < quantity
    # ):
    #     multiplier += 1
    #
    # print(f"min_multiplier: {min_multiplier}, expected: {multiplier}")
    #
    # # take out of the pool as much as necessary
    to_create = reaction.reaction_out.quantity * multiplier
    if to_create > quantity:
        pool[reaction.reaction_out.element] += to_create - quantity
    else:
        to_sub = quantity - to_create
        pool[reaction.reaction_out.element] -= to_sub

    # new_val = quantity - (reaction.reaction_out.quantity * multiplier + pool[reaction.reaction_out.element])
    # new_val = max(new_val, 0)
    # pool[reaction.reaction_out.element] = new_val

    # deduct from the pool
    # print("pool:")
    # for e in filter(lambda e: e[1] != 0, pool.items()):
    #     print(e)

    for el_in in reaction.reaction_in:
        # 1 in the pool
        # i need 9
        #

        # amount_needed = quantity - (multiplier * el_in.quantity + pool[el_in.element])

        found_required = find_inputs(
            reaction_steps,
            ore_producers,
            el_in.element,
            multiplier * el_in.quantity,
            pool,
            indent + 1,
        )
        for k in found_required:
            # print(f"{'  ' * indent}Will be provided by {found_required[k]} {k}")
            required_in[k] += found_required[k]

    # print(f"required in: {required_in}")
    # print(f"pool: {pool}")
    return required_in


if __name__ == "__main__":
    _lines = read_raw_entries("input14.txt")
    part1(_lines)
    part2(_lines)
    # too high 1001464936982691503
    pass
