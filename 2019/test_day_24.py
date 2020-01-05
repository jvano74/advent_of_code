from typing import List, NamedTuple
from collections import defaultdict


class Point(NamedTuple):
    x: int
    y: int


class Puzzle:
    """
    --- Day 24: Planet of Discord ---
    You land on Eris, your last stop before reaching Santa. As soon as you do,
     your sensors start picking up strange life forms moving around:
     Eris is infested with bugs! With an over 24-hour roundtrip for messages
     between you and Earth, you'll have to deal with this problem on your own.

    Eris isn't a very large place; a scan of the entire area fits into a 5x5 grid (your puzzle input).
    The scan shows bugs (#) and empty spaces (.).

    Each minute, The bugs live and die based on the number of bugs in the four adjacent tiles:

    A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
    An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
    Otherwise, a bug or empty space remains the same. (Tiles on the edges of the grid have fewer
    than four adjacent tiles; the missing tiles count as empty space.) This process happens in
    every location simultaneously; that is, within the same minute, the number of adjacent bugs
    is counted for every tile first, and then the tiles are updated.

    Here are the first few minutes of an example scenario:

    Initial state:
    ....#
    #..#.
    #..##
    ..#..
    #....

    After 1 minute:
    #..#.
    ####.
    ###.#
    ##.##
    .##..

    After 2 minutes:
    #####
    ....#
    ....#
    ...#.
    #.###

    After 3 minutes:
    #....
    ####.
    ...##
    #.##.
    .##.#

    After 4 minutes:
    ####.
    ....#
    ##..#
    .....
    ##...
    To understand the nature of the bugs, watch for the first time a layout of bugs and empty spaces matches
    any previous layout. In the example above, the first layout to appear twice is:

    .....
    .....
    .....
    #....
    .#...
    To calculate the biodiversity rating for this layout, consider each tile left-to-right in the top row,
    then left-to-right in the second row, and so on. Each of these tiles is worth biodiversity points equal
    to increasing powers of two: 1, 2, 4, 8, 16, 32, and so on. Add up the biodiversity points for tiles with
    bugs; in this example, the 16th tile (32768 points) and 22nd tile (2097152 points) have bugs, a total
    biodiversity rating of 2129920.

    What is the biodiversity rating for the first layout that appears twice?
    """

    INITIAL = ['#..#.',
               '..#..',
               '...##',
               '...#.',
               '#.###']

class Board:
    DELTAS = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]

    def __init__(self, raw: List):
        self.state = defaultdict(int)
        self.y_max = len(raw)
        self.x_max = len(raw[0])
        self.bio_history = set()
        for y, line in enumerate(raw):
            for x, c in enumerate(line):
                if c == '#':
                    self.state[Point(x,y)] = 1

    def show(self):
        for y in range(self.y_max):
            for x in range(self.x_max):
                print('#' if self.state[Point(x,y)] == 1 else '.', end='')
            print()

    def biodiversity(self):
        power = 1
        score = 0
        for y in range(self.y_max):
            for x in range(self.x_max):
                if self.state[Point(x,y)] == 1:
                    score += power
                power *= 2
        return score

    def step(self):
        next_state = defaultdict(int)
        for x in range(self.x_max):
            for y in range(self.y_max):
                neighbors = 0
                for d in self.DELTAS:
                    if self.state[Point(x + d.x, y + d.y)] == 1:
                        neighbors += 1
                if self.state[Point(x, y)] == 1:
                    next_state[Point(x, y)] = 1 if neighbors == 1 else 0
                else:
                    next_state[Point(x, y)] = 1 if neighbors == 1 or neighbors == 2 else 0
        self.state = next_state

    def find_first_repeated_state(self):
        biodiversity = self.biodiversity()
        while True:
            self.bio_history.add(biodiversity)
            self.step()
            biodiversity = self.biodiversity()
            if biodiversity in self.bio_history:
                return biodiversity


def test_submission():
    submission_board = Board(Puzzle.INITIAL)
    assert submission_board.find_first_repeated_state() == 24662545


def test_example_board_repeat():
    example_board = Board(['....#', '#..#.', '#..##', '..#..', '#....'])
    assert example_board.find_first_repeated_state() == 2129920


def test_small_board():
    small_board = Board(['###', '#.#', '###'])
    show = False
    if show:
        print()
        small_board.show()
    assert small_board.biodiversity() == 1 + 2 + 4 + 8 + 32 + 64 + 128 + 256


def test_example_board():
    example_board = Board(['....#', '#..#.', '#..##', '..#..', '#....'])
    show = False
    if show:
        print('Example Board')
        print()
        print('Initial')
        example_board.show()
    assert example_board.biodiversity() == 1205552
    example_board.step()
    if show:
        print()
        print('After 1 min')
        example_board.show()
    assert example_board.biodiversity() == 7200233
    example_board.step()
    if show:
        print()
        print('After 2 min')
        example_board.show()
    assert example_board.biodiversity() == 30687775
    example_board.step()
    if show:
        print()
        print('After 3 min')
        example_board.show()
    assert example_board.biodiversity() == 23519713
    example_board.step()
    if show:
        print()
        print('After 4 min')
        example_board.show()
    assert example_board.biodiversity() == 3165711
