from pathlib import Path
from typing import NamedTuple
from collections import defaultdict
import re


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def scale(self, factor):
        return Pt(factor * self.x, factor * self.y)

    def dot(self, other):
        return other.x * self.x + other.y * self.y


def test_pt_operations():
    assert Pt(1, 3) + Pt(2, -1) == Pt(3, 2)
    assert Pt(1, 3) - Pt(2, -1) == Pt(-1, 4)
    assert Pt(1, 3).scale(2) == Pt(2, 6)
    assert Pt(1, 3).dot(Pt(3, -1)) == 0


class Sky:
    """
    --- Day 10: The Stars Align ---
    It's no use; your navigation system simply isn't capable of providing walking directions
    in the arctic circle, and certainly not in 1018.

    The Elves suggest an alternative. In times like these, North Pole rescue operations will
    arrange points of light in the sky to guide missing Elves back to base. Unfortunately,
    the message is easy to miss: the points move slowly enough that it takes hours to align
    them, but have so much momentum that they only stay aligned for a second. If you blink
    at the wrong time, it might be hours before another message appears.

    You can see these points of light floating in the distance, and record their position in
    the sky and their velocity, the relative change in position per second (your puzzle input).
    The coordinates are all given from your perspective; given enough time, those positions
    and velocities will move the points into a cohesive message!

    Rather than wait, you decide to fast-forward the process and calculate what the points
    will eventually spell.

    For example, suppose you note the following points:

    position=< 9,  1> velocity=< 0,  2>
    position=< 7,  0> velocity=<-1,  0>
    position=< 3, -2> velocity=<-1,  1>
    position=< 6, 10> velocity=<-2, -1>
    position=< 2, -4> velocity=< 2,  2>
    position=<-6, 10> velocity=< 2, -2>
    position=< 1,  8> velocity=< 1, -1>
    position=< 1,  7> velocity=< 1,  0>
    position=<-3, 11> velocity=< 1, -2>
    position=< 7,  6> velocity=<-1, -1>
    position=<-2,  3> velocity=< 1,  0>
    position=<-4,  3> velocity=< 2,  0>
    position=<10, -3> velocity=<-1,  1>
    position=< 5, 11> velocity=< 1, -2>
    position=< 4,  7> velocity=< 0, -1>
    position=< 8, -2> velocity=< 0,  1>
    position=<15,  0> velocity=<-2,  0>
    position=< 1,  6> velocity=< 1,  0>
    position=< 8,  9> velocity=< 0, -1>
    position=< 3,  3> velocity=<-1,  1>
    position=< 0,  5> velocity=< 0, -1>
    position=<-2,  2> velocity=< 2,  0>
    position=< 5, -2> velocity=< 1,  2>
    position=< 1,  4> velocity=< 2,  1>
    position=<-2,  7> velocity=< 2, -2>
    position=< 3,  6> velocity=<-1, -1>
    position=< 5,  0> velocity=< 1,  0>
    position=<-6,  0> velocity=< 2,  0>
    position=< 5,  9> velocity=< 1, -2>
    position=<14,  7> velocity=<-2,  0>
    position=<-3,  6> velocity=< 2, -1>

    Each line represents one point. Positions are given as <X, Y> pairs: X represents how far
    left (negative) or right (positive) the point appears, while Y represents how far up (negative)
    or down (positive) the point appears.

    At 0 seconds, each point has the position given. Each second, each point's velocity is added to its
    position. So, a point with velocity <1, -2> is moving to the right, but is moving upward twice as
    quickly. If this point's initial position were <3, 9>, after 3 seconds, its position would become
    <6, 3>.

    Over time, the points listed above would move like this:

    Initially:
    ........#.............
    ................#.....
    .........#.#..#.......
    ......................
    #..........#.#.......#
    ...............#......
    ....#.................
    ..#.#....#............
    .......#..............
    ......#...............
    ...#...#.#...#........
    ....#..#..#.........#.
    .......#..............
    ...........#..#.......
    #...........#.........
    ...#.......#..........

    After 1 second:
    ......................
    ......................
    ..........#....#......
    ........#.....#.......
    ..#.........#......#..
    ......................
    ......#...............
    ....##.........#......
    ......#.#.............
    .....##.##..#.........
    ........#.#...........
    ........#...#.....#...
    ..#...........#.......
    ....#.....#.#.........
    ......................
    ......................

    After 2 seconds:
    ......................
    ......................
    ......................
    ..............#.......
    ....#..#...####..#....
    ......................
    ........#....#........
    ......#.#.............
    .......#...#..........
    .......#..#..#.#......
    ....#....#.#..........
    .....#...#...##.#.....
    ........#.............
    ......................
    ......................
    ......................

    After 3 seconds:
    ......................
    ......................
    ......................
    ......................
    ......#...#..###......
    ......#...#...#.......
    ......#...#...#.......
    ......#####...#.......
    ......#...#...#.......
    ......#...#...#.......
    ......#...#...#.......
    ......#...#..###......
    ......................
    ......................
    ......................
    ......................

    After 4 seconds:
    ......................
    ......................
    ......................
    ............#.........
    ........##...#.#......
    ......#.....#..#......
    .....#..##.##.#.......
    .......##.#....#......
    ...........#....#.....
    ..............#.......
    ....#......#...#......
    .....#.....##.........
    ...............#......
    ...............#......
    ......................
    ......................

    After 3 seconds, the message appeared briefly: HI. Of course, your message will be much longer
    and will take many more seconds to appear.

    What message will eventually appear in the sky?

    --- Part Two ---
    Good thing you didn't have to wait, because that would have taken a long time - much longer than the 3 seconds
    in the example above.

    Impressed by your sub-hour communication capabilities, the Elves are curious: exactly how many seconds would
    they have needed to wait for that message to appear?
    """

    def __init__(self, starting_positions_and_velocities):
        self.velocities = []
        self.initial_positions = []
        # position=<-3,  6> velocity=< 2, -1>
        pv = re.compile(
            r"position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>"
        )
        for spv in starting_positions_and_velocities:
            matches = pv.match(spv)
            if matches:
                x, y, vx, vy = matches.groups()
                self.initial_positions.append(Pt(int(x), int(y)))
                self.velocities.append(Pt(int(vx), int(vy)))
        self.positions = self.initial_positions[:]

    def view_at_time(self, t):
        for i in range(len(self.velocities)):
            self.positions[i] = self.initial_positions[i] + self.velocities[i].scale(t)

    def star_field_size(self):
        top = max([p.y for p in self.positions])
        bottom = min([p.y for p in self.positions])
        left = min([p.x for p in self.positions])
        right = max([p.x for p in self.positions])
        return left, right, bottom, top

    def look_up(self, overlay=None):
        left, right, bottom, top = self.star_field_size()
        rows = []
        for y in range(bottom - 1, top + 2):
            row = []
            for x in range(left - 1, right + 2):
                if Pt(x, y) in self.positions:
                    if overlay is None:
                        row.append("#")
                    else:
                        row.append("{:2d}".format(overlay[Pt(x, y)]))
                else:
                    if overlay is None:
                        row.append(".")
                    else:
                        row.append(". ")
            rows.append("".join(row))
        return rows

    def find_intersection_times(self):
        times = defaultdict(int)
        pairs = [
            (i, j)
            for i in range(len(self.velocities))
            for j in range(len(self.velocities))
            if i < j
        ]
        for i, j in pairs:
            dx = self.initial_positions[j] - self.initial_positions[i]
            dv = self.velocities[j] - self.velocities[i]
            if dv != Pt(0, 0):
                t = -dx.dot(dv) // dv.dot(dv)
                times[t] += 1
        return sorted([(c, t) for t, c in times.items()], reverse=True)

    def num_of_components(self):
        component = 0
        pt_as_component = {p: 0 for p in self.positions}
        for p in self.positions:
            if pt_as_component[p] == 0:
                component += 1
                component_boundary = [p]
                while len(component_boundary) > 0:
                    explore_pt = component_boundary.pop()
                    pt_as_component[explore_pt] = component
                    for d in [Pt(-1, 0), Pt(1, 0), Pt(0, 1), Pt(0, -1)]:
                        new_p = explore_pt + d
                        if new_p in pt_as_component and pt_as_component[new_p] == 0:
                            component_boundary.append(new_p)
        return component, pt_as_component


with open(Path(__file__).parent / "2018_10_sample.txt") as fp:
    SAMPLE = [line.strip() for line in fp]


with open(Path(__file__).parent / "2018_10_input.txt") as fp:
    INPUT = [line.strip() for line in fp]


def test_start():
    sample = Sky(SAMPLE)
    times = sample.find_intersection_times()
    print()
    print(times)
    for t in range(1, 5):
        sample.view_at_time(t)
        sz, overlay = sample.num_of_components()
        print()
        print(f"at time {t} has size {sz}")
        print("\n".join(sample.look_up(overlay)))
    assert True


def test_part1():
    sample = Sky(INPUT)
    times = sample.find_intersection_times()
    print()
    print(times)
    time = times[0][1]
    sample.view_at_time(time)
    answer = "\n".join(sample.look_up())
    # sz, overlay = sample.num_of_components()
    # print(f'at time {time} has size {sz}')
    # answer = '\n'.join(sample.look_up(overlay))
    answer = f"\n{answer}"
    print()
    print(answer)
    assert (
        answer
        == """
................................................................
..####...######..#....#..#....#...####....####....####...#....#.
.#....#..#.......##...#..#...#...#....#..#....#..#....#..#....#.
.#.......#.......##...#..#..#....#.......#.......#.......#....#.
.#.......#.......#.#..#..#.#.....#.......#.......#.......#....#.
.#.......#####...#.#..#..##......#.......#.......#.......######.
.#..###..#.......#..#.#..##......#.......#..###..#..###..#....#.
.#....#..#.......#..#.#..#.#.....#.......#....#..#....#..#....#.
.#....#..#.......#...##..#..#....#.......#....#..#....#..#....#.
.#...##..#.......#...##..#...#...#....#..#...##..#...##..#....#.
..###.#..#.......#....#..#....#...####....###.#...###.#..#....#.
................................................................"""
    )
    # Your puzzle answer was GFNKCGGH.
    assert time == 10274
