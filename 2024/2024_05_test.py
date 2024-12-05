from pathlib import Path
from typing import List, NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 5: Print Queue ---

    Satisfied with their search on Ceres, the squadron of scholars suggests
    subsequently scanning the stationery stacks of sub-basement 17.

    The North Pole printing department is busier than ever this close to
    Christmas, and while The Historians continue their search of this
    historically significant facility, an Elf operating a very familiar printer
    beckons you over.

    The Elf must recognize you, because they waste no time explaining that the
    new sleigh launch safety manual updates won't print correctly. Failure to
    update the safety manuals would be dire indeed, so you offer your services.

    Safety protocols clearly indicate that new pages for the safety manuals must
    be printed in a very specific order. The notation X|Y means that if both
    page number X and page number Y are to be produced as part of an update,
    page number X must be printed at some point before page number Y.

    The Elf has for you both the page ordering rules and the pages to produce in
    each update (your puzzle input), but can't figure out whether each update
    has the pages in the right order.

    For example:

    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47

    The first section specifies the page ordering rules, one per line. The first
    rule, 47|53, means that if an update includes both page number 47 and page
    number 53, then page number 47 must be printed at some point before page
    number 53. (47 doesn't necessarily need to be immediately before 53; other
    pages are allowed to be between them.)

    The second section specifies the page numbers of each update. Because most
    safety manuals are different, the pages needed in the updates are different
    too. The first update, 75,47,61,53,29, means that the update consists of
    page numbers 75, 47, 61, 53, and 29.

    To get the printers going as soon as possible, start by identifying which
    updates are already in the right order.

    In the above example, the first update (75,47,61,53,29) is in the right
    order:

    75 is correctly first because there are rules that put each other page after
    it: 75|47, 75|61, 75|53, and 75|29.

    47 is correctly second because 75 must be before it (75|47) and every other
    page must be after it according to 47|61, 47|53, and 47|29.

    61 is correctly in the middle because 75 and 47 are before it (75|61 and
    47|61) and 53 and 29 are after it (61|53 and 61|29).

    53 is correctly fourth because it is before page number 29 (53|29).

    29 is the only page left and so is correctly last.

    Because the first update does not include some page numbers, the ordering
    rules involving those missing page numbers are ignored.

    The second and third updates are also in the correct order according to the
    rules. Like the first update, they also do not include every page number,
    and so only some of the ordering rules apply - within each update, the
    ordering rules that involve missing page numbers are not used.

    The fourth update, 75,97,47,61,53, is not in the correct order: it would
    print 75 before 97, which violates the rule 97|75.

    The fifth update, 61,13,29, is also not in the correct order, since it
    breaks the rule 29|13.

    The last update, 97,13,75,29,47, is not in the correct order due to breaking
    several rules.

    For some reason, the Elves also need to know the middle page number of each
    update being printed. Because you are currently only printing the
    correctly-ordered updates, you will need to find the middle page number of
    each correctly-ordered update. In the above example, the correctly-ordered
    updates are:

    75,47,61,53,29
    97,61,53,29,13
    75,29,13

    These have middle page numbers of 61, 53, and 29 respectively. Adding these
    page numbers together gives 143.

    Of course, you'll need to be careful: the actual list of page ordering rules
    is bigger and more complicated than the above example.

    Determine which updates are already in the correct order. What do you get if
    you add up the middle page number from those correctly-ordered updates?

    Your puzzle answer was 5713.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---

    While the Elves get to work printing the correctly-ordered updates, you have
    a little time to fix the rest of them.

    For each of the incorrectly-ordered updates, use the page ordering rules to
    put the page numbers in the right order. For the above example, here are the
    three incorrectly-ordered updates and their correct orderings:

    75,97,47,61,53 becomes 97,75,47,61,53.
    61,13,29 becomes 61,29,13.
    97,13,75,29,47 becomes 97,75,47,29,13.

    After taking only the incorrectly-ordered updates and ordering them
    correctly, their middle page numbers are 47, 29, and 47. Adding these
    together produces 123.

    Find the updates which are not in the correct order. What do you get if you
    add up the middle page numbers after correctly ordering just those updates?

    Your puzzle answer was 5180.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


with open(Path(__file__).parent / "2024_05_input.txt") as fp:
    RAW_RULES, RAW_UPDATE = fp.read().split("\n\n")

SAMPLE_RULES = [
    "47|53",
    "97|13",
    "97|61",
    "97|47",
    "75|29",
    "61|13",
    "75|53",
    "29|13",
    "97|29",
    "53|29",
    "61|53",
    "97|53",
    "61|29",
    "47|13",
    "75|47",
    "97|75",
    "47|61",
    "75|61",
    "47|29",
    "75|13",
    "53|13",
]

SAMPLE_UPDATES = [
    [75, 47, 61, 53, 29],
    [97, 61, 53, 29, 13],
    [75, 29, 13],
    [75, 97, 47, 61, 53],
    [61, 13, 29],
    [97, 13, 75, 29, 47],
]


def parse_rules(raw_rules):
    pages_before = defaultdict(set)
    pages_after = defaultdict(set)
    if "\n" in raw_rules:
        raw_rules = raw_rules.split("\n")

    for pair in raw_rules:
        first, last = [int(digit) for digit in pair.split("|")]
        pages_before[last].add(first)
        pages_after[first].add(last)

    return dict(pages_before), dict(pages_after)


def test_parse_rules():
    assert parse_rules(SAMPLE_RULES) == (
        {
            53: {97, 75, 61, 47},
            13: {97, 75, 47, 61, 53, 29},
            61: {97, 75, 47},
            47: {97, 75},
            29: {97, 75, 47, 53, 61},
            75: {97},
        },
        {
            47: {29, 13, 61, 53},
            97: {75, 13, 47, 61, 53, 29},
            75: {13, 47, 29, 53, 61},
            61: {29, 53, 13},
            29: {13},
            53: {13, 29},
        },
    )

    # Random observation - but I think it is only an artifact of how
    # the dataset was generated and not provable - the sum of pages
    # before and pages after plus one equals total number of pages.
    # I think this is because a random ordering of pages is generated
    # and then all comparison pairs are generated for the "rules"

    my_pages_before, my_pages_after = parse_rules(RAW_RULES.split("\n"))
    lengths = set()
    for page in my_pages_before:
        lengths.add(len(my_pages_before[page]) + len(my_pages_after[page]))
    assert len(lengths) == 1
    assert lengths == set([48])


def update_is_valid(update, pages_after):
    previous = set()
    for page in update:
        if page in pages_after:
            for potential_violation in pages_after[page]:
                if potential_violation in previous:
                    return False
        previous.add(page)
    return True


def test_update_is_valid():
    _, pages_after = parse_rules(SAMPLE_RULES)
    update_is_valid(SAMPLE_UPDATES[0], pages_after) == True
    update_is_valid(SAMPLE_UPDATES[1], pages_after) == True
    update_is_valid(SAMPLE_UPDATES[2], pages_after) == True
    update_is_valid(SAMPLE_UPDATES[3], pages_after) == False
    update_is_valid(SAMPLE_UPDATES[4], pages_after) == False
    update_is_valid(SAMPLE_UPDATES[5], pages_after) == False


def score_updates(updates, pages_after):
    score = 0
    for update in updates:
        if update_is_valid(update, pages_after):
            center = len(update) // 2
            center_page = update[center]
            score += center_page
    return score


def test_score_updates():
    _, pages_after = parse_rules(SAMPLE_RULES)
    assert score_updates([SAMPLE_UPDATES[0]], pages_after) == SAMPLE_UPDATES[0][2]
    assert score_updates([SAMPLE_UPDATES[1]], pages_after) == SAMPLE_UPDATES[1][2]
    assert score_updates([SAMPLE_UPDATES[2]], pages_after) == SAMPLE_UPDATES[2][1]
    assert score_updates(SAMPLE_UPDATES, pages_after) == 143

    _, my_pages_after = parse_rules(RAW_RULES.split("\n"))
    my_updates = [
        [int(page) for page in update.split(",")] for update in RAW_UPDATE.split("\n")
    ]
    assert score_updates(my_updates, my_pages_after) == 5713
    # First answer was 11886 which was too high
    # -- oops found issue, forgot to parse the raw_rules


def fix_invalid_update(update, pages_before, pages_after):
    yet_to_place = set(update)
    last_first = []

    while yet_to_place:
        can_add = yet_to_place - {
            k for k, val in pages_after.items() if val & yet_to_place
        }
        match len(can_add):
            case 1:
                page_to_add = can_add.pop()
                last_first.append(page_to_add)
                yet_to_place.remove(page_to_add)
            case 0:
                raise Exception("Nothing can go at the end")
            case _:
                raise Exception("Ambiguous ordering")
    last_first.reverse()
    return last_first


def test_fix_invalid_update():
    pages_before, pages_after = parse_rules(SAMPLE_RULES)
    unordereds = [[75, 97, 47, 61, 53], [61, 13, 29], [97, 13, 75, 29, 47]]
    ordereds = [[97, 75, 47, 61, 53], [61, 29, 13], [97, 75, 47, 29, 13]]
    for unordered, ordered in zip(unordereds, ordereds):
        assert fix_invalid_update(unordered, pages_before, pages_after) == ordered


def fix_invalid_updates(updates, pages_before, pages_after):
    fixed_updates = []
    for update in updates:
        if update_is_valid(update, pages_after):
            continue
        fixed_updates.append(fix_invalid_update(update, pages_before, pages_after))
    return score_updates(fixed_updates, pages_after)


def test_fix_invalid_updates():
    pages_before, pages_after = parse_rules(SAMPLE_RULES)
    assert fix_invalid_updates(SAMPLE_UPDATES, pages_before, pages_after) == 123

    my_pages_before, my_pages_after = parse_rules(RAW_RULES.split("\n"))
    my_updates = [
        [int(page) for page in update.split(",")] for update in RAW_UPDATE.split("\n")
    ]
    assert fix_invalid_updates(my_updates, my_pages_before, my_pages_after) == 5180
