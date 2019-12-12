import numpy as np
from typing import List

def vector_angle(delta):
    return np.arctan2(delta[1], delta[0])

def normalize_vector(delta):
    if delta[0] > 0:
        return 1, delta[1] / delta[0]
    if delta[0] < 0:
        return -1, -delta[1] / delta[0]
    if delta[1] > 0:
        return 0, 1
    if delta[1] < 0:
        return 0, -1
    return 0, 0


def order_vectors(grid):
    return sorted(grid, cmp=vector_angle)


def count_directions(deltas: List):
    return len(set([vector_angle(d) for d in deltas]))


def find_deltas(x, map):
    return [(k[0] - x[0], k[1] - x[1]) for k in map if k is not x]


def build_map(map_str):
    map_dict = {}
    for y, line in enumerate(map_str.split('\n')):
        for x, c in enumerate(line):
            if c == '#':
                map_dict[(x, y)] = 1
    return map_dict


def eval_map(map):
    map_with_numbers = {k: count_directions(find_deltas(k, map)) for k in map}
    max_loc = max(map_with_numbers.keys(), key=(lambda k: map_with_numbers[k]))
    return map_with_numbers, max_loc


def test_normalize_vector():
    assert normalize_vector((0, 5)) == (0, 1.0)
    assert normalize_vector((0, -3)) == (0, -1.0)
    assert normalize_vector((2, 2)) == (1, 1.0)
    assert normalize_vector((1, -2)) == (1, -2.0)
    assert normalize_vector((-2, 1)) == (-1, 0.5)


def test_order_vectors():
    test_grid = [(-1, 1), (0, 1), (1, 1), (2, 1),
                 (-1, 0), (0, 0), (1, 0), (2, 0),
                 (-1, -1), (0, -1), (1, -1), (2, -1)]
    ordered_grid = order_vectors(test_grid)
    assert ordered_grid == []


def test_count_directions():
    assert count_directions([(0, 1), (0, 2)]) == 1
    assert count_directions([(0, 1), (0, -2)]) == 2
    assert count_directions([(-1, 1), (0, 1), (1, 1),
                             (-1, 0), (0, 0), (1, 0),
                             (-1, -1), (0, -1), (1, -1)]) == 8


def test_find_deltas():
    map = {(0, 0), (1, 0), (0, 1), (1, 1), }
    assert len(find_deltas((0, 0), map)) == 4
    assert count_directions(find_deltas((0, 0), map)) == 4


def test_build_map():
    map_str = '.#..#\n.....\n#####\n....#\n...##'
    map_dict = {(0, 2): 1, (1, 0): 1, (1, 2): 1, (2, 2): 1, (3, 2): 1,
                (3, 4): 1, (4, 0): 1, (4, 2): 1, (4, 3): 1, (4, 4): 1}
    assert build_map(map_str) == map_dict


def test_eval_map():
    map_str = '.#..#\n.....\n#####\n....#\n...##'
    map_with_numbers = {(0, 2): 7, (1, 0): 8, (1, 2): 8, (2, 2): 8, (3, 2): 8,
                        (3, 4): 9, (4, 0): 8, (4, 2): 6, (4, 3): 8, (4, 4): 8}
    assert eval_map(build_map(map_str)) == (map_with_numbers, (3, 4))


def test_eval_map():
    map_str = '.#..#\n.....\n#####\n....#\n...##'
    map_with_numbers = {(0, 2): 7, (1, 0): 8, (1, 2): 8, (2, 2): 8, (3, 2): 8,
                        (3, 4): 9, (4, 0): 8, (4, 2): 6, (4, 3): 8, (4, 4): 8}
    assert eval_map(build_map(map_str)) == (map_with_numbers, (3, 4))


def test_submission():
    with open('input_day_10.txt') as fp:
        map_str = fp.read()
    map = eval_map(build_map(map_str))
    assert map[1] == (28, 29)
    assert map[0][28, 29] == 341 - 1
