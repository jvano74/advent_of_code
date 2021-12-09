from typing import NamedTuple


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Puzzle:
    """
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents
release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that
much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your
puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is
the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent
locations. Most locations have four adjacent locations (up, down, left, and right); locations on
the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal
locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1
and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other
locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the
low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is
therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low
points on your heightmap?

To begin, get your puzzle input.

--- Part Two ---

Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every
low point has a basin, although some basins are very small. Locations of height 9 do not count
as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The
example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678

The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678

The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

Find the three largest basins and multiply their sizes together. In the above example,
this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?

    """


SAMPLE = ['2199943210', '3987894921', '9856789892', '8767896789', '9899965678']

with open('day_09_input.txt') as fp:
    INPUTS = [line.strip() for line in fp]
assert len(INPUTS) == 100
assert len(INPUTS[0]) == 100
assert len(INPUTS[-1]) == 100


class Heightmap:
    def __init__(self, heights):
        delta = [Pt(0, 1), Pt(1, 0), Pt(0, -1), Pt(-1, 0)]
        self.map = {}
        self.low_pts = {}
        self.basins = {}
        # fill map
        for y, row in enumerate(heights):
            for x, c in enumerate(row):
                self.map[Pt(x, y)] = int(c)
                # add a high boarder to simplify calculations
                if y == 0:
                    self.map[Pt(x, -1)] = 99
                if y + 1 == len(heights):
                    self.map[Pt(x, len(heights))] = 99
                if x == 0:
                    self.map[Pt(-1, y)] = 99
                if x + 1 == len(row):
                    self.map[Pt(len(row), y)] = 99
        # calculate low_pts
        for y, row in enumerate(heights):
            for x, c in enumerate(row):
                pt = Pt(x, y)
                v = self.map[pt]
                nbs = [self.map[pt + d] > v for d in delta]
                if all(nbs):
                    self.low_pts[pt] = v + 1
        # calculate basins
        for low in self.low_pts:
            self.basins[low] = {low}
            boundary = [low + d for d in delta]
            while len(boundary) > 0:
                test = boundary.pop()
                if self.map[test] < 9 and test not in self.basins[low]:
                    self.basins[low].add(test)
                    for nb in [test + d for d in delta]:
                        if self.map[test] < 9 and nb not in self.basins[low]:
                            boundary.append(nb)
        pass

    def sum_low_points(self):
        return sum(self.low_pts.values())

    def product_largest_basins(self):
        basin_size = [len(basin_set) for basin_set in self.basins.values()]
        basin_size.sort()
        return basin_size[-1] * basin_size[-2] * basin_size[-3]


def test_sum_low_points():
    sample_heightmap = Heightmap(SAMPLE)
    assert sample_heightmap.sum_low_points() == 15
    heightmap = Heightmap(INPUTS)
    assert heightmap.sum_low_points() == 532


def test_product_largest_basins():
    sample_heightmap = Heightmap(SAMPLE)
    assert sample_heightmap.product_largest_basins() == 1134
    heightmap = Heightmap(INPUTS)
    assert heightmap.product_largest_basins() == 1110780
