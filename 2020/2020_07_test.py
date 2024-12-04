from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 7: Handy Haversacks ---
    You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to
    grab some food: all flights are currently delayed due to issues in luggage processing.

    Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their
    contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently,
    nobody responsible for these regulations considered how long they would take to enforce!

    For example, consider the following rules:

    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    faded blue bags contain no other bags.
    dotted black bags contain no other bags.

    These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty,
    every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

    You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors
    would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least
    one shiny gold bag?)

    In the above rules, the following options would be available to you:

    - A bright white bag, which can hold your shiny gold bag directly.
    - A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
    - A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold
      your shiny gold bag.
    - A light red bag, which can hold bright white and muted yellow bags, either of which could then hold
      your shiny gold bag.

    So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

    How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make
    sure you get all of it.)

    --- Part Two ---
    It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous
    number of bags you need to buy!

    Consider again your shiny gold bag and the rules from the above example:

    faded blue bags contain 0 other bags.
    dotted black bags contain 0 other bags.
    vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
    dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

    So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it)
    plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

    Of course, the actual rules have a small chance of going several levels deeper than this example;
    be sure to count all of the bags, even if the nesting becomes topologically impractical!

    Here's another example:

    shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.
    dark yellow bags contain 2 dark green bags.
    dark green bags contain 2 dark blue bags.
    dark blue bags contain 2 dark violet bags.
    dark violet bags contain no other bags.

    In this example, a single shiny gold bag must contain 126 other bags.

    How many individual bags are required inside your single shiny gold bag?
    """

    pass


SAMPLE = [
    "light red bags contain 1 bright white bag, 2 muted yellow bags.",
    "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
    "bright white bags contain 1 shiny gold bag.",
    "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
    "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
    "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
    "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
    "faded blue bags contain no other bags.",
    "dotted black bags contain no other bags.",
]

SAMPLE2 = [
    "shiny gold bags contain 2 dark red bags.",
    "dark red bags contain 2 dark orange bags.",
    "dark orange bags contain 2 dark yellow bags.",
    "dark yellow bags contain 2 dark green bags.",
    "dark green bags contain 2 dark blue bags.",
    "dark blue bags contain 2 dark violet bags.",
    "dark violet bags contain no other bags.",
]

with open(Path(__file__).parent / "2020_07_input.txt") as f:
    INPUT = [line.strip() for line in f]


def split_line(line):
    line = line.strip(".").replace("bags", "bag").replace(" bag", "")
    outer_bag, inner_bags = line.split(" contain ")
    outer_bag = outer_bag
    inner_bags = inner_bags.split(", ")
    return outer_bag, {
        " ".join(c.split(" ")[1:]): int(c.split(" ")[0])
        for c in inner_bags
        if c.split(" ")[0] != "no"
    }


def test_split_line():
    assert split_line(SAMPLE[0]) == (
        "light red",
        {"bright white": 1, "muted yellow": 2},
    )
    assert split_line(SAMPLE[-1]) == ("dotted black", {})


def build_bag_graph(lines):
    bag_contains_graph = {}
    bag_inside_graph = defaultdict(set)
    for line in lines:
        outer, connections = split_line(line)
        bag_contains_graph[outer] = connections
        for bag in connections:
            bag_inside_graph[bag].add(outer)
    return bag_contains_graph, bag_inside_graph


def test_build_bag_graph():
    RESULT_CONTAINS, RESULT_INSIDE = build_bag_graph(SAMPLE)
    assert RESULT_CONTAINS["light red"] == {"bright white": 1, "muted yellow": 2}
    assert RESULT_CONTAINS["dotted black"] == {}
    assert RESULT_INSIDE["shiny gold"] == set(["bright white", "muted yellow"])
    assert RESULT_INSIDE["other"] == set(["faded blue", "dotted black"])


def find_over_bags(bag_inside_graph, starting_color):
    current_bag_list = set([starting_color])
    next_bag_list = set()
    possible_bags = set()
    while len(current_bag_list) > 0:
        for bag in current_bag_list:
            new_bags = bag_inside_graph[bag]
            for new_bag in new_bags:
                next_bag_list.add(new_bag)
                possible_bags.add(new_bag)
        current_bag_list = next_bag_list
        next_bag_list = set()
    return possible_bags


def test_find_over_bags():
    _, bag_inside = build_bag_graph(SAMPLE)
    RESULT = find_over_bags(bag_inside, "shiny gold")
    assert len(RESULT) == 4
    _, bag_inside = build_bag_graph(INPUT)
    RESULT = find_over_bags(bag_inside, "shiny gold")
    assert len(RESULT) == 144


def find_total_inner_bags(bag_contains_graph, starting_color):
    current_bag_list = {starting_color: 1}
    next_bag_list = defaultdict(int)
    count = 0
    while len(current_bag_list) > 0:
        for bag in current_bag_list:
            # print(f'{current_bag_list[bag]} {bag} bag contains {bag_contains_graph[bag]}')
            bag_multiplier = current_bag_list[bag]
            new_bags = bag_contains_graph[bag]
            for new_bag in new_bags:
                next_bag_list[new_bag] += bag_multiplier * new_bags[new_bag]
                count += bag_multiplier * new_bags[new_bag]
        current_bag_list = next_bag_list
        next_bag_list = defaultdict(int)
    return count


def test_find_total_inner_bags():
    assert len(INPUT) == 594
    bag_contains, _ = build_bag_graph(SAMPLE)
    assert find_total_inner_bags(bag_contains, "shiny gold") == 32
    bag_contains, _ = build_bag_graph(SAMPLE2)
    assert find_total_inner_bags(bag_contains, "shiny gold") == 126
    bag_contains, _ = build_bag_graph(INPUT)
    assert (
        find_total_inner_bags(bag_contains, "shiny gold") == 5956
    )  # too low 1906, 1907
