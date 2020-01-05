from typing import List, NamedTuple
from collections import defaultdict


class Point(NamedTuple):
    x: int
    y: int
    z: int


class Puzzle2:
    """
    --- Part Two ---
    After careful analysis, one thing is certain: you have no idea where all these bugs are coming from.

    Then, you remember: Eris is an old Plutonian settlement! Clearly, the bugs are coming from recursively-folded space.

    This 5x5 grid is only one level in an infinite number of recursion levels. The tile in the middle of the grid is actually another 5x5 grid, the grid in your scan is contained as the middle tile of a larger 5x5 grid, and so on. Two levels of grids look like this:

         |     |         |     |
         |     |         |     |
         |     |         |     |
    -----+-----+---------+-----+-----
         |     |         |     |
         |     |         |     |
         |     |         |     |
    -----+-----+---------+-----+-----
         |     | | | | | |     |
         |     |-+-+-+-+-|     |
         |     | | | | | |     |
         |     |-+-+-+-+-|     |
         |     | | |?| | |     |
         |     |-+-+-+-+-|     |
         |     | | | | | |     |
         |     |-+-+-+-+-|     |
         |     | | | | | |     |
    -----+-----+---------+-----+-----
         |     |         |     |
         |     |         |     |
         |     |         |     |
    -----+-----+---------+-----+-----
         |     |         |     |
         |     |         |     |
         |     |         |     |
    (To save space, some of the tiles are not drawn to scale.) Remember, this is only a small part of the infinitely recursive grid; there is a 5x5 grid that contains this diagram, and a 5x5 grid that contains that one, and so on. Also, the ? in the diagram contains another 5x5 grid, which itself contains another 5x5 grid, and so on.

    The scan you took (your puzzle input) shows where the bugs are on a single level of this structure. The middle tile of your scan is empty to accommodate the recursive grids within it. Initially, no other levels contain bugs.

    Tiles still count as adjacent if they are directly up, down, left, or right of a given tile. Some tiles have adjacent tiles at a recursion level above or below its own level. For example:

         |     |         |     |
      1  |  2  |    3    |  4  |  5
         |     |         |     |
    -----+-----+---------+-----+-----
         |     |         |     |
      6  |  7  |    8    |  9  |  10
         |     |         |     |
    -----+-----+---------+-----+-----
         |     |A|B|C|D|E|     |
         |     |-+-+-+-+-|     |
         |     |F|G|H|I|J|     |
         |     |-+-+-+-+-|     |
     11  | 12  |K|L|?|N|O|  14 |  15
         |     |-+-+-+-+-|     |
         |     |P|Q|R|S|T|     |
         |     |-+-+-+-+-|     |
         |     |U|V|W|X|Y|     |
    -----+-----+---------+-----+-----
         |     |         |     |
     16  | 17  |    18   |  19 |  20
         |     |         |     |
    -----+-----+---------+-----+-----
         |     |         |     |
     21  | 22  |    23   |  24 |  25
         |     |         |     |
    Tile 19 has four adjacent tiles: 14, 18, 20, and 24.
    Tile G has four adjacent tiles: B, F, H, and L.
    Tile D has four adjacent tiles: 8, C, E, and I.
    Tile E has four adjacent tiles: 8, D, 14, and J.
    Tile 14 has eight adjacent tiles: 9, E, J, O, T, Y, 15, and 19.
    Tile N has eight adjacent tiles: I, O, S, and five tiles within the sub-grid marked ?.
    The rules about bugs living and dying are the same as before.

    For example, consider the same initial state as above:

    ....#
    #..#.
    #.?##
    ..#..
    #....
    The center tile is drawn as ? to indicate the next recursive grid. Call this level 0; the grid within this one is level 1, and the grid that contains this one is level -1. Then, after ten minutes, the grid at each level would look like this:

    Depth -5:
    ..#..
    .#.#.
    ..?.#
    .#.#.
    ..#..

    Depth -4:
    ...#.
    ...##
    ..?..
    ...##
    ...#.

    Depth -3:
    #.#..
    .#...
    ..?..
    .#...
    #.#..

    Depth -2:
    .#.##
    ....#
    ..?.#
    ...##
    .###.

    Depth -1:
    #..##
    ...##
    ..?..
    ...#.
    .####

    Depth 0:
    .#...
    .#.##
    .#?..
    .....
    .....

    Depth 1:
    .##..
    #..##
    ..?.#
    ##.##
    #####

    Depth 2:
    ###..
    ##.#.
    #.?..
    .#.##
    #.#..

    Depth 3:
    ..###
    .....
    #.?..
    #....
    #...#

    Depth 4:
    .###.
    #..#.
    #.?..
    ##.#.
    .....

    Depth 5:
    ####.
    #..#.
    #.?#.
    ####.
    .....
    In this example, after 10 minutes, a total of 99 bugs are present.

    Starting with your scan, how many bugs are present after 200 minutes?
    """

    INITIAL = ['#..#.',
               '..#..',
               '..?##',
               '...#.',
               '#.###']

class InfiniteBoard:
    DELTAS = [Point(0, 1, 0), Point(1, 0, 0), Point(0, -1, 0), Point(-1, 0, 0)]

    def __init__(self, raw: List):
        self.state = set()
        self.fold = set()
        self.y_max = len(raw)
        self.x_max = len(raw[0])
        self.generation = 0

        for y, line in enumerate(raw):
            for x, c in enumerate(line):
                if c == '#':
                    self.state.add(Point(x, y, 0))
                elif c == '?':
                    self.fold.add(Point(x, y, 0))

    def show(self):
        z_min = z_max = 0
        for pt in self.state:
            z_min = min(z_min, pt.z)
            z_max = max(z_max, pt.z)
        for z in range(z_min, z_max + 1):
            print(f'Level {z}')
            for y in range(self.y_max):
                for x in range(self.x_max):
                    if Point(x, y, z) in self.state:
                        print('#', end='')
                    elif Point(x, y, z) in self.fold:
                        print('?', end='')
                    else:
                        print('.', end='')
                print()

    def neighbors(self, cell):
        result = []
        for d in self.DELTAS:
            result.append(Point(cell.x + d.x, cell.y + d.y, cell.z + d.z))
        return result

    def step(self):
        neighbor_count = defaultdict(int)
        for cell in self.state:
            for nbh in self.neighbors(cell):
                neighbor_count[nbh] += 1
        next_state = set()
        for pt, cnt in neighbor_count.items():
            if cnt == 1:
                next_state.add(pt)
            elif cnt == 2 and pt not in self.state:
                next_state.add(pt)
        self.state = next_state


def test_example_board():
    example_board = InfiniteBoard(['....#', '#..#.', '#.?##', '..#..', '#....'])
    show = True
    if show:
        print('Example Board')
        print()
        print('Initial')
        example_board.show()
    assert len(example_board.state) == 8
    example_board.step()
    if show:
        print()
        print('After 1 min')
        example_board.show()
    assert len(example_board.state) == 23
    example_board.step()
    if show:
        print()
        print('After 2 min')
        example_board.show()
    # #assert len(example_board.state) == 1
    # example_board.step()
    # if show:
    #     print()
    #     print('After 3 min')
    #     example_board.show()
    # #assert len(example_board.state) == 1
    # example_board.step()
    # if show:
    #     print()
    #     print('After 4 min')
    #     example_board.show()
    # #assert len(example_board.state) == 1


def test_submission():
    submission_board = InfiniteBoard(Puzzle2.INITIAL)
    for _ in range(200):
        submission_board.step()
    bugs = len(submission_board.state)
    assert bugs == 1
