from pathlib import Path
from typing import NamedTuple


class Puzzle:
    """
    --- Day 19: A Series of Tubes ---
    Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input),
    but it's confused about where to go.

    Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to
    take, starting by going down onto the only line connected to the top of the diagram. It needs to follow this path
    until it reaches the end (located somewhere within the diagram) and stop there.

    Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and
    only turn left or right when there's no other option. In addition, someone has left letters on the line; these
    also don't change its direction, but it can use them to keep track of where it's been. For example:

         |
         |  +--+
         A  |  C
     F---|----E|--+
         |  |  |  D
         +B-+  +--+

    Given this diagram, the packet needs to take the following path:

    - Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward
      to the first +.
    - Travel right, up, and right, passing through B in the process.
    - Continue down (collecting C), right, and up (collecting D).
    - Finally, go all the way left through E and stopping at F.

    Following the path to the end, the letters it sees on its path are ABCDEF.

    The little packet looks up at you, hoping you can help it find the way. What letters will it see
    (in the order it would see them) if it follows the path?
    (The routing diagram is very wide; make sure you view it without line wrapping.)

    --- Part Two ---
    The packet is curious how many steps it needs to go.

    For example, using the same routing diagram from the example above...

         |
         |  +--+
         A  |  C
     F---|--|-E---+
         |  |  |  D
         +B-+  +--+

    ...the packet would go:

    6 steps down (including the first line at the top of the diagram).
    3 steps right.
    4 steps up.
    3 steps right.
    4 steps down.
    3 steps right.
    2 steps up.
    13 steps left (including the F it stops on).
    This would result in a total of 38 steps.

    How many steps does the packet need to go?
    """

    pass


SAMPLE = [
    "     |         ",
    "     |  +--+   ",
    "     A  |  C   ",
    " F---|----E|--+",
    "     |  |  |  D",
    "     +B-+  +--+",
]

with open(Path(__file__).parent / "2017_19_input.txt") as fp:
    INPUTS = fp.read().split("\n")


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def rev(self):
        return Pt(-self.x, -self.y)


class Route:
    def __init__(self, raw_lines):
        self.map = {}
        for y, raw_line in enumerate(raw_lines):
            for x, c in enumerate(raw_line):
                if c != " ":
                    self.map[Pt(x, y)] = c
                    if y == 0:
                        self.start = Pt(x, y)

    def follow_path(self, loc=None, direction=Pt(0, 1)):
        dir_orientation = {Pt(1, 0): "-", Pt(0, 1): "|", Pt(-1, 0): "-", Pt(0, -1): "|"}
        ans = []
        dist = 0
        if loc is None:
            loc = self.start
        loc_c = self.map[loc]
        while loc_c != " ":
            if loc_c not in {"|", "-", "+"}:
                ans.append(loc_c)

            if loc_c != "+":
                loc += direction
                dist += 1
            else:
                for new_dir in {d for d in dir_orientation if d != direction.rev()}:
                    new_loc = loc + new_dir
                    if new_loc in self.map:
                        loc = new_loc
                        direction = new_dir
                        dist += 1
                        break
            if loc not in self.map:
                loc_c = " "
            else:
                loc_c = self.map[loc]
        return "".join(ans), dist


def test_route():
    route = Route(SAMPLE)
    assert route.follow_path() == ("ABCDEF", 38)


def test_puzzle_route():
    route = Route(INPUTS)
    assert route.follow_path() == ("EPYDUXANIT", 17544)
