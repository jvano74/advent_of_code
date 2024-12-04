from pathlib import Path
from typing import NamedTuple


class Pt(NamedTuple):
    x: int
    y: int


class Puzzle:
    """
    --- Day 11: Seating System ---
    Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly
    to the tropical island where you can finally start your vacation. As you reach the waiting area to board
    the ferry, you realize you're so early, nobody else has even arrived yet!

    By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty
    sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

    The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an
    occupied seat (#). For example, the initial seat layout might look like this:

    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL

    Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely
    predictable and always follow a simple set of rules. All decisions are based on the number of occupied
    seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal
    from the seat). The following rules are applied to every seat simultaneously:

    - If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.

    - If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.

    - Otherwise, the seat's state does not change.

    Floor (.) never changes; seats don't move, and nobody sits on the floor.

    After one round of these rules, every seat in the example layout becomes occupied:

    #.##.##.##
    #######.##
    #.#.#..#..
    ####.##.##
    #.##.##.##
    #.#####.##
    ..#.#.....
    ##########
    #.######.#
    #.#####.##

    After a second round, the seats with four or more occupied adjacent seats become empty again:

    #.LL.L#.##
    #LLLLLL.L#
    L.L.L..L..
    #LLL.LL.L#
    #.LL.LL.LL
    #.LLLL#.##
    ..L.L.....
    #LLLLLLLL#
    #.LLLLLL.L
    #.#LLLL.##

    This process continues for three more rounds:

    #.##.L#.##
    #L###LL.L#
    L.#.#..#..
    #L##.##.L#
    #.##.LL.LL
    #.###L#.##
    ..#.#.....
    #L######L#
    #.LL###L.L

    #.#L###.##
    #.#L.L#.##
    #LLL#LL.L#
    L.L.L..#..
    #LLL.##.L#
    #.LL.LL.LL
    #.LL#L#.##
    ..L.L.....
    #L#LLLL#L#
    #.LLLLLL.L

    #.#L#L#.##
    #.#L.L#.##
    #LLL#LL.L#
    L.#.L..#..
    #L##.##.L#
    #.#L.LL.LL
    #.#L#L#.##
    ..L.L.....
    #L#L##L#L#
    #.LLLLLL.L
    #.#L#L#.##

    At this point, something interesting happens: the chaos stabilizes and further applications of these rules
    cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

    Simulate your seating area by applying the seating rules repeatedly until no seats change state.
    How many seats end up occupied?

    --- Part Two ---
    As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they
    care about the first seat they can see in each of those eight directions!

    Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those
    eight directions. For example, the empty seat below would see eight occupied seats:

    .......#.
    ...#.....
    .#.......
    .........
    ..#L....#
    ....#....
    .........
    #........
    ...#.....

    The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

    .............
    .L.L.#.#.#.#.
    .............

    The empty seat below would see no occupied seats:

    .##.##.
    #.#.#.#
    ##...##
    ...L...
    ##...##
    #.#.#.#
    .##.##.

    Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats
    for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still
    apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and
    floor never changes.

    Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L

    L.LLLLL.LL
    #.##.##.##
    #######.##
    #.#.#..#..
    ####.##.##
    #.##.##.##
    #.#####.##
    ..#.#.....
    ##########
    #.######.#

    #.#####.##
    #.LL.LL.L#
    #LLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLL#
    #.LLLLLL.L

    #.LLLLL.L#
    #.L#.##.L#
    #L#####.LL
    L.#.#..#..
    ##L#.##.##
    #.##.#L.##
    #.#####.#L
    ..#.#.....
    LLL####LL#
    #.L#####.L

    #.L####.L#
    #.L#.L#.L#
    #LLLLLL.LL
    L.L.L..#..
    ##LL.LL.L#
    L.LL.LL.L#
    #.LLLLL.LL
    ..L.L.....
    LLLLLLLLL#
    #.LLLLL#.L

    #.L#LL#.L#
    #.L#.L#.L#
    #LLLLLL.LL
    L.L.L..#..
    ##L#.#L.L#
    L.L#.#L.L#
    #.L####.LL
    ..#.#.....
    LLL###LLL#
    #.LLLLL#.L
    #.L#LL#.L#

    #.L#.L#.L#
    #LLLLLL.LL
    L.L.L..#..
    ##L#.#L.L#
    L.L#.LL.L#
    #.LLLL#.LL
    ..#.L.....
    LLL###LLL#
    #.LLLLL#.L
    #.L#LL#.L#

    Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs,
    you count 26 occupied seats.

    Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is
    reached, how many seats end up occupied?
    """

    pass


SAMPLE = [
    "L.LL.LL.LL",
    "LLLLLLL.LL",
    "L.L.L..L..",
    "LLLL.LL.LL",
    "L.LL.LL.LL",
    "L.LLLLL.LL",
    "..L.L.....",
    "LLLLLLLLLL",
    "L.LLLLLL.L",
    "L.LLLLL.LL",
]

with open(Path(__file__).parent / "2020_11_input.txt") as fp:
    INPUT = [ln.strip() for ln in fp]


class Board:
    DELTAS = [
        Pt(0, 1),
        Pt(1, 1),
        Pt(1, 0),
        Pt(1, -1),
        Pt(0, -1),
        Pt(-1, -1),
        Pt(-1, 0),
        Pt(-1, 1),
    ]

    def __init__(self, layout, v=0):
        self.grid = {}
        self.generations = 0
        self.max_y = len(layout)
        self.max_x = len(layout[0])
        self.v = v

        for y, row in enumerate(layout):
            for x, pos in enumerate(row):
                self.grid[Pt(x, y)] = pos

    def next_state(self, x, y):
        if self.grid[Pt(x, y)] == ".":
            return "."
        occupied_neighbors = 0
        for d in self.DELTAS:
            pt_to_check = Pt(x + d.x, y + d.y)
            if pt_to_check in self.grid and self.grid[pt_to_check] == "#":
                occupied_neighbors += 1
        if self.grid[Pt(x, y)] == "L" and occupied_neighbors == 0:
            return "#"
        elif self.grid[Pt(x, y)] == "#" and occupied_neighbors >= 4:
            return "L"
        return self.grid[Pt(x, y)]

    def find_neighbor_in_direction(self, x, y, d):
        for dist in range(1, max(self.max_x, self.max_y)):
            pt = Pt(x + dist * d.x, y + dist * d.y)
            if pt not in self.grid:
                return "."
            if self.grid[pt] == "#":
                return "#"
            if self.grid[pt] == "L":
                return "L"

    def next_state_v2(self, x, y):
        if self.grid[Pt(x, y)] == ".":
            return "."
        occupied_neighbors = 0
        for d in self.DELTAS:
            pt_to_check = self.find_neighbor_in_direction(x, y, d)
            if pt_to_check == "#":
                occupied_neighbors += 1
        if self.grid[Pt(x, y)] == "L" and occupied_neighbors == 0:
            return "#"
        elif self.grid[Pt(x, y)] == "#" and occupied_neighbors >= 5:
            return "L"
        return self.grid[Pt(x, y)]

    def tick(self):
        self.generations += 1
        if self.v == 0:
            new_grid = {k: self.next_state(k.x, k.y) for k in self.grid}
        else:
            new_grid = {k: self.next_state_v2(k.x, k.y) for k in self.grid}
            # self.print_grid(new_grid)
        if new_grid != self.grid:
            self.grid = new_grid
            return 1
        return 0

    def run(self):
        while self.tick() == 1:
            pass

    def print_grid(self, next_grid=None):
        if next_grid is None:
            next_grid = {}
        print("\n\n")
        for y in range(self.max_y):
            row = []
            for x in range(self.max_x):
                row.append(self.grid[Pt(x, y)])
                if len(next_grid) > 0:
                    row.append(next_grid[Pt(x, y)])
                    row.append("+")
            print("".join(row))


def test_sample():
    sample = Board(SAMPLE)
    sample.run()
    assert sum([v == "#" for k, v in sample.grid.items()]) == 37
    sample2 = Board(SAMPLE, 1)
    sample2.run()
    assert sum([v == "#" for k, v in sample2.grid.items()]) == 26


def test_input():
    sample = Board(INPUT)
    sample.run()
    assert sum([v == "#" for k, v in sample.grid.items()]) == 2243
    sample2 = Board(INPUT, 1)
    sample2.run()
    assert sum([v == "#" for k, v in sample2.grid.items()]) == 2027
