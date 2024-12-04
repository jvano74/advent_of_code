from typing import NamedTuple


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Target(NamedTuple):
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def hit(self, p):
        return self.x_min <= p.x <= self.x_max and self.y_min <= p.y <= self.y_max


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Puzzle:
    """
--- Day 17: Trick Shot ---
You finally decode the Elves' message. HI, the message says. You continue searching for the sleigh keys.

Ahead of you is what appears to be a large ocean trench. Could the keys have fallen into it?
You'd better send a probe to investigate.

The probe launcher on your submarine can fire the probe with any integer velocity in
the x (forward) and y (upward, or downward if negative) directions. For example, an initial x,y velocity
like 0,10 would fire the probe straight up, while an initial velocity like 10,-1 would fire the probe
forward at a slight downward angle.

The probe's x,y position starts at 0,0. Then, it will follow some trajectory by moving in steps. On each
step, these changes occur in the following order:

- The probe's x position increases by its x velocity.
- The probe's y position increases by its y velocity.
- Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if
  it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
- Due to gravity, the probe's y velocity decreases by 1.

For the probe to successfully make it into the trench, the probe must be on some trajectory that causes
it to be within a target area after any step. The submarine computer has already calculated this target
area (your puzzle input). For example:

target area: x=20..30, y=-10..-5

This target area means that you need to find initial x,y velocity values such that after any step, the
probe's x position is at least 20 and at most 30, and the probe's y position is at least -10 and
at most -5.

Given this target area, one initial velocity that causes the probe to be within the target area after
any step is 7,2:

.............#....#............
.......#..............#........
...............................
S........................#.....
...............................
...............................
...........................#...
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTT#TT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

In this diagram, S is the probe's initial position, 0,0. The x coordinate increases to the right,
and the y coordinate increases upward. In the bottom right, positions that are within the target
area are shown as T. After each step (until the target area is reached), the position of the probe
is marked with #. (The bottom-right # is both a position the probe reaches and a position in the
target area.)

Another initial velocity that causes the probe to be within the target area after any step is 6,3:

...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT

Another one is 9,0:

S........#.....................
.................#.............
...............................
........................#......
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTT#
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

One initial velocity that doesn't cause the probe to be within the target area after
any step is 17,-4:

S..............................................................
...............................................................
...............................................................
...............................................................
.................#.............................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT..#.............................
....................TTTTTTTTTTT................................
...............................................................
...............................................................
...............................................................
...............................................................
................................................#..............
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
..............................................................#

The probe appears to pass through the target area, but is never within it after any step.
Instead, it continues down and to the right - only the first few steps are shown.

If you're going to fire a highly scientific probe out of a super cool probe launcher,
you might as well do it with style. How high can you make the probe go while still
reaching the target area?

In the above example, using an initial velocity of 6,9 is the best you can do, causing
the probe to reach a maximum y position of 45. (Any higher initial y velocity causes the
probe to overshoot the target area entirely.)

Find the initial velocity that causes the probe to reach the highest y position and still
eventually be within the target area after any step.

What is the highest y position it reaches on this trajectory?

--- Part Two ---
Maybe a fancy trick shot isn't the best idea; after all, you only have one probe, so you had better not miss.

To get the best idea of what your options are for launching the probe, you need to find every initial velocity
that causes the probe to eventually be within the target area after any step.

In the above example, there are 112 different initial velocity values that meet these criteria:

23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7

How many distinct initial velocity values cause the probe to be within the
target area after any step?
    """


sample_hits = {Pt(23, -10), Pt(25, -9), Pt(27, -5), Pt(29, -6), Pt(22, -6), Pt(21, -7), Pt(9, 0), Pt(27, -7),
               Pt(24, -5), Pt(25, -7), Pt(26, -6), Pt(25, -5), Pt(6, 8), Pt(11, -2), Pt(20, -5), Pt(29, -10),
               Pt(6, 3), Pt(28, -7), Pt(8, 0), Pt(30, -6), Pt(29, -8), Pt(20, -10), Pt(6, 7), Pt(6, 4),
               Pt(6, 1), Pt(14, -4), Pt(21, -6), Pt(26, -10), Pt(7, -1), Pt(7, 7), Pt(8, -1), Pt(21, -9),
               Pt(6, 2), Pt(20, -7), Pt(30, -10), Pt(14, -3), Pt(20, -8), Pt(13, -2), Pt(7, 3), Pt(28, -8),
               Pt(29, -9), Pt(15, -3), Pt(22, -5), Pt(26, -8), Pt(25, -8), Pt(25, -6), Pt(15, -4), Pt(9, -2),
               Pt(15, -2), Pt(12, -2), Pt(28, -9), Pt(12, -3), Pt(24, -6), Pt(23, -7), Pt(25, -10), Pt(7, 8),
               Pt(11, -3), Pt(26, -7), Pt(7, 1), Pt(23, -9), Pt(6, 0), Pt(22, -10), Pt(27, -6), Pt(8, 1),
               Pt(22, -8), Pt(13, -4), Pt(7, 6), Pt(28, -6), Pt(11, -4), Pt(12, -4), Pt(26, -9), Pt(7, 4),
               Pt(24, -10), Pt(23, -8), Pt(30, -8), Pt(7, 0), Pt(9, -1), Pt(10, -1), Pt(26, -5), Pt(22, -9),
               Pt(6, 5), Pt(7, 5), Pt(23, -6), Pt(28, -10), Pt(10, -2), Pt(11, -1), Pt(20, -9), Pt(14, -2),
               Pt(29, -7), Pt(13, -3), Pt(23, -5), Pt(24, -8), Pt(27, -9), Pt(30, -7), Pt(28, -5), Pt(21, -10),
               Pt(7, 9), Pt(6, 6), Pt(21, -5), Pt(27, -10), Pt(7, 2), Pt(30, -9), Pt(21, -8), Pt(22, -7),
               Pt(24, -9), Pt(20, -6), Pt(6, 9), Pt(29, -5), Pt(8, -2), Pt(27, -8), Pt(30, -5), Pt(24, -7)}

MY_TARGET = Target(60, 94, -171, -136)  # target area: x=60..94, y=-171..-136


def print_grid(x_min, x_max, y_min, y_max, points, points2=None):
    output = []
    if points2 is None:
        points2 = set()
    for y in range(y_min, y_max + 1):
        line = [f'y={y:>4}']
        for x in range(x_min, x_max + 1):
            if Pt(x, y) in points and Pt(x, y) in points2:
                line.append(f'{Color.PURPLE}{Color.BOLD}*{Color.END}')
            elif Pt(x, y) in points:
                line.append(f'{Color.GREEN}{Color.BOLD}*{Color.END}')
            elif Pt(x, y) in points2:
                line.append(f'{Color.RED}{Color.BOLD}*{Color.END}')
            else:
                line.append('.')
        if y == y_min:
            line.append(f'x={x_min:>4}..{x_max:>4}')
        output.append(''.join(line))
    output.reverse()
    print('\n\n')
    print('\n'.join(output))
    print('\n\n')


def brute_force_find_max_y_hit(target: Target, comparison=None):
    hits = set()
    y_max = 0
    best_initial_velocity = Pt(target.x_min, target.y_max)
    zone = [Pt(x, y) for x in range(target.x_max + 11) for y in range(target.y_min - 10, -target.y_min + 11)]
    for initial_velocity in zone:
        hit, shot_y_max, final_p, final_v = hit_target(initial_velocity, target)
        if hit:
            hits.add(initial_velocity)
            if shot_y_max > y_max:
                y_max = shot_y_max
                best_initial_velocity = initial_velocity
    print_grid(0, target.x_max + 11, target.y_min - 10, -target.y_min + 11, hits, comparison)
    return best_initial_velocity, y_max, len(hits)


def hit_target(initial_velocity: Pt, target: Target):
    n = 0
    p = Pt(0, 0)
    v = initial_velocity
    y_max = 0
    while True:
        if n > 0:
            v += Pt(-1 if v.x > 0 else 1 if v.x < 0 else 0, -1)
        n += 1
        p += v
        y_max = max(p.y, y_max)
        # check target
        if target.hit(p):
            return True, y_max, p, v
        if v.x >= 0 and p.x >= target.x_max:
            return False, y_max, p, v
        if v.y <= 0 and p.y <= target.y_min:
            return False, y_max, p, v


def test_hit_target():
    assert hit_target(Pt(7, 2), Target(20, 30, -10, -5)) == (True, 3, Pt(x=28, y=-7), Pt(x=1, y=-4))
    assert hit_target(Pt(6, 3), Target(20, 30, -10, -5)) == (True, 6, Pt(x=21, y=-9), Pt(x=0, y=-5))
    assert hit_target(Pt(9, 0), Target(20, 30, -10, -5)) == (True, 0, Pt(x=30, y=-6), Pt(x=6, y=-3))
    assert hit_target(Pt(17, -4), Target(20, 30, -10, -5)) == (False, 0, Pt(x=33, y=-9), Pt(x=16, y=-5))


def test_brute_force_find_max_y_hit():
    assert brute_force_find_max_y_hit(Target(20, 30, -10, -5), sample_hits) == (Pt(x=6, y=9), 45, 112)
    assert brute_force_find_max_y_hit(MY_TARGET) == (Pt(x=11, y=170), 14535, 2270)  # Right answer but ugly algorithm
