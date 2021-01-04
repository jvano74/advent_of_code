from collections import defaultdict


class Puzzle:
    """
    --- Day 12: Digital Plumber ---
    Walking along the memory banks of the stream, you find a small village that is experiencing a little confusion:
    some programs can't communicate with each other.

    Programs in this village communicate using a fixed system of pipes. Messages are passed between programs using
    these pipes, but most programs aren't connected to each other directly. Instead, programs pass messages between
    each other until the message reaches the intended recipient.

    For some reason, though, some of these messages aren't ever reaching their intended recipient, and the programs
    suspect that some pipes are missing. They would like you to investigate.

    You walk through the village and record the ID of each program and the IDs with which it can communicate directly
    (your puzzle input). Each program has one or more programs with which it can communicate, and these pipes are
    bidirectional; if 8 says it can communicate with 11, then 11 will say it can communicate with 8.

    You need to figure out how many programs are in the group that contains program ID 0.

    For example, suppose you go door-to-door like a travelling salesman and record the following list:

    0 <-> 2
    1 <-> 1
    2 <-> 0, 3, 4
    3 <-> 2, 4
    4 <-> 2, 3, 6
    5 <-> 6
    6 <-> 4, 5

    In this example, the following programs are in the group that contains program ID 0:

    Program 0 by definition.
    Program 2, directly connected to program 0.
    Program 3 via program 2.
    Program 4 via program 2.
    Program 5 via programs 6, then 4, then 2.
    Program 6 via programs 4, then 2.
    Therefore, a total of 6 programs are in this group; all but program 1, which has a pipe that connects it to itself.

    How many programs are in the group that contains program ID 0?

    --- Part Two ---
    There are more programs than just the ones in the group containing program ID 0. The rest of them have no way of
    reaching that group, and still might have no way of reaching each other.

    A group is a collection of programs that can all communicate via pipes either directly or indirectly. The programs
    you identified just a moment ago are all part of the same group. Now, they would like you to determine the total
    number of groups.

    In the example above, there were 2 groups: one consisting of programs 0,2,3,4,5,6, and the other consisting
    solely of program 1.

    How many groups are there in total?
    """
    pass


SAMPLE = ['0 <-> 2', '1 <-> 1', '2 <-> 0, 3, 4', '3 <-> 2, 4',
          '4 <-> 2, 3, 6', '5 <-> 6', '6 <-> 4, 5']


with open('day_12_input.txt') as fp:
    INPUTS = [line.strip() for line in fp]


def parse_input(raw_data):
    graph = defaultdict(set)
    for raw_line in raw_data:
        program, raw_dest = raw_line.split(' <-> ')
        graph[int(program)] = set(int(p) for p in raw_dest.split(', '))
    return graph


def get_component(graph, node):
    to_check = set()
    elements = {node}
    to_check = to_check.union(graph[node])
    while len(to_check) > 0:
        current_node = to_check.pop()
        elements.add(current_node)
        for test_node in graph[current_node]:
            if test_node not in elements:
                elements.add(test_node)
                to_check = to_check.union(graph[test_node])
    return elements


def get_groups(graph):
    groups = set()
    all_elements = {k for k in graph}
    while len(all_elements) > 0:
        next_node = all_elements.pop()
        component = get_component(graph, next_node)
        groups.add(frozenset(component))
        all_elements = all_elements - component
    return groups


def test_sample():
    sample_graph = parse_input(SAMPLE)
    assert sample_graph == {0: {2}, 1: {1}, 2: {0, 3, 4}, 3: {2, 4}, 4: {2, 3, 6}, 5: {6}, 6: {4, 5}}
    assert get_component(sample_graph, 0) == {0, 2, 3, 4, 5, 6}
    assert get_groups(sample_graph) == {frozenset({1}), frozenset({0, 2, 3, 4, 5, 6})}


def test_puzzle():
    puzzle_graph = parse_input(INPUTS)
    assert len(get_component(puzzle_graph, 0)) == 288
    assert len(get_groups(puzzle_graph)) == 211
