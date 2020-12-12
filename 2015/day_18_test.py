from typing import List, NamedTuple
from collections import defaultdict


class Point(NamedTuple):
    x: int
    y: int


class Problem:
    """
    --- Day 18: Like a GIF For Your Yard ---
    After the million lights incident, the fire code has gotten stricter: now, at most
    ten thousand lights are allowed. You arrange them in a 100x100 grid.

    Never one to let you down, Santa again mails you instructions on the ideal lighting configuration.
    With so few lights, he says, you'll have to resort to animation.

    Start by setting your lights to the included initial configuration (your puzzle input). A # means "on",
    and a . means "off".

    Then, animate your grid in steps, where each step decides the next configuration based on the current one.
    Each light's next state (either on or off) depends on its current state and the current states of the eight
    lights adjacent to it (including diagonals). Lights on the edge of the grid might have fewer than eight
    neighbors; the missing ones always count as "off".

    For example, in a simplified 6x6 grid, the light marked A has the neighbors numbered 1 through 8, and
    the light marked B, which is on an edge, only has the neighbors marked 1 through 5:

    1B5...
    234...
    ......
    ..123.
    ..8A4.
    ..765.
    The state a light should have next is based on its current state (on or off) plus the number of
    neighbors that are on:

    A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
    All of the lights update simultaneously; they all consider the same current state before moving to the next.

    Here's a few steps from an example configuration of another 6x6 grid:

    Initial state:
    .#.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####..

    After 1 step:
    ..##..
    ..##.#
    ...##.
    ......
    #.....
    #.##..

    After 2 steps:
    ..###.
    ......
    ..###.
    ......
    .#....
    .#....

    After 3 steps:
    ...#..
    ......
    ...#..
    ..##..
    ......
    ......

    After 4 steps:
    ......
    ......
    ..##..
    ..##..
    ......
    ......

    After 4 steps, this example has four lights on.

    In your grid of 100x100 lights, given your initial configuration, how many lights are on after 100 steps?
    """

class Board:
    DELTAS = [Point(0, 1), Point(1, 1), Point(1, 0), Point(1, -1),
              Point(0, -1), Point(-1, -1), Point(-1, 0), Point(-1, 1)]

    def __init__(self, raw: List, broken=False):
        self.state = defaultdict(int)
        self.y_max = len(raw)
        self.x_max = len(raw[0])
        self.broken = broken
        for y, line in enumerate(raw):
            for x, c in enumerate(line):
                if c == '#':
                    self.state[Point(x,y)] = 1
        if self.broken:
            self.set_broken()

    def set_broken(self):
        self.state[Point(0, 0)] = 1
        self.state[Point(self.x_max - 1, 0)] = 1
        self.state[Point(self.x_max - 1, self.y_max - 1)] = 1
        self.state[Point(0, self.y_max - 1)] = 1

    def show(self):
        for y in range(self.y_max):
            for x in range(self.x_max):
                print('#' if self.state[Point(x,y)] == 1 else '.', end='')
            print()

    def step(self):
        next_state = defaultdict(int)
        for x in range(self.x_max):
            for y in range(self.y_max):
                neighbors = 0
                for d in self.DELTAS:
                    if self.state[Point(x + d.x, y + d.y)] == 1:
                        neighbors += 1
                if self.state[Point(x, y)] == 1:
                    if neighbors == 2 or neighbors == 3:
                        next_state[Point(x, y)] = 1
                else:
                    if neighbors == 3:
                        next_state[Point(x, y)] = 1
        self.state = next_state
        if self.broken:
            self.set_broken()
        return len(self.state)

TEST = ['.#.#.#',
        '...##.',
        '#....#',
        '..#...',
        '#.#..#',
        '####..']

def test_board():
    test_board = Board(TEST)
    for _ in range(4):
        num_on = test_board.step()
    assert num_on == 4


def test_submission():
    with open('day_18_input.txt') as fp:
        raw = fp.read()
    SUBMISSION = raw.split('\n')
    board = Board(SUBMISSION)
    for _ in range(100):
        num_on = board.step()
    assert num_on == 1061
    broken_board = Board(SUBMISSION,broken=True)
    for _ in range(100):
        num_on = broken_board.step()
        assert num_on == 1006


