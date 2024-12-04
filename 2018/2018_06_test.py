from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 6: Chronal Coordinates ---
    The device on your wrist beeps several times, and once again you feel like you're falling.

    "Situation critical," the device announces. "Destination indeterminate. Chronal interference detected.
    Please specify new target coordinates."

    The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or
    dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

    If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance
    from the other points.

    Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer
    X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

    Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list
    of coordinates:

    1, 1
    1, 6
    8, 3
    3, 4
    5, 5
    8, 9

    If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

    ..........
    .A........
    ..........
    ........C.
    ...D......
    .....E....
    .B........
    ..........
    ..........
    ........F.

    This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance,
    each location's closest coordinate can be determined, shown here in lowercase:

    aaaaa.cccc
    aAaaa.cccc
    aaaddecccc
    aadddeccCc
    ..dDdeeccc
    bb.deEeecc
    bBb.eeee..
    bbb.eeefff
    bbb.eeffff
    bbb.ffffFf

    Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

    In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend
    forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9
    locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example,
    the size of the largest area is 17.

    What is the size of the largest area that isn't infinite?

    --- Part Two ---
    On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near
    as many coordinates as possible.

    For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32.
    For each location, add up the distances to all of the given coordinates; if the total of those distances is
    less than 32, that location is within the desired region. Using the same coordinates as above, the resulting
    region looks like this:

    ..........
    .A........
    ..........
    ...###..C.
    ..#D###...
    ..###E#...
    .B.###....
    ..........
    ..........
    ........F.

    In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation
    is as follows, where abs() is the absolute value function:

    Distance to coordinate A: abs(4-1) + abs(3-1) =  5
    Distance to coordinate B: abs(4-1) + abs(3-6) =  6
    Distance to coordinate C: abs(4-8) + abs(3-3) =  4
    Distance to coordinate D: abs(4-3) + abs(3-4) =  2
    Distance to coordinate E: abs(4-5) + abs(3-5) =  3
    Distance to coordinate F: abs(4-8) + abs(3-9) = 10
    Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
    Because the total distance to all coordinates (30) is less than 32, the location is within the region.

    This region, which also includes coordinates D and E, has a total size of 16.

    Your actual region will need to be much larger than this example, though, instead including all locations with
    a total distance of less than 10000.

    What is the size of the region containing all locations which have a total distance to all given coordinates
    of less than 10000?
    """

    pass


with open(Path(__file__).parent / "2018_06_input.txt") as fp:
    INPUT = [tuple(int(n) for n in line.strip().split(",")) for line in fp]

SAMPLE = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]


def test_input():
    assert len(INPUT) == 50
    assert type(INPUT[0]) == type((1, 2))


def points_on_boarder(point_list):
    x_min = min([x for (x, y) in point_list])
    x_max = max([x for (x, y) in point_list])
    y_min = min([y for (x, y) in point_list])
    y_max = max([y for (x, y) in point_list])
    boarder = set()
    for x, y in point_list:
        if x == x_min or x == x_max or y == y_min or y == y_max:
            boarder.add((x, y))
    return boarder, (x_min, y_min), (x_max, y_max)


def test_points_on_boarder():
    assert points_on_boarder(SAMPLE) == (
        {(8, 9), (8, 3), (1, 6), (1, 1)},
        (1, 1),
        (8, 9),
    )


def dist(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])


def test_dist():
    assert dist((1, 3), (2, 2)) == 2


def make_grid(point_list, boarder_points, min_pt, max_pt):
    x_min, y_min = min_pt
    x_max, y_max = max_pt

    grid = defaultdict(tuple)
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            if (x, y) in point_list:
                if (x, y) not in boarder_points:
                    grid[(x, y)] = (x, y)
            else:
                distances = defaultdict(list)
                for pt in point_list:
                    distances[dist(pt, (x, y))].append(pt)
                _, points = min(distances.items())
                if len(points) == 1 and points[0] not in boarder_points:
                    grid[(x, y)] = points[0]
    return grid


def test_make_grid():
    RESULT = make_grid(SAMPLE, {(8, 9), (8, 3), (1, 6), (1, 1)}, (1, 1), (8, 9))
    assert RESULT[(1, 1)] == ()
    assert RESULT[(3, 2)] == (3, 4)


def count_grid(grid):
    count = defaultdict(int)
    for pt in grid:
        count[grid[pt]] += 1
    return sorted(count.items(), key=lambda x: -x[1])


def test_count_grid():
    pts, min_pt, max_pt = points_on_boarder(SAMPLE)
    assert count_grid(make_grid(SAMPLE, pts, min_pt, max_pt)) == ((5, 5), 17)


def test_submission_count_grid():
    ignore_pts, min_pt, max_pt = points_on_boarder(INPUT)
    result = count_grid(make_grid(INPUT, ignore_pts, min_pt, max_pt))
    assert result[0][1] == 3238
    # ((354, 278), 971) --> 971 too low...  oops, wrong sorting for max


def total_dist_grid(point_list, max_total_dist, min_pt, max_pt):
    x_min, y_min = min_pt
    x_max, y_max = max_pt
    count = 0
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            dist_sum = 0
            for pt in point_list:
                if dist_sum < max_total_dist:
                    dist_sum += dist(pt, (x, y))
            if dist_sum < max_total_dist:
                count += 1
    return count


def test_total_dist_grid():
    boarder_pts, min_pt, max_pt = points_on_boarder(SAMPLE)
    assert total_dist_grid(SAMPLE, 32, min_pt, max_pt) == 16
    boarder_pts, min_pt, max_pt = points_on_boarder(INPUT)
    assert total_dist_grid(INPUT, 10000, min_pt, max_pt) == 45046
