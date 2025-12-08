from pathlib import Path
from typing import List, NamedTuple


class Puzzle:
    """
    --- Day 4: Printing Department ---
    You ride the escalator down to the printing department. They're clearly
    getting ready for Christmas; they have lots of large rolls of paper
    everywhere, and there's even a massive printer in the corner (to handle the
    really big print jobs).

    Decorating here will be easy: they can make their own decorations. What you
    really need is a way to get further into the North Pole base while the
    elevators are offline.

    "Actually, maybe we can help with that," one of the Elves replies when you
    ask for help. "We're pretty sure there's a cafeteria on the other side of
    the back wall. If we could break through the wall, you'd be able to keep
    moving. It's too bad all of our forklifts are so busy moving those big rolls
    of paper around."

    If you can optimize the work the forklifts are doing, maybe they would have
    time to spare to break through the wall.

    The rolls of paper (@) are arranged on a large grid; the Elves even have a
    helpful diagram (your puzzle input) indicating where everything is located.

    For example:

    ..@@.@@@@.
    @@@.@.@.@@
    @@@@@.@.@@
    @.@@@@..@.
    @@.@@@@.@@
    .@@@@@@@.@
    .@.@.@.@@@
    @.@@@.@@@@
    .@@@@@@@@.
    @.@.@@@.@.

    The forklifts can only access a roll of paper if there are fewer than four
    rolls of paper in the eight adjacent positions. If you can figure out which
    rolls of paper the forklifts can access, they'll spend less time looking and
    more time breaking down the wall to the cafeteria.

    In this example, there are 13 rolls of paper that can be accessed by a
    forklift (marked with x):

    ..xx.xx@x.
    x@@.@.@.@@
    @@@@@.x.@@
    @.@@@@..@.
    x@.@@@@.@x
    .@@@@@@@.@
    .@.@.@.@@@
    x.@@@.@@@@
    .@@@@@@@@.
    x.x.@@@.x.

    Consider your complete diagram of the paper roll locations. How many rolls
    of paper can be accessed by a forklift?

    Your puzzle answer was 1549.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    Now, the Elves just need help accessing as much of the paper as they can.

    Once a roll of paper can be accessed by a forklift, it can be removed. Once
    a roll of paper is removed, the forklifts might be able to access more rolls
    of paper, which they might also be able to remove. How many total rolls of
    paper could the Elves remove if they keep repeating this process?

    Starting with the same example as above, here is one way you could remove as
    many rolls of paper as possible, using highlighted @ to indicate that a roll
    of paper is about to be removed, and using x to indicate that a roll of
    paper was just removed:

    Initial state:
    ..@@.@@@@.
    @@@.@.@.@@
    @@@@@.@.@@
    @.@@@@..@.
    @@.@@@@.@@
    .@@@@@@@.@
    .@.@.@.@@@
    @.@@@.@@@@
    .@@@@@@@@.
    @.@.@@@.@.

    Remove 13 rolls of paper:
    ..xx.xx@x.
    x@@.@.@.@@
    @@@@@.x.@@
    @.@@@@..@.
    x@.@@@@.@x
    .@@@@@@@.@
    .@.@.@.@@@
    x.@@@.@@@@
    .@@@@@@@@.
    x.x.@@@.x.

    Remove 12 rolls of paper:
    .......x..
    .@@.x.x.@x
    x@@@@...@@
    x.@@@@..x.
    .@.@@@@.x.
    .x@@@@@@.x
    .x.@.@.@@@
    ..@@@.@@@@
    .x@@@@@@@.
    ....@@@...

    Remove 7 rolls of paper:
    ..........
    .x@.....x.
    .@@@@...xx
    ..@@@@....
    .x.@@@@...
    ..@@@@@@..
    ...@.@.@@x
    ..@@@.@@@@
    ..x@@@@@@.
    ....@@@...

    Remove 5 rolls of paper:
    ..........
    ..x.......
    .x@@@.....
    ..@@@@....
    ...@@@@...
    ..x@@@@@..
    ...@.@.@@.
    ..x@@.@@@x
    ...@@@@@@.
    ....@@@...

    Remove 2 rolls of paper:
    ..........
    ..........
    ..x@@.....
    ..@@@@....
    ...@@@@...
    ...@@@@@..
    ...@.@.@@.
    ...@@.@@@.
    ...@@@@@x.
    ....@@@...

    Remove 1 roll of paper:
    ..........
    ..........
    ...@@.....
    ..x@@@....
    ...@@@@...
    ...@@@@@..
    ...@.@.@@.
    ...@@.@@@.
    ...@@@@@..
    ....@@@...

    Remove 1 roll of paper:
    ..........
    ..........
    ...x@.....
    ...@@@....
    ...@@@@...
    ...@@@@@..
    ...@.@.@@.
    ...@@.@@@.
    ...@@@@@..
    ....@@@...

    Remove 1 roll of paper:
    ..........
    ..........
    ....x.....
    ...@@@....
    ...@@@@...
    ...@@@@@..
    ...@.@.@@.
    ...@@.@@@.
    ...@@@@@..
    ....@@@...

    Remove 1 roll of paper:
    ..........
    ..........
    ..........
    ...x@@....
    ...@@@@...
    ...@@@@@..
    ...@.@.@@.
    ...@@.@@@.
    ...@@@@@..
    ....@@@...

    Stop once no more rolls of paper are accessible by a forklift. In this
    example, a total of 43 rolls of paper can be removed.

    Start with your original diagram. How many rolls of paper in total can be
    removed by the Elves and their forklifts?

    Your puzzle answer was 8887.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open(Path(__file__).parent / "2025_04_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")

SAMPLE = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@.",
]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


DELTAS = {
    Pt(1, 0),
    Pt(-1, 0),
    Pt(0, 1),
    Pt(0, -1),
    Pt(1, 1),
    Pt(-1, 1),
    Pt(-1, -1),
    Pt(1, -1),
}


class PaperGrid:
    def __init__(self, raw_rows: List[str]):
        self.rolls = set()
        for j, row in enumerate(raw_rows):
            for i, c in enumerate(row):
                if c == "@":
                    self.rolls.add(Pt(i, j))

    def nbhd(self, pt: Pt) -> int:
        count = 0
        for delta in DELTAS:
            if (pt + delta) in self.rolls:
                count += 1
        return count

    def free_rolls(self, remove: bool = False) -> int:
        total = 0
        removal_set = set()
        for roll in self.rolls:
            if self.nbhd(roll) < 4:
                if remove:
                    removal_set.add(roll)
                total += 1
        if remove:
            self.rolls = self.rolls - removal_set
        return total

    def free_all_rolls(self) -> int:
        running_total = 0
        while next_level := self.free_rolls(remove=True):
            running_total += next_level
        return running_total


def test_paper_grid():
    sample = PaperGrid(SAMPLE)
    assert sample.free_rolls() == 13
    assert sample.free_all_rolls() == 43

    my_puzzle = PaperGrid(RAW_INPUT)
    assert my_puzzle.free_rolls() == 1549
    assert my_puzzle.free_all_rolls() == 8887
