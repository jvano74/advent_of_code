from heapq import heappush, heappop
from typing import NamedTuple


class Puzzle:
    """
    --- Day 17: Clumsy Crucible ---
    The lava starts flowing rapidly once the Lava Production Facility is
    operational. As you leave, the reindeer offers you a parachute, allowing you
    to quickly reach Gear Island.

    As you descend, your bird's-eye view of Gear Island reveals why you had
    trouble finding anyone on your way up: half of Gear Island is empty, but the
    half below you is a giant factory city!

    You land near the gradually-filling pool of lava at the base of your new
    lavafall. Lavaducts will eventually carry the lava throughout the city, but
    to make use of it immediately, Elves are loading it into large crucibles on
    wheels.

    The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles
    become very difficult to steer at high speeds, and so it can be hard to go
    in a straight line for very long.

    To get Desert Island the machine parts it needs as soon as possible, you'll
    need to find the best way to get the crucible from the lava pool to the
    machine parts factory. To do this, you need to minimize heat loss while
    choosing a route that doesn't require the crucible to go in a straight line
    for too long.

    Fortunately, the Elves here have a map (your puzzle input) that uses traffic
    patterns, ambient temperature, and hundreds of other parameters to calculate
    exactly how much heat loss can be expected for a crucible entering any
    particular city block.

    For example:

    2413432311323
    3215453535623
    3255245654254
    3446585845452
    4546657867536
    1438598798454
    4457876987766
    3637877979653
    4654967986887
    4564679986453
    1224686865563
    2546548887735
    4322674655533

    Each city block is marked by a single digit that represents the amount of
    heat loss if the crucible enters that block. The starting point, the lava
    pool, is the top-left city block; the destination, the machine parts
    factory, is the bottom-right city block. (Because you already start in the
    top-left block, you don't incur that block's heat loss unless you leave that
    block and then return to it.)

    Because it is difficult to keep the top-heavy crucible going in a straight
    line for very long, it can move at most three blocks in a single direction
    before it must turn 90 degrees left or right. The crucible also can't
    reverse direction; after entering each city block, it may only turn left,
    continue straight, or turn right.

    One way to minimize heat loss is this path:

    2>>34^>>>1323
    32v>>>35v5623
    32552456v>>54
    3446585845v52
    4546657867v>6
    14385987984v4
    44578769877v6
    36378779796v>
    465496798688v
    456467998645v
    12246868655<v
    25465488877v5
    43226746555v>

    This path never moves more than three consecutive blocks in the same
    direction and incurs a heat loss of only 102.

    Directing the crucible from the lava pool to the machine parts factory, but
    not moving more than three consecutive blocks in the same direction, what is
    the least heat loss it can incur?

    Your puzzle answer was 1138.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The crucibles of lava simply aren't large enough to provide an adequate
    supply of lava to the machine parts factory. Instead, the Elves are going to
    upgrade to ultra crucibles.

    Ultra crucibles are even more difficult to steer than normal crucibles. Not
    only do they have trouble going in a straight line, but they also have
    trouble turning!

    Once an ultra crucible starts moving in a direction, it needs to move a
    minimum of four blocks in that direction before it can turn (or even before
    it can stop at the end). However, it will eventually start to get wobbly: an
    ultra crucible can move a maximum of ten consecutive blocks without turning.

    In the above example, an ultra crucible could follow this path to minimize
    heat loss:

    2>>>>>>>>1323
    32154535v5623
    32552456v4254
    34465858v5452
    45466578v>>>>
    143859879845v
    445787698776v
    363787797965v
    465496798688v
    456467998645v
    122468686556v
    254654888773v
    432267465553v

    In the above example, an ultra crucible would incur the minimum possible
    heat loss of 94.

    Here's another example:

    111111111111
    999999999991
    999999999991
    999999999991
    999999999991

    Sadly, an ultra crucible would need to take an unfortunate path like this
    one:

    1>>>>>>>1111
    9999999v9991
    9999999v9991
    9999999v9991
    9999999v>>>>

    This route causes the ultra crucible to incur the minimum possible heat loss
    of 71.

    Directing the ultra crucible from the lava pool to the machine parts
    factory, what is the least heat loss it can incur?

    """


with open("day_17_input.txt") as fp:
    MY_INPUT = fp.read().split("\n")

SAMPLE = [
    "2413432311323",
    "3215453535623",
    "3255245654254",
    "3446585845452",
    "4546657867536",
    "1438598798454",
    "4457876987766",
    "3637877979653",
    "4654967986887",
    "4564679986453",
    "1224686865563",
    "2546548887735",
    "4322674655533",
]

SAMPLE_2 = [
    "111111111111",
    "999999999991",
    "999999999991",
    "999999999991",
    "999999999991",
]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


LEFT = {
    Pt(1, 0): Pt(0, -1),
    Pt(0, -1): Pt(-1, 0),
    Pt(-1, 0): Pt(0, 1),
    Pt(0, 1): Pt(1, 0),
}

RIGHT = {
    Pt(1, 0): Pt(0, 1),
    Pt(0, 1): Pt(-1, 0),
    Pt(-1, 0): Pt(0, -1),
    Pt(0, -1): Pt(1, 0),
}


class V(NamedTuple):
    p: Pt
    v: Pt

    def fwd(self):
        return V(self.p + self.v, self.v)

    def left(self):
        new_v = LEFT[self.v]
        return V(self.p + new_v, new_v)

    def right(self):
        new_v = RIGHT[self.v]
        return V(self.p + new_v, new_v)


class Path:
    def __init__(self, heat_loss) -> None:
        self.heat_loss = dict()
        self.x_max = 0
        self.y_max = 0
        for y, row in enumerate(heat_loss):
            self.y_max = max(y, self.y_max)
            for x, loss in enumerate(row):
                self.x_max = max(x, self.x_max)
                self.heat_loss[Pt(x, y)] = int(loss)

    def find_least_heat_loss_path(
        self, start: V = None, end: Pt = None, ultra=False
    ) -> int:
        if start is None:
            start = V(Pt(0, 0), Pt(1, 0))
        if end is None:
            end = Pt(self.x_max, self.y_max)
        partial_paths = []
        history = set()
        min_turn = 4 if ultra else 0
        max_straight = 10 if ultra else 3

        heappush(partial_paths, (0, start, 0))
        history.add((start, 0))
        while partial_paths:
            lost_heat, current_v, turn_timer = heappop(partial_paths)
            # fwd
            if turn_timer < max_straight:
                next_v = current_v.fwd()
                if next_v.p == end and min_turn < turn_timer + 1:
                    return lost_heat + self.heat_loss[next_v.p]
                if (
                    next_v,
                    turn_timer + 1,
                ) not in history and next_v.p in self.heat_loss:
                    history.add((next_v, turn_timer + 1))
                    heappush(
                        partial_paths,
                        (
                            lost_heat + self.heat_loss[next_v.p],
                            next_v,
                            turn_timer + 1,
                        ),
                    )
            # left and right
            if min_turn < turn_timer:
                for next_v in [current_v.left(), current_v.right()]:
                    if next_v.p == end and not ultra:
                        return lost_heat + self.heat_loss[next_v.p]
                    if (next_v, 1) not in history and next_v.p in self.heat_loss:
                        history.add((next_v, 1))
                        heappush(
                            partial_paths,
                            (
                                lost_heat + self.heat_loss[next_v.p],
                                next_v,
                                1,
                            ),
                        )


def test_path():
    # part 1
    sample_path = Path(SAMPLE)
    min_heat_loss = sample_path.find_least_heat_loss_path()
    assert min_heat_loss == 102
    # part 2
    sample_path_2 = Path(SAMPLE_2)
    min_heat_loss = sample_path_2.find_least_heat_loss_path(ultra=True)
    print(min_heat_loss)

    min_heat_loss = sample_path.find_least_heat_loss_path(ultra=True)
    print(min_heat_loss)

    my_path = Path(MY_INPUT)
    min_heat_loss = my_path.find_least_heat_loss_path()
    # 1169 was too high (some bugs), 1138 is correct
    assert min_heat_loss == 1138
    min_heat_loss = my_path.find_least_heat_loss_path(ultra=True)
    print(min_heat_loss)
    # 1291 was too low


test_path()
