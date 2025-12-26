import re
from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 12: Christmas Tree Farm ---
    You're almost out of time, but there can't be much left to decorate.
    Although there are no stairs, elevators, escalators, tunnels, chutes,
    teleporters, firepoles, or conduits here that would take you deeper into the
    North Pole base, there is a ventilation duct. You jump in.

    After bumping around for a few minutes, you emerge into a large, well-lit
    cavern full of Christmas trees!

    There are a few Elves here frantically decorating before the deadline. They
    think they'll be able to finish most of the work, but the one thing they're
    worried about is the presents for all the young Elves that live here at the
    North Pole. It's an ancient tradition to put the presents under the trees,
    but the Elves are worried they won't fit.

    The presents come in a few standard but very weird shapes. The shapes and
    the regions into which they need to fit are all measured in standard units.
    To be aesthetically pleasing, the presents need to be placed into the
    regions in a way that follows a standardized two-dimensional unit grid; you
    also can't stack presents.

    As always, the Elves have a summary of the situation (your puzzle input) for
    you. First, it contains a list of the presents' shapes. Second, it contains
    the size of the region under each tree and a list of the number of presents
    of each shape that need to fit into that region. For example:

    0:
    ###
    ##.
    ##.

    1:
    ###
    ##.
    .##

    2:
    .##
    ###
    ##.

    3:
    ##.
    ###
    ##.

    4:
    ###
    #..
    ###

    5:
    ###
    .#.
    ###

    4x4: 0 0 0 0 2 0
    12x5: 1 0 1 0 2 2
    12x5: 1 0 1 0 3 2

    The first section lists the standard present shapes. For convenience, each
    shape starts with its index and a colon; then, the shape is displayed
    visually, where # is part of the shape and . is not.

    The second section lists the regions under the trees. Each line starts with
    the width and length of the region; 12x5 means the region is 12 units wide
    and 5 units long. The rest of the line describes the presents that need to
    fit into that region by listing the quantity of each shape of present; 1 0 1
    0 3 2 means you need to fit one present with shape index 0, no presents with
    shape index 1, one present with shape index 2, no presents with shape index
    3, three presents with shape index 4, and two presents with shape index 5.

    Presents can be rotated and flipped as necessary to make them fit in the
    available space, but they have to always be placed perfectly on the grid.
    Shapes can't overlap (that is, the # part from two different presents can't
    go in the same place on the grid), but they can fit together (that is, the .
    part in a present's shape's diagram does not block another present from
    occupying that space on the grid).

    The Elves need to know how many of the regions can fit the presents listed.
    In the above example, there are six unique present shapes and three regions
    that need checking.

    The first region is 4x4:

    ....
    ....
    ....
    ....

    In it, you need to determine whether you could fit two presents that have
    shape index 4:

    ###
    #..
    ###

    After some experimentation, it turns out that you can fit both presents in
    this region. Here is one way to do it, using A to represent one present and
    B to represent the other:

    AAA.
    ABAB
    ABAB
    .BBB

    The second region, 12x5: 1 0 1 0 2 2, is 12 units wide and 5 units long. In
    that region, you need to try to fit one present with shape index 0, one
    present with shape index 2, two presents with shape index 4, and two
    presents with shape index 5.

    It turns out that these presents can all fit in this region. Here is one way
    to do it, again using different capital letters to represent all the
    required presents:

    ....AAAFFE.E
    .BBBAAFFFEEE
    DDDBAAFFCECE
    DBBB....CCC.
    DDD.....C.C.

    The third region, 12x5: 1 0 1 0 3 2, is the same size as the previous
    region; the only difference is that this region needs to fit one additional
    present with shape index 4. Unfortunately, no matter how hard you try, there
    is no way to fit all of the presents into this region.

    So, in this example, 2 regions can fit all of their listed presents.

    Consider the regions beneath each tree and the presents the Elves would like
    to fit into each of them. How many of the regions can fit all of the
    presents listed?

    """


with open(Path(__file__).parent / "2025_12_input.txt") as fp:
    RAW_INPUT = fp.read()

RAW_SAMPLE = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""


class Farm:

    def __init__(self, raw_input):
        grid_pattern = r"(\d+):\n(([.#]+\n)+)\n"
        raw_grids = re.finditer(grid_pattern, raw_input)
        self.shapes = {int(g.group(1)): g.group(2)[:-1].split("\n") for g in raw_grids}

        self.shape_areas = {
            id: sum(ln.count("#") for ln in region)
            for id, region in self.shapes.items()
        }

        region_pattern = r"(\d+)x(\d+): ((\d+ ?)+)\n"
        raw_regions = re.finditer(region_pattern, raw_input)
        self.regions = [
            (
                (int(r.group(1)), int(r.group(2))),
                [int(d) for d in r.group(3).split(" ")],
            )
            for r in raw_regions
        ]

        self.region_classification = defaultdict(list)
        for region_dim, gift_count in self.regions:
            grid_count = (region_dim[0] // 3) * (region_dim[0] // 3)
            total_gifts = sum(gift_count)

            region_area = region_dim[0] * region_dim[0]
            gift_area = sum(
                number_gifts * self.shape_areas[id]
                for id, number_gifts in enumerate(gift_count)
            )

            if region_area < gift_area:
                self.region_classification["invalid"].append(
                    (
                        region_dim,
                        gift_count,
                        region_area,
                        gift_area,
                        region_area - gift_area,
                    )
                )
                continue
            if total_gifts <= grid_count:
                self.region_classification["valid"].append(
                    (
                        region_dim,
                        gift_count,
                        region_area,
                        gift_area,
                        region_area - gift_area,
                    )
                )
                continue
            if total_gifts * 9 <= region_area:
                self.region_classification["likely_valid"].append(
                    (
                        region_dim,
                        gift_count,
                        region_area,
                        gift_area,
                        region_area - gift_area,
                    )
                )
                continue
            self.region_classification["unknown"].append(
                (
                    region_dim,
                    gift_count,
                    region_area,
                    gift_area,
                    region_area - gift_area,
                )
            )

    def region_count(self):
        return {key: len(value) for key, value in self.region_classification.items()}

    def guess_valid_region_count(self, cutoff=100):
        valid = len(self.region_classification["valid"])
        valid += len(self.region_classification["likely_valid"])
        for (
            region_dim,
            gift_count,
            area,
            gift_area,
            extra_area,
        ) in self.region_classification["unknown"]:
            if extra_area > cutoff:
                valid += 1
        return valid


def test_farm():
    sample_farm = Farm(RAW_SAMPLE)
    assert sample_farm.shapes == {
        0: ["###", "##.", "##."],
        1: ["###", "##.", ".##"],
        2: [".##", "###", "##."],
        3: ["##.", "###", "##."],
        4: ["###", "#..", "###"],
        5: ["###", ".#.", "###"],
    }
    assert sample_farm.shape_areas == {
        0: 7,
        1: 7,
        2: 7,
        3: 7,
        4: 7,
        5: 7,
    }
    assert sample_farm.regions == [
        ((4, 4), [0, 0, 0, 0, 2, 0]),
        ((12, 5), [1, 0, 1, 0, 2, 2]),
        ((12, 5), [1, 0, 1, 0, 3, 2]),
    ]

    assert sample_farm.region_count() == {"unknown": 1, "valid": 2}

    my_farm = Farm(RAW_INPUT)
    assert my_farm.regions[0] == ((40, 41), [44, 53, 34, 42, 33, 43])
    assert my_farm.regions[-1] == ((42, 47), [51, 54, 60, 48, 42, 48])
    assert my_farm.region_count() == {
        "invalid": 245,
        "unknown": 411,
        "likely_valid": 33,
        "valid": 311,
    }
    # if we go with saying we can likely get all unknown to work
    assert my_farm.guess_valid_region_count(cutoff=-1) == 311 + 33 + 411 == 755
    # but guess of 755 is too high - so some of the unknown are probably not possible
    # 344 = 311 (valid) + 33 (likely_valid) to low
    # looking - a natural cutoff seems to be having 100 extra spaces,
    # which gives 685 valid, but this answer is incorrect (don't know too low or high)
    assert my_farm.guess_valid_region_count(cutoff=100) == 685
