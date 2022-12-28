from __future__ import annotations
from typing import NamedTuple


class Puzzle:
    """
    --- Day 22: Monkey Map ---
    The monkeys take you on a surprisingly easy trail through the jungle.
    They're even going in roughly the right direction according to your handheld
    device's Grove Positioning System.

    As you walk, the monkeys explain that the grove is protected by a force
    field. To pass through the force field, you have to enter a password; doing
    so involves tracing a specific path on a strangely-shaped board.

    At least, you're pretty sure that's what you have to do; the elephants
    aren't exactly fluent in monkey.

    The monkeys give you notes that they took when they last saw the password
    entered (your puzzle input).

    For example:

            ...#
            .#..
            #...
            ....
    ...#.......#
    ........#...
    ..#....#....
    ..........#.
            ...#....
            .....#..
            .#......
            ......#.

    10R5L5R10L4R5L5

    The first half of the monkeys' notes is a map of the board. It is comprised
    of a set of open tiles (on which you can move, drawn .) and solid walls
    (tiles which you cannot enter, drawn #).

    The second half is a description of the path you must follow. It consists of
    alternating numbers and letters:

    A number indicates the number of tiles to move in the direction you are
    facing. If you run into a wall, you stop moving forward and continue with
    the next instruction.

    A letter indicates whether to turn 90 degrees clockwise (R) or
    counterclockwise (L). Turning happens in-place; it does not change your
    current tile.

    So, a path like 10R5 means "go forward 10 tiles, then turn clockwise 90
    degrees, then go forward 5 tiles".

    You begin the path in the leftmost open tile of the top row of tiles.
    Initially, you are facing to the right (from the perspective of how the map
    is drawn).

    If a movement instruction would take you off of the map, you wrap around to
    the other side of the board. In other words, if your next tile is off of the
    board, you should instead look in the direction opposite of your current
    facing as far as you can until you find the opposite edge of the board, then
    reappear there.

    For example, if you are at A and facing to the right, the tile in front of
    you is marked B; if you are at C and facing down, the tile in front of you
    is marked D:

            ...#
            .#..
            #...
            ....
    ...#.D.....#
    ........#...
    B.#....#...A
    .....C....#.
            ...#....
            .....#..
            .#......
            ......#.

    It is possible for the next tile (after wrapping around) to be a wall; this
    still counts as there being a wall in front of you, and so movement stops
    before you actually wrap to the other side of the board.

    By drawing the last facing you had with an arrow on each tile you visit, the
    full path taken by the above example looks like this:

            >>v#
            .#v.
            #.v.
            ..v.
    ...#...v..v#
    >>>v...>#.>>
    ..#v...#....
    ...>>>>v..#.
            ...#....
            .....#..
            .#......
            ......#.

    To finish providing the password to this strange input device, you need to
    determine numbers for your final row, column, and facing as your final
    position appears from the perspective of the original map. Rows start from 1
    at the top and count downward; columns start from 1 at the left and count
    rightward. (In the above example, row 1, column 1 refers to the empty space
    with no tile on it in the top-left corner.) Facing is 0 for right (>), 1 for
    down (v), 2 for left (<), and 3 for up (^). The final password is the sum of
    1000 times the row, 4 times the column, and the facing.

    In the above example, the final row is 6, the final column is 8, and the
    final facing is 0. So, the final password is 1000 * 6 + 4 * 8 + 0: 6032.

    Follow the path given in the monkeys' notes. What is the final password?

    Your puzzle answer was 106094.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    As you reach the force field, you think you hear some Elves in the distance.
    Perhaps they've already arrived?

    You approach the strange input device, but it isn't quite what the monkeys
    drew in their notes. Instead, you are met with a large cube; each of its six
    faces is a square of 50x50 tiles.

    To be fair, the monkeys' map does have six 50x50 regions on it. If you were
    to carefully fold the map, you should be able to shape it into a cube!

    In the example above, the six (smaller, 4x4) faces of the cube are:

            1111
            1111
            1111
            1111
    222233334444
    222233334444
    222233334444
    222233334444
            55556666
            55556666
            55556666
            55556666

    You still start in the same position and with the same facing as before, but
    the wrapping rules are different. Now, if you would walk off the board, you
    instead proceed around the cube. From the perspective of the map, this can
    look a little strange. In the above example, if you are at A and move to the
    right, you would arrive at B facing down; if you are at C and move down, you
    would arrive at D facing up:

            ...#
            .#..
            #...
            ....
    ...#.......#
    ........#..A
    ..#....#....
    .D........#.
            ...#..B.
            .....#..
            .#......
            ..C...#.

    Walls still block your path, even if they are on a different face of the
    cube. If you are at E facing up, your movement is blocked by the wall marked
    by the arrow:

            ...#
            .#..
        -->#...
            ....
    ...#..E....#
    ........#...
    ..#....#....
    ..........#.
            ...#....
            .....#..
            .#......
            ......#.

    Using the same method of drawing the last facing you had with an arrow on
    each tile you visit, the full path taken by the above example now looks like
    this:

            >>v#
            .#v.
            #.v.
            ..v.
    ...#..^...v#
    .>>>>>^.#.>>
    .^#....#....
    .^........#.
            ...#..v.
            .....#v.
            .#v<<<<.
            ..v...#.

    The final password is still calculated from your final position and facing
    from the perspective of the map. In this example, the final row is 5, the
    final column is 7, and the final facing is 3, so the final password is 1000
    * 5 + 4 * 7 + 3 = 5031.

    Fold the map into a cube, then follow the path given in the monkeys' notes.
    What is the final password?

    """


with open("day_22_sample.txt") as fp:
    SAMPLE_MAP, SAMPLE_DIRECTIONS = fp.read().split("\n\n")


with open("day_22_input.txt") as fp:
    MY_MAP, MY_DIRECTIONS = fp.read().split("\n\n")


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Pt) -> Pt:
        return Pt(x=self.x + other.x, y=self.y + other.y)

    def __neg__(self) -> Pt:
        return Pt(x=-self.x, y=-self.y)

    def __sub__(self, other: Pt) -> Pt:
        return Pt(x=self.x - other.x, y=self.y - other.y)


DIRECTIONS = [Pt(1, 0), Pt(0, 1), Pt(-1, 0), Pt(0, -1)]


ROTATION = {
    (Pt(1, 0), "L"): Pt(0, -1),
    (Pt(0, -1), "L"): Pt(-1, 0),
    (Pt(-1, 0), "L"): Pt(0, 1),
    (Pt(0, 1), "L"): Pt(1, 0),
    (Pt(1, 0), "R"): Pt(0, 1),
    (Pt(0, 1), "R"): Pt(-1, 0),
    (Pt(-1, 0), "R"): Pt(0, -1),
    (Pt(0, -1), "R"): Pt(1, 0),
}


class V(NamedTuple):
    pt: Pt
    v: Pt

    def __neg__(self) -> V:
        return V(pt=self.pt, v=-self.v)

    def fwd(self) -> V:
        return V(pt=self.pt + self.v, v=self.v)

    def bkwd(self) -> V:
        return V(pt=self.pt - self.v, v=self.v)

    def cw(self) -> V:
        return V(pt=self.pt, v=ROTATION[self.v, "R"])

    def ccw(self) -> V:
        return V(pt=self.pt, v=ROTATION[self.v, "L"])

    def cw_fwd(self) -> V:
        return V(pt=self.pt + ROTATION[self.v, "R"], v=self.v)

    def ccw_fwd(self) -> V:
        return V(pt=self.pt + ROTATION[self.v, "L"], v=self.v)

    def cw_fwd_ccw(self) -> V:
        next_pt = self.pt + self.v + ROTATION[self.v, "R"]
        return V(pt=next_pt, v=ROTATION[self.v, "L"])

    def ccw_fwd_cw(self) -> V:
        next_pt = self.pt + self.v + ROTATION[self.v, "L"]
        return V(pt=next_pt, v=ROTATION[self.v, "R"])


class MonkeyMap:
    def __init__(self, map, directions, cube=False, trace=False) -> None:
        self.trace = trace

        self.directions = directions.replace("L", ",L,").replace("R", ",R,").split(",")

        # process board
        self.board = {}
        self.boundry = {}
        self.process_map(map=map)

        # mark starting point
        loc_y = 0  # assume map starts on first line
        loc_x = min(ptn.pt.x for ptn in self.boundry if ptn.pt.y == 0)
        self.location = V(pt=Pt(x=loc_x, y=loc_y), v=Pt(x=1, y=0))

        self.flat_map = {}
        for ptn in self.boundry:
            self.flat_map[ptn] = self.wrap_flat_point(ptn)

        self.cube_map = {}
        corners = [ptn for ptn, type in self.boundry.items() if type == "-x"]
        while corners:
            ccw_ptn = corners.pop()
            cw_ptn = ccw_ptn.cw_fwd_ccw()
            self.boundry[cw_ptn] = "*-"
            self.boundry[ccw_ptn] = "-*"
            self.cube_map[ccw_ptn] = -cw_ptn
            self.cube_map[cw_ptn] = -ccw_ptn
            while f"{self.boundry[cw_ptn]}{self.boundry[ccw_ptn]}".count("o") < 2:
                # move
                match self.boundry[cw_ptn]:
                    case "*-" | "--" | "o-":
                        cw_ptn = cw_ptn.cw_fwd()
                    case "-o":
                        cw_ptn = cw_ptn.cw()
                    case "-x" | "x-" | _:
                        raise Exception(f"boundry[{cw_ptn}]={self.boundry[cw_ptn]}")
                match self.boundry[ccw_ptn]:
                    case "-*" | "--" | "-o":
                        ccw_ptn = ccw_ptn.ccw_fwd()
                    case "o-":
                        ccw_ptn = ccw_ptn.ccw()
                    case "x-" | "-x" | _:
                        raise Exception(f"boundry[{ccw_ptn}]={self.boundry[ccw_ptn]}")
                self.cube_map[ccw_ptn] = -cw_ptn
                self.cube_map[cw_ptn] = -ccw_ptn

        if cube:
            self.boundry_map = self.cube_map
        else:
            self.boundry_map = self.flat_map

    def process_map(self, map):
        self.board = {}
        for y, row in enumerate(map.split("\n")):
            for x, c in enumerate(row):
                if c not in {".", "#"}:
                    continue
                self.board[Pt(x=x, y=y)] = c
        self.boundry = {}
        for pt in self.board:
            for normal in DIRECTIONS:
                if pt + normal not in self.board:
                    ptn = V(pt=pt, v=normal)
                    self.boundry[ptn] = None
        for ptn in self.boundry:
            if ptn.cw() in self.boundry:
                self.boundry[ptn] = "-o"
            elif ptn.ccw() in self.boundry:
                self.boundry[ptn] = "o-"
            elif ptn.cw_fwd_ccw() in self.boundry:
                self.boundry[ptn] = "-x"
            elif ptn.ccw_fwd_cw() in self.boundry:
                self.boundry[ptn] = "x-"
            else:
                self.boundry[ptn] = "--"

    def wrap_flat_point(self, ptn: V) -> V:
        current_pt = ptn
        while (next_pt := current_pt.bkwd()).pt in self.board:
            current_pt = next_pt
        # print(f"ptn={ptn} jumps to current_pt={current_pt}")
        return current_pt

    def run_map(self):
        for movement in self.directions:
            self.move(movement)
            if self.trace:
                print(f"movement={movement} > loc={self.location}")
        return self.location

    def move(self, movement):
        match movement:
            case "R":
                self.location = self.location.cw()
            case "L":
                self.location = self.location.ccw()
            case _:
                ptn = self.location
                for _ in range(int(movement)):
                    ptn = self.move_foward(ptn)
                self.location = ptn

    def move_foward(self, ptn: V) -> V:
        # find next step
        next_ptn = ptn.fwd()
        if next_ptn.pt not in self.board:
            next_ptn = self.boundry_map[ptn]
            if self.trace:
                print(f"wrap={ptn} > {next_ptn}")
        # check if next step is clear
        if self.board[next_ptn.pt] == ".":
            return next_ptn
        return ptn

    def password(self):
        return (
            1000 * (self.location.pt.y + 1)
            + 4 * (self.location.pt.x + 1)
            + DIRECTIONS.index(self.location.v)
        )


def test_sample_map():
    sample = MonkeyMap(SAMPLE_MAP, SAMPLE_DIRECTIONS)
    assert sample.location == V(Pt(8, 0), Pt(1, 0))
    assert sample.run_map() == V(Pt(7, 5), Pt(1, 0))
    assert sample.password() == 6032
    # from self.boundry looking at -x and x- elements
    a = V(pt=Pt(x=7, y=4), v=Pt(x=0, y=-1))
    b = V(pt=Pt(x=8, y=3), v=Pt(x=-1, y=0))
    assert sample.boundry[a] == "-*"
    assert sample.boundry[b] == "*-"
    assert a.cw_fwd_ccw() == b
    assert set(sample.boundry.keys()) == set(sample.flat_map.keys())
    assert set(sample.flat_map.keys()) == set(sample.cube_map.keys())
    sample = MonkeyMap(SAMPLE_MAP, SAMPLE_DIRECTIONS, cube=True, trace=True)
    assert sample.run_map() == V(pt=Pt(x=6, y=4), v=Pt(x=0, y=-1))
    assert sample.password() == 5031


def test_my_map():
    my_map = MonkeyMap(MY_MAP, MY_DIRECTIONS)
    my_map.run_map()
    assert my_map.password() == 106094
    my_map = MonkeyMap(MY_MAP, MY_DIRECTIONS, cube=True)
    my_map.run_map()
    assert my_map.password() == 162038
