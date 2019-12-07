from collections import deque

from helpers import read_raw_entries


class Node:
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.children = []


def count_links_to_com(nodes, starting_id):
    if nodes[starting_id] == "COM":
        return 1

    return 1 + count_links_to_com(nodes, nodes[starting_id])


def find_path_to_com(nodes, starting_id):
    if nodes[starting_id] == "COM":
        return [starting_id, "COM"]

    return [starting_id] + find_path_to_com(nodes, nodes[starting_id])


def part1(lines):
    nodes = parse_nodes(lines)

    total = 0
    for key in nodes.keys():
        total += count_links_to_com(nodes, key)
    return total


def parse_nodes(lines):
    nodes = {}
    for line in lines:
        parent, orbiter = line.split(")")
        nodes[orbiter] = parent
    return nodes


def part2_with_search(lines):
    relationships = parse_nodes(lines)
    nodes = {"COM": Node("COM")}

    for node in relationships.keys():
        nodes[node] = Node(node)
    for node in relationships.keys():
        nodes[node].parent = nodes[relationships[node]]
        nodes[node].parent.children.append(nodes[node])

    start = relationships["YOU"]
    dest = relationships["SAN"]

    open = deque()
    open.append(start)
    steps_needed = {start: 0}
    closed = set()

    iterations = 0
    while True:

        # print(f"Open: {len(open)}, Closed: {len(closed)}, Iterations: {iterations}")
        iterations += 1

        current = open.popleft()
        steps = steps_needed[current]

        closed.add(current)

        if current == dest:
            return steps

        current_node = nodes[current]

        if (
            current_node.parent
            and current_node.parent.id not in closed
            and current_node.parent.id not in open
        ):
            open.append(current_node.parent.id)
            steps_needed[current_node.parent.id] = steps + 1

        for child in current_node.children:
            if child.id not in closed and child.id not in open:
                open.append(child.id)
                steps_needed[child.id] = steps + 1


def part2_with_sets(lines):
    orbiter_to_parent_map = parse_nodes(lines)
    # We don't want to include YOU or SAN, so we're starting with each of their direct ancestors
    parents_of_you = find_path_to_com(
        orbiter_to_parent_map, orbiter_to_parent_map["YOU"]
    )
    parents_of_santa = find_path_to_com(
        orbiter_to_parent_map, orbiter_to_parent_map["SAN"]
    )

    shortest_path = len(set(parents_of_you).symmetric_difference(set(parents_of_santa)))
    return shortest_path


if __name__ == "__main__":
    raw_lines = read_raw_entries("input06.txt")
    part1 = part1(raw_lines)
    print(f"Part 1: {part1}")

    part2_search = part2_with_search(raw_lines)
    print(f"Part 2: {part2_search} (using search)")

    part2_sets = part2_with_sets(raw_lines)
    print(f"Part 2: {part2_sets} (using sets)")
