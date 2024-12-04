from pathlib import Path


class Puzzle:
    """
    --- Day 8: Treetop Tree House ---
    The expedition comes across a peculiar patch of tall trees all planted carefully
    in a grid.  The Elves explain that a previous expedition planted these trees as
    a reforestation effort. Now, they're curious if this would be a good location
    for a tree house.

    First, determine whether there is enough tree cover here to keep a tree house
    hidden. To do this, you need to count the number of trees that are visible from
    outside the grid when looking directly along a row or column.

    The Elves have already launched a quadcopter to generate a map with the height of
    each tree (your puzzle input). For example:

    30373
    25512
    65332
    33549
    35390

    Each tree is represented as a single digit whose value is its height, where 0
    is the shortest and 9 is the tallest.

    A tree is visible if all of the other trees between it and an edge of the grid
    are shorter than it. Only consider trees in the same row or column; that is, only
    look up, down, left, or right from any given tree.

    All of the trees around the edge of the grid are visible - since they are already
    on the edge, there are no trees to block the view. In this example, that only
    leaves the interior nine trees to consider:

    The top-left 5 is visible from the left and top. (It isn't visible from the right
    or bottom since other trees of height 5 are in the way.)

    The top-middle 5 is visible from the top and right.

    The top-right 1 is not visible from any direction; for it to be visible, there
    would need to only be trees of height 0 between it and an edge.

    The left-middle 5 is visible, but only from the right.

    The center 3 is not visible from any direction; for it to be visible, there would
    need to be only trees of at most height 2 between it and an edge.

    The right-middle 3 is visible from the right.

    In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

    With 16 trees visible on the edge and another 5 visible in the interior, a total
    of 21 trees are visible in this arrangement.

    Consider your map; how many trees are visible from outside the grid?

    --- Part Two ---
    Content with the amount of tree cover available, the Elves just need
    to know the best spot to build their tree house: they would like to
    be able to see a lot of trees.

    To measure the viewing distance from a given tree, look up, down,
    left, and right from that tree; stop if you reach an edge or at
    the first tree that is the same height or taller than the tree under
    consideration. (If a tree is right on the edge, at least one of its
    viewing distances will be zero.)

    The Elves don't care about distant trees taller than those found
    by the rules above; the proposed tree house has large eaves to
    keep it dry, so they wouldn't be able to see higher than the tree
    house anyway.

    In the example above, consider the middle 5 in the second row:

    3 0 3 7 3
    2 5[5]1 2
    6 5 3 3 2
    3 3 5 4 9
    3 5 3 9 0

    Looking up, its view is not blocked; it can see 1 tree (of height 3).
    Looking left, its view is blocked immediately; it can see only 1 tree
    (of height 5, right next to it).
    Looking right, its view is not blocked; it can see 2 trees.
    Looking down, its view is blocked eventually; it can see 2 trees
    (one of height 3, then the tree of height 5 that blocks its view).
    A tree's scenic score is found by multiplying together its viewing
    distance in each of the four directions. For this tree, this is 4
    (found by multiplying 1 * 1 * 2 * 2).

    However, you can do even better: consider the tree of height 5 in
    the middle of the fourth row:

    3 0 3 7 3
    2 5 5 1 2
    6 5 3 3 2
    3 3[5]4 9
    3 5 3 9 0

    Looking up, its view is blocked at 2 trees
    (by another tree with a height of 5).
    Looking left, its view is not blocked; it can see 2 trees.
    Looking down, its view is also not blocked; it can see 1 tree.
    Looking right, its view is blocked at 2 trees
    (by a massive tree of height 9).

    This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the
    ideal spot for the tree house.

    Consider each tree on your map. What is the highest scenic
    score possible for any tree?
    """


with open(Path(__file__).parent / "2022_08_input.txt") as fp:
    RAW_INPUT = [line.strip() for line in fp]

RAW_SAMPLE = ["30373", "25512", "65332", "33549", "35390"]


def parse_raw_forest(raw_rows):
    coord_forest = {}
    y_max, x_max = 0, 0
    for y, raw_row in enumerate(raw_rows):
        y_max = max(y, y_max)
        for x, h in enumerate(raw_row):
            x_max = max(x, x_max)
            coord_forest[(x, y)] = int(h)
    return coord_forest, x_max, y_max


def count_external(coord_forest, x_max, y_max):
    # start out with all but outer ring hidden
    can_be_seen = {}
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            can_be_seen[(x, y)] = False if 0 < x < x_max and 0 < y < y_max else True
    # look up to down and left to right
    max_v_scan = {x: coord_forest[(x, 0)] for x in range(1, x_max)}
    max_h_scan = {y: coord_forest[(0, y)] for y in range(1, y_max)}
    for y in range(1, y_max):
        for x in range(1, x_max):
            if max_v_scan[x] < coord_forest[(x, y)]:
                can_be_seen[(x, y)] = True
                max_v_scan[x] = coord_forest[(x, y)]
            if max_h_scan[y] < coord_forest[(x, y)]:
                can_be_seen[(x, y)] = True
                max_h_scan[y] = coord_forest[(x, y)]

    # look down to up and right to left
    max_v_scan = {x: coord_forest[(x, y_max)] for x in range(1, x_max)}
    max_h_scan = {y: coord_forest[(x_max, y)] for y in range(1, y_max)}
    for y in range(y_max - 1, 0, -1):
        for x in range(x_max - 1, 0, -1):
            if max_v_scan[x] < coord_forest[(x, y)]:
                can_be_seen[(x, y)] = True
                max_v_scan[x] = coord_forest[(x, y)]
            if max_h_scan[y] < coord_forest[(x, y)]:
                can_be_seen[(x, y)] = True
                max_h_scan[y] = coord_forest[(x, y)]
    return sum(1 for v in can_be_seen.values() if v is True)


def test_find_cover():
    coord_forest, x_max, y_max = parse_raw_forest(RAW_SAMPLE)
    assert count_external(coord_forest, x_max, y_max) == 21
    coord_forest, x_max, y_max = parse_raw_forest(RAW_INPUT)
    assert count_external(coord_forest, x_max, y_max) == 1736


def scenic_score(x, y, forest, x_max, y_max):
    if x == 0 or x == x_max or y == 0 or y == y_max:
        return 0
    score = 1
    for dx, dy in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
        for r in range(1, max(x_max, y_max)):
            tx, ty = x + r * dx, y + r * dy
            if (tx, ty) in forest:
                if forest[(tx, ty)] < forest[(x, y)]:
                    continue
                if forest[(tx, ty)] >= forest[(x, y)]:
                    score *= r
                    break
            # out of forest need to back up
            score *= r - 1
            break
    return score


def max_scenic_score(forest, x_max, y_max):
    scores = set()
    for y in range(1, y_max):
        for x in range(1, x_max):
            scores.add(scenic_score(x, y, forest, x_max, y_max))
    return max(scores)


def test_scenic_score():
    forest, x_max, y_max = parse_raw_forest(RAW_SAMPLE)
    assert scenic_score(2, 1, forest, x_max, y_max) == 4
    assert scenic_score(2, 3, forest, x_max, y_max) == 8
    assert max_scenic_score(forest, x_max, y_max) == 8
    forest, x_max, y_max = parse_raw_forest(RAW_INPUT)
    assert max_scenic_score(forest, x_max, y_max) == 268800
