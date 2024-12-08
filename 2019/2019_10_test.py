from pathlib import Path
from numpy import pi, arctan2
from collections import defaultdict
from typing import List


class Puzzle:
    """
    --- Day 10: Monitoring Station ---
    You fly into the asteroid belt and reach the Ceres monitoring station. The Elves here have an emergency: they're
    having trouble tracking all of the asteroids and can't be sure they're safe.

    The Elves would like to build a new monitoring station in a nearby area of space; they hand you a map of all of
    the asteroids in that region (your puzzle input).

    The map indicates whether each position is empty (.) or contains an asteroid (#). The asteroids are much smaller
    than they appear on the map, and every asteroid is exactly in the center of its marked position. The asteroids
    can be described with X,Y coordinates where X is the distance from the left edge and Y is the distance from the
    top edge (so the top-left corner is 0,0 and the position immediately to its right is 1,0).

    Your job is to figure out which asteroid would be the best place to build a new monitoring station. A monitoring
    station can detect any asteroid to which it has direct line of sight - that is, there cannot be another asteroid
    exactly between them. This line of sight can be at any angle, not just lines aligned to the grid or diagonally.
    The best location is the asteroid that can detect the largest number of other asteroids.

    For example, consider the following map:

    .#..#
    .....
    #####
    ....#
    ...##

    The best location for a new monitoring station on this map is the highlighted asteroid at 3,4 because it can
    detect 8 asteroids, more than any other location. (The only asteroid it cannot detect is the one at 1,0; its
    view of this asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse locations; they can
    detect 7 or fewer other asteroids. Here is the number of other asteroids a monitoring station on each asteroid
    could detect:

    .7..7
    .....
    67775
    ....7
    ...87

    Here is an asteroid (#) and some examples of the ways its line of sight might be blocked. If there were another
    asteroid at the location of a capital letter, the locations marked with the corresponding lowercase letter would
    be blocked and could not be detected:

    #.........
    ...A......
    ...B..a...
    .EDCG....a
    ..F.c.b...
    .....c....
    ..efd.c.gb
    .......c..
    ....f...c.
    ...e..d..c

    Here are some larger examples:

    Best is 5,8 with 33 other asteroids detected:

    ......#.#.
    #..#.#....
    ..#######.
    .#.#.###..
    .#..#.....
    ..#....#.#
    #..#....#.
    .##.#..###
    ##...#..#.
    .#....####

    Best is 1,2 with 35 other asteroids detected:

    #.#...#.#.
    .###....#.
    .#....#...
    ##.#.#.#.#
    ....#.#.#.
    .##..###.#
    ..#...##..
    ..##....##
    ......#...
    .####.###.

    Best is 6,3 with 41 other asteroids detected:

    .#..#..###
    ####.###.#
    ....###.#.
    ..###.##.#
    ##.##.#.#.
    ....###..#
    ..#.#..#.#
    #..#.#.###
    .##...##.#
    .....#.#..

    Best is 11,13 with 210 other asteroids detected:

    .#..##.###...#######
    ##.############..##.
    .#.######.########.#
    .###.#######.####.#.
    #####.##.#.##.###.##
    ..#####..#.#########
    ####################
    #.####....###.#.#.##
    ##.#################
    #####.##.###..####..
    ..######..##.#######
    ####.##.####...##..#
    .#####..#.######.###
    ##...#.##########...
    #.##########.#######
    .####.#.###.###.#.##
    ....##.##.###..#####
    .#.#.###########.###
    #.#.#.#####.####.###
    ###.##.####.##.#..##

    Find the best location for a new monitoring station. How many other asteroids can be detected from that location?

    Your puzzle answer was 340.

    --- Part Two ---
    Once you give them the coordinates, the Elves quickly deploy an Instant Monitoring Station to the location and
    discover the worst: there are simply too many asteroids.

    The only solution is complete vaporization by giant laser.

    Fortunately, in addition to an asteroid scanner, the new monitoring station also comes equipped with a giant
    rotating laser perfect for vaporizing asteroids. The laser starts by pointing up and always rotates clockwise,
    vaporizing any asteroid it hits.

    If multiple asteroids are exactly in line with the station, the laser only has enough power to vaporize one of
    them before continuing its rotation. In other words, the same asteroids that can be detected can be vaporized,
    but if vaporizing one asteroid makes another one detectable, the newly-detected asteroid won't be vaporized until
    the laser has returned to the same position by rotating a full 360 degrees.

    For example, consider the following map, where the asteroid with the new monitoring station (and laser) is
    marked X:

    .#....#####...#..
    ##...##.#####..##
    ##...#...#.#####.
    ..#.....X...###..
    ..#.#.....#....##

    The first nine asteroids to get vaporized, in order, would be:

    .#....###24...#..
    ##...##.13#67..9#
    ##...#...5.8####.
    ..#.....X...###..
    ..#.#.....#....##

    Note that some asteroids (the ones behind the asteroids marked 1, 5, and 7) won't have a chance to be vaporized
    until the next full rotation. The laser continues rotating; the next nine to be vaporized are:

    .#....###.....#..
    ##...##...#.....#
    ##...#......1234.
    ..#.....X...5##..
    ..#.9.....8....76

    The next nine to be vaporized are then:

    .8....###.....#..
    56...9#...#.....#
    34...7...........
    ..2.....X....##..
    ..1..............

    Finally, the laser completes its first full rotation (1 through 3), a second rotation (4 through 8), and vaporizes
    the last asteroid (9) partway through its third rotation:

    ......234.....6..
    ......1...5.....7
    .................
    ........X....89..
    .................

    In the large example above (the one with the best monitoring station location at 11,13):

    The 1st asteroid to be vaporized is at 11,12.
    The 2nd asteroid to be vaporized is at 12,1.
    The 3rd asteroid to be vaporized is at 12,2.
    The 10th asteroid to be vaporized is at 12,8.
    The 20th asteroid to be vaporized is at 16,0.
    The 50th asteroid to be vaporized is at 16,9.
    The 100th asteroid to be vaporized is at 10,16.
    The 199th asteroid to be vaporized is at 9,6.
    The 200th asteroid to be vaporized is at 8,2.
    The 201st asteroid to be vaporized is at 10,9.
    The 299th and final asteroid to be vaporized is at 11,1.

    The Elves are placing bets on which will be the 200th asteroid to be vaporized. Win the bet by determining which
    asteroid that will be; what do you get if you multiply its X coordinate by 100 and then add its Y coordinate?
    (For example, 8,2 becomes 802.)

    Your puzzle answer was 2628.
    """

    pass


def vector_angle(delta):
    return 1 - arctan2(delta[0], delta[1]) / pi


def vec_length(v):
    return v[0] * v[0] + v[1] * v[1]


def order_vectors(grid):
    by_angle = defaultdict(list)
    for vec in grid:
        by_angle[vector_angle(vec)].append(vec)
    for vec_list in by_angle:
        by_angle[vec_list].sort(key=vec_length)
    return by_angle


def count_directions(deltas: List):
    return len(set([vector_angle(d) for d in deltas]))


def find_deltas(x, asteroid_map):
    return [(k[0] - x[0], k[1] - x[1]) for k in asteroid_map if k != x]


def build_map(map_str):
    map_dict = {}
    for y, line in enumerate(map_str.split("\n")):
        for x, c in enumerate(line):
            if c == "#":
                map_dict[(x, y)] = 1
    return map_dict


def eval_map(asteroid_map):
    map_with_numbers = {
        k: count_directions(find_deltas(k, asteroid_map)) for k in asteroid_map
    }
    max_loc = max(map_with_numbers.keys(), key=(lambda k: map_with_numbers[k]))
    return map_with_numbers, max_loc


def test_vector_angles():
    # assert [(vector_angle(v),v) for v in [(sin(2*pi*n/128),-cos(2*pi*n/128),) for n in range(129)]] == []
    assert vector_angle((0, -1)) == 0.0
    assert vector_angle((1, -1)) == 0.25
    assert vector_angle((1, 0)) == 0.5
    assert vector_angle((1, 1)) == 0.75
    assert vector_angle((0, 1)) == 1.0
    assert vector_angle((-1, 1)) == 1.25
    assert vector_angle((-1, 0)) == 1.5
    assert vector_angle((-1, -1)) == 1.75


def test_order_vectors():
    test_grid = [
        (-1, 1),
        (0, 1),
        (1, 1),
        (2, 1),
        (-1, 0),
        (1, 0),
        (2, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
        (2, -1),
    ]
    ordered_grid = dict(order_vectors(test_grid))
    assert ordered_grid[0] == [(0, -1)]
    assert ordered_grid[0.25] == [(1, -1)]
    assert ordered_grid[0.5] == [(1, 0), (2, 0)]
    assert ordered_grid[0.75] == [(1, 1)]
    assert ordered_grid[1] == [(0, 1)]
    assert ordered_grid[1.25] == [(-1, 1)]


def test_count_directions():
    assert count_directions([(0, 1), (0, 2)]) == 1
    assert count_directions([(0, 1), (0, -2)]) == 2
    assert (
        count_directions(
            [
                (-1, 1),
                (0, 1),
                (1, 1),
                (-1, 0),
                (0, 0),
                (1, 0),
                (-1, -1),
                (0, -1),
                (1, -1),
            ]
        )
        == 8
    )


def test_find_deltas():
    asteroid_map = {
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
    }
    assert len(find_deltas((0, 0), asteroid_map)) == 3
    assert count_directions(find_deltas((0, 0), asteroid_map)) == 3


def test_build_map():
    map_str = ".#..#\n.....\n#####\n....#\n...##"
    map_dict = {
        (0, 2): 1,
        (1, 0): 1,
        (1, 2): 1,
        (2, 2): 1,
        (3, 2): 1,
        (3, 4): 1,
        (4, 0): 1,
        (4, 2): 1,
        (4, 3): 1,
        (4, 4): 1,
    }
    assert build_map(map_str) == map_dict


def test_eval_map():
    map_str = ".#..#\n.....\n#####\n....#\n...##"
    map_with_numbers = {
        (0, 2): 6,
        (1, 0): 7,
        (1, 2): 7,
        (2, 2): 7,
        (3, 2): 7,
        (3, 4): 8,
        (4, 0): 7,
        (4, 2): 5,
        (4, 3): 7,
        (4, 4): 7,
    }
    assert eval_map(build_map(map_str)) == (map_with_numbers, (3, 4))


def test_large_sample():
    with open(Path(__file__).parent / "2019_10_input_sample.txt") as fp:
        map_str = fp.read()
    asteroid_map = eval_map(build_map(map_str))
    assert asteroid_map[1] == (11, 13)
    assert asteroid_map[0][11, 13] == 210
    ordered_list = order_vectors(find_deltas((11, 13), asteroid_map[0]))
    bet_angle = sorted(ordered_list)[199]
    # assert bet_angle == 0
    bet_delta = ordered_list[bet_angle][0]
    # assert bet_delta == (0, -1)
    assert (bet_delta[0] + 11, bet_delta[1] + 13) == (8, 2)


def test_submission():
    with open(Path(__file__).parent / "2019_10_input.txt") as fp:
        map_str = fp.read()
    asteroid_map = eval_map(build_map(map_str))
    assert asteroid_map[1] == (28, 29)
    assert asteroid_map[0][28, 29] == 340
    ordered_list = order_vectors(find_deltas((28, 29), asteroid_map[0]))
    bet_angle = sorted(ordered_list)[199]
    # assert bet_angle == 0
    bet_delta = ordered_list[bet_angle][0]
    # assert bet_delta == (0, -1)
    assert (bet_delta[0] + 28, bet_delta[1] + 29) == (26, 28)
