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

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

DIRECTION_VALUE = {
    Pt(1, 0): 0,
    Pt(0, 1): 1,
    Pt(-1, 0): 2,
    Pt(0, -1): 3,
}

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


class MonkeyMap:
    def __init__(self, map, directions) -> None:
        self.directions = directions.replace("L", ",L,").replace("R", ",R,").split(",")
        self.board = {}
        self.foward = Pt(1, 0)
        self.location = None
        for y, row in enumerate(map.split("\n")):
            for x, c in enumerate(row):
                if c not in {".", "#"}:
                    continue
                self.board[Pt(x=x, y=y)] = c
                if self.location is None and c == ".":
                    self.location = Pt(x=x, y=y)

    def run_map(self):
        for movement in self.directions:
            self.move(movement)
        return self.location

    def move(self, movement):
        match movement:
            case "L" | "R":
                self.foward = ROTATION[(self.foward, movement)]
            case _:
                dir = self.foward
                pt = self.location
                for _ in range(int(movement)):
                    pt, dir = self.move_foward(pt, dir)
                self.foward = dir
                self.location = pt

    def move_foward(self, pt, dir):
        next_pt, next_dir = pt + dir, dir
        if next_pt not in self.board:
            next_pt, next_dir = self.wrap_point(pt, dir)
        if self.board[next_pt] == ".":
            return next_pt, next_dir
        return pt, dir

    def wrap_point(self, pt, dir):
        next_pt = pt
        while next_pt - dir in self.board:
            next_pt -= dir
        # print(f"pt={pt}, dir={dir} jumps to next_pt={next_pt}")
        return next_pt, dir

    def password(self):
        return 1000 * (self.location.y + 1) + 4 * (self.location.x + 1) + DIRECTION_VALUE[self.foward] 

def test_sample_map():
    sample = MonkeyMap(SAMPLE_MAP, SAMPLE_DIRECTIONS)
    assert sample.location == Pt(8, 0)
    assert sample.foward == Pt(1, 0)
    assert sample.run_map() == Pt(7, 5)
    assert sample.password() == 6032

def test_sample_map():
    my_map = MonkeyMap(MY_MAP, MY_DIRECTIONS)
    my_map.run_map()
    assert my_map.password() == 106094