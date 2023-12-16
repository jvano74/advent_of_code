from collections import defaultdict
from typing import NamedTuple


class Puzzle:
    """
    --- Day 16: The Floor Will Be Lava ---
    With the beam of light completely focused somewhere, the reindeer leads you
    deeper still into the Lava Production Facility. At some point, you realize
    that the steel facility walls have been replaced with cave, and the doorways
    are just cave, and the floor is cave, and you're pretty sure this is
    actually just a giant cave.

    Finally, as you approach what must be the heart of the mountain, you see a
    bright light in a cavern up ahead. There, you discover that the beam of
    light you so carefully focused is emerging from the cavern wall closest to
    the facility and pouring all of its energy into a contraption on the
    opposite side.

    Upon closer inspection, the contraption appears to be a flat,
    two-dimensional square grid containing empty space (.), mirrors (/ and \),
    and splitters (| and -).

    The contraption is aligned so that most of the beam bounces around the grid,
    but each tile on the grid converts some of the beam's light into heat to
    melt the rock in the cavern.

    You note the layout of the contraption (your puzzle input). For example:

    .|...\....
    |.-.\.....
    .....|-...
    ........|.
    ..........
    .........\
    ..../.\\..
    .-.-/..|..
    .|....-|.\
    ..//.|....

    The beam enters in the top-left corner from the left and heading to the
    right. Then, its behavior depends on what it encounters as it moves:

    - If the beam encounters empty space (.), it continues in the same
      direction.
    - If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees
      depending on the angle of the mirror. For instance, a rightward-moving
      beam that encounters a / mirror would continue upward in the mirror's
      column, while a rightward-moving beam that encounters a \ mirror would
      continue downward from the mirror's column.
    - If the beam encounters the pointy end of a splitter (| or -), the beam
      passes through the splitter as if the splitter were empty space. For
      instance, a rightward-moving beam that encounters a - splitter would
      continue in the same direction.
    - If the beam encounters the flat side of a splitter (| or -), the beam is
      split into two beams going in each of the two directions the splitter's
      pointy ends are pointing. For instance, a rightward-moving beam that
      encounters a | splitter would split into two beams: one that continues
      upward from the splitter's column and one that continues downward from the
      splitter's column.

    Beams do not interact with other beams; a tile can have many beams passing
    through it at the same time. A tile is energized if that tile has at least
    one beam pass through it, reflect in it, or split in it.

    In the above example, here is how the beam of light bounces around the contraption:

    >|<<<\....
    |v-.\^....
    .v...|->>>
    .v...v^.|.
    .v...v^...
    .v...v^..\
    .v../2\\..
    <->-/vv|..
    .|<<<2-|.\
    .v//.|.v..

    Beams are only shown on empty tiles; arrows indicate the direction of the
    beams. If a tile contains beams moving in multiple directions, the number of
    distinct directions is shown instead. Here is the same diagram but instead
    only showing whether a tile is energized (#) or not (.):

    ######....
    .#...#....
    .#...#####
    .#...##...
    .#...##...
    .#...##...
    .#..####..
    ########..
    .#######..
    .#...#.#..

    Ultimately, in this example, 46 tiles become energized.

    The light isn't energizing enough tiles to produce lava; to debug the
    contraption, you need to start by analyzing the current situation. With the
    beam starting in the top-left heading right, how many tiles end up being
    energized?

    """

    """
    Your puzzle answer was 7884.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    As you try to work out what might be wrong, the reindeer tugs on your shirt
    and leads you to a nearby control panel. There, a collection of buttons lets
    you align the contraption so that the beam enters from any edge tile and
    heading away from that edge. (You can choose either of two directions for
    the beam if it starts on a corner; for instance, if the beam starts in the
    bottom-right corner, it can start heading either left or upward.)

    So, the beam could start on any tile in the top row (heading downward), any
    tile in the bottom row (heading upward), any tile in the leftmost column
    (heading right), or any tile in the rightmost column (heading left). To
    produce lava, you need to find the configuration that energizes as many
    tiles as possible.

    In the above example, this can be achieved by starting the beam in the
    fourth tile from the left in the top row:

    .|<2<\....
    |v-v\^....
    .v.v.|->>>
    .v.v.v^.|.
    .v.v.v^...
    .v.v.v^..\
    .v.v/2\\..
    <-2-/vv|..
    .|<<<2-|.\
    .v//.|.v..

    Using this configuration, 51 tiles are energized:

    .#####....
    .#.#.#....
    .#.#.#####
    .#.#.##...
    .#.#.##...
    .#.#.##...
    .#.#####..
    ########..
    .#######..
    .#...#.#..

    Find the initial beam configuration that energizes the largest number of
    tiles; how many tiles are energized in that configuration?

    Your puzzle answer was 8185.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


class Pt(NamedTuple):
    x: str
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


with open("day_16_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")


RAW_SAMPLE = [
    ".|...\\....",  # note need to escape the \
    "|.-.\\.....",
    ".....|-...",
    "........|.",
    "..........",
    ".........\\",
    "..../.\\\\..",
    ".-.-/..|..",
    ".|....-|.\\",
    "..//.|....",
]

MIRROR_MAP = {
    "/": {
        Pt(1, 0): [Pt(0, -1)],
        Pt(0, 1): [Pt(-1, 0)],
        Pt(-1, 0): [Pt(0, 1)],
        Pt(0, -1): [Pt(1, 0)],
    },
    "\\": {
        Pt(1, 0): [Pt(0, 1)],
        Pt(0, 1): [Pt(1, 0)],
        Pt(-1, 0): [Pt(0, -1)],
        Pt(0, -1): [Pt(-1, 0)],
    },
    "-": {
        Pt(1, 0): [Pt(1, 0)],
        Pt(0, 1): [Pt(-1, 0), Pt(1, 0)],
        Pt(-1, 0): [Pt(-1, 0)],
        Pt(0, -1): [Pt(-1, 0), Pt(1, 0)],
    },
    "|": {
        Pt(1, 0): [Pt(0, -1), Pt(0, 1)],
        Pt(0, 1): [Pt(0, 1)],
        Pt(-1, 0): [Pt(0, -1), Pt(0, 1)],
        Pt(0, -1): [Pt(0, -1)],
    },
}


class Lava:
    def __init__(self, raw_mirrors) -> None:
        self.mirrors = dict()
        self.y_max = 0
        self.x_max = 0
        for y, raw_line in enumerate(raw_mirrors):
            self.y_max = max(self.y_max, y)
            for x, c in enumerate(raw_line):
                self.x_max = max(self.x_max, x)
                if c != ".":
                    self.mirrors[Pt(x, y)] = c

    def shine_light(self, start=Pt(0, 0), direction=Pt(1, 0)):
        light = defaultdict(set)
        light[start].add(direction)
        boundry = [(start, direction)]
        while boundry:
            (position, direction) = boundry.pop()
            if position not in self.mirrors:
                new_position = position + direction
                if (
                    direction not in light[new_position]
                    and 0 <= new_position.x <= self.x_max
                    and 0 <= new_position.y <= self.y_max
                ):
                    boundry.append((new_position, direction))
                    light[new_position].add(direction)
            else:
                for new_direction in MIRROR_MAP[self.mirrors[position]][direction]:
                    new_position = position + new_direction
                    if (
                        new_direction not in light[new_position]
                        and 0 <= new_position.x <= self.x_max
                        and 0 <= new_position.y <= self.y_max
                    ):
                        boundry.append((new_position, new_direction))
                        light[new_position].add(new_direction)
        return sum(1 for _, d in light.items() if len(d))

    def all_around(self):
        positions = []
        for x in range(self.x_max + 1):
            positions.append((Pt(x, 0), Pt(0, 1)))
            positions.append((Pt(x, self.y_max), Pt(0, -1)))
        for y in range(self.y_max + 1):
            positions.append((Pt(0, y), Pt(1, 0)))
            positions.append((Pt(self.x_max, y), Pt(-1, 0)))
        return max(self.shine_light(p, v) for p, v in positions)


def test_lava():
    my_sample = Lava(RAW_SAMPLE)
    assert my_sample.shine_light() == 46
    assert my_sample.all_around() == 51

    my_input = Lava(RAW_INPUT)
    assert my_input.shine_light() == 7884
    assert my_input.all_around() == 8185
