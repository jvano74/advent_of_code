from pathlib import Path
from collections import defaultdict
from heapq import heappush, heappop
from typing import NamedTuple


class Puzzle:
    """
    --- Day 23: A Long Walk ---
    The Elves resume water filtering operations! Clean water starts flowing over
    the edge of Island Island.

    They offer to help you go over the edge of Island Island, too! Just hold on
    tight to one end of this impossibly lng rope and they'll lower you down a
    safe distance from the massive waterfall you just created.

    As you finally reach Snow Island, you see that the water isn't really
    reaching the ground: it's being absorbed by the air itself. It looks like
    you'll finally have a little downtime while the moisture builds up to
    snow-producing levels. Snow Island is pretty scenic, even without any snow;
    why not take a walk?

    There's a map of nearby hiking trails (your puzzle input) that indicates
    paths (.), forest (#), and steep slopes (^, >, v, and <).

    For example:

    #.#####################
    #.......#########...###
    #######.#########.#.###
    ###.....#.>.>.###.#.###
    ###v#####.#v#.###.#.###
    ###.>...#.#.#.....#...#
    ###v###.#.#.#########.#
    ###...#.#.#.......#...#
    #####.#.#.#######.#.###
    #.....#.#.#.......#...#
    #.#####.#.#.#########v#
    #.#...#...#...###...>.#
    #.#.#v#######v###.###v#
    #...#.>.#...>.>.#.###.#
    #####v#.#.###v#.#.###.#
    #.....#...#...#.#.#...#
    #.#########.###.#.#.###
    #...###...#...#...#.###
    ###.###.#.###v#####v###
    #...#...#.#.>.>.#.>.###
    #.###.###.#.###.#.#v###
    #.....###...###...#...#
    #####################.#

    You're currently on the single path tile in the top row; your goal is to
    reach the single path tile in the bottom row. Because of all the mist from
    the waterfall, the slopes are probably quite icy; if you step onto a slope
    tile, your next step must be downhill (in the direction the arrow is
    pointing). To make sure you have the most scenic hike possible, never step
    onto the same tile twice. What is the longest hike you can take?

    In the example above, the longest hike you can take is marked with O, and
    your starting position is marked S:

    #S#####################
    #OOOOOOO#########...###
    #######O#########.#.###
    ###OOOOO#OOO>.###.#.###
    ###O#####O#O#.###.#.###
    ###OOOOO#O#O#.....#...#
    ###v###O#O#O#########.#
    ###...#O#O#OOOOOOO#...#
    #####.#O#O#######O#.###
    #.....#O#O#OOOOOOO#...#
    #.#####O#O#O#########v#
    #.#...#OOO#OOO###OOOOO#
    #.#.#v#######O###O###O#
    #...#.>.#...>OOO#O###O#
    #####v#.#.###v#O#O###O#
    #.....#...#...#O#O#OOO#
    #.#########.###O#O#O###
    #...###...#...#OOO#O###
    ###.###.#.###v#####O###
    #...#...#.#.>.>.#.>O###
    #.###.###.#.###.#.#O###
    #.....###...###...#OOO#
    #####################O#

    This hike contains 94 steps. (The other possible hikes you could have taken
    were 90, 86, 82, 82, and 74 steps long.)

    Find the longest hike you can take through the hiking trails listed on your
    map. How many steps long is the longest hike?

    Your puzzle answer was 2202.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    As you reach the trailhead, you realize that the ground isn't as slippery as
    you expected; you'll have no problem climbing up the steep slopes.

    Now, treat all slopes as if they were normal paths (.). You still want to
    make sure you have the most scenic hike possible, so continue to ensure that
    you never step onto the same tile twice. What is the longest hike you can
    take?

    In the example above, this increases the longest hike to 154 steps:

    #S#####################
    #OOOOOOO#########OOO###
    #######O#########O#O###
    ###OOOOO#.>OOO###O#O###
    ###O#####.#O#O###O#O###
    ###O>...#.#O#OOOOO#OOO#
    ###O###.#.#O#########O#
    ###OOO#.#.#OOOOOOO#OOO#
    #####O#.#.#######O#O###
    #OOOOO#.#.#OOOOOOO#OOO#
    #O#####.#.#O#########O#
    #O#OOO#...#OOO###...>O#
    #O#O#O#######O###.###O#
    #OOO#O>.#...>O>.#.###O#
    #####O#.#.###O#.#.###O#
    #OOOOO#...#OOO#.#.#OOO#
    #O#########O###.#.#O###
    #OOO###OOO#OOO#...#O###
    ###O###O#O###O#####O###
    #OOO#OOO#O#OOO>.#.>O###
    #O###O###O#O###.#.#O###
    #OOOOO###OOO###...#OOO#
    #####################O#

    Find the longest hike you can take through the surprisingly dry hiking
    trails listed on your map. How many steps long is the longest hike?

    Your puzzle answer was 6226.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open(Path(__file__).parent / "2023_23_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")

SAMPLE = [
    "#.#####################",
    "#.......#########...###",
    "#######.#########.#.###",
    "###.....#.>.>.###.#.###",
    "###v#####.#v#.###.#.###",
    "###.>...#.#.#.....#...#",
    "###v###.#.#.#########.#",
    "###...#.#.#.......#...#",
    "#####.#.#.#######.#.###",
    "#.....#.#.#.......#...#",
    "#.#####.#.#.#########v#",
    "#.#...#...#...###...>.#",
    "#.#.#v#######v###.###v#",
    "#...#.>.#...>.>.#.###.#",
    "#####v#.#.###v#.#.###.#",
    "#.....#...#...#.#.#...#",
    "#.#########.###.#.#.###",
    "#...###...#...#...#.###",
    "###.###.#.###v#####v###",
    "#...#...#.#.>.>.#.>.###",
    "#.###.###.#.###.#.#v###",
    "#.....###...###...#...#",
    "#####################.#",
]


class Pt(NamedTuple):
    x: int
    y: int

    def adjacent(self):
        return {
            Pt(self.x - 1, self.y),
            Pt(self.x + 1, self.y),
            Pt(self.x, self.y + 1),
            Pt(self.x, self.y - 1),
        }


class Trails:
    def __init__(self, raw_map) -> None:
        self.trail = set()
        self.hill = dict()
        self.branch = set()
        self.dead_ends = set()
        self.connections = defaultdict(dict)
        self.connections_directed = defaultdict(dict)
        self.end_y = 0
        for y, raw_row in enumerate(raw_map):
            self.end_y = max(y, self.end_y)
            for x, c in enumerate(raw_row):
                pt = Pt(x, y)
                if c == "#":
                    continue
                self.trail.add(pt)
                if c == "<":
                    self.hill[pt] = Pt(x - 1, y)
                elif c == ">":
                    self.hill[pt] = Pt(x + 1, y)
                elif c == "v":
                    self.hill[pt] = Pt(x, y + 1)
                elif c == "^":
                    self.hill[pt] = Pt(x, y - 1)
        # Further processing
        for pt in self.trail:
            branch_count = len(pt.adjacent().intersection(self.trail))
            if branch_count == 1:
                self.dead_ends.add(pt)
            elif branch_count > 2:
                self.branch.add(pt)

        for pt in self.dead_ends:
            end_pt, length = self.move_to_branch(pt)
            if end_pt:
                self.connections[pt][end_pt] = length
                self.connections[end_pt][pt] = length
                self.connections_directed[pt][end_pt] = length

        for branch_pt in self.branch:
            for pt in branch_pt.adjacent().intersection(self.trail):
                hx = set([branch_pt])
                end_pt, length = self.move_to_branch(pt, hx)
                if end_pt:
                    self.connections[branch_pt][end_pt] = length + 1
                    self.connections[end_pt][branch_pt] = length + 1
                    self.connections_directed[branch_pt][end_pt] = length + 1

    def move_to_branch(self, starting_pt, hx=None):
        pt = starting_pt
        length = 0
        if hx is None:
            hx = set()
        hx.add(pt)
        next_set = starting_pt.adjacent().intersection(self.trail) - hx
        while len(next_set) == 1:
            next_pt = next_set.pop()
            if pt in self.hill and self.hill[pt] != next_pt:
                return None, 0
            length += 1
            pt = next_pt
            hx.add(pt)
            next_set = pt.adjacent().intersection(self.trail) - hx
        return next_pt, length

    def find_longest(self, slippery=True):
        hikes = []
        boundary = []
        heappush(
            boundary,
            (
                0,
                Pt(1, 0),
                [Pt(1, 0)],
            ),
        )
        while boundary:
            (neg_length, pt, path_hx) = heappop(boundary)
            if pt.y == self.end_y:
                hikes.append(-neg_length)
            elif slippery and pt in self.hill:
                potential_pt = self.hill[pt]
                if potential_pt not in path_hx:
                    path_hx.append(potential_pt)
                    heappush(boundary, (neg_length - 1, potential_pt, path_hx))
            else:
                for potential_pt in pt.adjacent():
                    if potential_pt in self.trail and potential_pt not in path_hx:
                        new_history = path_hx[:]
                        new_history.append(potential_pt)
                        heappush(boundary, (neg_length - 1, potential_pt, new_history))
        return hikes

    def fast_find_longest(self, slippery=True):
        hikes = []
        boundary = []
        heappush(
            boundary,
            (
                0,
                Pt(1, 0),
                [Pt(1, 0)],
            ),
        )
        while boundary:
            (neg_length, pt, path_hx) = heappop(boundary)
            if pt.y == self.end_y:
                hikes.append(-neg_length)
            else:
                if slippery:
                    potential_pts = self.connections_directed[pt]
                else:
                    potential_pts = self.connections[pt]
                for potential_pt, additional_dist in potential_pts.items():
                    if potential_pt not in path_hx:
                        new_history = path_hx[:]
                        new_history.append(potential_pt)
                        heappush(
                            boundary,
                            (neg_length - additional_dist, potential_pt, new_history),
                        )
        return hikes


def test_trails():
    # Part 1
    sample_trail = Trails(SAMPLE)
    lengths = sample_trail.find_longest()
    assert max(lengths) == 94
    lengths = sample_trail.fast_find_longest()
    assert max(lengths) == 94
    # Part 2
    lengths = sample_trail.find_longest(slippery=False)
    assert max(lengths) == 154
    lengths = sample_trail.fast_find_longest(slippery=False)
    assert max(lengths) == 154

    # Part 1
    my_trail = Trails(RAW_INPUT)
    lengths = my_trail.find_longest()
    assert max(lengths) == 2202  # 2212 is too high (incorrect starting pt)
    lengths = my_trail.fast_find_longest()
    assert max(lengths) == 2202
    # Part 2
    lengths = my_trail.fast_find_longest(slippery=False)
    assert max(lengths) == 6226
