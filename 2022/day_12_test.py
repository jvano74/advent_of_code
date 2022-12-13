from typing import NamedTuple
from queue import PriorityQueue


class Puzzle:
    """
    --- Day 12: Hill Climbing Algorithm ---

    You try contacting the Elves using your handheld device, but the river
    you're following must be too low to get a decent signal.

    You ask the device for a heightmap of the surrounding area (your puzzle
    input). The heightmap shows the local area from above broken into a grid;
    the elevation of each square of the grid is given by a single lowercase
    letter, where a is the lowest elevation, b is the next-lowest, and so on up
    to the highest elevation, z.

    Also included on the heightmap are marks for your current position (S) and
    the location that should get the best signal (E). Your current position (S)
    has elevation a, and the location that should get the best signal (E) has
    elevation z.

    You'd like to reach E, but to save energy, you should do it in as few steps
    as possible. During each step, you can move exactly one square up, down,
    left, or right. To avoid needing to get out your climbing gear, the
    elevation of the destination square can be at most one higher than the
    elevation of your current square; that is, if your current elevation is m,
    you could step to elevation n, but not to elevation o. (This also means that
    the elevation of the destination square can be much lower than the elevation
    of your current square.)

    For example:

    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi

    Here, you start in the top-left corner; your goal is near the middle. You
    could start by moving down or right, but eventually you'll need to head
    toward the e at the bottom. From there, you can spiral around to the goal:

    v..v<<<<
    >v.vv<<^
    .>vv>E^^
    ..v>>>^^
    ..>>>>>^

    In the above diagram, the symbols indicate whether the path exits each
    square moving up (^), down (v), left (<), or right (>). The location that
    should get the best signal is still E, and . marks unvisited squares.

    This path reaches the goal in 31 steps, the fewest possible.

    What is the fewest steps required to move from your current position to the
    location that should get the best signal?

    --- Part Two ---

    As you walk up the hill, you suspect that the Elves will want to turn this
    into a hiking trail. The beginning isn't very scenic, though; perhaps you
    can find a better starting point.

    To maximize exercise while hiking, the trail should start as low as
    possible: elevation a. The goal is still the square marked E. However, the
    trail should still be direct, taking the fewest steps to reach its goal. So,
    you'll need to find the shortest path from any square at elevation a to the
    square marked E.

    Again consider the example from above:

    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi

    Now, there are six choices for starting position (five marked a, plus the
    square marked S that counts as being at elevation a). If you start at the
    bottom-left square, you can reach the goal most quickly:

    ...v<<<<
    ...vv<<^
    ...v>E^^
    .>v>>>^^
    >^>>>>>^

    This path reaches the goal in only 29 steps, the fewest possible.

    What is the fewest steps required to move starting from any square with
    elevation a to the location that should get the best signal?
    """


SAMPLE = ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]


with open("day_12_input.txt") as fp:
    INPUT = [line.strip() for line in fp]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def up(self):
        return Pt(self.x, self.y - 1)

    def down(self):
        return Pt(self.x, self.y + 1)

    def left(self):
        return Pt(self.x - 1, self.y)

    def right(self):
        return Pt(self.x + 1, self.y)


class Map:
    def __init__(self, raw_map) -> None:
        self.map = {}
        for y, line in enumerate(raw_map):
            for x, c in enumerate(line):
                pt = Pt(x, y)
                h = ord(c) - ord("a") + 1
                if c == "S":
                    self.start = pt
                    h = 1
                if c == "E":
                    self.end = pt
                    h = ord("z") - ord("a") + 1
                self.map[pt] = h

    def neighbors(self, pt: Pt):
        ok = set()
        for tst in [pt.up(), pt.down(), pt.left(), pt.right()]:
            if tst in self.map and self.map[pt] + 1 >= self.map[tst]:
                ok.add(tst)
        return ok

    def find_route(self, start, end, max_path=None):
        exploring = PriorityQueue()
        history = set()
        exploring.put((0, start))
        history.add(start)
        while not exploring.empty():
            move_count, current_pt = exploring.get()
            if max_path is not None and move_count > max_path:
                return
            if current_pt == end:
                return move_count
            else:
                for next_pt in self.neighbors(current_pt):
                    if next_pt not in history:
                        exploring.put((move_count + 1, next_pt))
                        history.add(next_pt)

    def min_distance(self):
        return self.find_route(self.start, self.end)

    def min_distance_any_start(self):
        min_distance = self.find_route(self.start, self.end)
        for start in self.map:
            if self.map[start] == 1:
                alt_route = self.find_route(start, self.end, max_path=min_distance)
                if alt_route is not None and alt_route < min_distance:
                    min_distance = alt_route
        return min_distance


def test_map():
    sample_map = Map(SAMPLE)
    assert sample_map.start == Pt(0, 0)
    assert sample_map.end == Pt(5, 2)
    assert sample_map.min_distance() == 31
    assert sample_map.min_distance_any_start() == 29

    my_map = Map(INPUT)
    assert my_map.min_distance() == 420
    assert my_map.min_distance_any_start() == 414
