from __future__ import annotations
from typing import NamedTuple, List, Set
from collections import defaultdict


class Puzzle:
    """
    --- Day 23: Unstable Diffusion ---
    You enter a large crater of gray dirt where the grove is supposed to be. All
    around you, plants you imagine were expected to be full of fruit are instead
    withered and broken. A large group of Elves has formed in the middle of the
    grove.

    "...but this volcano has been dormant for months. Without ash, the fruit
    can't grow!"

    You look up to see a massive, snow-capped mountain towering above you.

    "It's not like there are other active volcanoes here; we've looked
    everywhere."

    "But our scanners show active magma flows; clearly it's going somewhere."

    They finally notice you at the edge of the grove, your pack almost
    overflowing from the random star fruit you've been collecting. Behind you,
    elephants and monkeys explore the grove, looking concerned. Then, the Elves
    recognize the ash cloud slowly spreading above your recent detour.

    "Why do you--" "How is--" "Did you just--"

    Before any of them can form a complete question, another Elf speaks up:
    "Okay, new plan. We have almost enough fruit already, and ash from the plume
    should spread here eventually. If we quickly plant new seedlings now, we can
    still make it to the extraction point. Spread out!"

    The Elves each reach into their pack and pull out a tiny plant. The plants
    rely on important nutrients from the ash, so they can't be planted too close
    together.

    There isn't enough time to let the Elves figure out where to plant the
    seedlings themselves; you quickly scan the grove (your puzzle input) and
    note their positions.

    For example:

    ....#..
    ..###.#
    #...#.#
    .#...##
    #.###..
    ##.#.##
    .#..#..

    The scan shows Elves # and empty ground .; outside your scan, more empty
    ground extends a long way in every direction. The scan is oriented so that
    north is up; orthogonal directions are written N (north), S (south), W
    (west), and E (east), while diagonal directions are written NE, NW, SE, SW.

    The Elves follow a time-consuming process to figure out where they should
    each go; you can speed up this process considerably. The process consists of
    some number of rounds during which Elves alternate between considering where
    to move and actually moving.

    During the first half of each round, each Elf considers the eight positions
    adjacent to themself. If no other Elves are in one of those eight positions,
    the Elf does not do anything during this round. Otherwise, the Elf looks in
    each of four directions in the following order and proposes moving one step
    in the first valid direction:

    If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes
    moving north one step.

    If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes
    moving south one step.

    If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes
    moving west one step.

    If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes
    moving east one step.

    After each Elf has had a chance to propose a move, the second half of the
    round can begin. Simultaneously, each Elf moves to their proposed
    destination tile if they were the only Elf to propose moving to that
    position. If two or more Elves propose moving to the same position, none of
    those Elves move.

    Finally, at the end of the round, the first direction the Elves considered
    is moved to the end of the list of directions. For example, during the
    second round, the Elves would try proposing a move to the south first, then
    west, then east, then north. On the third round, the Elves would first
    consider west, then east, then north, then south.

    As a smaller example, consider just these five Elves:

    .....
    ..##.
    ..#..
    .....
    ..##.
    .....

    The northernmost two Elves and southernmost two Elves all propose moving
    north, while the middle Elf cannot move north and proposes moving south. The
    middle Elf proposes the same destination as the southwest Elf, so neither of
    them move, but the other three do:

    ..##.
    .....
    ..#..
    ...#.
    ..#..
    .....

    Next, the northernmost two Elves and the southernmost Elf all propose moving
    south. Of the remaining middle two Elves, the west one cannot move south and
    proposes moving west, while the east one cannot move south or west and
    proposes moving east. All five Elves succeed in moving to their proposed
    positions:

    .....
    ..##.
    .#...
    ....#
    .....
    ..#..

    Finally, the southernmost two Elves choose not to move at all. Of the
    remaining three Elves, the west one proposes moving west, the east one
    proposes moving east, and the middle one proposes moving north; all three
    succeed in moving:

    ..#..
    ....#
    #....
    ....#
    .....
    ..#..

    At this point, no Elves need to move, and so the process ends.

    The larger example above proceeds as follows:

    == Initial State ==
    ..............
    ..............
    .......#......
    .....###.#....
    ...#...#.#....
    ....#...##....
    ...#.###......
    ...##.#.##....
    ....#..#......
    ..............
    ..............
    ..............

    == End of Round 1 ==
    ..............
    .......#......
    .....#...#....
    ...#..#.#.....
    .......#..#...
    ....#.#.##....
    ..#..#.#......
    ..#.#.#.##....
    ..............
    ....#..#......
    ..............
    ..............

    == End of Round 2 ==
    ..............
    .......#......
    ....#.....#...
    ...#..#.#.....
    .......#...#..
    ...#..#.#.....
    .#...#.#.#....
    ..............
    ..#.#.#.##....
    ....#..#......
    ..............
    ..............

    == End of Round 3 ==
    ..............
    .......#......
    .....#....#...
    ..#..#...#....
    .......#...#..
    ...#..#.#.....
    .#..#.....#...
    .......##.....
    ..##.#....#...
    ...#..........
    .......#......
    ..............

    == End of Round 4 ==
    ..............
    .......#......
    ......#....#..
    ..#...##......
    ...#.....#.#..
    .........#....
    .#...###..#...
    ..#......#....
    ....##....#...
    ....#.........
    .......#......
    ..............

    == End of Round 5 ==
    .......#......
    ..............
    ..#..#.....#..
    .........#....
    ......##...#..
    .#.#.####.....
    ...........#..
    ....##..#.....
    ..#...........
    ..........#...
    ....#..#......
    ..............
    After a few more rounds...

    == End of Round 10 ==
    .......#......
    ...........#..
    ..#.#..#......
    ......#.......
    ...#.....#..#.
    .#......##....
    .....##.......
    ..#........#..
    ....#.#..#....
    ..............
    ....#..#..#...
    ..............

    To make sure they're on the right track, the Elves like to check after round
    10 that they're making good progress toward covering enough ground. To do
    this, count the number of empty ground tiles contained by the smallest
    rectangle that contains every Elf. (The edges of the rectangle should be
    aligned to the N/S/E/W directions; the Elves do not have the patience to
    calculate arbitrary rectangles.) In the above example, that rectangle is:

    ......#.....
    ..........#.
    .#.#..#.....
    .....#......
    ..#.....#..#
    #......##...
    ....##......
    .#........#.
    ...#.#..#...
    ............
    ...#..#..#..

    In this region, the number of empty ground tiles is 110.

    Simulate the Elves' process and find the smallest rectangle that contains
    the Elves after 10 rounds. How many empty ground tiles does that rectangle
    contain?

    Your puzzle answer was 3862.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    It seems you're on the right track. Finish simulating the process and figure
    out where the Elves need to go. How many rounds did you save them?

    In the example above, the first round where no Elf moved was round 20:

    .......#......
    ....#......#..
    ..#.....#.....
    ......#.......
    ...#....#.#..#
    #.............
    ....#.....#...
    ..#.....#.....
    ....#.#....#..
    .........#....
    ....#......#..
    .......#......

    Figure out where the Elves need to go. What is the number of the first round
    where no Elf moves?
    """


with open("day_23_large_sample.txt") as fp:
    SAMPLE_MAP = [line for line in fp]


with open("day_23_input.txt") as fp:
    MY_MAP = [line for line in fp]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Pt) -> Pt:
        return Pt(x=self.x + other.x, y=self.y + other.y)

    def __neg__(self) -> Pt:
        return Pt(x=-self.x, y=-self.y)

    def __sub__(self, other: Pt) -> Pt:
        return Pt(x=self.x - other.x, y=self.y - other.y)

    def alone(self, others) -> bool:
        bubble = {
            Pt(self.x - 1, self.y - 1),
            Pt(self.x, self.y - 1),
            Pt(self.x + 1, self.y - 1),
            Pt(self.x - 1, self.y),
            Pt(self.x + 1, self.y),
            Pt(self.x - 1, self.y + 1),
            Pt(self.x, self.y + 1),
            Pt(self.x + 1, self.y + 1),
        }
        if bubble & others:
            return False
        return True

    def field(self, dir) -> Set[Pt]:
        match dir:
            case "N":
                return [
                    Pt(self.x - 1, self.y - 1),
                    Pt(self.x, self.y - 1),
                    Pt(self.x + 1, self.y - 1),
                ]
            case "S":
                return [
                    Pt(self.x - 1, self.y + 1),
                    Pt(self.x, self.y + 1),
                    Pt(self.x + 1, self.y + 1),
                ]
            case "W":
                return [
                    Pt(self.x - 1, self.y - 1),
                    Pt(self.x - 1, self.y),
                    Pt(self.x - 1, self.y + 1),
                ]
            case "E":
                return [
                    Pt(self.x + 1, self.y - 1),
                    Pt(self.x + 1, self.y),
                    Pt(self.x + 1, self.y + 1),
                ]


class Box(NamedTuple):
    min: Pt
    max: Pt


def bound(pts) -> Box:
    new_min_x = min([p.x for p in pts])
    new_min_y = min([p.y for p in pts])
    new_max_x = max([p.x for p in pts])
    new_max_y = max([p.y for p in pts])
    return Box(Pt(new_min_x, new_min_y), Pt(new_max_x, new_max_y))


class Diffusion:
    def __init__(self, map: List[str]) -> None:
        self.board = set()
        for y, row in enumerate(map):
            for x, c in enumerate(row):
                if c == "#":
                    self.board.add(Pt(x=x, y=y))
        self.move_order = "NSWE"

    def step_to_stable(self):
        n = 0
        old_board = self.board
        while True:
            self.step()
            n += 1
            if self.board == old_board:
                return n
            old_board = self.board

    def step(self):
        # first half
        next_board = defaultdict(list)
        for pt in self.board:
            if pt.alone(self.board):
                next_board[pt].append(None)
                continue
            placed = False
            for dir in self.move_order:
                if not set(d := pt.field(dir)) & self.board:
                    next_board[d[1]].append(pt)
                    placed = True
                    break
            if not placed:
                next_board[pt].append(None)

        # second half
        self.board = set()
        for new_pt, old_pts in next_board.items():
            if len(old_pts) == 1:
                self.board.add(new_pt)
            else:
                self.board = self.board.union(old_pts)

        # finally update move order
        self.move_order = f"{self.move_order[1:]}{self.move_order[0]}"

    def display(self):
        bound_box = bound(self.board)
        result = []
        for y in range(bound_box.min.y, bound_box.max.y + 1):
            line = []
            for x in range(bound_box.min.x, bound_box.max.x + 1):
                line.append("#" if Pt(x, y) in self.board else ".")
            result.append("".join(line))
        return result

    def empty_region(self):
        bound_box = bound(self.board)
        rl = bound_box.max.x - bound_box.min.x + 1
        rw = bound_box.max.y - bound_box.min.y + 1
        return rl * rw - len(self.board)


def test_sample_diffusion():
    my_bound = bound({Pt(-2, 0), Pt(3, 0), Pt(0, 5)})
    assert my_bound == Box(Pt(-2, 0), Pt(3, 5))
    sample = Diffusion(SAMPLE_MAP)
    assert len(sample.board) == 22
    assert sample.empty_region() == 27
    print("\nInitial board")
    print("\n".join(sample.display()))
    for n in range(10):
        sample.step()
        print(f"\nstep={n+1}")
        print("\n".join(sample.display()))
    assert len(sample.board) == 22
    assert sample.empty_region() == 110
    sample = Diffusion(SAMPLE_MAP)
    assert sample.step_to_stable() == 20


def test_my_diffusion():
    my_diffusion = Diffusion(MY_MAP)
    for _ in range(10):
        my_diffusion.step()
    assert my_diffusion.empty_region() == 3862
    my_diffusion = Diffusion(MY_MAP)
    assert my_diffusion.step_to_stable() == 913
