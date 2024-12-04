from typing import NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 17: Conway Cubes ---
    As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the
    North Pole contact you. They'd like some help debugging a malfunctioning experimental energy source
    aboard one of their super-secret imaging satellites.

    The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained
    in a pocket dimension! When you hear it's having problems, you can't help but agree to take a look.

    The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional
    coordinate (x,y,z), there exists a single cube which is either active or inactive.

    In the initial state of the pocket dimension, almost all cubes start inactive. The only exception
    to this is a small flat region of cubes (your puzzle input); the cubes in this region start in
    the specified active (#) or inactive (.) state.

    The energy source then proceeds to boot up by executing six cycles.

    Each cube only ever considers its neighbors: any of the 26 other cubes where any of their
    coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3, its neighbors
    include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.

    During a cycle, all cubes simultaneously change their state according to the following rules:

    - If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
      Otherwise, the cube becomes inactive.

    - If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
      Otherwise, the cube remains inactive.

    The engineers responsible for this experimental energy source would like you to simulate the
    pocket dimension and determine what the configuration of cubes should be at the end of the
    six-cycle boot process.

    For example, consider the following initial state:

    .#.
    ..#
    ###

    Even though the pocket dimension is 3-dimensional, this initial state represents a small
    2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of
    the 3-dimensional space.)

    Simulating a few cycles from this initial state produces the following configurations,
    where the result of each cycle is shown layer-by-layer at each given z coordinate (and
    the frame of view follows the active cells in each cycle):

    Before any cycles:
    z=0
    .#.
    ..#
    ###

    After 1 cycle:
    z=-1    z=0    z=1
    #..     #.#    #..
    ..#     .##    ..#
    .#.     .#.    .#.

    After 2 cycles:
    z=-2     z=-1     z=0      z=1       z=2
    .....    ..#..    ##...    ..#..    .....
    .....    .#..#    ##...    .#..#    .....
    ..#..    ....#    #....    ....#    ..#..
    .....    .#...    ....#    .#...    .....
    .....    .....    .###.    .....    .....

    After 3 cycles:
    z=-2       z=-1       z=0        z=1        z=2
    .......    ..#....    ...#...    ..#....    .......
    .......    ...#...    .......    ...#...    .......
    ..##...    #......    #......    #......    ..##...
    ..###..    .....##    .......    .....##    ..###..
    .......    .#...#.    .....##    .#...#.    .......
    .......    ..#.#..    .##.#..    ..#.#..    .......
    .......    ...#...    ...#...    ...#...    .......

    After the full six-cycle boot process completes, 112 cubes are left in the active state.

    Starting with your given initial configuration, simulate six cycles.
    How many cubes are left in the active state after the sixth cycle?

    --- Part Two ---
    For some reason, your simulated results don't match what the experimental energy source engineers expected.
    Apparently, the pocket dimension actually has four spatial dimensions, not three.

    The pocket dimension contains an infinite 4-dimensional grid. At every integer 4-dimensional coordinate
    (x,y,z,w), there exists a single cube (really, a hypercube) which is still either active or inactive.

    Each cube only ever considers its neighbors: any of the 80 other cubes where any of their coordinates
    differ by at most 1. For example, given the cube at x=1,y=2,z=3,w=4, its neighbors include the cube at
    x=2,y=2,z=3,w=3, the cube at x=0,y=2,z=3,w=4, and so on.

    The initial state of the pocket dimension still consists of a small flat region of cubes. Furthermore,
    the same rules for cycle updating still apply: during each cycle, consider the number of active
    neighbors of each cube.

    For example, consider the same initial state as in the example above. Even though the pocket dimension
    is 4-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular,
    this initial state defines a 3x3x1x1 region of the 4-dimensional space.)

    Simulating a few cycles from this initial state produces the following configurations, where the result
    of each cycle is shown layer-by-layer at each given z and w coordinate:

    Before any cycles:

    z=0, w=0
    .#.
    ..#
    ###


    After 1 cycle:

    z=-1, w=-1
    #..
    ..#
    .#.

    z=0, w=-1
    #..
    ..#
    .#.

    z=1, w=-1
    #..
    ..#
    .#.

    z=-1, w=0
    #..
    ..#
    .#.

    z=0, w=0
    #.#
    .##
    .#.

    z=1, w=0
    #..
    ..#
    .#.

    z=-1, w=1
    #..
    ..#
    .#.

    z=0, w=1
    #..
    ..#
    .#.

    z=1, w=1
    #..
    ..#
    .#.


    After 2 cycles:

    z=-2, w=-2
    .....
    .....
    ..#..
    .....
    .....

    z=-1, w=-2
    .....
    .....
    .....
    .....
    .....

    z=0, w=-2
    ###..
    ##.##
    #...#
    .#..#
    .###.

    z=1, w=-2
    .....
    .....
    .....
    .....
    .....

    z=2, w=-2
    .....
    .....
    ..#..
    .....
    .....

    z=-2, w=-1
    .....
    .....
    .....
    .....
    .....

    z=-1, w=-1
    .....
    .....
    .....
    .....
    .....

    z=0, w=-1
    .....
    .....
    .....
    .....
    .....

    z=1, w=-1
    .....
    .....
    .....
    .....
    .....

    z=2, w=-1
    .....
    .....
    .....
    .....
    .....

    z=-2, w=0
    ###..
    ##.##
    #...#
    .#..#
    .###.

    z=-1, w=0
    .....
    .....
    .....
    .....
    .....

    z=0, w=0
    .....
    .....
    .....
    .....
    .....

    z=1, w=0
    .....
    .....
    .....
    .....
    .....

    z=2, w=0
    ###..
    ##.##
    #...#
    .#..#
    .###.

    z=-2, w=1
    .....
    .....
    .....
    .....
    .....

    z=-1, w=1
    .....
    .....
    .....
    .....
    .....

    z=0, w=1
    .....
    .....
    .....
    .....
    .....

    z=1, w=1
    .....
    .....
    .....
    .....
    .....

    z=2, w=1
    .....
    .....
    .....
    .....
    .....

    z=-2, w=2
    .....
    .....
    ..#..
    .....
    .....

    z=-1, w=2
    .....
    .....
    .....
    .....
    .....

    z=0, w=2
    ###..
    ##.##
    #...#
    .#..#
    .###.

    z=1, w=2
    .....
    .....
    .....
    .....
    .....

    z=2, w=2
    .....
    .....
    ..#..
    .....
    .....
    After the full six-cycle boot process completes, 848 cubes are left in the active state.

    Starting with your given initial configuration, simulate six cycles in a 4-dimensional space. How many cubes are left in the active state after the sixth cycle?
    """
    pass


SAMPLE = [
    '.#.',
    '..#',
    '###']

INPUT = [
    '#.#####.',
    '#..##...',
    '.##..#..',
    '#.##.###',
    '.#.#.#..',
    '#.##..#.',
    '#####..#',
    '..#.#.##']


class Pt(NamedTuple):
    x: int
    y: int
    z: int


class Board:
    def __init__(self, initial_lines, active_char='#'):
        self.grid = defaultdict(int)
        z = 0
        for y in range(len(initial_lines)):
            line = initial_lines[y]
            for x in range(len(line)):
                if line[x] == active_char:
                    self.grid[Pt(x, y, z)] = 1

    def total(self):
        return sum(self.grid[pt] for pt in self.grid)

    def step(self):
        radiation = defaultdict(int)
        for pt in self.grid:
            for dz in range(-1, 2):
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if not dx == dy == dz == 0:
                            radiation[Pt(pt.x + dx, pt.y + dy, pt.z + dz)] += 1
        next_grid = defaultdict(int)
        horizon = set(radiation).union(set(self.grid))
        for pt in horizon:
            if self.grid[pt] == 1 and 2 <= radiation[pt] <= 3:
                next_grid[pt] = 1
            elif self.grid[pt] == 0 and radiation[pt] == 3:
                next_grid[pt] = 1
        self.grid = next_grid


def test_board():
    sample_board = Board(SAMPLE)
    assert sample_board.total() == 5
    sample_board.step()
    assert sample_board.total() == 11
    for _ in range(5):
        sample_board.step()
    assert sample_board.total() == 112
    # and now for my input
    game_board = Board(INPUT)
    for _ in range(6):
        game_board.step()
    assert game_board.total() == 353


class P4(NamedTuple):
    x: int
    y: int
    z: int
    w: int


class Board4:
    def __init__(self, initial_lines, active_char='#'):
        self.grid = defaultdict(int)
        z, w = 0, 0
        for y in range(len(initial_lines)):
            line = initial_lines[y]
            for x in range(len(line)):
                if line[x] == active_char:
                    self.grid[P4(x, y, z, w)] = 1

    def total(self):
        return sum(self.grid[pt] for pt in self.grid)

    def step(self):
        radiation = defaultdict(int)
        for pt in self.grid:
            for dw in range(-1, 2):
                for dz in range(-1, 2):
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if not dx == dy == dz == dw == 0:
                                radiation[P4(pt.x + dx, pt.y + dy, pt.z + dz, pt.w + dw)] += 1
        next_grid = defaultdict(int)
        horizon = set(radiation).union(set(self.grid))
        for pt in horizon:
            if self.grid[pt] == 1 and 2 <= radiation[pt] <= 3:
                next_grid[pt] = 1
            elif self.grid[pt] == 0 and radiation[pt] == 3:
                next_grid[pt] = 1
        self.grid = next_grid


def test_board():
    sample_board = Board4(SAMPLE)
    assert sample_board.total() == 5
    sample_board.step()
    assert sample_board.total() == 29
    for _ in range(5):
        sample_board.step()
    assert sample_board.total() == 848
    # and now for my input
    game_board = Board4(INPUT)
    for _ in range(6):
        game_board.step()
    assert game_board.total() == 2472
