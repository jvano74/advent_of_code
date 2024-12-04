from pathlib import Path
from typing import NamedTuple


class Puzzle:
    """
    --- Day 17: Reservoir Research ---
    You arrive in the year 18. If it weren't for the coat you got in 1018, you would be very cold: the North Pole base
    hasn't even been constructed.

    Rather, it hasn't been constructed yet. The Elves are making a little progress, but there's not a lot of liquid
    water in this climate, so they're getting very dehydrated. Maybe there's more underground?

    You scan a two-dimensional vertical slice of the ground nearby and discover that it is mostly sand with veins of
    clay. The scan only provides data with a granularity of square meters, but it should be good enough to determine
    how much water is trapped there. In the scan, x represents the distance to the right, and y represents the distance
    down. There is also a spring of water near the surface at x=500, y=0. The scan identifies which square meters are
    clay (your puzzle input).

    For example, suppose your scan shows the following veins of clay:

    x=495, y=2..7
    y=7, x=495..501
    x=501, y=3..7
    x=498, y=2..4
    x=506, y=1..2
    x=498, y=10..13
    x=504, y=10..13
    y=13, x=498..504

    Rendering clay as #, sand as ., and the water spring as +, and with x increasing to the right and y increasing
    downward, this becomes:

       44444455555555
       99999900000000
       45678901234567
     0 ......+.......
     1 ............#.
     2 .#..#.......#.
     3 .#..#..#......
     4 .#..#..#......
     5 .#.....#......
     6 .#.....#......
     7 .#######......
     8 ..............
     9 ..............
    10 ....#.....#...
    11 ....#.....#...
    12 ....#.....#...
    13 ....#######...

    The spring of water will produce water forever. Water can move through sand, but is blocked by clay. Water always
    moves down when possible, and spreads to the left and right otherwise, filling space that has clay on both sides
    and falling out otherwise.

    For example, if five squares of water are created, they will flow downward until they reach the clay and settle
    there. Water that has come to rest is shown here as ~, while sand through which water has passed (but which is
    now dry again) is shown as |:

    ......+.......
    ......|.....#.
    .#..#.|.....#.
    .#..#.|#......
    .#..#.|#......
    .#....|#......
    .#~~~~~#......
    .#######......
    ..............
    ..............
    ....#.....#...
    ....#.....#...
    ....#.....#...
    ....#######...

    Two squares of water can't occupy the same location. If another five squares of water are created, they will
    settle on the first five, filling the clay reservoir a little more:

    ......+.......
    ......|.....#.
    .#..#.|.....#.
    .#..#.|#......
    .#..#.|#......
    .#~~~~~#......
    .#~~~~~#......
    .#######......
    ..............
    ..............
    ....#.....#...
    ....#.....#...
    ....#.....#...
    ....#######...

    Water pressure does not apply in this scenario. If another four squares of water are created, they will stay on
    the right side of the barrier, and no water will reach the left side:

    ......+.......
    ......|.....#.
    .#..#.|.....#.
    .#..#~~#......
    .#..#~~#......
    .#~~~~~#......
    .#~~~~~#......
    .#######......
    ..............
    ..............
    ....#.....#...
    ....#.....#...
    ....#.....#...
    ....#######...

    At this point, the top reservoir overflows. While water can reach the tiles above the surface of the water, it
    cannot settle there, and so the next five squares of water settle like this:

    ......+.......
    ......|.....#.
    .#..#||||...#.
    .#..#~~#|.....
    .#..#~~#|.....
    .#~~~~~#|.....
    .#~~~~~#|.....
    .#######|.....
    ........|.....
    ........|.....
    ....#...|.#...
    ....#...|.#...
    ....#~~~~~#...
    ....#######...

    Note especially the leftmost |: the new squares of water can reach this tile, but cannot stop there. Instead,
    eventually, they all fall to the right and settle in the reservoir below.

    After 10 more squares of water, the bottom reservoir is also full:

    ......+.......
    ......|.....#.
    .#..#||||...#.
    .#..#~~#|.....
    .#..#~~#|.....
    .#~~~~~#|.....
    .#~~~~~#|.....
    .#######|.....
    ........|.....
    ........|.....
    ....#~~~~~#...
    ....#~~~~~#...
    ....#~~~~~#...
    ....#######...

    Finally, while there is nowhere left for the water to settle, it can reach a few more tiles before overflowing
    beyond the bottom of the scanned data:

    ......+.......    (line not counted: above minimum y value)
    ......|.....#.
    .#..#||||...#.
    .#..#~~#|.....
    .#..#~~#|.....
    .#~~~~~#|.....
    .#~~~~~#|.....
    .#######|.....
    ........|.....
    ...|||||||||..
    ...|#~~~~~#|..
    ...|#~~~~~#|..
    ...|#~~~~~#|..
    ...|#######|..
    ...|.......|..    (line not counted: below maximum y value)
    ...|.......|..    (line not counted: below maximum y value)
    ...|.......|..    (line not counted: below maximum y value)

    How many tiles can be reached by the water? To prevent counting forever, ignore tiles with a y coordinate smaller
    than the smallest y coordinate in your scan data or larger than the largest one. Any x coordinate is valid. In
    this example, the lowest y coordinate given is 1, and the highest is 13, causing the water spring (in row 0)
    and the water falling off the bottom of the render (in rows 14 through infinity) to be ignored.

    So, in the example above, counting both water at rest (~) and other sand tiles the water can hypothetically
    reach (|), the total number of tiles the water can reach is 57.

    How many tiles can the water reach within the range of y values in your scan?

    --- Part Two ---
    After a very long time, the water spring will run dry. How much water will be retained?

    In the example above, water that won't eventually drain out is shown as ~, a total of 29 tiles.

    How many water tiles are left after the water spring stops producing water and all remaining water not at
    rest has drained?
    """

    pass


with open(Path(__file__).parent / "2018_17_input.txt") as fp:
    INPUTS = [ln.strip() for ln in fp]


SAMPLE = [
    "x=495, y=2..7",
    "y=7, x=495..501",
    "x=501, y=3..7",
    "x=498, y=2..4",
    "x=506, y=1..2",
    "x=498, y=10..13",
    "x=504, y=10..13",
    "y=13, x=498..504",
]


def test_input():
    assert INPUTS[0] == "x=732, y=919..935"
    assert INPUTS[1] == "y=161, x=655..663"


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Reservoir:
    def __init__(self, raw_inputs, spring_x=500):
        self.spring_x = spring_x
        self.y_min = None
        self.y_max = None
        self.clay = set()
        self.moving_water = set()
        self.still_water = set()

        for line in raw_inputs:
            raw_fixed, raw_range = line.split(", ")
            c, v = raw_fixed.split("=")
            l, h = raw_range[2:].split("..")
            v, l, h = int(v), int(l), int(h)
            for i in range(l, h + 1):
                if c == "x":
                    pt = Pt(v, i)
                else:
                    pt = Pt(i, v)
                self.clay.add(pt)
                if self.y_min is None:
                    self.y_min = pt.y
                else:
                    self.y_min = min(self.y_min, pt.y)
                if self.y_max is None:
                    self.y_max = pt.y
                else:
                    self.y_max = max(self.y_max, pt.y)

    def find_edge(self, pt, direction):
        test_pt = pt
        while True:
            below_test = test_pt + Pt(0, 1)
            if below_test not in self.clay and below_test not in self.still_water:
                return test_pt, True
            if test_pt + direction in self.clay:
                return test_pt, False
            test_pt += direction

    def add_water(self, pt):
        down = pt + Pt(0, 1)
        if down not in self.clay and down not in self.still_water:
            self.moving_water.add(pt)
            return {down}

        left_edge, left_spill = self.find_edge(pt, Pt(-1, 0))
        right_edge, right_spill = self.find_edge(pt, Pt(1, 0))

        if not left_spill and not right_spill:
            for x in range(left_edge.x, right_edge.x + 1):  # fill as still_water
                self.still_water.add(Pt(x, pt.y))
            up = pt + Pt(0, -1)
            return {up}

        for x in range(left_edge.x, right_edge.x + 1):  # fill as moving_water
            self.moving_water.add(Pt(x, pt.y))
        new_sources = set()
        if left_spill:
            new_sources.add(left_edge)
        if right_spill:
            new_sources.add(right_edge)
        return new_sources

    def fill(self):
        sources = {Pt(self.spring_x, self.y_min)}
        while len(sources) > 0:
            pt = sources.pop()
            if pt.y > self.y_max:
                pass
            else:
                new_sources = self.add_water(pt)
                sources = sources | new_sources


def test_sample_reservoir():
    reservoir = Reservoir(SAMPLE)
    reservoir.fill()
    assert len(reservoir.moving_water | reservoir.still_water) == 57
    assert len(reservoir.still_water) == 29


def test_puzzle_reservoir():
    reservoir = Reservoir(INPUTS)
    assert reservoir.y_min == 6
    assert reservoir.y_max == 1870
    assert len(reservoir.clay) == 22555
    reservoir.fill()
    assert len(reservoir.moving_water | reservoir.still_water) == 37858
    assert len(reservoir.still_water) == 30410
