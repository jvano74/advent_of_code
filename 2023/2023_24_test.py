from pathlib import Path
from typing import NamedTuple
from fractions import Fraction
from operator import sub


class Puzzle:
    """
    --- Day 24: Never Tell Me The Odds ---
    It seems like something is going wrong with the snow-making process. Instead
    of forming snow, the water that's been absorbed into the air seems to be
    forming hail!

    Maybe there's something you can do to break up the hailstones?

    Due to strong, probably-magical winds, the hailstones are all flying through
    the air in perfectly linear trajectories. You make a note of each
    hailstone's position and velocity (your puzzle input). For example:

    19, 13, 30 @ -2,  1, -2
    18, 19, 22 @ -1, -1, -2
    20, 25, 34 @ -2, -2, -4
    12, 31, 28 @ -1, -2, -1
    20, 19, 15 @  1, -5, -3

    Each line of text corresponds to the position and velocity of a single
    hailstone. The positions indicate where the hailstones are right now (at
    time 0). The velocities are constant and indicate exactly how far each
    hailstone will move in one nanosecond.

    Each line of text uses the format px py pz @ vx vy vz. For instance, the
    hailstone specified by 20, 19, 15 @ 1, -5, -3 has initial X position 20, Y
    position 19, Z position 15, X velocity 1, Y velocity -5, and Z velocity -3.
    After one nanosecond, the hailstone would be at 21, 14, 12.

    Perhaps you won't have to do anything. How likely are the hailstones to
    collide with each other and smash into tiny ice crystals?

    To estimate this, consider only the X and Y axes; ignore the Z axis. Looking
    forward in time, how many of the hailstones' paths will intersect within a
    test area? (The hailstones themselves don't have to collide, just test for
    intersections between the paths they will trace.)

    In this example, look for intersections that happen with an X and Y position
    each at least 7 and at most 27; in your actual data, you'll need to check a
    much larger test area. Comparing all pairs of hailstones' future paths
    produces the following results:

    Hailstone A: 19, 13, 30 @ -2, 1, -2
    Hailstone B: 18, 19, 22 @ -1, -1, -2

    Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

    Hailstone A: 19, 13, 30 @ -2, 1, -2
    Hailstone B: 20, 25, 34 @ -2, -2, -4

    Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).

    Hailstone A: 19, 13, 30 @ -2, 1, -2
    Hailstone B: 12, 31, 28 @ -1, -2, -1

    Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).

    Hailstone A: 19, 13, 30 @ -2, 1, -2
    Hailstone B: 20, 19, 15 @ 1, -5, -3

    Hailstones' paths crossed in the past for hailstone A.

    Hailstone A: 18, 19, 22 @ -1, -1, -2
    Hailstone B: 20, 25, 34 @ -2, -2, -4

    Hailstones' paths are parallel; they never intersect.

    Hailstone A: 18, 19, 22 @ -1, -1, -2
    Hailstone B: 12, 31, 28 @ -1, -2, -1

    Hailstones' paths will cross outside the test area (at x=-6, y=-5).

    Hailstone A: 18, 19, 22 @ -1, -1, -2
    Hailstone B: 20, 19, 15 @ 1, -5, -3

    Hailstones' paths crossed in the past for both hailstones.

    Hailstone A: 20, 25, 34 @ -2, -2, -4
    Hailstone B: 12, 31, 28 @ -1, -2, -1

    Hailstones' paths will cross outside the test area (at x=-2, y=3).

    Hailstone A: 20, 25, 34 @ -2, -2, -4
    Hailstone B: 20, 19, 15 @ 1, -5, -3

    Hailstones' paths crossed in the past for hailstone B.

    Hailstone A: 12, 31, 28 @ -1, -2, -1
    Hailstone B: 20, 19, 15 @ 1, -5, -3
    Hailstones' paths crossed in the past for both hailstones.

    So, in this example, 2 hailstones' future paths cross inside the boundaries
    of the test area.

    However, you'll need to search a much larger test area if you want to see if
    any hailstones might collide. Look for intersections that happen with an X
    and Y position each at least 200000000000000 and at most 400000000000000.
    Disregard the Z axis entirely.

    Considering only the X and Y axes, check all pairs of hailstones' future
    paths for intersections. How many of these intersections occur within the
    test area?

    Your puzzle answer was 17867.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    Upon further analysis, it doesn't seem like any hailstones will naturally
    collide. It's up to you to fix that!

    You find a rock on the ground nearby. While it seems extremely unlikely, if
    you throw it just right, you should be able to hit every hailstone in a
    single throw!

    You can use the probably-magical winds to reach any integer position you
    like and to propel the rock at any integer velocity. Now including the Z
    axis in your calculations, if you throw the rock at time 0, where do you
    need to be so that the rock perfectly collides with every hailstone? Due to
    probably-magical inertia, the rock won't slow down or change direction when
    it collides with a hailstone.

    In the example above, you can achieve this by moving to position 24, 13, 10
    and throwing the rock at velocity -3, 1, 2. If you do this, you will hit
    every hailstone as follows:

    Hailstone: 19, 13, 30 @ -2, 1, -2
    Collision time: 5
    Collision position: 9, 18, 20

    Hailstone: 18, 19, 22 @ -1, -1, -2
    Collision time: 3
    Collision position: 15, 16, 16

    Hailstone: 20, 25, 34 @ -2, -2, -4
    Collision time: 4
    Collision position: 12, 17, 18

    Hailstone: 12, 31, 28 @ -1, -2, -1
    Collision time: 6
    Collision position: 6, 19, 22

    Hailstone: 20, 19, 15 @ 1, -5, -3
    Collision time: 1
    Collision position: 21, 14, 12

    Above, each hailstone is identified by its initial position and its
    velocity. Then, the time and position of that hailstone's collision with
    your rock are given.

    After 1 nanosecond, the rock has exactly the same position as one of the
    hailstones, obliterating it into ice dust! Another hailstone is smashed to
    bits two nanoseconds after that. After a total of 6 nanoseconds, all of the
    hailstones have been destroyed.

    So, at time 0, the rock needs to be at X position 24, Y position 13, and Z
    position 10. Adding these three coordinates together produces 47. (Don't add
    any coordinates from the rock's velocity.)

    Determine the exact position and velocity the rock needs to have at time 0
    so that it perfectly collides with every hailstone. What do you get if you
    add up the X, Y, and Z coordinates of that initial position?

    Your puzzle answer was 557743507346379.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


SAMPLE = [
    "19, 13, 30 @ -2,  1, -2",
    "18, 19, 22 @ -1, -1, -2",
    "20, 25, 34 @ -2, -2, -4",
    "12, 31, 28 @ -1, -2, -1",
    "20, 19, 15 @  1, -5, -3",
]

with open(Path(__file__).parent / "2023_24_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")


class PV(NamedTuple):
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    @property
    def p(self):
        return self.x, self.y, self.z

    @property
    def v(self):
        return self.dx, self.dy, self.dz

    @classmethod
    def from_string(cls, raw_str):
        raw_p, raw_v = raw_str.split(" @ ")
        x, y, z = (int(d) for d in raw_p.split(", "))
        dx, dy, dz = (int(d) for d in raw_v.split(", "))
        return cls(x, y, z, dx, dy, dz)


def cross(v_i, v_j):
    return [
        v_i[1] * v_j[2] - v_i[2] * v_j[1],
        v_i[2] * v_j[0] - v_i[0] * v_j[2],
        v_i[0] * v_j[1] - v_i[1] * v_j[0],
    ]


def intersect_xy(a: PV, b: PV, x_min, x_max, y_min, y_max):
    desc_x = a.dx * b.dy - b.dx * a.dy
    num_x = a.dx * b.dy * b.x - b.dx * a.dy * a.x + a.dx * b.dx * (a.y - b.y)
    if desc_x < 0:
        num_x *= -1
        desc_x *= -1
    if not (x_min * desc_x <= num_x <= x_max * desc_x):
        return False
    # Check for positive time
    if (a.dx > 0 and num_x < a.x * desc_x) or (a.dx < 0 and num_x > a.x * desc_x):
        return False
    if (b.dx > 0 and num_x < b.x * desc_x) or (b.dx < 0 and num_x > b.x * desc_x):
        return False
    desc_y = a.dy * b.dx - b.dy * a.dx
    num_y = a.dy * b.dx * b.y - b.dy * a.dx * a.y + a.dy * b.dy * (a.x - b.x)
    if desc_y < 0:
        num_y *= -1
        desc_y *= -1
    if not (y_min * desc_y <= num_y <= y_max * desc_y):
        return False
    return True


def check_intersections(pvs, x_min, x_max, y_min, y_max):
    hx = set()
    intersections = []
    for a in pvs:
        hx.add(a)
        for b in pvs:
            if b not in hx and intersect_xy(
                a, b, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max
            ):
                # print(f"{a=}, {b=} PASS")
                intersections.append((a, b))
    return len(intersections)


################################################################################
#                                                                              #
# NOTE: For part 2 ended up basically copying solution from                    #
# https://github.com/jmd-dk/advent-of-code/blob/main/2023/solution/24/solve.py #
#                                                                              #
################################################################################


def construct_system(hails):
    matrix = []
    b = []
    for i in range(2):
        j = i + 1
        hail_i, hail_j = hails[i], hails[j]
        b += list(
            map(
                sub,
                cross(hail_i.p, hail_i.v),
                cross(hail_j.p, hail_j.v),
            )
        )[::-1]

        row_v = [+(hail_i.v[1] - hail_j.v[1]), -(hail_i.v[0] - hail_j.v[0]), 0]
        row_p = [-(hail_i.p[1] - hail_j.p[1]), +(hail_i.p[0] - hail_j.p[0]), 0]
        matrix.append(row_v + row_p)

        row_v = [-(hail_i.v[2] - hail_j.v[2]), 0, +(hail_i.v[0] - hail_j.v[0])]
        row_p = [+(hail_i.p[2] - hail_j.p[2]), 0, -(hail_i.p[0] - hail_j.p[0])]
        matrix.append(row_v + row_p)

        row_v = [0, +(hail_i.v[2] - hail_j.v[2]), -(hail_i.v[1] - hail_j.v[1])]
        row_p = [0, -(hail_i.p[2] - hail_j.p[2]), +(hail_i.p[1] - hail_j.p[1])]
        matrix.append(row_v + row_p)

    augment(matrix, b)
    return matrix


def augment(matrix, b):
    for row, el in zip(matrix, b):
        row.append(el)


def gauss(matrix):
    n = len(matrix)
    for i in range(n):
        i_pivot = i
        pivot = matrix[i_pivot][i]
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > pivot:
                pivot = matrix[j][i]
                i_pivot = j
        if matrix[i][i_pivot] == 0:
            return True
        for j in range(n + 1):
            matrix[i][j], matrix[i_pivot][j] = matrix[i_pivot][j], matrix[i][j]
        for j in range(i + 1, n):
            ratio = matrix[j][i] / matrix[i][i]
            for k in range(i + 1, n + 1):
                matrix[j][k] -= matrix[i][k] * ratio
            matrix[j][i] = 0


def back_substitute(matrix):
    n = len(matrix)
    x = [None for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = (
            matrix[i][n] - sum(matrix[i][j] * x[j] for j in range(i + 1, n))
        ) / matrix[i][i]
    return x


def solve_part2(sample):
    matrix = construct_system(sample)
    for row in matrix:
        for i, el in enumerate(row):
            row[i] = Fraction(el)
        if gauss(matrix):
            return
        return type(sample[0])(*back_substitute((matrix)))


def test_intersections():
    sample_paths = [PV.from_string(s) for s in SAMPLE]
    results = check_intersections(sample_paths, x_min=7, x_max=27, y_min=7, y_max=27)
    assert results == 2
    part2 = solve_part2([sample_paths[0], sample_paths[1], sample_paths[2]])
    assert sum(part2.p) == 47

    my_paths = [PV.from_string(s) for s in RAW_INPUT]
    results = check_intersections(
        my_paths,
        x_min=200000000000000,
        x_max=400000000000000,
        y_min=200000000000000,
        y_max=400000000000000,
    )
    assert results == 17867
    part2 = solve_part2([my_paths[0], my_paths[10], my_paths[12]])
    assert sum(part2.p) == 557743507346379
