from pathlib import Path
from collections import defaultdict
from heapq import heappush, heappop
from typing import NamedTuple


class Puzzle:
    """
    --- Day 18: Lavaduct Lagoon ---
    Thanks to your efforts, the machine parts factory is one of the first
    factories up and running since the lavafall came back. However, to catch up
    with the large backlog of parts requests, the factory will also need a large
    supply of lava for a while; the Elves have already started creating a large
    lagoon nearby for this purpose.

    However, they aren't sure the lagoon will be big enough; they've asked you
    to take a look at the dig plan (your puzzle input). For example:

    R 6 (#70c710)
    D 5 (#0dc571)
    L 2 (#5713f0)
    D 2 (#d2c081)
    R 2 (#59c680)
    D 2 (#411b91)
    L 5 (#8ceee2)
    U 2 (#caa173)
    L 1 (#1b58a2)
    U 2 (#caa171)
    R 2 (#7807d2)
    U 3 (#a77fa3)
    L 2 (#015232)
    U 2 (#7a21e3)

    The digger starts in a 1 meter cube hole in the ground. They then dig the
    specified number of meters up (U), down (D), left (L), or right (R),
    clearing full 1 meter cubes as they go. The directions are given as seen
    from above, so if "up" were north, then "right" would be east, and so on.
    Each trench is also listed with the color that the edge of the trench should
    be painted as an RGB hexadecimal color code.

    When viewed from above, the above example dig plan would result in the
    following loop of trench (#) having been dug out from otherwise ground-level
    terrain (.):

    #######
    #.....#
    ###...#
    ..#...#
    ..#...#
    ###.###
    #...#..
    ##..###
    .#....#
    .######

    At this point, the trench could contain 38 cubic meters of lava. However,
    this is just the edge of the lagoon; the next step is to dig out the
    interior so that it is one meter deep as well:

    #######
    #######
    #######
    ..#####
    ..#####
    #######
    #####..
    #######
    .######
    .######

    Now, the lagoon can contain a much more respectable 62 cubic meters of lava.
    While the interior is dug out, the edges are also painted according to the
    color codes in the dig plan.

    The Elves are concerned the lagoon won't be large enough; if they follow
    their dig plan, how many cubic meters of lava could it hold?

    Your puzzle answer was 48795.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The Elves were right to be concerned; the planned lagoon would be much too
    small.

    After a few minutes, someone realizes what happened; someone swapped the
    color and instruction parameters when producing the dig plan. They don't
    have time to fix the bug; one of them asks if you can extract the correct
    instructions from the hexadecimal codes.

    Each hexadecimal code is six hexadecimal digits long. The first five
    hexadecimal digits encode the distance in meters as a five-digit hexadecimal
    number. The last hexadecimal digit encodes the direction to dig: 0 means R,
    1 means D, 2 means L, and 3 means U.

    So, in the above example, the hexadecimal codes can be converted into the
    true instructions:

    #70c710 = R 461937
    #0dc571 = D 56407
    #5713f0 = R 356671
    #d2c081 = D 863240
    #59c680 = R 367720
    #411b91 = D 266681
    #8ceee2 = L 577262
    #caa173 = U 829975
    #1b58a2 = L 112010
    #caa171 = D 829975
    #7807d2 = L 491645
    #a77fa3 = U 686074
    #015232 = L 5411
    #7a21e3 = U 500254

    Digging out this loop and its interior produces a lagoon that can hold an
    impressive 952408144115 cubic meters of lava.

    Convert the hexadecimal color codes into the correct instructions; if the
    Elves follow this new dig plan, how many cubic meters of lava could the
    lagoon hold?

    Your puzzle answer was 40654918441248.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open(Path(__file__).parent / "2023_18_input.txt") as fp:
    MY_INPUT = fp.read().split("\n")

SAMPLE = [
    "R 6 (#70c710)",
    "D 5 (#0dc571)",
    "L 2 (#5713f0)",
    "D 2 (#d2c081)",
    "R 2 (#59c680)",
    "D 2 (#411b91)",
    "L 5 (#8ceee2)",
    "U 2 (#caa173)",
    "L 1 (#1b58a2)",
    "U 2 (#caa171)",
    "R 2 (#7807d2)",
    "U 3 (#a77fa3)",
    "L 2 (#015232)",
    "U 2 (#7a21e3)",
]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def scale(self, d):
        return Pt(d * self.x, d * self.y)


class Lagoon:
    def __init__(self, outline, use_hex=False, use_vectors=False) -> None:
        self.map = defaultdict(dict)
        self.fill = set()
        pt = Pt(0, 0)
        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0
        dir_map = {
            "0": Pt(1, 0),  # R
            "R": Pt(1, 0),  # R
            "1": Pt(0, 1),  # D
            "D": Pt(0, 1),  # D
            "2": Pt(-1, 0),  # L
            "L": Pt(-1, 0),  # L
            "3": Pt(0, -1),  # U
            "U": Pt(0, -1),  # U
        }
        for raw in outline:
            direction, distance, color = raw.split(" ")
            if use_hex:
                use_vectors = True
                direction = dir_map[color[-2]]
                distance = int(color[2:-2], 16)
            else:
                direction = dir_map[direction]
                distance = int(distance)

            if use_vectors:
                # calculate
                next_pt = pt + direction.scale(distance)
                if abs(direction.y) == 1:
                    if "v" in self.map[pt]:
                        raise Exception(f"Existing v at {pt=}")
                    if "v" in self.map[next_pt]:
                        raise Exception(f"Existing v at {next_pt=}")
                    self.map[pt]["v"] = next_pt
                    self.map[next_pt]["v"] = pt
                elif abs(direction.x) == 1:
                    if "h" in self.map[pt]:
                        raise Exception(f"Existing h at {pt=}")
                    if "h" in self.map[next_pt]:
                        raise Exception(f"Existing h at {next_pt=}")
                    self.map[pt]["h"] = next_pt
                    self.map[next_pt]["h"] = pt
                # move
                pt = next_pt
            else:
                for _ in range(int(distance)):
                    pt += direction
                    self.map[pt] = {"color": color}

            self.x_min = min(pt.x, self.x_min)
            self.y_min = min(pt.y, self.y_min)
            self.x_max = max(pt.x, self.x_max)
            self.y_max = max(pt.y, self.y_max)

        # check end pt ties to start
        if pt != Pt(0, 0):
            raise Exception("Loop not closed")

    def find_blocks(self):
        total = 0
        keys = []
        x_slices = set()
        y_slices = set()
        map = self.map.copy()
        ignore_pt = set()
        ignore_strip = set()
        for key in map.keys():
            x_slices.add(key.x)
            y_slices.add(key.y)
            heappush(keys, key)
        x_slices = sorted([x for x in x_slices])
        y_slices = sorted([y for y in y_slices])

        next_x = x_slices.pop(0)
        while keys:
            pt1 = heappop(keys)
            while keys and pt1 in ignore_pt:
                pt1 = heappop(keys)
            if not keys:
                break
            pt2 = heappop(keys)
            while keys and pt2 in ignore_pt:
                pt2 = heappop(keys)
            if pt2 in ignore_pt:
                raise Exception("Unexpected data format - no second pair")
            if pt1.x != pt2.x:
                raise Exception(f"Points not in pairs {pt1=} {pt2=} {keys=}")
            if pt1.x == next_x:
                next_x = x_slices.pop(0)

            # check for left strips above pt1 or below pt2
            if "v" in map[pt1]:
                pt1_n = map[pt1]["v"]
                if (pt1_n, pt1) not in ignore_strip:
                    left_strip_n = pt1.y - pt1_n.y
                    if "h" in map[pt1_n] and map[pt1_n]["h"].x > pt1_n.x:
                        left_strip_n += -1
                    if left_strip_n > 0:
                        ignore_strip.add((pt1_n, pt1))
                        total += left_strip_n
            if "v" in map[pt2]:
                pt2_s = map[pt2]["v"]
                if (pt2, pt2_s) not in ignore_strip:
                    left_strip_s = pt2_s.y - pt2.y
                    if "h" in map[pt2_s] and map[pt2_s]["h"].x > pt2_s.x:
                        left_strip_s += -1
                    if left_strip_s > 0:
                        ignore_strip.add((pt2, pt2_s))
                        total += left_strip_s

            width = pt2.y - pt1.y + 1
            length = next_x - pt1.x
            total += width * length

            pt1_r = Pt(next_x, pt1.y)
            pt1_next = map[pt1]["h"]

            pt2_r = Pt(next_x, pt2.y)
            pt2_next = map[pt2]["h"]

            # If pt1_new or pt2_new go down or up capture additional length,
            # and if it closes off a loop only add one with a +2, e.g.
            #
            #         |
            #     pt1 +--+ pt1_r pt2_new
            #            |
            #     pt2 +--+ pt2_r pt1_new
            #         |
            #
            if pt1_r not in map:
                heappush(keys, pt1_r)
                pt1_ignore = None
                map[pt1_r]["h"] = pt1_next
            else:
                pt1_ignore = pt1_r
                pt1_r = map[pt1_r]["v"]
                ignore_pt.add(pt1_ignore)

            if pt2_r not in map:
                heappush(keys, pt2_r)
                pt2_ignore = None
                map[pt2_r]["h"] = pt2_next
            else:
                pt2_ignore = pt2_r
                pt2_r = map[pt2_r]["v"]
                ignore_pt.add(pt2_ignore)
            if pt1_ignore and pt2_ignore and pt1_ignore == pt2_r:
                close = pt2_ignore.y - pt1_ignore.y + 1
                total += close

        return total

    def count(self, fill=False):
        if not fill:
            return sum(1 for k in self.map.keys())
        for y in range(self.y_min, self.y_max + 1):
            inside_n = 0
            inside_s = 0
            for x in range(self.x_min, self.x_max + 1):
                if Pt(x, y) in self.map:
                    self.fill.add(Pt(x, y))
                    if Pt(x, y - 1) in self.map:
                        inside_n = 1 - inside_n
                    if Pt(x, y + 1) in self.map:
                        inside_s = 1 - inside_s
                elif inside_n and inside_s:
                    self.fill.add(Pt(x, y))
        return len(self.fill)

    def show(self, fill=False):
        lines = []
        for y in range(self.y_min, self.y_max + 1):
            row = ""
            for x in range(self.x_min, self.x_max + 1):
                if Pt(x, y) in self.map:
                    row += "#"
                elif fill and Pt(x, y) in self.fill:
                    row += "#"
                else:
                    row += "."
            lines.append(row)
        print("\n".join(lines))


def test_lagoon():
    # part 1
    sample = Lagoon(SAMPLE)
    sample_count = sample.count(fill=True)
    assert sample_count == 62
    sample_vector_version = Lagoon(SAMPLE, use_vectors=True)
    sample_vector_version_count = sample_vector_version.find_blocks()
    assert sample_vector_version_count == 62

    my_lagoon = Lagoon(MY_INPUT)
    my_lagoon_count = my_lagoon.count(fill=True)
    assert my_lagoon_count == 48795  # 49728 not right answer

    my_lagoon_vector_version = Lagoon(MY_INPUT, use_vectors=True)
    my_lagoon_vector_version_count = my_lagoon_vector_version.find_blocks()
    assert my_lagoon_vector_version_count == 48795

    # part 2
    sample_pt2 = Lagoon(SAMPLE, use_hex=True)
    sample_pt2_count = sample_pt2.find_blocks()
    assert sample_pt2_count == 952408144115

    my_lagoon = Lagoon(MY_INPUT)
    # 49728 not right answer
    assert my_lagoon.count(fill=True) == 48795
    my_lagoon2 = Lagoon(MY_INPUT, use_hex=True)
    my_lagoon2_count = my_lagoon2.find_blocks()
    assert my_lagoon2_count == 40654918441248
