from numpy import sin, cos, pi, arctan2
from collections import defaultdict
from typing import List


def vector_angle(delta):
    return 1 - arctan2(delta[0], delta[1]) / pi


def vec_length(v):
    return v[0]*v[0] + v[1]*v[1]


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
    for y, line in enumerate(map_str.split('\n')):
        for x, c in enumerate(line):
            if c == '#':
                map_dict[(x, y)] = 1
    return map_dict


def eval_map(asteroid_map):
    map_with_numbers = {k: count_directions(find_deltas(k, asteroid_map)) for k in asteroid_map}
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
    test_grid = [(-1, 1), (0, 1), (1, 1), (2, 1),
                 (-1, 0), (1, 0), (2, 0),
                 (-1, -1), (0, -1), (1, -1), (2, -1)]
    ordered_grid = dict(order_vectors(test_grid))
    assert ordered_grid[0] == [(0, 1)]
    assert ordered_grid[0.25] == [(1, 1)]
    assert ordered_grid[0.5] == [(1, 0), (2, 0)]
    assert ordered_grid[0.75] == [(1, -1)]
    assert ordered_grid[1] == [(0, -1)]
    assert ordered_grid[1.25] == [(-1, -1)]


def test_count_directions():
    assert count_directions([(0, 1), (0, 2)]) == 1
    assert count_directions([(0, 1), (0, -2)]) == 2
    assert count_directions([(-1, 1), (0, 1), (1, 1),
                             (-1, 0), (0, 0), (1, 0),
                             (-1, -1), (0, -1), (1, -1)]) == 8


def test_find_deltas():
    asteroid_map = {(0, 0), (1, 0), (0, 1), (1, 1), }
    assert len(find_deltas((0, 0), asteroid_map)) == 3
    assert count_directions(find_deltas((0, 0), asteroid_map)) == 3


def test_build_map():
    map_str = '.#..#\n.....\n#####\n....#\n...##'
    map_dict = {(0, 2): 1, (1, 0): 1, (1, 2): 1, (2, 2): 1, (3, 2): 1,
                (3, 4): 1, (4, 0): 1, (4, 2): 1, (4, 3): 1, (4, 4): 1}
    assert build_map(map_str) == map_dict


def test_eval_map():
    map_str = '.#..#\n.....\n#####\n....#\n...##'
    map_with_numbers = {(0, 2): 6, (1, 0): 7, (1, 2): 7, (2, 2): 7, (3, 2): 7,
                        (3, 4): 8, (4, 0): 7, (4, 2): 5, (4, 3): 7, (4, 4): 7}
    assert eval_map(build_map(map_str)) == (map_with_numbers, (3, 4))


def test_large_sample():
    with open('input_day_10_sample.txt') as fp:
        map_str = fp.read()
    asteroid_map = eval_map(build_map(map_str))
    assert asteroid_map[1] == (11, 13)
    assert asteroid_map[0][11, 13] == 210
    ordered_list = order_vectors(find_deltas((11,13),asteroid_map[0]))
    bet_angle = sorted(ordered_list)[199]
    # assert bet_angle == 0
    bet_delta = ordered_list[bet_angle][0]
    # assert bet_delta == (0, -1)
    assert (bet_delta[0] + 11, bet_delta[1] + 13) == (8, 2)


def test_submission():
    with open('input_day_10.txt') as fp:
        map_str = fp.read()
    asteroid_map = eval_map(build_map(map_str))
    assert asteroid_map[1] == (28, 29)
    assert asteroid_map[0][28, 29] == 340
    ordered_list = order_vectors(find_deltas((28, 29), asteroid_map[0]))
    bet_angle = sorted(ordered_list)[199]
    #assert bet_angle == 0
    bet_delta = ordered_list[bet_angle][0]
    #assert bet_delta == (0, -1)
    assert (bet_delta[0] + 28, bet_delta[1] + 29) == (26, 28)
