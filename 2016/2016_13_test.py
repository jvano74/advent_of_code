from typing import NamedTuple
from queue import PriorityQueue


class Puzzle:
    """
    --- Day 13: A Maze of Twisty Little Cubicles ---
    You arrive at the first floor of this new building to discover a much less welcoming environment than the shiny
    atrium of the last one. Instead, you are in a maze of twisty little cubicles, all alike.

    Every location in this area is addressed by a pair of non-negative integers (x,y). Each such coordinate is either
    a wall or an open space. You can't move diagonally. The cube maze starts at 0,0 and seems to extend infinitely
    toward positive x and y; negative values are invalid, as they represent a location outside the building. You
    are in a small waiting area at 1,1.

    While it seems chaotic, a nearby morale-boosting poster explains, the layout is actually quite logical. You can
    determine whether a given x,y coordinate will be a wall or an open space using a simple system:

    Find x*x + 3*x + 2*x*y + y + y*y.
    Add the office designer's favorite number (your puzzle input).
    Find the binary representation of that sum; count the number of bits that are 1.
    If the number of bits that are 1 is even, it's an open space.
    If the number of bits that are 1 is odd, it's a wall.

    For example, if the office designer's favorite number were 10, drawing walls as # and open spaces as .,
    the corner of the building containing 0,0 would look like this:

      0123456789
    0 .#.####.##
    1 ..#..#...#
    2 #....##...
    3 ###.#.###.
    4 .##..#..#.
    5 ..##....#.
    6 #...##.###

    Now, suppose you wanted to reach 7,4. The shortest route you could take is marked as O:

      0123456789
    0 .#.####.##
    1 .O#..#...#
    2 #OOO.##...
    3 ###O#.###.
    4 .##OO#OO#.
    5 ..##OOO.#.
    6 #...##.###

    Thus, reaching 7,4 would take a minimum of 11 steps (starting from your current location, 1,1).

    What is the fewest number of steps required for you to reach 31,39?

    Your puzzle input is 1362.

    --- Part Two ---
    How many locations (distinct x,y coordinates, including your starting location) can you reach
    in at most 50 steps?
    """
    pass


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Grid:
    def __init__(self, favorite):
        self.walls = {}
        self.favorite = favorite

    def is_wall(self, pt):
        if pt.x < 0 or pt.y < 0:
            return 1
        if pt in self.walls:
            return self.walls[pt]
        val = pt.x*pt.x + 3*pt.x + 2*pt.x*pt.y + pt.y + pt.y*pt.y + self.favorite
        bval = sum(1 for s in str(bin(val))[2:] if s == '1') % 2
        self.walls[pt] = bval
        return bval

    def display(self, max_pt, min_pt=Pt(0, 0)):
        result = []
        for y in range(min_pt[1], max_pt[1]):
            line = []
            for x in range(min_pt[0], max_pt[0]):
                wall_val = self.is_wall(Pt(x,y))
                line.append('#' if wall_val == 1 else '.')
            result.append(''.join(line))
        return result

    def find_open(self, pt, history):
        results = set()
        for delta in [Pt(1,0), Pt(0,1), Pt(-1,0), Pt(0,-1)]:
            pt_to_check = pt + delta
            if pt_to_check not in history and self.is_wall(pt_to_check) == 0:
                results.add(pt_to_check)
        return results

    def route(self, start, end=None, max_steps=None):
        boundary = PriorityQueue()
        history = set()

        boundary.put((0, start))
        history.add(start)
        while boundary.not_empty:
            cur_dist, cur_pt = boundary.get()
            if end is not None and cur_pt == end:
                return cur_dist
            if max_steps is not None and cur_dist >= max_steps:
                return len(history)
            for next_pt in self.find_open(cur_pt, history):
                boundary.put((cur_dist+1, next_pt))
                history.add(next_pt)


def test_sample_grid():
    sample_grid = Grid(10)
    result = sample_grid.display((10, 7))
    print('\n'.join(result))
    assert result == ['.#.####.##',
                      '..#..#...#',
                      '#....##...',
                      '###.#.###.',
                      '.##..#..#.',
                      '..##....#.',
                      '#...##.###']
    assert sample_grid.route(Pt(1, 1), Pt(7, 4)) == 11


def test_puzzle_grid():
    puzzle_grid = Grid(1362)
    assert puzzle_grid.route(Pt(1, 1), Pt(31, 39)) == 82
    assert puzzle_grid.route(Pt(1, 1), max_steps=50) == 138
