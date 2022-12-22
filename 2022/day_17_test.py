from typing import List, NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 17: Pyroclastic Flow ---

    Your handheld device has located an alternative exit from the cave for you
    and the elephants. The ground is rumbling almost continuously now, but the
    strange valves bought you some time. It's definitely getting warmer in here,
    though.

    The tunnels eventually open into a very tall, narrow chamber. Large,
    oddly-shaped rocks are falling into the chamber from above, presumably due
    to all the rumbling. If you can't work out where the rocks will fall next,
    you might be crushed!

    The five types of rocks have the following peculiar shapes, where # is rock
    and . is empty space:

    ####

    .#.
    ###
    .#.

    ..#
    ..#
    ###

    #
    #
    #
    #

    ##
    ##

    The rocks fall in the order shown above: first the - shape, then the +
    shape, and so on. Once the end of the list is reached, the same order
    repeats: the - shape falls first, sixth, 11th, 16th, etc.

    The rocks don't spin, but they do get pushed around by jets of hot gas
    coming out of the walls themselves. A quick scan reveals the effect the jets
    of hot gas will have on the rocks as they fall (your puzzle input).

    For example, suppose this was the jet pattern in your cave:

    >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>

    In jet patterns, < means a push to the left, while > means a push to the
    right. The pattern above means that the jets will push a falling rock right,
    then right, then right, then left, then left, then right, and so on. If the
    end of the list is reached, it repeats.

    The tall, vertical chamber is exactly seven units wide. Each rock appears so
    that its left edge is two units away from the left wall and its bottom edge
    is three units above the highest rock in the room (or the floor, if there
    isn't one).

    After a rock appears, it alternates between being pushed by a jet of hot gas
    one unit (in the direction indicated by the next symbol in the jet pattern)
    and then falling one unit down. If any movement would cause any part of the
    rock to move into the walls, floor, or a stopped rock, the movement instead
    does not occur. If a downward movement would have caused a falling rock to
    move into the floor or an already-fallen rock, the falling rock stops where
    it is (having landed on something) and a new rock immediately begins
    falling.

    Drawing falling rocks with @ and stopped rocks with #, the jet pattern in
    the example above manifests as follows:

    The first rock begins falling:
    |..@@@@.|
    |.......|
    |.......|
    |.......|
    +-------+

    Jet of gas pushes rock right:
    |...@@@@|
    |.......|
    |.......|
    |.......|
    +-------+

    Rock falls 1 unit:
    |...@@@@|
    |.......|
    |.......|
    +-------+

    Jet of gas pushes rock right, but nothing happens:
    |...@@@@|
    |.......|
    |.......|
    +-------+

    Rock falls 1 unit:
    |...@@@@|
    |.......|
    +-------+

    Jet of gas pushes rock right, but nothing happens:
    |...@@@@|
    |.......|
    +-------+

    Rock falls 1 unit:
    |...@@@@|
    +-------+

    Jet of gas pushes rock left:
    |..@@@@.|
    +-------+

    Rock falls 1 unit, causing it to come to rest:
    |..####.|
    +-------+

    A new rock begins falling:
    |...@...|
    |..@@@..|
    |...@...|
    |.......|
    |.......|
    |.......|
    |..####.|
    +-------+

    Jet of gas pushes rock left:
    |..@....|
    |.@@@...|
    |..@....|
    |.......|
    |.......|
    |.......|
    |..####.|
    +-------+

    Rock falls 1 unit:
    |..@....|
    |.@@@...|
    |..@....|
    |.......|
    |.......|
    |..####.|
    +-------+

    Jet of gas pushes rock right:
    |...@...|
    |..@@@..|
    |...@...|
    |.......|
    |.......|
    |..####.|
    +-------+

    Rock falls 1 unit:
    |...@...|
    |..@@@..|
    |...@...|
    |.......|
    |..####.|
    +-------+

    Jet of gas pushes rock left:
    |..@....|
    |.@@@...|
    |..@....|
    |.......|
    |..####.|
    +-------+

    Rock falls 1 unit:
    |..@....|
    |.@@@...|
    |..@....|
    |..####.|
    +-------+

    Jet of gas pushes rock right:
    |...@...|
    |..@@@..|
    |...@...|
    |..####.|
    +-------+

    Rock falls 1 unit, causing it to come to rest:
    |...#...|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    A new rock begins falling:
    |....@..|
    |....@..|
    |..@@@..|
    |.......|
    |.......|
    |.......|
    |...#...|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    The moment each of the next few rocks begins falling, you would see this:

    |..@....|
    |..@....|
    |..@....|
    |..@....|
    |.......|
    |.......|
    |.......|
    |..#....|
    |..#....|
    |####...|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    |..@@...|
    |..@@...|
    |.......|
    |.......|
    |.......|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    |..@@@@.|
    |.......|
    |.......|
    |.......|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    |...@...|
    |..@@@..|
    |...@...|
    |.......|
    |.......|
    |.......|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    |....@..|
    |....@..|
    |..@@@..|
    |.......|
    |.......|
    |.......|
    |..#....|
    |.###...|
    |..#....|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    |..@....|
    |..@....|
    |..@....|
    |..@....|
    |.......|
    |.......|
    |.......|
    |.....#.|
    |.....#.|
    |..####.|
    |.###...|
    |..#....|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    |..@@...|
    |..@@...|
    |.......|
    |.......|
    |.......|
    |....#..|
    |....#..|
    |....##.|
    |....##.|
    |..####.|
    |.###...|
    |..#....|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    |..@@@@.|
    |.......|
    |.......|
    |.......|
    |....#..|
    |....#..|
    |....##.|
    |##..##.|
    |######.|
    |.###...|
    |..#....|
    |.####..|
    |....##.|
    |....##.|
    |....#..|
    |..#.#..|
    |..#.#..|
    |#####..|
    |..###..|
    |...#...|
    |..####.|
    +-------+

    To prove to the elephants your simulation is accurate, they want to know how
    tall the tower will get after 2022 rocks have stopped (but before the 2023rd
    rock begins falling). In this example, the tower of rocks will be 3068 units
    tall.

    How many units tall will the tower of rocks be after 2022 rocks have stopped
    falling?

    Your puzzle answer was 3177.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The elephants are not impressed by your simulation. They demand to know how
    tall the tower will be after 1000000000000 rocks have stopped! Only then
    will they feel confident enough to proceed through the cave.

    In the example above, the tower would be 1514285714288 units tall!

    How tall will the tower be after 1000000000000 rocks have stopped?

    """


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def left(self):
        return Pt(self.x - 1, self.y)

    def right(self):
        return Pt(self.x + 1, self.y)

    def down(self):
        return Pt(self.x, self.y - 1)


def p1(pt: Pt):
    """
    ####
    """
    return {Pt(pt.x, pt.y), Pt(pt.x + 1, pt.y), Pt(pt.x + 2, pt.y), Pt(pt.x + 3, pt.y)}


def p2(pt: Pt):
    """
    .#.
    ###
    .#.
    """
    return {
        Pt(pt.x, pt.y + 1),
        Pt(pt.x + 1, pt.y),
        Pt(pt.x + 1, pt.y + 1),
        Pt(pt.x + 1, pt.y + 2),
        Pt(pt.x + 2, pt.y + 1),
    }


def p3(pt: Pt):
    """
    ..#
    ..#
    ###
    """
    return {
        Pt(pt.x, pt.y),
        Pt(pt.x + 1, pt.y),
        Pt(pt.x + 2, pt.y),
        Pt(pt.x + 2, pt.y + 1),
        Pt(pt.x + 2, pt.y + 2),
    }


def p4(pt: Pt):
    """
    #
    #
    #
    #
    """
    return {
        Pt(pt.x, pt.y),
        Pt(pt.x, pt.y + 1),
        Pt(pt.x, pt.y + 2),
        Pt(pt.x, pt.y + 3),
    }


def p5(pt: Pt):
    """
    ##
    ##
    """
    return {
        Pt(pt.x, pt.y),
        Pt(pt.x + 1, pt.y),
        Pt(pt.x, pt.y + 1),
        Pt(pt.x + 1, pt.y + 1),
    }


class Board:
    def __init__(self, winds: List) -> None:
        self.board = {
            Pt(1, 0),
            Pt(2, 0),
            Pt(3, 0),
            Pt(4, 0),
            Pt(5, 0),
            Pt(6, 0),
            Pt(7, 0),
        }  # this is the floor
        self.winds = winds
        self.wind_index = 0
        self.wind_max = len(winds)
        self.piece_functions = [p1, p2, p3, p4, p5]
        self.piece_index = 0
        self.long_hx = defaultdict(list)
        self.fits = defaultdict(list)

    def add_next(self):
        starting_max_y = max(p.y for p in self.board)
        piece_index = self.piece_index % 5
        starting_wind_index = self.wind_index % self.wind_max
        piece = self.piece_functions[piece_index]
        self.piece_index += 1
        pt = Pt(x=3, y=starting_max_y + 4)
        falling = True
        while falling:
            # wind step
            wind_direction = self.winds[self.wind_index % self.wind_max]
            self.wind_index += 1
            if wind_direction == "<":
                pos = piece(pt.left())
                if min(p.x for p in pos) > 0 and all(p not in self.board for p in pos):
                    pt = pt.left()
            else:
                pos = piece(pt.right())
                if max(p.x for p in pos) < 8 and all(p not in self.board for p in pos):
                    pt = pt.right()
            # fall step
            pos = piece(pt.down())
            if all(p not in self.board for p in pos):
                pt = pt.down()
            else:
                falling = False
                pos = piece(pt)
                self.board = self.board.union(pos)
        ending_max_y = max(p.y for p in self.board)
        ending_wind_index = self.wind_index % self.wind_max
        self.long_hx[
            (
                piece_index,
                f"{starting_wind_index}-{ending_wind_index}",
                Pt(pt.x, pt.y - starting_max_y),
            )
        ].append((self.piece_index - 1, ending_max_y))

    def fit_history(self, final_piece):
        # not the best way do fit a linear regression but it worked
        fits = defaultdict(list)
        estimates = set()
        for start_key, snapshots in self.long_hx.items():
            if len(snapshots) < 2:
                continue
            old_piece, old_height = snapshots[0]
            piece, height = snapshots[1]
            delta_piece, delta_height = piece - old_piece, height - old_height
            old_piece, old_height = piece, height
            for piece, height in snapshots[2:]:
                if (
                    delta_piece != piece - old_piece
                    or delta_height != height - old_height
                ):
                    delta_piece = None
                    delta_height = None
                    # print(f"throwing out start_key={start_key}")
                    break
                old_piece, old_height = piece, height
            if delta_piece is None:
                continue
            piece, height = snapshots[0]
            fits[
                (piece % delta_piece, delta_piece, height % delta_height, delta_height)
            ].append(start_key)
            # print(f"final_piece={final_piece} -> piece={piece}, mod={delta_piece}")
            # print(f"mod={final_piece % delta_piece} -> mod={piece % delta_piece}")
            if final_piece % delta_piece == piece % delta_piece:
                n = final_piece // delta_piece
                estimates.add(height % delta_height + n * delta_height)
        self.fits = fits
        return estimates

    def get_board(self):
        image = []
        for y in range(max(p.y for p in self.board) + 4):
            line = []
            for x in range(9):
                if y == 0:
                    line.append("+" if x == 0 or x == 8 else "-")
                elif x == 0 or x == 8:
                    line.append("|")
                elif Pt(x, y) in self.board:
                    line.append("#")
                else:
                    line.append(".")
            image.append("".join(line))
        image.reverse()
        return image


SAMPLE = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


with open("day_17_input.txt") as fp:
    MY_INPUT = fp.read()


def test_sample_board():
    sample = Board(SAMPLE)
    sample.add_next()
    # print("\n".join(sample.get_board()))
    assert max(p.y for p in sample.board) == 1
    sample.add_next()
    # print("\n".join(sample.get_board()))
    assert max(p.y for p in sample.board) == 4
    sample.add_next()
    # print("\n".join(sample.get_board()))
    assert max(p.y for p in sample.board) == 6
    # reset
    sample = Board(SAMPLE)
    for _ in range(2022):
        sample.add_next()
    assert max(p.y for p in sample.board) == 3068
    assert sample.fit_history(1000000000000) == {1514285714288 + 1}


def test_my_board():
    my_board = Board(MY_INPUT)
    for _ in range(2022):
        my_board.add_next()
    assert max(p.y for p in my_board.board) == 3177
    for _ in range(5_000):
        my_board.add_next()
    assert my_board.fit_history(1000000000000) == {1565517241382 + 1}
