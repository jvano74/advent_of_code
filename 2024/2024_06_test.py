from pathlib import Path
from typing import List, NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 6: Guard Gallivant ---

    The Historians use their fancy device again, this time to whisk you all away
    to the North Pole prototype suit manufacturing lab... in the year 1518! It
    turns out that having direct access to history is very convenient for a
    group of historians.

    You still have to be careful of time paradoxes, and so it will be important
    to avoid anyone from 1518 while The Historians search for the Chief.
    Unfortunately, a single guard is patrolling this part of the lab.

    Maybe you can work out where the guard will go ahead of time so that The
    Historians can search safely?

    You start by making a map (your puzzle input) of the situation. For example:

    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...

    The map shows the current position of the guard with ^ (to indicate the
    guard is currently facing up from the perspective of the map). Any
    obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

    Lab guards in 1518 follow a very strict patrol protocol which involves
    repeatedly following these steps:

    If there is something directly in front of you, turn right 90 degrees.

    Otherwise, take a step forward.

    Following the above protocol, the guard moves up several times until she
    reaches an obstacle (in this case, a pile of failed suit prototypes):

    ....#.....
    ....^....#
    ..........
    ..#.......
    .......#..
    ..........
    .#........
    ........#.
    #.........
    ......#...

    Because there is now an obstacle in front of the guard, she turns right
    before continuing straight in her new facing direction:

    ....#.....
    ........>#
    ..........
    ..#.......
    .......#..
    ..........
    .#........
    ........#.
    #.........
    ......#...

    Reaching another obstacle (a spool of several very long polymers), she turns
    right again and continues downward:

    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#......v.
    ........#.
    #.........
    ......#...

    This process continues for a while, but the guard eventually leaves the
    mapped area (after walking past a tank of universal solvent):

    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#........
    ........#.
    #.........
    ......#v..

    By predicting the guard's route, you can determine which specific positions
    in the lab will be in the patrol path. Including the guard's starting
    position, the positions visited by the guard before leaving the area are
    marked with an X:

    ....#.....
    ....XXXXX#
    ....X...X.
    ..#.X...X.
    ..XXXXX#X.
    ..X.X.X.X.
    .#XXXXXXX.
    .XXXXXXX#.
    #XXXXXXX..
    ......#X..

    In this example, the guard will visit 41 distinct positions on your map.

    Predict the path of the guard. How many distinct positions will the guard
    visit before leaving the mapped area?

    Your puzzle answer was 5404.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---

    While The Historians begin working around the guard's patrol route, you
    borrow their fancy device and step outside the lab. From the safety of a
    supply closet, you time travel through the last few months and record the
    nightly status of the lab's guard post on the walls of the closet.

    Returning after what seems like only a few seconds to The Historians, they
    explain that the guard's patrol area is simply too large for them to safely
    search the lab without getting caught.

    Fortunately, they are pretty sure that adding a single new obstruction won't
    cause a time paradox. They'd like to place the new obstruction in such a way
    that the guard will get stuck in a loop, making the rest of the lab safe to
    search.

    To have the lowest chance of creating a time paradox, The Historians would
    like to know all of the possible positions for such an obstruction. The new
    obstruction can't be placed at the guard's starting position - the guard is
    there right now and would notice.

    In the above example, there are only 6 different positions where a new
    obstruction would cause the guard to get stuck in a loop. The diagrams of
    these six situations use O to mark the new obstruction, | to show a position
    where the guard moves up/down, - to show a position where the guard moves
    left/right, and + to show a position where the guard moves both up/down and
    left/right.

    Option one, put a printing press next to the guard's starting position:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ....|..#|.
    ....|...|.
    .#.O^---+.
    ........#.
    #.........
    ......#...

    Option two, put a stack of failed suit prototypes in the bottom right
    quadrant of the mapped area:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    ......O.#.
    #.........
    ......#...

    Option three, put a crate of chimney-squeeze prototype fabric next to the
    standing desk in the bottom right quadrant:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    .+----+O#.
    #+----+...
    ......#...

    Option four, put an alchemical retroencabulator near the bottom left corner:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    ..|...|.#.
    #O+---+...
    ......#...

    Option five, put the alchemical retroencabulator a bit to the right instead:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    ....|.|.#.
    #..O+-+...
    ......#...

    Option six, put a tank of sovereign glue right next to the tank of universal
    solvent:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    .+----++#.
    #+----++..
    ......#O..

    It doesn't really matter what you choose to use as an obstacle so long as
    you and The Historians can put it into position without the guard noticing.
    The important thing is having enough options that you can find one that
    minimizes time paradoxes, and in this example, there are 6 different
    positions you could choose.

    You need to get the guard stuck in a loop by adding a single new
    obstruction. How many different positions could you choose for this
    obstruction?

    Your puzzle answer was 1984.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


with open(Path(__file__).parent / "2024_06_input.txt") as fp:
    MY_MAP = fp.read().split("\n")

SAMPLE_MAP = [
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#..^.....",
    "........#.",
    "#.........",
    "......#...",
]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


RIGHT_TURN = {
    Pt(0, -1): Pt(1, 0),
    Pt(1, 0): Pt(0, 1),
    Pt(0, 1): Pt(-1, 0),
    Pt(-1, 0): Pt(0, -1),
}


class Factory:
    def __init__(self, map: List[str]):
        self.max_x, self.may_y = 0, 0
        self.obstacles = set()

        self.patrolled = defaultdict(set)
        self.loop_obstacles = set()

        for y, line in enumerate(map):
            self.max_y = y
            for x, c in enumerate(line):
                self.max_x = max(self.max_x, x)
                if c == "#":
                    self.obstacles.add(Pt(x, y))
                elif c == "^":
                    self.guard_start = Pt(x, y)
                    self.guard = Pt(x, y)
                    self.guard_dir = Pt(0, -1)

    def run_guard(self):
        while 0 <= self.guard.x <= self.max_x and 0 <= self.guard.y <= self.max_y:
            self.patrolled[self.guard].add(self.guard_dir)

            candidate_step = self.guard + self.guard_dir
            if candidate_step in self.obstacles:
                next_dir = RIGHT_TURN[self.guard_dir]
                next_step = self.guard
            else:
                next_dir = self.guard_dir
                next_step = candidate_step

            if (
                candidate_step not in self.patrolled
                and candidate_step not in self.obstacles
                and 0 <= candidate_step.x <= self.max_x
                and 0 <= candidate_step.y <= self.max_y
            ):
                alt_next_dir = RIGHT_TURN[self.guard_dir]
                alt_next_step = self.guard
                alt_patrolled = defaultdict(set)
                while (
                    candidate_step != self.guard_start
                    and 0 <= alt_next_step.x <= self.max_x
                    and 0 <= alt_next_step.y <= self.max_y
                ):
                    if (
                        alt_next_step in self.patrolled
                        and alt_next_dir in self.patrolled[alt_next_step]
                    ) or alt_next_dir in alt_patrolled[alt_next_step]:
                        self.loop_obstacles.add(candidate_step)
                        break
                    alt_patrolled[alt_next_step].add(alt_next_dir)
                    if alt_next_step + alt_next_dir in self.obstacles or (
                        alt_next_step + alt_next_dir == candidate_step
                    ):
                        alt_next_dir = RIGHT_TURN[alt_next_dir]
                    else:
                        alt_next_step += alt_next_dir

            self.guard = next_step
            self.guard_dir = next_dir


def test_obstacle_count():
    sample_factory = Factory(SAMPLE_MAP)
    assert len(sample_factory.obstacles) == 8
    my_factory = Factory(MY_MAP)
    assert len(my_factory.obstacles) == 817


def test_patrolled_size_and_loop_obstacles():
    sample_factory = Factory(SAMPLE_MAP)
    sample_factory.run_guard()
    assert len(sample_factory.patrolled) == 41
    assert len(sample_factory.loop_obstacles) == 6
    my_factory = Factory(MY_MAP)
    my_factory.run_guard()
    assert len(my_factory.patrolled) == 5404
    assert len(my_factory.loop_obstacles) == 1984
    # First answer 912 was too low
    # Realized alt_next_step was checking loop_obstacles, not obstacles
    # Fixed but second answer 2133 was too high
    # Realized was also allowing loop_obstacles to be placed after earlier
    # path passed through location which would have diverted
    # Fixed but third answer 1985 was still too high
    # Realized wasn't checking loop_obstacles within range
    # Fixed and got 1984 which was finally right
