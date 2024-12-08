from pathlib import Path
from typing import List, NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 8: Resonant Collinearity ---

    You find yourselves on the roof of a top-secret Easter Bunny installation.

    While The Historians do their thing, you take a look at the familiar huge
    antenna. Much to your surprise, it seems to have been reconfigured to emit a
    signal that makes people 0.1% more likely to buy Easter Bunny brand
    Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

    Scanning across the city, you find that there are actually many such
    antennas. Each antenna is tuned to a specific frequency indicated by a
    single lowercase letter, uppercase letter, or digit. You create a map (your
    puzzle input) of these antennas. For example:

    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............

    The signal only applies its nefarious effect at specific antinodes based on
    the resonant frequencies of the antennas. In particular, an antinode occurs
    at any point that is perfectly in line with two antennas of the same
    frequency - but only when one of the antennas is twice as far away as the
    other. This means that for any pair of antennas with the same frequency,
    there are two antinodes, one on either side of them.

    So, for these two antennas with frequency a, they create the two antinodes
    marked with #:

    ..........
    ...#......
    ..........
    ....a.....
    ..........
    .....a....
    ..........
    ......#...
    ..........
    ..........

    Adding a third antenna with the same frequency creates several more
    antinodes. It would ideally add four antinodes, but two are off the right
    side of the map, so instead it adds only two:

    ..........
    ...#......
    #.........
    ....a.....
    ........a.
    .....a....
    ..#.......
    ......#...
    ..........
    ..........

    Antennas with different frequencies don't create antinodes; A and a count as
    different frequencies. However, antinodes can occur at locations that
    contain antennas. In this diagram, the lone antenna with frequency capital A
    creates no antinodes but has a lowercase-a-frequency antinode at its
    location:

    ..........
    ...#......
    #.........
    ....a.....
    ........a.
    .....a....
    ..#.......
    ......A...
    ..........
    ..........

    The first example has antennas with two different frequencies, so the
    antinodes they create look like this, plus an antinode overlapping the
    topmost A-frequency antenna:

    ......#....#
    ...#....0...
    ....#0....#.
    ..#....0....
    ....0....#..
    .#....A.....
    ...#........
    #......#....
    ........A...
    .........A..
    ..........#.
    ..........#.

    Because the topmost A-frequency antenna overlaps with a 0-frequency
    antinode, there are 14 total unique locations that contain an antinode
    within the bounds of the map.

    Calculate the impact of the signal. How many unique locations within the
    bounds of the map contain an antinode?

    Your puzzle answer was 271.

    --- Part Two ---
    Watching over your shoulder as you work, one of The Historians asks if you
    took the effects of resonant harmonics into your calculations.

    Whoops!

    After updating your model, it turns out that an antinode occurs at any grid
    position exactly in line with at least two antennas of the same frequency,
    regardless of distance. This means that some of the new antinodes will occur
    at the position of each antenna (unless that antenna is the only one of its
    frequency).

    So, these three T-frequency antennas now create many antinodes:

    T....#....
    ...T......
    .T....#...
    .........#
    ..#.......
    ..........
    ...#......
    ..........
    ....#.....
    ..........

    In fact, the three T-frequency antennas are all exactly in line with two
    antennas, so they are all also antinodes! This brings the total number of
    antinodes in the above example to 9.

    The original example now has 34 antinodes, including the antinodes that
    appear on every antenna:

    ##....#....#
    .#.#....0...
    ..#.#0....#.
    ..##...0....
    ....0....#..
    .#...#A....#
    ...#..#.....
    #....#.#....
    ..#.....A...
    ....#....A..
    .#........#.
    ...#......##

    Calculate the impact of the signal using this updated model. How many unique
    locations within the bounds of the map contain an antinode?

    Your puzzle answer was 994.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


with open(Path(__file__).parent / "2024_08_input.txt") as fp:
    MY_INPUTS = fp.read().split("\n")

SAMPLE_INPUTS = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)


DELTAS = {
    Pt(1, 0),
    Pt(-1, 0),
    Pt(0, 1),
    Pt(0, -1),
    Pt(1, 1),
    Pt(-1, 1),
    Pt(-1, -1),
    Pt(1, -1),
}


class Map:
    def __init__(self, raw_rows: List[str]):
        self.antenna_map = defaultdict(set)
        self.x_max = 0
        self.y_max = 0
        for y, row in enumerate(raw_rows):
            for x, c in enumerate(row):
                self.x_max = max(self.x_max, x)
                self.y_max = max(self.y_max, y)
                if c == ".":
                    continue
                self.antenna_map[c].add(Pt(x, y))

        self.vectors_to_check = defaultdict(set)
        for _, locations in self.antenna_map.items():
            for a in locations:
                for b in locations:
                    if a == b:
                        continue
                    self.vectors_to_check[a].add(b - a)

    def find_antinodes(self):
        antinodes = set()
        for _, locations in self.antenna_map.items():
            for a in locations:
                for b in locations:
                    if a == b:
                        continue
                    antinode = (b - a) + b
                    if 0 <= antinode.x <= self.x_max and 0 <= antinode.y <= self.y_max:
                        antinodes.add(antinode)
        return antinodes

    def check_point(self, test_pt) -> bool:
        for antenna, directions in self.vectors_to_check.items():
            delta = antenna - test_pt
            normal = Pt(delta.y, -delta.x)
            for direction in directions:
                if direction.x * normal.x + direction.y * normal.y == 0:
                    return True
        return False

    def find_antinode_lines(self):
        antinodes = set()
        for y in range(self.y_max + 1):
            for x in range(self.x_max + 1):
                test_pt = Pt(x, y)
                if self.check_point(test_pt):
                    antinodes.add(test_pt)
        return antinodes


def test_find_antinodes():
    sample_map = Map(SAMPLE_INPUTS)
    assert len(sample_map.find_antinodes()) == 14
    assert len(sample_map.find_antinode_lines()) == 34
    my_map = Map(MY_INPUTS)
    assert len(my_map.find_antinodes()) == 271
    assert len(my_map.find_antinode_lines()) == 994
