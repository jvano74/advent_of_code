from pathlib import Path
from typing import NamedTuple
from collections import defaultdict
import numpy as np
import re


class Puzzle:
    """
    --- Day 23: Experimental Emergency Teleportation ---
    Using your torch to search the darkness of the rocky cavern, you finally locate the man's friend: a small reindeer.

    You're not sure how it got so far in this cave. It looks sick - too sick to walk - and too heavy for you to carry
    all the way back. Sleighs won't be invented for another 1500 years, of course.

    The only option is experimental emergency teleportation.

    You hit the "experimental emergency teleportation" button on the device and push I accept the risk on no fewer
    than 18 different warning messages. Immediately, the device deploys hundreds of tiny nanobots which fly around
    the cavern, apparently assembling themselves into a very specific formation. The device lists the X,Y,Z
    position (pos) for each nanobot as well as its signal radius (r) on its tiny screen (your puzzle input).

    Each nanobot can transmit signals to any integer coordinate which is a distance away from it less than or equal
    to its signal radius (as measured by Manhattan distance). Coordinates a distance away of less than or equal to
    a nanobot's signal radius are said to be in range of that nanobot.

    Before you start the teleportation process, you should determine which nanobot is the strongest (that is, which
    has the largest signal radius) and then, for that nanobot, the total number of nanobots that are in range of it,
    including itself.

    For example, given the following nanobots:

    pos=<0,0,0>, r=4
    pos=<1,0,0>, r=1
    pos=<4,0,0>, r=3
    pos=<0,2,0>, r=1
    pos=<0,5,0>, r=3
    pos=<0,0,3>, r=1
    pos=<1,1,1>, r=1
    pos=<1,1,2>, r=1
    pos=<1,3,1>, r=1

    The strongest nanobot is the first one (position 0,0,0) because its signal radius, 4 is the largest. Using that
    nanobot's location and signal radius, the following nanobots are in or out of range:

    The nanobot at 0,0,0 is distance 0 away, and so it is in range.
    The nanobot at 1,0,0 is distance 1 away, and so it is in range.
    The nanobot at 4,0,0 is distance 4 away, and so it is in range.
    The nanobot at 0,2,0 is distance 2 away, and so it is in range.
    The nanobot at 0,5,0 is distance 5 away, and so it is not in range.
    The nanobot at 0,0,3 is distance 3 away, and so it is in range.
    The nanobot at 1,1,1 is distance 3 away, and so it is in range.
    The nanobot at 1,1,2 is distance 4 away, and so it is in range.
    The nanobot at 1,3,1 is distance 5 away, and so it is not in range.

    In this example, in total, 7 nanobots are in range of the nanobot with the largest signal radius.

    Find the nanobot with the largest signal radius. How many nanobots are in range of its signals?

    --- Part Two ---
    Now, you just need to figure out where to position yourself so that you're actually teleported when the
    nanobots activate.

    To increase the probability of success, you need to find the coordinate which puts you in range of the largest
    number of nanobots. If there are multiple, choose one closest to your position (0,0,0, measured by manhattan
    distance).

    For example, given the following nanobot formation:

    pos=<10,12,12>, r=2
    pos=<12,14,12>, r=2
    pos=<16,12,12>, r=4
    pos=<14,14,14>, r=6
    pos=<50,50,50>, r=200
    pos=<10,10,10>, r=5

    Many coordinates are in range of some of the nanobots in this formation. However, only the coordinate 12,12,12 is
    in range of the most nanobots: it is in range of the first five, but is not in range of the nanobot at 10,10,10.
    (All other coordinates are in range of fewer than five nanobots.) This coordinate's distance from 0,0,0 is 36.

    Find the coordinates that are in range of the largest number of nanobots. What is the shortest manhattan distance
    between any of those points and 0,0,0?
    """

    pass


with open(Path(__file__).parent / "2018_23_input.txt") as fp:
    INPUTS = [ln.strip() for ln in fp]


class Pt(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y, self.z + other.z)

    def distance_from(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


def parse_input(inputs):
    bots = {}
    for line in inputs:
        """
        Format
        pos=<46996129,9836603,55545536>, r=52259660
        """
        digits = re.findall(r"(-?\d+)", line)
        x, y, z, r = [int(d) for d in digits]
        bots[Pt(x, y, z)] = r
    return bots


def test_parse_input():
    bots = parse_input(INPUTS)
    assert len(bots) == 1000
    assert bots[Pt(46996129, 9836603, 55545536)] == 52259660
    assert bots[Pt(-32703529, 41373674, 38773710)] == 91253877

    print()

    hist, bin_edges = np.histogram([r for pt, r in bots.items()])
    print("r values")
    print(hist)
    print(bin_edges)

    hist, bin_edges = np.histogram([pt.x for pt, r in bots.items()])
    print("x values")
    print(hist)
    print(bin_edges)

    hist, bin_edges = np.histogram([pt.y for pt, r in bots.items()])
    print("y values")
    print(hist)
    print(bin_edges)

    hist, bin_edges = np.histogram([pt.z for pt, r in bots.items()])
    print("z values")
    print(hist)
    print(bin_edges)

    assert True


def test_puzzle_1():
    bots = parse_input(INPUTS)
    max_radius = max(bots.values())
    assert max_radius == 99487886
    max_bots = [pt for pt, r in bots.items() if r == max_radius]
    assert len(max_bots) == 1
    max_bot = max_bots[0]
    in_range = [1 for pt in bots if max_bot.distance_from(pt) <= max_radius]
    assert len(in_range) == 935


class Bot(NamedTuple):
    loc: Pt
    r: int

    def region(self):
        ppp = self.loc.x + self.loc.y + self.loc.z
        ppm = self.loc.x + self.loc.y - self.loc.z
        pmp = self.loc.x - self.loc.y + self.loc.z
        pmm = self.loc.x - self.loc.y - self.loc.z

        return Region(
            R(ppp - self.r, ppp + self.r),
            R(ppm - self.r, ppm + self.r),
            R(pmp - self.r, pmp + self.r),
            R(pmm - self.r, pmm + self.r),
        )

    def rectangle(self):
        mins = Pt(self.loc.x - self.r, self.loc.y - self.r, self.loc.z - self.r)
        maxs = Pt(self.loc.x + self.r, self.loc.y + self.r, self.loc.z + self.r)
        return Parallelogram(mins, maxs)


class R(NamedTuple):
    min: int
    max: int

    def contains(self, item):
        if self.min <= item <= self.max:
            return True
        return False


class Region(NamedTuple):
    ppp: R
    ppm: R
    pmp: R
    pmm: R

    def contains_pt(self, pt):
        if not self.ppp.contains(pt.x + pt.y + pt.z):
            return False
        if not self.ppm.contains(pt.x + pt.y - pt.z):
            return False
        if not self.pmp.contains(pt.x - pt.y + pt.z):
            return False
        if not self.pmm.contains(pt.x - pt.y - pt.z):
            return False
        return True

    @staticmethod
    def region_count(ranges):
        delta = defaultdict(int)
        for p in ranges:
            delta[p.min] += 1
            delta[p.max + 1] -= 1
        in_region = {}
        total = 0
        prev_x = None
        for x, v in sorted(delta.items()):
            in_region[(prev_x, x)] = total
            total += v
            prev_x = x
        in_region[(prev_x, None)] = total
        return in_region

    @staticmethod
    def count_intersection(set_of_regions):
        oppp = Region.region_count(r.ppp for r in set_of_regions)
        oppm = Region.region_count(r.ppm for r in set_of_regions)
        opmp = Region.region_count(r.pmp for r in set_of_regions)
        opmm = Region.region_count(r.pmm for r in set_of_regions)

        return oppp, oppm, opmp, opmm

    @staticmethod
    def overlap(ranges):
        set_of_ranges = {p for p in ranges}
        new_min = max(p.min for p in set_of_ranges)
        new_max = min(p.max for p in set_of_ranges)
        if new_min > new_max:
            return None
        return R(new_min, new_max)

    @staticmethod
    def intersection(set_of_regions):
        if len(set_of_regions) == 0:
            return None

        oppp = Region.overlap(r.ppp for r in set_of_regions)
        if oppp is None:
            return None

        oppm = Region.overlap(r.ppm for r in set_of_regions)
        if oppm is None:
            return None

        opmp = Region.overlap(r.pmp for r in set_of_regions)
        if opmp is None:
            return None

        opmm = Region.overlap(r.pmm for r in set_of_regions)
        if opmm is None:
            return None

        return Region(oppp, oppm, opmp, opmm)


class Parallelogram(NamedTuple):
    mins: Pt
    maxs: Pt

    def contains_pt(self, pt):
        if not self.mins.x <= pt.x <= self.maxs.x:
            return False
        if not self.mins.y <= pt.y <= self.maxs.y:
            return False
        if not self.mins.z <= pt.z <= self.maxs.z:
            return False
        return True

    @staticmethod
    def overlap(min1, max1, min2, max2):
        new_min = max([min1, min2])
        new_max = min([max1, max2])
        if new_min > new_max:
            return None
        return new_min, new_max

    def intersection(self, other):
        ox = Parallelogram.overlap(self.mins.x, self.maxs.x, other.mins.x, other.maxs.x)
        if ox is None:
            return None
        oy = Parallelogram.overlap(self.mins.y, self.maxs.y, other.mins.y, other.maxs.y)
        if oy is None:
            return None
        oz = Parallelogram.overlap(self.mins.z, self.maxs.z, other.mins.z, other.maxs.z)
        if oz is None:
            return None
        return Parallelogram(Pt(ox[0], oy[0], oz[0]), Pt(ox[1], oy[1], oz[1]))


def test_parallelogram():
    r1 = Parallelogram(Pt(0, 0, 0), Pt(10, 2, 2))
    r2 = Parallelogram(Pt(-2, 1, -1), Pt(15, 2, 5))
    both = r1.intersection(r2)
    assert both == Parallelogram(mins=Pt(x=0, y=1, z=0), maxs=Pt(x=10, y=2, z=2))
    assert r1.contains_pt(Pt(0, 1, 0))
    assert r2.contains_pt(Pt(0, 1, 0))
    assert r1.contains_pt(Pt(10, 2, 2))
    assert r2.contains_pt(Pt(10, 2, 2))


class MaxIntersection:
    def __init__(self, bots):
        self.bots = bots
        self.num_initial_regions = len(bots)
        self.initial_regions = [Bot(pt, r).region() for pt, r in bots.items()]

    def points_in_range(self, pt):
        return sum(1 for c, r in self.bots.items() if c.distance_from(pt) <= r)

    def count_intersection(self):
        regions = Region.count_intersection(self.initial_regions)
        new_regions = []
        for r in regions:
            max_num = max(v for v in r.values())
            new_regions.append({x: v for x, v in r.items() if v == max_num})
        return new_regions

    def set_intersection_empty(self, region_ids):
        if len(region_ids) == 0:
            return True
        regions = {self.initial_regions[s] for s in region_ids}
        region = Region.intersection(regions)
        if region is None:
            return True
        return False

    def build_intersections(self):
        all_regions = frozenset({i for i in range(self.num_initial_regions)})
        interested_regions = {all_regions}
        found_regions = set()
        while len(interested_regions) > 0:
            next_regions = set()
            for composition in interested_regions:
                for i in composition:
                    if self.set_intersection_empty(composition - {i}):
                        next_regions.add(composition - {i})
                    else:
                        found_regions.add(composition - {i})
            if len(found_regions) > 0:
                return found_regions
            interested_regions = next_regions
        return {}


SAMPLE = [
    "pos=<10,12,12>, r=2",
    "pos=<12,14,12>, r=2",
    "pos=<16,12,12>, r=4",
    "pos=<14,14,14>, r=6",
    "pos=<50,50,50>, r=200",
    "pos=<10,10,10>, r=5",
]


def find_xyz(ppp, ppm, pmp, pmm):
    """
    ppp = x + y + z
    ppm = x + y - z
    pmp = x - y + z
    pmm = x - y - z
    """
    z = (ppp - ppm) // 2
    y = (ppp - pmp) // 2
    x = (ppp + pmm) // 2
    return Pt(x, y, z)


def test_build_intersections():
    max_intersection = MaxIntersection(parse_input(SAMPLE))
    interested_regions = max_intersection.build_intersections()
    assert interested_regions == {frozenset({0, 1, 2, 3, 4})}
    assert max_intersection.count_intersection() == [
        {(36, 37): 5},
        {(12, 13): 6},
        {(12, 13): 6},
        {(-12, -11): 6},
    ]
    assert find_xyz(36, 12, 12, -12) == (12, 12, 12)

    max_intersection = MaxIntersection(parse_input(INPUTS))
    assert max_intersection.count_intersection() == [
        {(138697281, 138697284): 981},
        {(53546326, 53546328): 980},
        {(53739757, 53739759): 980},
        {(-31411197, -31411195): 982},
    ]
    pts = set()
    for ppp in range(138697281, 138697284):
        for ppm in range(53546326, 53546328):
            for pmp in range(53739757, 53739759):
                for pmm in range(-31411197, -31411195):
                    pts.add(find_xyz(ppp, ppm, pmp, pmm))
    assert {p: max_intersection.points_in_range(p) for p in pts} == {
        Pt(x=53643042, y=42478761, z=42575477): 972,
        Pt(x=53643042, y=42478762, z=42575477): 976,
        Pt(x=53643042, y=42478762, z=42575478): 973,
        Pt(x=53643043, y=42478762, z=42575477): 972,
        Pt(x=53643043, y=42478762, z=42575478): 975,
        Pt(x=53643043, y=42478763, z=42575478): 968,
    }
    assert 53643042 + 42478762 + 42575477 == 138697281
