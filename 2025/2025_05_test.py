from pathlib import Path
from typing import List


class Puzzle:
    """
    --- Day 5: Cafeteria ---
    As the forklifts break through the wall, the Elves are delighted to discover
    that there was a cafeteria on the other side after all.

    You can hear a commotion coming from the kitchen. "At this rate, we won't
    have any time left to put the wreaths up in the dining hall!" Resolute in
    your quest, you investigate.

    "If only we hadn't switched to the new inventory management system right
    before Christmas!" another Elf exclaims. You ask what's going on.

    The Elves in the kitchen explain the situation: because of their complicated
    new inventory management system, they can't figure out which of their
    ingredients are fresh and which are spoiled. When you ask how it works, they
    give you a copy of their database (your puzzle input).

    The database operates on ingredient IDs. It consists of a list of fresh
    ingredient ID ranges, a blank line, and a list of available ingredient IDs.
    For example:

    3-5
    10-14
    16-20
    12-18

    1
    5
    8
    11
    17
    32

    The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs
    3, 4, and 5 are all fresh. The ranges can also overlap; an ingredient ID is
    fresh if it is in any range.

    The Elves are trying to determine which of the available ingredient IDs are
    fresh. In this example, this is done as follows:

    Ingredient ID 1 is spoiled because it does not fall into any range.
    Ingredient ID 5 is fresh because it falls into range 3-5.
    Ingredient ID 8 is spoiled.
    Ingredient ID 11 is fresh because it falls into range 10-14.
    Ingredient ID 17 is fresh because it falls into range 16-20 as well as range 12-18.
    Ingredient ID 32 is spoiled.

    So, in this example, 3 of the available ingredient IDs are fresh.

    Process the database file from the new inventory management system. How many
    of the available ingredient IDs are fresh?

    Your puzzle answer was 758.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The Elves start bringing their spoiled inventory to the trash chute at the
    back of the kitchen.

    So that they can stop bugging you when they get new inventory, the Elves
    would like to know all of the IDs that the fresh ingredient ID ranges
    consider to be fresh. An ingredient ID is still considered fresh if it is in
    any range.

    Now, the second section of the database (the available ingredient IDs) is
    irrelevant. Here are the fresh ingredient ID ranges from the above example:

    3-5
    10-14
    16-20
    12-18

    The ingredient IDs that these ranges consider to be fresh are 3, 4, 5, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19, and 20. So, in this example, the fresh
    ingredient ID ranges consider a total of 14 ingredient IDs to be fresh.

    Process the database file again. How many ingredient IDs are considered to
    be fresh according to the fresh ingredient ID ranges?

    Your puzzle answer was 343143696885053.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open(Path(__file__).parent / "2025_05_input.txt") as fp:
    MY_RANGES, MY_IDS = (pc.split("\n") for pc in fp.read().split("\n\n"))

SAMPLE_RANGES = ["3-5", "10-14", "16-20", "12-18"]
SAMPLE_IDS = [1, 5, 8, 11, 17, 32]


class Inventory:
    def __init__(self, raw_ranges: List[str]):
        self.ranges = []
        self.clean_ranges = []
        potential_ends = set()
        for raw_range in raw_ranges:
            low, high = (int(d) for d in raw_range.split("-"))
            potential_ends.add(low)
            potential_ends.add(high)
            self.ranges.append(range(low, high + 1))
        grab_bag = sorted(potential_ends)
        while grab_bag:
            a = grab_bag.pop(0)
            b = grab_bag.pop(0)
            while self.fresh(b + 1):
                b = grab_bag.pop(0)
            self.clean_ranges.append((a, b))

    def fresh(self, item: int) -> bool:
        for range in self.ranges:
            if item in range:
                return True
        return False

    def count_ranges(self) -> int:
        return sum(max - min + 1 for (min, max) in self.clean_ranges)


# Turns out the BetterInventory wasn't better - it was too complex and
# the above simpler approach was better and much faster.
#
# class BetterInventory:
#     def __init__(self, raw_ranges: List[str]):
#         existing_ranges = []
#         for raw_range in raw_ranges:
#             low, high = (int(d) for d in raw_range.split("-"))
#             new_ranges = []
#             while existing_ranges:
#                 (e_low, e_high) = existing_ranges.pop(0)
#                 if e_high < low:
#                     new_ranges.append((e_low, e_high))
#                     continue
#                 if high < e_low:
#                     new_ranges.append((low, high))
#                     new_ranges.append((e_low, e_high))
#                     continue
#                     # new_ranges.extend(existing_ranges)
#                     # break
#                 # new_ranges.append((min(low, e_low), max(high, e_high)))
#                 low, high = (min(low, e_low), max(high, e_high))
#             else:
#                 new_ranges.append((low, high))
#             existing_ranges = new_ranges
#         self.ranges = existing_ranges
#
#     def count_ranges(self) -> int:
#         return sum(max - min + 1 for (min, max) in self.ranges)


def test_freshness():
    sample = Inventory(SAMPLE_RANGES)
    assert sum(1 for id in SAMPLE_IDS if sample.fresh(id)) == 3
    assert sample.count_ranges() == 14

    my_ranges = Inventory(MY_RANGES)
    assert sum(1 for id in MY_IDS if id != "" and my_ranges.fresh(int(id))) == 758
    assert my_ranges.count_ranges() == 343143696885053


# def test_count_ranges():
#     sample = BetterInventory(SAMPLE_RANGES)
#     assert sample.count_ranges() == 14
#     my_ranges = BetterInventory(MY_RANGES)
#     assert my_ranges.count_ranges() == 1
