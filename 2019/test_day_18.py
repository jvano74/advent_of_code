from dataclasses import dataclass
from typing import Set, Dict, List, NamedTuple
from collections import namedtuple, deque
from queue import PriorityQueue

class Pos(NamedTuple):
    x: int
    y: int


DELTAS = {Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1)}


def signature(new_key, key_hx):
    return frozenset(new_key), frozenset(key_hx)


class Maze:
    def __init__(self, grid: List[List[str]]):
        self.tiles = set()
        self.doors = {}
        self.keys = {}
        self.start = set()
        for j, row in enumerate(grid):
            for i,c in enumerate(row):
                if c == '#':
                    continue
                self.tiles.add(Pos(i, j))
                if c == '@':
                    self.start.add(Pos(i, j))
                    continue
                if 'a' <= c <= 'z':
                    self.keys[c] = Pos(i, j)
                    continue
                if 'A' <= c <= 'Z':
                    self.doors[Pos(i, j)] = c.lower()
                    continue

    def neighbors(self, pos: Pos) -> Set[Pos]:
        found = set()
        for d in DELTAS:
            possible_neighbor = Pos(pos.x + d.x, pos.y + d.y)
            if possible_neighbor in self.tiles:
                found.add(possible_neighbor)
        return found

    def shortest_path(self, start: Pos, end: Pos) -> List:
        frontier = deque()
        visited = set()

        frontier.append((start,[start],set()))
        visited.add(start)

        while frontier:
            pos, path_hx, door_hx = frontier.popleft()
            for nn in self.neighbors(pos):
                if nn not in visited:
                    new_door_hx = set(door_hx)
                    if nn in self.doors:
                        new_door_hx.add(self.doors[nn])
                    if nn == end:
                        path_hx.append(nn)
                        return path_hx, new_door_hx
                    new_hx = list(path_hx)
                    new_hx.append(nn)
                    frontier.append((nn, new_hx, new_door_hx))
                    visited.add(nn)
        raise LookupError(f'Not {end} not part of {start}')

    def key_to_key_distances(self):
        data = {}
        all_positions = dict(self.keys)
        for ri, robot in enumerate(self.start):
            all_positions[f'@{ri}'] = robot
        for k1 in all_positions:
            for k2 in all_positions:
                if k2 == k1:
                    continue
                try:
                    path, keys = self.shortest_path(all_positions[k1], all_positions[k2])
                    data[(k1, k2)] = (keys, len(path))
                except LookupError:
                    print(f'Oh my, {k1} cannot reach {k2}')
                finally:
                    pass
        return data

    def all_key_graph(self):
        data = self.key_to_key_distances()
        truncations = set()
        lengths = []

        frontier = PriorityQueue()
        robots = {f'@{ri}' for ri, _ in enumerate(self.start) }
        frontier.put((0, robots, robots))

        while not frontier.empty():
            dist, robots, key_hx = frontier.get()
            sig = signature(robots, key_hx)
            if sig in truncations:
                continue
            for new_key in self.keys:
                if new_key in key_hx:
                    continue
                for key in robots:
                    if (key, new_key) not in data:
                        continue
                    doors, new_dist = data[(key, new_key)]
                    if len(doors - key_hx) > 0:
                        continue
                    new_key_hx = set(key_hx)
                    new_key_hx.add(new_key)
                    new_robots = set(robots)
                    new_robots.remove(key)
                    new_robots.add(new_key)
                    if len(new_key_hx) == len(self.keys) + len(robots):
                        lengths.append(dist + new_dist - len(self.keys))
                    frontier.put((dist + new_dist, new_robots, new_key_hx))
            truncations.add(sig)
        return min(lengths)


MINI_MAZE = """#########
               #b.A.@.a#
               #########"""


MAZE_86 = """########################
            #f.D.E.e.C.b.A.@.a.B.c.#
            ######################.#
            #d.....................#
            ########################"""


MAX_MAZE = """#################
              #i.G..c...e..H.p#
              ########.########
              #j.A..b...f..D.o#
              ########@########
              #k.E..a...g..B.n#
              ########.########
              #l.F..d...h..C.m#
              #################"""


SPLIT_MAZE_8 = """#######
                  #a.#Cd#
                  ##@#@##
                  #######
                  ##@#@##
                  #cB#Ab#
                  #######"""


SPLIT_MAZE_24 = """###############
                   #d.ABC.#.....a#
                   ######@#@######
                   ###############
                   ######@#@######
                   #b.....#.....c#
                   ###############"""


SPLIT_MAZE_32 = """#############
                   #DcBa.#.GhKl#
                   #.###@#@#I###
                   #e#d#####j#k#
                   ###C#@#@###J#
                   #fEbA.#.FgHi#
                   #############"""


SPLIT_MAZE_72 = """#############
                   #g#f.D#..h#l#
                   #F###e#E###.#
                   #dCba@#@BcIJ#
                   #############
                   #nK.L@#@G...#
                   #M###N#H###.#
                   #o#m..#i#jk.#
                   #############"""


with open('input_day_18.txt') as fp:
    SUBMISSION = fp.read()


with open('input_day_18_pt2.txt') as fp:
    SUBMISSION2 = fp.read()


def help_test_maze(raw: str, expected_path_length: int):
    maze = Maze([list(row.strip()) for row in raw.split('\n')])
    # assert maze.key_to_key_distances() == {}
    assert maze.all_key_graph() == expected_path_length


def test_create_maze():
    maze1 = Maze([list(row.strip()) for row in MINI_MAZE.split('\n')])
    left_to_right = [Pos(1, 1), Pos(2, 1), Pos(3, 1), Pos(4, 1), Pos(5, 1), Pos(6, 1), Pos(7, 1)]
    assert maze1.tiles == set(left_to_right)
    assert maze1.keys == {'b': Pos(1, 1), 'a': Pos(7, 1)}
    assert maze1.doors == {Pos(3, 1): 'a'}
    assert maze1.start == {Pos(5, 1)}
    assert maze1.neighbors(Pos(2, 1)) == {Pos(1, 1), Pos(3, 1)}
    assert maze1.shortest_path(Pos(1, 1), Pos(7, 1)) == (left_to_right, {'a'})
    assert maze1.key_to_key_distances() == {('@0', 'a'): (set(), 3),
                                            ('a', '@0'): (set(), 3),
                                            ('@0', 'b'): ({'a'}, 5),
                                            ('b', '@0'): ({'a'}, 5),
                                            ('a', 'b'): ({'a'}, 7),
                                            ('b', 'a'): ({'a'}, 7)}
    assert maze1.all_key_graph() == 8


def test_create_max_maze():
    help_test_maze(MAZE_86, 86)
    help_test_maze(MAX_MAZE, 136)
    help_test_maze(SPLIT_MAZE_8, 8)
    help_test_maze(SPLIT_MAZE_24, 24)
    help_test_maze(SPLIT_MAZE_32, 32)
    help_test_maze(SPLIT_MAZE_72, 72)


def test_submission():
    help_test_maze(SUBMISSION, 3270)


def test_submission2():
    help_test_maze(SUBMISSION2, 1628)
