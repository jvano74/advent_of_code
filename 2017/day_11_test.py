from collections import defaultdict


class Puzzle:
    """
    --- Day 11: Hex Ed ---
    Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you,
    clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

    Fortunately for her, you have plenty of experience with infinite grids.

    Unfortunately for you, it's a hex grid.

    The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north,
    northeast, southeast, south, southwest, and northwest:

      \ n  /
    nw +--+ ne
      /    \
    -+      +-
      \    /
    sw +--+ se
      / s  \

    You have the path the child process took. Starting where he started, you need to determine the fewest
    number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

    For example:

    ne,ne,ne is 3 steps away.
    ne,ne,sw,sw is 0 steps away (back where you started).
    ne,ne,s,s is 2 steps away (se,se).
    se,sw,se,sw,sw is 3 steps away (s,s,sw).

    --- Part Two ---
    How many steps away is the furthest he ever got from his starting position?
    """
    pass


with open('day_11_input.txt') as f:
    INPUTS = f.read().split(',')


def hex_dist(totals):
    """
    from http://www-cs-students.stanford.edu/~amitp/Articles/HexLOS.html
                       __   5
                   __/D \__   4
                __/  \__/  \__   3      "Y" coord
             __/  \__/  \__/  \__   2
          __/A \__/  \__/  \__/  \__   1
       __/  \__/  \__/E \__/B \__/  \__   0
      /  \__/G \__/  \__/  \__/F \__/C \
      \__/  \__/  \__/  \__/  \__/  \__/
         \__/  \__/  \__/  \__/  \__/   5
            \__/  \__/  \__/  \__/   4
               \__/  \__/  \__/    3
                  \__/  \__/    2     "X" coord
                     \__/    1
                         0
    if sign(dx) == sign(dy)
        dist = max(abs(dx),abs(dy))
    else dist = abs(dx) + abs(dy)

    with nw, ne, and n
    dx = nw + n, dy = ne + n

    """
    ne = (totals['ne'] - totals['sw'])
    nw = (totals['nw'] - totals['se'])
    n = totals['n'] - totals['s']
    x = nw + n
    y = ne + n
    if x > 0 and y > 0:
        return max(x, y)
    if x < 0 and y < 0:
        return max(-x, -y)
    return abs(x) + abs(y)


def dist_from_end_of_path(steps):
    totals = defaultdict(int)
    max_dist = 0
    for s in steps:
        totals[s] += 1
        d = hex_dist(totals)
        max_dist = max(max_dist, d)
    return d, max_dist


def test_dist_from_end_of_path():
    assert dist_from_end_of_path(['ne', 'ne', 'ne']) == (3, 3)
    assert dist_from_end_of_path(['ne', 'ne', 'sw', 'sw']) == (0, 2)
    assert dist_from_end_of_path(['ne', 'ne', 's', 's']) == (2, 2)
    assert dist_from_end_of_path(['se', 'sw', 'se', 'sw', 'sw']) == (3, 3)
    assert dist_from_end_of_path(INPUTS) == (877, 1622)