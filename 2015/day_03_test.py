def move(d, x, y):
    if d == '>':
        x += 1
    elif d == '<':
        x -= 1
    elif d == '^':
        y += 1
    elif d == 'v':
        y -= 1
    return (x, y)


def ans(directions):
    """
    --- Day 3: Perfectly Spherical Houses in a Vacuum ---
    Santa is delivering presents to an infinite two-dimensional grid of houses.

    He begins by delivering a present to the house at his starting location,
    and then an elf at the North Pole calls him via radio and tells him where to move next.
    Moves are always exactly one house to the north (^), south (v), east (>), or west (<).
    After each move, he delivers another present to the house at his new location.

    However, the elf back at the north pole has had a little too much eggnog, and so his
    directions are a little off, and Santa ends up visiting some houses more than once.
    How many houses receive at least one present?

    For example:

    > delivers presents to 2 houses: one at the starting location, and one to the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.
    """

    presents = dict()
    (x, y) = (0, 0)
    presents[(x, y)] = 1
    for d in directions:
        (x, y) = move(d, x, y)
        presents[(x, y)] = 1
    return len(presents)


def robot_ans(directions):
    """
    --- Part Two ---
    The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.

    Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns
    moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

    This year, how many houses receive at least one present?

    For example:

    ^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
    ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
    ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.
    """
    presents = dict()
    (x, y) = (0, 0)
    presents[(x, y)] = 1
    (rx, ry) = (0, 0)
    presents[(rx, ry)] = 1
    for who, direction in enumerate(directions):
        if who % 2 == 0:
            (x, y) = move(direction, x, y)
            presents[(x, y)] = 1
        else:
            (rx, ry) = move(direction, rx, ry)
            presents[(rx, ry)] = 1
    return len(presents)


def test_houses_visited():
    assert ans('>') == 2
    assert ans('^>v<') == 4
    assert ans('^v^v^v^v^v') == 2

def test_robot_houses_visited():
    assert robot_ans('^>') == 3
    assert robot_ans('^>v<') == 3
    assert robot_ans('^v^v^v^v^v') == 11

def test_submission():
    fp = open('./input_day_3.txt', 'r')
    if fp.mode == 'r':
        submission_input = fp.read()
    assert robot_ans(submission_input) == 2639
