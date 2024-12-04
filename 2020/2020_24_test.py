from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 24: Lobby Layout ---
    Your raft makes it to the tropical island; it turns out that the small crab was an excellent navigator.
    You make your way to the resort.

    As you enter the lobby, you discover a small problem: the floor is being renovated. You can't even reach the
    check-in desk until they've finished installing the new tile floor.

    The tiles are all hexagonal; they need to be arranged in a hex grid with a very specific color pattern. Not
    in the mood to wait, you offer to help figure out the pattern.

    The tiles are all white on one side and black on the other. They start with the white side facing up. The
    lobby is large enough to fit whatever pattern might need to appear there.

    A member of the renovation crew gives you a list of the tiles that need to be flipped over (your puzzle input).
    Each line in the list identifies a single tile that needs to be flipped by giving a series of steps starting
    from a reference tile in the very center of the room. (Every line starts from the same reference tile.)

    Because the tiles are hexagonal, every tile has six neighbors: east, southeast, southwest, west, northwest,
    and northeast. These directions are given in your list, respectively, as e, se, sw, w, nw, and ne. A tile
    is identified by a series of these directions with no delimiters; for example, esenee identifies the tile
    you land on if you start at the reference tile and then move one tile east, one tile southeast, one tile
    northeast, and one tile east.

    Each time a tile is identified, it flips from white to black or from black to white. Tiles might be flipped
    more than once. For example, a line like esew flips a tile immediately adjacent to the reference tile, and a
    line like nwwswee flips the reference tile itself.

    Here is a larger example:

    sesenwnenenewseeswwswswwnenewsewsw
    neeenesenwnwwswnenewnwwsewnenwseswesw
    seswneswswsenwwnwse
    nwnwneseeswswnenewneswwnewseswneseene
    swweswneswnenwsewnwneneseenw
    eesenwseswswnenwswnwnwsewwnwsene
    sewnenenenesenwsewnenwwwse
    wenwwweseeeweswwwnwwe
    wsweesenenewnwwnwsenewsenwwsesesenwne
    neeswseenwwswnwswswnw
    nenwswwsewswnenenewsenwsenwnesesenew
    enewnwewneswsewnwswenweswnenwsenwsw
    sweneswneswneneenwnewenewwneswswnese
    swwesenesewenwneswnwwneseswwne
    enesenwswwswneneswsenwnewswseenwsese
    wnwnesenesenenwwnenwsewesewsesesew
    nenewswnwewswnenesenwnesewesw
    eneswnwswnwsenenwnwnwwseeswneewsenese
    neswnwewnwnwseenwseesewsenwsweewe
    wseweeenwnesenwwwswnew

    In the above example, 10 tiles are flipped once (to black), and 5 more are flipped twice (to black, then back
    to white). After all of these instructions have been followed, a total of 10 tiles are black.

    Go through the renovation crew's list and determine which tiles they need to flip. After all of the instructions
    have been followed, how many tiles are left with the black side up?

    --- Part Two ---
    The tile floor in the lobby is meant to be a living art exhibit. Every day, the tiles are all flipped according
    to the following rules:

    Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    Here, tiles immediately adjacent means the six tiles directly touching the tile in question.

    The rules are applied simultaneously to every tile; put another way, it is first determined which tiles need to
    be flipped, then they are all flipped at the same time.

    In the above example, the number of black tiles that are facing up after the given number of days has passed is
    as follows:

    Day 1: 15
    Day 2: 12
    Day 3: 25
    Day 4: 14
    Day 5: 23
    Day 6: 28
    Day 7: 41
    Day 8: 37
    Day 9: 49
    Day 10: 37

    Day 20: 132
    Day 30: 259
    Day 40: 406
    Day 50: 566
    Day 60: 788
    Day 70: 1106
    Day 80: 1373
    Day 90: 1844
    Day 100: 2208

    After executing this process a total of 100 times, there would be 2208 black tiles facing up.

    How many tiles will be black after 100 days?
    """

    pass


SAMPLE = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".split(
    "\n"
)


with open(Path(__file__).parent / "2020_24_input.txt") as fp:
    INPUT = [line.strip() for line in fp]


def move_to(move_sequence, loc=(0, 0)):
    while len(move_sequence) > 0:
        d = move_sequence[0]
        move_sequence = move_sequence[1:]
        if d == "w":
            loc = (loc[0] + 2, loc[1])
        elif d == "e":
            loc = (loc[0] - 2, loc[1])
        else:
            if d == "n":
                loc = (loc[0], loc[1] + 1)
            elif d == "s":
                loc = (loc[0], loc[1] - 1)
            d = move_sequence[0]
            move_sequence = move_sequence[1:]
            if d == "w":
                loc = (loc[0] + 1, loc[1])
            elif d == "e":
                loc = (loc[0] - 1, loc[1])
    return loc


def neighborhood(loc):
    return set(
        [
            (loc[0] + 2, loc[1]),
            (loc[0] - 2, loc[1]),
            (loc[0] + 1, loc[1] + 1),
            (loc[0] + 1, loc[1] - 1),
            (loc[0] - 1, loc[1] + 1),
            (loc[0] - 1, loc[1] - 1),
        ]
    )


class Board:
    def __init__(self, moves):
        self.grid = defaultdict(int)
        for move in moves:
            loc = move_to(move)
            if self.grid[loc] == 0:
                self.grid[loc] = 1
            elif self.grid[loc] == 1:
                self.grid[loc] = 0

    def number_nbrs(self, loc):
        return sum(self.grid[p] for p in neighborhood(loc))

    def evolve(self):
        next_state = defaultdict(int)
        set_to_check = set(self.grid.keys())
        for loc in self.grid.keys():
            set_to_check = set_to_check.union(neighborhood(loc))
        for loc in set_to_check:
            nb_total = self.number_nbrs(loc)
            if nb_total == 2:
                next_state[loc] = 1
            elif nb_total == 1 and self.grid[loc] == 1:
                next_state[loc] = 1
        self.grid = next_state


def test_sample_board():
    sample_board = Board(SAMPLE)
    assert sum(sample_board.grid.values()) == 10
    sample_board.evolve()
    assert sum(sample_board.grid.values()) == 15
    sample_board.evolve()
    assert sum(sample_board.grid.values()) == 12
    sample_board.evolve()
    assert sum(sample_board.grid.values()) == 25


def test_puzzle_board():
    puzzle_board = Board(INPUT)
    assert sum(puzzle_board.grid.values()) == 523
    for _ in range(100):
        puzzle_board.evolve()
    assert sum(puzzle_board.grid.values()) == 4225
