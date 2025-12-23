from pathlib import Path
from typing import List, NamedTuple


class Puzzle:
    """
    --- Day 9: Movie Theater ---
    You slide down the firepole in the corner of the playground and land in the
    North Pole base movie theater!

    The movie theater has a big tile floor with an interesting pattern. Elves
    here are redecorating the theater by switching out some of the square tiles
    in the big grid they form. Some of the tiles are red; the Elves would like
    to find the largest rectangle that uses red tiles for two of its opposite
    corners. They even have a list of where the red tiles are located in the
    grid (your puzzle input).

    For example:

    7,1
    11,1
    11,7
    9,7
    9,5
    2,5
    2,3
    7,3

    Showing red tiles as # and other tiles as ., the above arrangement of red
    tiles would look like this:

    ..............
    .......#...#..
    ..............
    ..#....#......
    ..............
    ..#......#....
    ..............
    .........#.#..
    ..............

    You can choose any two red tiles as the opposite corners of your rectangle;
    your goal is to find the largest rectangle possible.

    For example, you could make a rectangle (shown as O) with an area of 24
    between 2,5 and 9,7:

    ..............
    .......#...#..
    ..............
    ..#....#......
    ..............
    ..OOOOOOOO....
    ..OOOOOOOO....
    ..OOOOOOOO.#..
    ..............

    Or, you could make a rectangle with area 35 between 7,1 and 11,7:

    ..............
    .......OOOOO..
    .......OOOOO..
    ..#....OOOOO..
    .......OOOOO..
    ..#....OOOOO..
    .......OOOOO..
    .......OOOOO..
    ..............

    You could even make a thin rectangle with an area of only 6 between 7,3 and
    2,3:

    ..............
    .......#...#..
    ..............
    ..OOOOOO......
    ..............
    ..#......#....
    ..............
    .........#.#..
    ..............

    Ultimately, the largest rectangle you can make in this example has area 50.
    One way to do this is between 2,5 and 11,1:

    ..............
    ..OOOOOOOOOO..
    ..OOOOOOOOOO..
    ..OOOOOOOOOO..
    ..OOOOOOOOOO..
    ..OOOOOOOOOO..
    ..............
    .........#.#..
    ..............

    Using two red tiles as opposite corners, what is the largest area of any
    rectangle you can make?

    Your puzzle answer was 4739623064.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two --- The Elves just remembered: they can only switch out tiles
    that are red or green. So, your rectangle can only include red or green
    tiles.

    In your list, every red tile is connected to the red tile before and after
    it by a straight line of green tiles. The list wraps, so the first red tile
    is also connected to the last red tile. Tiles that are adjacent in your list
    will always be on either the same row or the same column.

    Using the same example as before, the tiles marked X would be green:

    ..............
    .......#XXX#..
    .......X...X..
    ..#XXXX#...X..
    ..X........X..
    ..#XXXXXX#.X..
    .........X.X..
    .........#X#..
    ..............

    In addition, all of the tiles inside this loop of red and green tiles are
    also green. So, in this example, these are the green tiles:

    ..............
    .......#XXX#..
    .......XXXXX..
    ..#XXXX#XXXX..
    ..XXXXXXXXXX..
    ..#XXXXXX#XX..
    .........XXX..
    .........#X#..
    ..............

    The remaining tiles are never red nor green.

    The rectangle you choose still must have red tiles in opposite corners, but
    any other tiles it includes must now be red or green. This significantly
    limits your options.

    For example, you could make a rectangle out of red and green tiles with an
    area of 15 between 7,3 and 11,1:

    ..............
    .......OOOOO..
    .......OOOOO..
    ..#XXXXOOOOO..
    ..XXXXXXXXXX..
    ..#XXXXXX#XX..
    .........XXX..
    .........#X#..
    ..............

    Or, you could make a thin rectangle with an area of 3 between 9,7 and 9,5:

    ..............
    .......#XXX#..
    .......XXXXX..
    ..#XXXX#XXXX..
    ..XXXXXXXXXX..
    ..#XXXXXXOXX..
    .........OXX..
    .........OX#..
    ..............

    The largest rectangle you can make in this example using only red and green
    tiles has area 24. One way to do this is between 9,5 and 2,3:

    ..............
    .......#XXX#..
    .......XXXXX..
    ..OOOOOOOOXX..
    ..OOOOOOOOXX..
    ..OOOOOOOOXX..
    .........XXX..
    .........#X#..
    ..............

    Using two red tiles as opposite corners, what is the largest area of any
    rectangle you can make using only red and green tiles?

    Your puzzle answer was 1654141440.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


RAW_SAMPLE = ["7,1", "11,1", "11,7", "9,7", "9,5", "2,5", "2,3", "7,3"]

with open(Path(__file__).parent / "2025_09_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")
    RAW_INPUT.pop()


class Pt(NamedTuple):
    x: int
    y: int

    @classmethod
    def raw(cls, raw):
        x, y = raw.split(",")
        return cls(int(x), int(y))

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def area(self, other):
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


def clean_raw(raw_points: List[str]) -> List[Pt]:
    return [Pt.raw(p) for p in raw_points]


SAMPLE = clean_raw(RAW_SAMPLE)
MY_INPUT = clean_raw(RAW_INPUT)


class Ln(NamedTuple):
    a: Pt
    b: Pt

    def min(self):
        return Pt(min(self.a.x, self.b.x), min(self.a.y, self.b.y))

    def max(self):
        return Pt(max(self.a.x, self.b.x), max(self.a.y, self.b.y))

    def is_horizontal(self):
        return self.a.y == self.b.y

    def is_vertical(self):
        return self.a.x == self.b.x

    def left(self) -> int:
        return min(self.a.x, self.b.x)

    def right(self) -> int:
        return max(self.a.x, self.b.x)

    def top(self) -> int:
        return min(self.a.y, self.b.y)

    def bottom(self) -> int:
        return max(self.a.y, self.b.y)


class Box(NamedTuple):
    upper_left: Pt
    lower_right: Pt

    @classmethod
    def raw(cls, a, b):
        return cls(
            upper_left=Pt(min(a.x, b.x), min(a.y, b.y)),
            lower_right=Pt(max(a.x, b.x), max(a.y, b.y)),
        )

    def left(self) -> int:
        return self.upper_left.x

    def right(self) -> int:
        return self.lower_right.x

    def top(self) -> int:
        return self.upper_left.y

    def bottom(self) -> int:
        return self.lower_right.y

    def area(self) -> int:
        return self.lower_right.area(self.upper_left)

    def inside(self, ln: Ln):
        if ln.is_vertical():
            if ln.a.x < self.left() or self.right() < ln.a.x:
                return False
            if ln.bottom() < self.top() or self.bottom() < ln.top():
                return False
            if ln.bottom() == self.top():
                # overlap = Pt(ln.a.x, ln.bottom())
                return False
            if self.bottom() == ln.top():
                # overlap = Pt(ln.a.x, ln.top())
                return False
            # overlap = Ln(
            #     a=Pt(ln.a.x, max(ln.top(), self.top())),
            #     b=Pt(ln.a.x, min(ln.bottom(), self.bottom())),
            # )
            if ln.a.x == self.left() and ln.a.y > ln.b.y:
                return False
            if ln.a.x == self.right() and ln.a.y < ln.b.y:
                return False
            return True

        if ln.is_horizontal():
            if ln.a.y < self.top() or self.bottom() < ln.a.y:
                return False
            if ln.right() < self.left() or self.right() < ln.left():
                return False
            if ln.right() == self.left():
                # overlap = Pt(ln.right(), ln.a.y)
                return False
            if self.right() == ln.left():
                # overlap = Pt(ln.left(), ln.a.y)
                return False
            # overlap = Ln(
            #     a=Pt(max(ln.left(), self.left()), ln.a.y),
            #     b=Pt(min(ln.right(), self.right()), ln.a.y),
            # )
            if ln.a.y == self.top() and ln.a.x < ln.b.x:
                return False
            if ln.a.y == self.bottom() and ln.a.x > ln.b.x:
                return False
            return True


class Theater:
    def __init__(
        self,
        points: List[Pt],
    ):
        self.points = points
        self.outline = {}
        length = len(points)
        max_x, max_y = -1, -1
        min_x, min_y = 1_000_000_000, 1_000_000_000

        for i, pt in enumerate(points):
            min_x, max_x = min(min_x, pt.x), max(max_x, pt.x)
            min_y, max_y = min(min_y, pt.y), max(max_y, pt.y)
            # prev_pt = self.points[(i - 1) % length]
            next_pt = self.points[(i + 1) % length]
            # self.outline[pt] = Ln(a=pt, b=next_pt, z=prev_pt)
            self.outline[pt] = Ln(a=pt, b=next_pt)
        self.min = Pt(min_x, min_y)
        self.max = Pt(max_x, max_y)

    def is_intersected(self, box: Box) -> bool:
        # This @ on the  | These @s on the
        # boundary is OK | boundary are not
        # .............. | ..............
        # .......#XXX#.. | .......#XXX#..
        # .......XXXXX.. | .......XXXXX..
        # ..1OOOO@O2XX.. | ..1OOOORO2XX..
        # ..OOOOOOOOXX.. | ..OOOOOOOOXX..
        # ..4OOOOOO3XX.. | ..@OOOOOO@XX..
        # .........XXX.. | ..?......?XX..
        # .........#X#.. | ..4??????3X#..
        # .............. | ..............
        # TESTING STUFF
        # if box.area() in (24, 50):
        #     test_area = box.area()
        #     pass
        for ln in self.outline.values():
            # TESTING STUFF
            # if ln.a == Pt(x=9, y=7):
            #     pass
            # if ln.a == Pt(x=9, y=5):
            #     pass
            # if ln == Ln(a=Pt(x=7, y=3), b=Pt(x=7, y=1)):
            #     pass
            if box.inside(ln):
                return True
        return False

    def max_rectangle(self, constrained=False) -> int:
        max_area = 0
        points = self.points[:]
        while points:
            a = points.pop()
            for b in points:
                box = Box.raw(a, b)
                if constrained and self.is_intersected(box):
                    continue
                max_area = max(max_area, box.area())
        return max_area


def test_max():
    sample_theater = Theater(SAMPLE)
    assert sample_theater.max_rectangle() == 50
    assert sample_theater.max_rectangle(constrained=True) == 24

    my_theater = Theater(MY_INPUT)
    assert my_theater.max_rectangle() == 4739623064

    # Guessed 4566128621 but this was too high, and 70757038 is too low
    # More refinement resulted in 4621312612 which is still too high
    # Updating the intersection detection dropped things to 1393287318
    # but this answer is still incorrect, finally did more refactoring
    # debugging and cleanup and finally got the answer of 1654141440
    assert my_theater.max_rectangle(constrained=True) == 1654141440
