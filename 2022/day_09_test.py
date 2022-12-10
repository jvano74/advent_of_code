import curses
from curses import wrapper
from time import sleep
from typing import List, NamedTuple


class Puzzle:
    """
    --- Day 9: Rope Bridge ---
    This rope bridge creaks as you walk along it. You aren't sure how old it is,
    or whether it can even support your weight.

    It seems to support the Elves just fine, though. The bridge spans a gorge
    which was carved out by the massive river far below you.

    You step carefully; as you do, the ropes stretch and twist. You decide to
    distract yourself by modeling rope physics; maybe you can even figure out
    where not to step.

    Consider a rope with a knot at each end; these knots mark the head and the
    tail of the rope. If the head moves far enough away from the tail, the tail
    is pulled toward the head.

    Due to nebulous reasoning involving Planck lengths, you should be able to
    model the positions of the knots on a two-dimensional grid. Then, by
    following a hypothetical series of motions (your puzzle input) for the
    head, you can determine how the tail will move.

    Due to the aforementioned Planck lengths, the rope must be quite short;
    in fact, the head (H) and tail (T) must always be touching (diagonally
    adjacent and even overlapping both count as touching):

    ....
    .TH.
    ....

    ....
    .H..
    ..T.
    ....

    ...
    .H. (H covers T)
    ...

    If the head is ever two steps directly up, down, left, or right from
    the tail, the tail must also move one step in that direction so it
    remains close enough:

    .....    .....    .....
    .TH.. -> .T.H. -> ..TH.
    .....    .....    .....

    ...    ...    ...
    .T.    .T.    ...
    .H. -> ... -> .T.
    ...    .H.    .H.
    ...    ...    ...

    Otherwise, if the head and tail aren't touching and aren't in the
    same row or column, the tail always moves one step diagonally to
    keep up:

    .....    .....    .....
    .....    ..H..    ..H..
    ..H.. -> ..... -> ..T..
    .T...    .T...    .....
    .....    .....    .....

    .....    .....    .....
    .....    .....    .....
    ..H.. -> ...H. -> ..TH.
    .T...    .T...    .....
    .....    .....    .....

    You just need to work out where the tail goes as the head
    follows a series of motions. Assume the head and the tail
    both start at the same position, overlapping.

    For example:

    R 4
    U 4
    L 3
    D 1
    R 4
    D 1
    L 5
    R 2

    This series of motions moves the head right four steps,
    then up four steps, then left three steps, then down one
    step, and so on. After each step, you'll need to update
    the position of the tail if the step means the head is
    no longer adjacent to the tail. Visually, these motions
    occur as follows (s marks the starting position as a
    reference point):

    == Initial State ==

    ......
    ......
    ......
    ......
    H.....  (H covers T, s)

    == R 4 ==

    ......
    ......
    ......
    ......
    TH....  (T covers s)

    ......
    ......
    ......
    ......
    sTH...

    ......
    ......
    ......
    ......
    s.TH..

    ......
    ......
    ......
    ......
    s..TH.

    == U 4 ==

    ......
    ......
    ......
    ....H.
    s..T..

    ......
    ......
    ....H.
    ....T.
    s.....

    ......
    ....H.
    ....T.
    ......
    s.....

    ....H.
    ....T.
    ......
    ......
    s.....

    == L 3 ==

    ...H..
    ....T.
    ......
    ......
    s.....

    ..HT..
    ......
    ......
    ......
    s.....

    .HT...
    ......
    ......
    ......
    s.....

    == D 1 ==

    ..T...
    .H....
    ......
    ......
    s.....

    == R 4 ==

    ..T...
    ..H...
    ......
    ......
    s.....

    ..T...
    ...H..
    ......
    ......
    s.....

    ......
    ...TH.
    ......
    ......
    s.....

    ......
    ....TH
    ......
    ......
    s.....

    == D 1 ==

    ......
    ....T.
    .....H
    ......
    s.....

    == L 5 ==

    ......
    ....T.
    ....H.
    ......
    s.....

    ......
    ....T.
    ...H..
    ......
    s.....

    ......
    ......
    ..HT..
    ......
    s.....

    ......
    ......
    .HT...
    ......
    s.....

    ......
    ......
    HT....
    ......
    s.....

    == R 2 ==

    ......
    ......
    .H....  (H covers T)
    ......
    s.....

    ......
    ......
    .TH...
    ......
    s.....

    After simulating the rope, you can count up all of the positions
    the tail visited at least once. In this diagram, s again marks
    the starting position (which the tail also visited) and # marks
    other positions the tail visited:

    ..##..
    ...##.
    .####.
    ....#.
    s###..

    So, there are 13 positions the tail visited at least once.

    Simulate your complete hypothetical series of motions.

    How many positions does the tail of the rope visit at least once?

    Your puzzle answer was 6522.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    A rope snaps! Suddenly, the river is getting a lot closer than you
    remember. The bridge is still there, but some of the ropes that broke
    are now whipping toward you as you fall through the air!

    The ropes are moving too quickly to grab; you only have a few seconds
    to choose how to arch your body to avoid being hit. Fortunately, your
    simulation can be extended to support longer ropes.

    Rather than two knots, you now must simulate a rope consisting of ten
    knots. One knot is still the head of the rope and moves according to
    the series of motions. Each knot further down the rope follows the
    knot in front of it using the same rules as before.

    Using the same series of motions as the above example, but with the
    knots marked H, 1, 2, ..., 9, the motions now occur as follows:

    == Initial State ==

    ......
    ......
    ......
    ......
    H.....  (H covers 1, 2, 3, 4, 5, 6, 7, 8, 9, s)

    == R 4 ==

    ......
    ......
    ......
    ......
    1H....  (1 covers 2, 3, 4, 5, 6, 7, 8, 9, s)

    ......
    ......
    ......
    ......
    21H...  (2 covers 3, 4, 5, 6, 7, 8, 9, s)

    ......
    ......
    ......
    ......
    321H..  (3 covers 4, 5, 6, 7, 8, 9, s)

    ......
    ......
    ......
    ......
    4321H.  (4 covers 5, 6, 7, 8, 9, s)

    == U 4 ==

    ......
    ......
    ......
    ....H.
    4321..  (4 covers 5, 6, 7, 8, 9, s)

    ......
    ......
    ....H.
    .4321.
    5.....  (5 covers 6, 7, 8, 9, s)

    ......
    ....H.
    ....1.
    .432..
    5.....  (5 covers 6, 7, 8, 9, s)

    ....H.
    ....1.
    ..432.
    .5....
    6.....  (6 covers 7, 8, 9, s)

    == L 3 ==

    ...H..
    ....1.
    ..432.
    .5....
    6.....  (6 covers 7, 8, 9, s)

    ..H1..
    ...2..
    ..43..
    .5....
    6.....  (6 covers 7, 8, 9, s)

    .H1...
    ...2..
    ..43..
    .5....
    6.....  (6 covers 7, 8, 9, s)

    == D 1 ==

    ..1...
    .H.2..
    ..43..
    .5....
    6.....  (6 covers 7, 8, 9, s)

    == R 4 ==

    ..1...
    ..H2..
    ..43..
    .5....
    6.....  (6 covers 7, 8, 9, s)

    ..1...
    ...H..  (H covers 2)
    ..43..
    .5....
    6.....  (6 covers 7, 8, 9, s)

    ......
    ...1H.  (1 covers 2)
    ..43..
    .5....
    6.....  (6 covers 7, 8, 9, s)

    ......
    ...21H
    ..43..
    .5....
    6.....  (6 covers 7, 8, 9, s)

    == D 1 ==

    ......
    ...21.
    ..43.H
    .5....
    6.....  (6 covers 7, 8, 9, s)

    == L 5 ==

    ......
    ...21.
    ..43H.
    .5....
    6.....  (6 covers 7, 8, 9, s)

    ......
    ...21.
    ..4H..  (H covers 3)
    .5....
    6.....  (6 covers 7, 8, 9, s)

    ......
    ...2..
    ..H1..  (H covers 4; 1 covers 3)
    .5....
    6.....  (6 covers 7, 8, 9, s)

    ......
    ...2..
    .H13..  (1 covers 4)
    .5....
    6.....  (6 covers 7, 8, 9, s)

    ......
    ......
    H123..  (2 covers 4)
    .5....
    6.....  (6 covers 7, 8, 9, s)

    == R 2 ==

    ......
    ......
    .H23..  (H covers 1; 2 covers 4)
    .5....
    6.....  (6 covers 7, 8, 9, s)

    ......
    ......
    .1H3..  (H covers 2, 4)
    .5....
    6.....  (6 covers 7, 8, 9, s)

    Now, you need to keep track of the positions the new tail,
    9, visits. In this example, the tail never moves, and so it
    only visits 1 position. However, be careful: more types of
    motion are possible than before, so you might want to visually
    compare your simulated rope to the one above.

    Here's a larger example:

    R 5
    U 8
    L 8
    D 3
    R 17
    D 10
    L 25
    U 20

    These motions occur as follows (individual steps are not shown):

    == Initial State ==

    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ...........H..............  (H covers 1, 2, 3, 4, 5, 6, 7, 8, 9, s)
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................

    == R 5 ==

    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ...........54321H.........  (5 covers 6, 7, 8, 9, s)
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................

    == U 8 ==

    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ................H.........
    ................1.........
    ................2.........
    ................3.........
    ...............54.........
    ..............6...........
    .............7............
    ............8.............
    ...........9..............  (9 covers s)
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................

    == L 8 ==

    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ........H1234.............
    ............5.............
    ............6.............
    ............7.............
    ............8.............
    ............9.............
    ..........................
    ..........................
    ...........s..............
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................

    == D 3 ==

    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    .........2345.............
    ........1...6.............
    ........H...7.............
    ............8.............
    ............9.............
    ..........................
    ..........................
    ...........s..............
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................

    == R 17 ==

    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ................987654321H
    ..........................
    ..........................
    ..........................
    ..........................
    ...........s..............
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................

    == D 10 ==

    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ...........s.........98765
    .........................4
    .........................3
    .........................2
    .........................1
    .........................H

    == L 25 ==

    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ...........s..............
    ..........................
    ..........................
    ..........................
    ..........................
    H123456789................

    == U 20 ==

    H.........................
    1.........................
    2.........................
    3.........................
    4.........................
    5.........................
    6.........................
    7.........................
    8.........................
    9.........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ...........s..............
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................

    Now, the tail (9) visits 36 positions (including s) at least once:

    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    ..........................
    #.........................
    #.............###.........
    #............#...#........
    .#..........#.....#.......
    ..#..........#.....#......
    ...#........#.......#.....
    ....#......s.........#....
    .....#..............#.....
    ......#............#......
    .......#..........#.......
    ........#........#........
    .........########.........

    Simulate your complete series of motions on a larger rope with ten knots.
    How many positions does the tail of the rope visit at least once?
    """


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def dist(self):
        return max(abs(self.x), abs(self.y))

    def follow(self, target):
        """
        if the head and tail aren't touching and aren't in the same row
        or column, the tail always moves one step diagonally to keep up
        """

        def sign(n):
            if n < 0:
                return -1
            if n > 0:
                return 1
            return 0

        delta = target - self
        if abs(delta.x) >= 2 or abs(delta.y) >= 2:
            return Pt(self.x + sign(delta.x), self.y + sign(delta.y))
        return self


DIR = {
    "U": Pt(0, -1),
    "D": Pt(0, 1),
    "L": Pt(-1, 0),
    "R": Pt(1, 0),
}


class String:
    def __init__(self, length=2) -> None:
        self.bits = [Pt(x=0, y=0) for _ in range(length)]
        self.path_of_tail = set()
        self.path_of_tail.add(self.bits[-1])

    def display(self, zoom_in=""):
        frame = []
        if zoom_in == "H":
            x_min = self.bits[0].x
            x_max = self.bits[0].x
            y_min = self.bits[0].y
            y_max = self.bits[0].y
        elif zoom_in == "T":
            x_min = self.bits[-1].x
            x_max = self.bits[-1].x
            y_min = self.bits[-1].y
            y_max = self.bits[-1].y
        else:
            x_min = min(p.x for p in self.path_of_tail)
            x_max = max(p.x for p in self.path_of_tail)
            y_min = min(p.y for p in self.path_of_tail)
            y_max = max(p.y for p in self.path_of_tail)
        for y in range(y_min - len(self.bits), y_max + 1 + len(self.bits)):
            line = []
            for x in range(x_min - len(self.bits), x_max + 1 + len(self.bits)):
                pt = Pt(x=x, y=y)
                if pt in self.bits:
                    c = None
                    for pos, bit_pt in enumerate(self.bits):
                        if c is not None:
                            break
                        if pt == bit_pt:
                            c = pos
                    if c == 0:
                        c = "H"
                    line.append(f"{c}")
                elif pt == Pt(x=0, y=0):
                    line.append("s")
                elif pt in self.path_of_tail:
                    line.append("#")
                else:
                    line.append(".")
            frame.append("".join(line))
        return "\n".join(frame)

    def drag(self, dir):
        next_bits = []
        head = self.bits[0] + dir
        next_bits.append(head)
        for nxt in self.bits[1:]:
            head = nxt.follow(head)
            next_bits.append(head)
        self.bits = next_bits
        self.path_of_tail.add(next_bits[-1])

    def make_move(self, move, animate=""):
        dir_key, count = move.split(" ")
        dir = DIR[dir_key]
        display = []
        for step in range(int(count)):
            self.drag(dir)
            if animate:
                frame = self.display(zoom_in=animate)
                display.append(f"{frame}\n{dir_key} {step+1}")
        return display

    def make_all_moves(self, move_list, animate=""):
        display = []
        for next_move in move_list:
            display += self.make_move(next_move, animate=animate)
        return display


with open("day_09_input.txt") as fp:
    RAW_INPUT = [line.strip() for line in fp]

RAW_SAMPLE = ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]

RAW_SAMPLE_2 = ["R 5", "U 8", "L 8", "D 3", "R 17", "D 10", "L 25", "U 20"]


def test_parse_move():
    assert len(RAW_SAMPLE) == 8
    assert len(RAW_INPUT) == 2000
    assert Pt(0, 0).follow(Pt(0, 0)) == Pt(0, 0)
    assert Pt(0, 0).follow(Pt(1, 0)) == Pt(0, 0)
    assert Pt(0, 0).follow(Pt(1, 1)) == Pt(0, 0)
    assert Pt(0, 0).follow(Pt(0, 2)) == Pt(0, 1)
    assert Pt(0, 0).follow(Pt(2, 1)) == Pt(1, 1)
    sample = String()
    sample.make_all_moves(RAW_SAMPLE)
    assert len(sample.path_of_tail) == 13

    sample = String(length=10)
    sample.make_all_moves(RAW_SAMPLE)
    assert len(sample.path_of_tail) == 1

    sample = String(length=10)
    sample.make_all_moves(RAW_SAMPLE_2)
    # sample.display()
    assert len(sample.path_of_tail) == 36

    sample = String()
    sample.make_all_moves(RAW_INPUT)
    assert len(sample.path_of_tail) == 6522
    # Originally guess of 6533 was high because
    # I forgot to reset the String()

    sample = String(length=10)
    sample.make_all_moves(RAW_INPUT)
    # sample.display()
    assert len(sample.path_of_tail) == 2717
    # Original guess of 2714 was too low
    # Finally debugged and got correct 2717
    # Issue was when moved more than 1,2 or 2,1
    # away need to just follow diagonal not jump
    # fully in line, fixed with sign function


def main(stdscr):
    sample = String(length=10)
    # frames = sample.make_all_moves(RAW_INPUT, animate='H')
    frames = sample.make_all_moves(RAW_SAMPLE_2, animate="H")
    for frame in frames:
        stdscr.clear()
        stdscr.addstr(0, 0, frame)
        stdscr.getch()
        # sleep(0.5)
        stdscr.refresh()


if __name__ == "__main__":
    wrapper(main)
