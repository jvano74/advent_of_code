from pathlib import Path
from typing import List, NamedTuple
from collections import defaultdict


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

    """


with open(Path(__file__).parent / "2025_09_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")
    RAW_INPUT.pop()

RAW_SAMPLE = ["7,1", "11,1", "11,7", "9,7", "9,5", "2,5", "2,3", "7,3"]


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


class Ln(NamedTuple):
    a: Pt
    b: Pt
    o: Pt
    v: Pt
    back_v: Pt
    v_unit: Pt
    v_len: int

    @classmethod
    def raw(cls, o, next, prev):
        v = next - o
        back_v = prev - o
        if v.x > 0:
            return cls(a=o, b=next, o=o, v=v, back_v=back_v, v_unit=Pt(1, 0), v_len=v.x)
        if v.x < 0:
            return cls(
                a=o, b=next, o=o, v=v, back_v=back_v, v_unit=Pt(-1, 0), v_len=-v.x
            )
        if v.y > 0:
            return cls(a=o, b=next, o=o, v=v, back_v=back_v, v_unit=Pt(0, 1), v_len=v.y)
        if v.y < 0:
            return cls(
                a=o, b=next, o=o, v=v, back_v=back_v, v_unit=Pt(0, -1), v_len=-v.y
            )

    def min(self):
        return Pt(min(self.a.x, self.b.x), min(self.a.y, self.b.y))

    def max(self):
        return Pt(max(self.a.x, self.b.x), max(self.a.y, self.b.y))

    def is_horizontal(self):
        return self.a.y == self.b.y

    def is_vertical(self):
        return self.a.x == self.b.x


class Box(NamedTuple):
    upper_left: Pt
    lower_right: Pt

    @classmethod
    def raw(cls, a, b):
        return cls(
            upper_left=Pt(min(a.x, b.x), min(a.y, b.y)),
            lower_right=Pt(max(a.x, b.x), max(a.y, b.y)),
        )

    def upper_right(self) -> Pt:
        return Pt(self.lower_right.x, self.upper_left.y)

    def lower_left(self) -> Pt:
        return Pt(self.upper_left.x, self.lower_right.y)

    def area(self) -> int:
        return self.lower_right.area(self.upper_left)

    def boundary(self) -> List[Ln]:
        return [
            Ln(a=self.upper_left, b=self.upper_right()),
            Ln(a=self.upper_right(), b=self.lower_right),
            Ln(a=self.lower_right, b=self.lower_left()),
            Ln(a=self.lower_left(), b=self.upper_left),
        ]


def clean_raw(raw_points: List[str]) -> List[Pt]:
    return [Pt.raw(p) for p in raw_points]


SAMPLE = clean_raw(RAW_SAMPLE)
MY_INPUT = clean_raw(RAW_INPUT)


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
            prev_pt = self.points[(i - 1) % length]
            next_pt = self.points[(i + 1) % length]
            self.outline[pt] = Ln.raw(pt, next_pt, prev_pt)
        self.min = Pt(min_x, min_y)
        self.max = Pt(max_x, max_y)

    def print(self, r_min, r_max, marked_points):
        boundary_pts = set()
        for pt in self.points:
            v_unit = self.outline[pt].v_unit
            step = pt
            for _ in range(1, self.outline[pt].v_len):
                step += v_unit
                if (r_min.x <= step.x <= r_max.x) and (r_min.y <= step.y <= r_max.y):
                    boundary_pts.add(step)

        out_array = []
        for y in range(r_min.y, r_max.y + 1):
            out_line = ""
            for x in range(r_min.x, r_max.x + 1):
                pt = Pt(x, y)
                if pt in marked_points:
                    out_line += marked_points[pt]
                elif pt in self.points:
                    out_line += "#"
                elif pt in boundary_pts:
                    out_line += "x"
                else:
                    out_line += "."
            out_array.append(out_line)
        return "\n".join(out_array)

    def is_intersected(self, a: Pt, b: Pt, new_area) -> bool:
        if new_area in (
            24,
            1393287318,
        ):
            _foo = self.outline[a]
            _bar = self.outline[b]
            display = self.print(
                Pt(min(a.x, b.x) - 5, min(a.y, b.y) - 5),
                Pt(max(a.x, b.x) + 5, max(a.y, b.y) + 5),
                {a: "A", b: "B"},
            )
            print(display)
            # debugging

        # box = Box.raw(a,b)

        min_x, max_x = min(a.x, b.x), max(a.x, b.x)
        min_y, max_y = min(a.y, b.y), max(a.y, b.y)

        if min_x == max_x or min_y == max_y:
            return False

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

        on_square_boundary = []
        for ln in self.outline.values():
            if ln.v.x == 0 and (min_x <= ln.o.x <= max_x):
                left_edge = True if min_x == ln.o.x else False
                right_edge = True if ln.o.x == max_x else False
                ln_min_y = min(ln.o.y, ln.o.y + ln.v.y)
                ln_max_y = max(ln.o.y, ln.o.y + ln.v.y)
                if ln_max_y < min_y or max_y < ln_min_y:
                    continue
                if ln_max_y == min_y or max_y == ln_min_y:
                    on_square_boundary.append(Pt(ln.o.x, ln_max_y))
                    continue
                if min_y < ln_max_y <= max_y:
                    if left_edge:
                        on_square_boundary.append(Pt(min_x, ln_max_y))
                        continue
                    if right_edge:
                        on_square_boundary.append(Pt(max_x, ln_max_y))
                        continue
                    return True
                if min_y <= ln_min_y < max_y:
                    if left_edge:
                        on_square_boundary.append(Pt(min_x, ln_min_y))
                        continue
                    if right_edge:
                        on_square_boundary.append(Pt(max_x, ln_min_y))
                        continue
                    return True
                # I think this occurs when the line goes clean through?
                return True

            if ln.v.y == 0 and (min_y <= ln.o.y <= max_y):
                top_edge = True if min_y == ln.o.y else False
                bottom_edge = True if ln.o.y == max_y else False
                ln_min_x = min(ln.o.x, ln.o.x + ln.v.x)
                ln_max_x = max(ln.o.x, ln.o.x + ln.v.x)
                if ln_max_x < min_x or max_x < ln_min_x:
                    continue
                if ln_max_x == min_x or max_x == ln_min_x:
                    on_square_boundary.append(Pt(ln_max_x, ln.o.y))
                    continue
                if min_x < ln_max_x <= max_x:
                    if top_edge:
                        on_square_boundary.append(Pt(ln_max_x, min_y))
                        continue
                    if bottom_edge:
                        on_square_boundary.append(Pt(ln_max_x, max_y))
                        continue
                    return True
                if min_x <= ln_min_x < max_x:
                    if top_edge:
                        on_square_boundary.append(Pt(ln_min_x, min_y))
                        continue
                    if bottom_edge:
                        on_square_boundary.append(Pt(ln_min_x, max_y))
                        continue
                    return True
                # I think this occurs when the line goes clean through?
                return True

        upper_left = Pt(min_x, min_y)
        upper_right = Pt(max_x, min_y)
        lower_right = Pt(max_x, max_y)
        lower_left = Pt(min_x, max_y)

        for corner in (self.outline[a], self.outline[b]):
            if corner.o == upper_left:
                if corner.v.x == 0 and (corner.v.y > 0 or corner.back_v.x < 0):
                    return True
                if corner.v.y == 0 and (corner.v.x < 0 and corner.back_v.y > 0):
                    return True
            if corner.o == upper_right:
                # REVIEW
                if corner.v.x == 0 and (corner.v.y < 0 and corner.back_v.x < 0):
                    return True
                if corner.v.y == 0 and (corner.v.x < 0 or corner.back_v.y < 0):
                    return True
            if corner.o == lower_right:
                if corner.v.x == 0 and (corner.v.y < 0 or corner.back_v.x > 0):
                    return True
                if corner.v.y == 0 and (corner.v.x > 0 and corner.back_v.y < 0):
                    return True
            if corner.o == lower_left:
                if corner.v.x == 0 and (corner.v.y > 0 and corner.back_v.x > 0):
                    return True
                if corner.v.y == 0 and (corner.v.x > 0 or corner.back_v.y > 0):
                    return True
        return False

    def max_rectangle(self, constrained=False) -> int:
        max_area = 0
        points = self.points[:]
        while points:
            a = points.pop()
            for b in points:
                new_area = a.area(b)
                if constrained and self.is_intersected(a, b, new_area):
                    continue
                max_area = max(max_area, new_area)
        return max_area


def test_max():
    sample_theater = Theater(SAMPLE)
    assert sample_theater.max_rectangle() == 50
    assert sample_theater.max_rectangle(constrained=True) == 24
    my_theater = Theater(MY_INPUT)
    assert my_theater.max_rectangle() == 4739623064
    assert my_theater.max_rectangle(constrained=True) == 1393287318
    # Guessed 4566128621 but this was too high, and 70757038 is too low
    # More refinement resulted in 4621312612 which is still too high
    # Updating the intersection detection dropped things to 1393287318
    # but this answer is still incorrect
