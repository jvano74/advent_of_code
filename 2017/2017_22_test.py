from pathlib import Path
from typing import NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 22: Sporifica Virus ---
    Diagnostics indicate that the local grid computing cluster has been contaminated with the Sporifica Virus.
    The grid computing cluster is a seemingly-infinite two-dimensional grid of compute nodes. Each node is either
    clean or infected by the virus.

    To prevent overloading the nodes (which would render them useless to the virus) or detection by system
    administrators, exactly one virus carrier moves through the network, infecting or cleaning nodes as it moves.
    The virus carrier is always located on a single node in the network (the current node) and keeps track of the
    direction it is facing.

    To avoid detection, the virus carrier works in bursts; in each burst, it wakes up, does some work, and goes
    back to sleep. The following steps are all executed in order one time each burst:

    - If the current node is infected, it turns to its right. Otherwise, it turns to its left.
      (Turning is done in-place; the current node does not change.)
    - If the current node is clean, it becomes infected. Otherwise, it becomes cleaned.
      (This is done after the node is considered for the purposes of changing direction.)
    - The virus carrier moves forward one node in the direction it is facing.

    Diagnostics have also provided a map of the node infection status (your puzzle input).
    Clean nodes are shown as .; infected nodes are shown as #. This map only shows the center of the grid;
    there are many more nodes beyond those shown, but none of them are currently infected.

    The virus carrier begins in the middle of the map facing up.

    For example, suppose you are given a map like this:

    ..#
    #..
    ...

    Then, the middle of the infinite grid looks like this, with the virus carrier's position marked with [ ]:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . # . . .
    . . . #[.]. . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .

    The virus carrier is on a clean node, so it turns left, infects the node, and moves left:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . # . . .
    . . .[#]# . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .

    The virus carrier is on an infected node, so it turns right, cleans the node, and moves up:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . .[.]. # . . .
    . . . . # . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .

    Four times in a row, the virus carrier finds a clean, infects it, turns left, and moves forward, ending in
    the same place and still facing up:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . #[#]. # . . .
    . . # # # . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .

    Now on the same node as before, it sees an infection, which causes it to turn right, clean the node,
    and move forward:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . # .[.]# . . .
    . . # # # . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .

    After the above actions, a total of 7 bursts of activity had taken place. Of them, 5 bursts of activity
    caused an infection.

    After a total of 70, the grid looks like this, with the virus carrier facing up:

    . . . . . # # . .
    . . . . # . . # .
    . . . # . . . . #
    . . # . #[.]. . #
    . . # . # . . # .
    . . . . . # # . .
    . . . . . . . . .
    . . . . . . . . .

    By this time, 41 bursts of activity caused an infection (though most of those nodes have since been cleaned).

    After a total of 10000 bursts of activity, 5587 bursts will have caused an infection.

    Given your actual map, after 10000 bursts of activity, how many bursts cause a node to become infected?
    (Do not count nodes that begin infected.)

    --- Part Two ---
    As you go to remove the virus from the infected nodes, it evolves to resist your attempt.

    Now, before it infects a clean node, it will weaken it to disable your defenses. If it encounters an infected node,
    it will instead flag the node to be cleaned in the future. So:

    - Clean nodes become weakened.
    - Weakened nodes become infected.
    - Infected nodes become flagged.
    - Flagged nodes become clean.

    Every node is always in exactly one of the above states.

    The virus carrier still functions in a similar way, but now uses the following logic during its bursts of action:

    - Decide which way to turn based on the current node:
      - If it is clean, it turns left.
      - If it is weakened, it does not turn, and will continue moving in the same direction.
      - If it is infected, it turns right.
      - If it is flagged, it reverses direction, and will go back the way it came.
    - Modify the state of the current node, as described above.
    - The virus carrier moves forward one node in the direction it is facing.

    Start with the same map (still using . for clean and # for infected) and still with the virus carrier starting
    in the middle and facing up.

    Using the same initial state as the previous example, and drawing weakened as W and flagged as F, the middle of
    the infinite grid looks like this, with the virus carrier's position again marked with [ ]:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . # . . .
    . . . #[.]. . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .

    This is the same as before, since no initial nodes are weakened or flagged. The virus carrier is on a clean node,
    so it still turns left, instead weakens the node, and moves left:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . # . . .
    . . .[#]W . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    The virus carrier is on an infected node, so it still turns right, instead flags the node, and moves up:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . .[.]. # . . .
    . . . F W . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    This process repeats three more times, ending on the previously-flagged node and facing right:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . W W . # . . .
    . . W[F]W . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    Finding a flagged node, it reverses direction and cleans the node:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . W W . # . . .
    . .[W]. W . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    The weakened node becomes infected, and it continues in the same direction:

    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . W W . # . . .
    .[.]# . W . . . .
    . . . . . . . . .
    . . . . . . . . .
    . . . . . . . . .
    Of the first 100 bursts, 26 will result in infection. Unfortunately, another feature of this evolved virus is
    speed; of the first 10_000_000 bursts, 2_511_944 will result in infection.

    Given your actual map, after 10_000_000 bursts of activity, how many bursts cause a node to become infected?
    (Do not count nodes that begin infected.)
    """

    pass


SAMPLE = ["..#", "#..", "..."]

with open(Path(__file__).parent / "2017_22_input.txt") as fp:
    INPUTS = [line.strip() for line in fp]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Turtle(NamedTuple):
    loc: Pt
    dir: int

    deltas = {0: Pt(0, -1), 1: Pt(1, 0), 2: Pt(0, 1), 3: Pt(-1, 0)}

    def right(self):
        return Turtle(self.loc, (self.dir + 1) % 4)

    def left(self):
        return Turtle(self.loc, (self.dir - 1) % 4)

    def step(self):
        return Turtle(self.loc + self.deltas[self.dir], self.dir)


def test_turtle():
    t = Turtle(Pt(0, 0), 0)
    assert t.loc == Pt(0, 0)
    t = t.right().step()
    assert t == Turtle(Pt(1, 0), 1)
    t = t.right().step()
    assert t == Turtle(Pt(1, 1), 2)
    t = t.right().step()
    assert t == Turtle(Pt(0, 1), 3)
    t = t.right().step()
    assert t == Turtle(Pt(0, 0), 0)
    t = t.left().step()
    assert t == Turtle(Pt(-1, 0), 3)
    t = t.left().step()
    assert t == Turtle(Pt(-1, 1), 2)
    t = t.left().step()
    assert t == Turtle(Pt(0, 1), 1)
    t = t.left().step()
    assert t == Turtle(Pt(0, 0), 0)


class Sporifica:
    def __init__(self, raw_inputs, evolved=False):
        self.evolved = evolved
        y = len(raw_inputs) // 2
        x = len(raw_inputs[0]) // 2
        self.start = Pt(x, y)
        self.t = Turtle(self.start, 0)
        self.initial_infections = defaultdict(chr)
        self.infections = 0
        for y, line in enumerate(raw_inputs):
            for x, c in enumerate(line):
                if c == "#":
                    self.initial_infections[Pt(x, y)] = "#"
        self.current = self.initial_infections.copy()

    def reset(self):
        self.t = Turtle(self.start, 0)
        self.current = self.initial_infections.copy()
        self.infections = 0

    def print_current(self):
        x_min = min(x for x, _ in self.current)
        x_max = max(x for x, _ in self.current)
        y_min = min(y for _, y in self.current)
        y_max = max(y for _, y in self.current)
        result = []
        boarder = 3
        for y in range(y_min - boarder, y_max + boarder + 1):
            line = []
            for x in range(x_min - boarder, x_max + boarder + 1):
                if y == self.t.loc.y and x + 1 == self.t.loc.x:
                    pad = "["
                elif y == self.t.loc.y and x == self.t.loc.x:
                    pad = "]"
                else:
                    pad = " "
                if Pt(x, y) in self.current:
                    c = self.current[Pt(x, y)]
                else:
                    c = "."
                line.append(f"{c}{pad}")
            result.append("".join(line))
        return result

    def step(self):
        t = self.t
        if t.loc not in self.current:
            if self.evolved:
                self.current[t.loc] = "W"
            else:
                self.current[t.loc] = "#"
                self.infections += 1
            self.t = t.left().step()
        elif self.current[t.loc] == "#":
            if self.evolved:
                self.current[t.loc] = "F"
            else:
                self.current.pop(t.loc)
            self.t = t.right().step()
        elif self.current[t.loc] == "W":
            self.current[t.loc] = "#"
            self.infections += 1
            self.t = t.step()
        elif self.current[t.loc] == "F":
            self.current.pop(t.loc)
            self.t = t.right().right().step()

    def run(self, number):
        for _ in range(number):
            self.step()
        return self.infections


def test_sample_sporifica():
    sporifica = Sporifica(SAMPLE)
    assert sporifica.start == Pt(1, 1)
    assert sporifica.initial_infections.keys() == {Pt(2, 0), Pt(0, 1)}

    for s in range(15):
        if s > 0:
            sporifica.step()
        print()
        print(s, sporifica.t)
        print("\n".join(sporifica.print_current()))

    sporifica.reset()
    assert sporifica.run(1) == 1
    assert sporifica.run(1) == 1
    assert sporifica.run(1) == 2
    assert sporifica.run(1) == 3
    assert sporifica.run(1) == 4

    sporifica.reset()
    assert sporifica.run(70) == 41

    sporifica.reset()
    assert sporifica.run(10000) == 5587


def test_puzzle_sporifica():
    sporifica = Sporifica(INPUTS)
    assert sporifica.run(10000) == 5447
    sporifica = Sporifica(INPUTS, evolved=True)
    assert sporifica.run(10_000_000) == 2511705
