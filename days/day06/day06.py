from collections import deque
from typing import List, Dict

from helpers import read_raw_entries


# For use with the search-based approach
class Node:
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.children = []


# Simple recursive function to count links from
# any node to "COM"
def count_links_to_com(nodes, starting_id):
    if nodes[starting_id] == "COM":
        return 1

    return 1 + count_links_to_com(nodes, nodes[starting_id])


# Simple recursive function to create a full list
# of all the links from start to "COM"
def find_path_to_com(nodes, starting_id):
    if nodes[starting_id] == "COM":
        return [starting_id, "COM"]

    return [starting_id] + find_path_to_com(nodes, nodes[starting_id])


# Compute the total of all the links
def part1(lines):
    nodes = parse_nodes(lines)

    total = 0
    for key in nodes.keys():
        total += count_links_to_com(nodes, key)
    return total


# Parse the input data into a relationship map
def parse_nodes(lines: List[str]) -> Dict[str, str]:
    # Relationship map. Parent => Child that orbits parent
    relationship_map = {}
    for line in lines:
        parent, orbiter = line.split(")")
        relationship_map[orbiter] = parent

    return relationship_map


# This turns out to be a terribly inefficient way of getting
# this solution, but it *does* work. Basically do a BFS from
# YOU to SAN, pruning away possibilities as we go.
# Note: since this is a proper tree, with no weird or bad
# directed links, using sets (as below) is much faster and simpler.
def part2_with_search(lines):
    relationship_map = parse_nodes(lines)
    nodes = {"COM": Node("COM")}

    # Build up a list of all the Node objects
    for node in relationship_map.keys():
        nodes[node] = Node(node)
    # Then link them all up so they know their parents
    # and children
    for node in relationship_map.keys():
        nodes[node].parent = nodes[relationship_map[node]]
        nodes[node].parent.children.append(nodes[node])

    # We're starting at the node that YOU is orbiting
    start = relationship_map["YOU"]
    # and ending at the node that SAN is orbiting
    dest = relationship_map["SAN"]

    # queue will track points we need to search
    # and closed will track points we've visited
    queue = deque()
    closed = set()

    # Seed it with the start
    queue.append(start)
    # Use this map to track how many steps each place
    # we've visited took to get there
    steps_needed = {start: 0}

    iterations = 0
    while True:

        # print(f"Open: {len(open)}, Closed: {len(closed)}, Iterations: {iterations}")
        iterations += 1

        # Get the next place to search from
        current = queue.popleft()
        # Update the steps map for this node
        steps = steps_needed[current]

        # Move it to closed, now that we're looking at it
        closed.add(current)

        # Did we get there?
        if current == dest:
            return steps

        # Get the actual node object
        current_node = nodes[current]

        # If we have a parent and the parent hasn't been searched
        # and isn't scheduled for search already, queue it up
        if (
                current_node.parent
                and current_node.parent.id not in closed
                and current_node.parent.id not in queue
        ):
            queue.append(current_node.parent.id)
            steps_needed[current_node.parent.id] = steps + 1

        # For each child node, do the same check and queue it up
        # if it hasn't been seen before
        for child in current_node.children:
            if child.id not in closed and child.id not in queue:
                queue.append(child.id)
                steps_needed[child.id] = steps + 1


# Here's the much simpler approach ... get the full list of
# nodes between YOU and COM, then from SAN to COM, cast them
# to sets, and do a symmetric difference to find all the nodes
# that are not shared. This is the path from YOU to some shared
# parent, and from SAN to the same shared parent. Nodes in this
# set are the same number of steps needed. Tada!
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
