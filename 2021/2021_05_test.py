from pathlib import Path
from typing import List, NamedTuple
from collections import defaultdict
import re


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def scale(self, r):
        return Pt(r * self.x, r * self.y)


class Puzzle:
    """
    --- Day 5: Hydrothermal Venture ---

    You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce
    large, opaque clouds, so it would be best to avoid them if possible.

    They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents
    (your puzzle input) for you to review. For example:

    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2

    Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the
    coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These
    line segments include the points at both ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

    For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

    So, the horizontal and vertical lines from the above list would produce the following diagram:

    .......1..
    ..1....1..
    ..1....1..
    .......1..
    .112111211
    ..........
    ..........
    ..........
    ..........
    222111....

    In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position
    is shown as the number of lines which cover that point or . if no line covers that point. The
    top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the
    overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

    To avoid the most dangerous areas, you need to determine the number of points where at least
    two lines overlap. In the above example, this is anywhere in the diagram with a 2 or
    larger - a total of 5 points.

    Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

    To begin, get your puzzle input.

    """


SAMPLE = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]

with open(Path(__file__).parent / "2021_05_input.txt") as fp:
    INPUTS = [line.strip() for line in fp]


class Floor:
    def __init__(self, vent_vectors, mode):
        self.sea_floor = defaultdict(int)
        for v in vent_vectors:
            x_s, y_s, x_e, y_e = (int(n) for n in re.split(r"\D+", v))
            if x_s == x_e:
                for y in range(min(y_s, y_e), max(y_s, y_e) + 1):
                    self.sea_floor[Pt(x_s, y)] += 1
            elif y_s == y_e:
                for x in range(min(x_s, x_e), max(x_s, x_e) + 1):
                    self.sea_floor[Pt(x, y_s)] += 1
            elif mode == "advanced":
                dx = x_e - x_s
                dy = y_e - y_s
                scale = max(abs(dx), abs(dy))
                dx = dx // scale
                dy = dy // scale
                for s in range(scale + 1):
                    self.sea_floor[Pt(x_s + s * dx, y_s + s * dy)] += 1

    def danger_zones(self):
        return sum([1 for v in self.sea_floor.values() if v > 1])


def test_danger_zones():
    sample_floor = Floor(SAMPLE, "basic")
    assert sample_floor.danger_zones() == 5
    sea_floor = Floor(INPUTS, "basic")
    assert sea_floor.danger_zones() == 7473


def test_advanced_danger_zones():
    sample_floor = Floor(SAMPLE, "advanced")
    assert sample_floor.danger_zones() == 12
    sea_floor = Floor(INPUTS, "advanced")
    assert sea_floor.danger_zones() == 24164
