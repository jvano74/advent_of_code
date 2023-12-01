from typing import List, NamedTuple
from collections import deque, defaultdict
from heapq import heappush, heappop


class Solution:
    """
    --- Day 13: Knights of the Dinner Table ---
    In years past, the holiday feast with your family hasn't gone so well.
    Not everyone gets along! This year, you resolve, will be different.
    You're going to find the optimal seating arrangement and avoid
    all those awkward conversations.

    You start by writing up a list of everyone invited and the amount their
    happiness would increase or decrease if they were to find themselves sitting
    next to each other person. You have a circular table that will be just big
    enough to fit everyone comfortably, and so each person will have exactly
    two neighbors.

    For example, suppose you have only four attendees planned, and you calculate
    their potential happiness as follows:

    Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.

    Then, if you seat Alice next to David, Alice would lose 2 happiness units
    (because David talks so much), but David would gain 46 happiness units
    (because Alice is such a good listener), for a total change of 44.

    If you continue around the table, you could then seat Bob next to
    Alice (Bob gains 83, Alice gains 54). Finally, seat Carol, who sits
    next to Bob (Carol gains 60, Bob loses 7) and David (Carol gains 55,
    David gains 41). The arrangement looks like this:

         +41 +46
    +55   David    -2
    Carol       Alice
    +60    Bob    +54
         -7  +83

    After trying every other seating arrangement in this hypothetical scenario, you
    find that this one is the most optimal, with a total change in happiness of 330.

    What is the total change in happiness for the optimal seating arrangement of the actual guest list?
    """


class Person:
    def __init__(self):
        self.relation = defaultdict(int)


class Seating:
    def __init__(self, guest_info: List):
        self.guests = defaultdict(Person)

        for person_info in guest_info:
            # sample line of guest info
            # Carol would gain 8 happiness units by sitting next to Bob.
            info = person_info.split(" ")
            name = info[0]
            neighbor = info[-1][:-1]
            if info[2] == "gain":
                happy = int(info[3])
            else:
                happy = -int(info[3])
            self.guests[name].relation[neighbor] = happy

    def add_self(self):
        self.guests["Me"] = Person()
        for name in self.guests:
            if name == "Me":
                continue
            self.guests[name].relation["Me"] = 0
            self.guests["Me"].relation[name] = 0

    def max_happiness(self) -> List:
        guest_count = len(self.guests)
        frontier = []

        for name in self.guests:
            heappush(frontier, (0, name, [name]))

        arrangements = []

        while frontier:
            happyness, name, path_hx = heappop(frontier)
            for nn in self.guests[name].relation:
                if nn not in path_hx:
                    new_happyness = happyness
                    new_happyness -= self.guests[name].relation[nn]
                    new_happyness -= self.guests[nn].relation[name]
                    new_hx = path_hx[:]
                    new_hx.append(nn)
                    if len(new_hx) == guest_count:
                        n0 = new_hx[0]
                        new_happyness -= self.guests[n0].relation[nn]
                        new_happyness -= self.guests[nn].relation[n0]
                        heappush(arrangements, (new_happyness, new_hx))
                    heappush(frontier, (new_happyness, nn, new_hx))
        return heappop(arrangements)


SAMPLE = [
    "Alice would gain 54 happiness units by sitting next to Bob.",
    "Alice would lose 79 happiness units by sitting next to Carol.",
    "Alice would lose 2 happiness units by sitting next to David.",
    "Bob would gain 83 happiness units by sitting next to Alice.",
    "Bob would lose 7 happiness units by sitting next to Carol.",
    "Bob would lose 63 happiness units by sitting next to David.",
    "Carol would lose 62 happiness units by sitting next to Alice.",
    "Carol would gain 60 happiness units by sitting next to Bob.",
    "Carol would gain 55 happiness units by sitting next to David.",
    "David would gain 46 happiness units by sitting next to Alice.",
    "David would lose 7 happiness units by sitting next to Bob.",
    "David would gain 41 happiness units by sitting next to Carol.",
]


def test_sample():
    table = Seating(SAMPLE)
    assert set(table.guests.keys()) == {"Alice", "Bob", "Carol", "David"}
    assert table.max_happiness()[0] == -330


with open("day_13_input.txt") as fp:
    SUBMISSION = fp.read()


def test_submission():
    guest_list = [dist.strip() for dist in SUBMISSION.split("\n")]
    my_table = Seating(guest_list)
    assert my_table.max_happiness()[0] == -709
    my_table.add_self()
    assert my_table.max_happiness()[0] == -668
