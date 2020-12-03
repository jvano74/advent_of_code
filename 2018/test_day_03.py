from __future__ import  annotations
from typing import NamedTuple
from collections import defaultdict

class Fabric():
    """
    -- Day 3: No Matter How You Slice It ---

    The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit
    (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in
    the middle of the night). Unfortunately, anomalies are still affecting them - nobody
    can even agree on how to cut the fabric.

    The whole piece of fabric they're working on is a very large square - at least
    1000 inches on each side.

    Each Elf has made a claim about which area of fabric would be ideal for Santa's suit.
    All claims have an ID and consist of a single rectangle with edges parallel to the
    edges of the fabric. Each claim's rectangle is defined as follows:

    The number of inches between the left edge of the fabric and the left edge of the rectangle.
    The number of inches between the top edge of the fabric and the top edge of the rectangle.
    The width of the rectangle in inches.
    The height of the rectangle in inches.

    A claim like #123 @ 3,2: 5x4 means that claim
    ID 123 specifies a rectangle
    3 inches from the left edge,
    2 inches from the top edge,
    5 inches wide, and
    4 inches tall.

    Visually, it claims the square inches of fabric represented by #
    (and ignores the square inches of fabric represented by .)
    in the diagram below:

    ...........
    ...........
    ...#####...
    ...#####...
    ...#####...
    ...#####...
    ...........
    ...........
    ...........

    The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas.

    For example, consider the following claims:

    #1 @ 1,3: 4x4
    #2 @ 3,1: 4x4
    #3 @ 5,5: 2x2

    Visually, these claim the following areas:

    ........
    ...2222.
    ...2222.
    .11XX22.
    .11XX22.
    .111133.
    .111133.
    ........

    The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others,
    does not overlap either of them.)

    If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of
    fabric are within two or more claims?

    --- Part Two ---
    Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with
    any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit
    after all!

    For example, in the claims above, only claim 3 is intact after all claims are made.

    What is the ID of the only claim that doesn't overlap?
    """

    def __init__(self):
        self.grid = defaultdict(list)

    def cut(self, ec: ElfCut):
        for x in range(ec.x, ec.x + ec.dx):
            for y in range(ec.y, ec.y + ec.dy):
                self.grid[(x,y)].append(ec.who)

    def overlap(self):
        total = 0
        for pos in self.grid:
            if len(self.grid[pos]) > 1:
                total += 1
        return total

    def unique(self):
        overlaping = set()
        solo = set()
        for pos in self.grid:
            layers = len(self.grid[pos])
            if layers > 1:
                for who in self.grid[pos]:
                    solo.discard(who)
                    overlaping.add(who)
            elif layers == 1 and self.grid[pos][0] not in overlaping:
                solo.add(self.grid[pos][0])
        return solo


    def print(self, x_range, y_range):
        for y in y_range:
            y_line = ''
            for x in x_range:
                l = len(self.grid[(x,y)])
                if l == 0:
                    y_line += '.'
                elif l == 1:
                    y_line += 'x'
                else:
                    y_line += '#'
            print(y_line)


class ElfCut(NamedTuple):
    who: int
    x: int
    dx: int
    y: int
    dy: int

    @staticmethod
    def parse(line: str) -> ElfCut:
        """
        '#1 @ 1,3: 4x4',
        """
        who, _, start, size = line.split()
        who = int(who[1:])
        x,y = [int(n) for n in start[:-1].split(",")]
        dx,dy = [int(n) for n in size.split("x")]
        return ElfCut(who, x, dx, y, dy)


SAMPLE = [
    '#1 @ 1,3: 4x4',
    '#2 @ 3,1: 4x4',
    '#3 @ 5,5: 2x2',
    ]

with open('input_day_03.txt') as f:
    INPUTS = [line.strip() for line in f]

sample_fabric = Fabric()
final_fabric = Fabric()

for elf in SAMPLE:
    sample_fabric.cut(ElfCut.parse(elf))

for elf in INPUTS:
    final_fabric.cut(ElfCut.parse(elf))

sample_fabric.print(range(8), range(8))
# final_fabric.print(range(18), range(18))


def test_part1():
    assert sample_fabric.overlap() == 4
    assert final_fabric.overlap() == 4

def test_part2():
    assert sample_fabric.unique() == set([3])
    assert final_fabric.unique() == set([567])
