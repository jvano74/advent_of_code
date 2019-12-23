from typing import Set, Dict, List, NamedTuple
from collections import deque, defaultdict

class Pos(NamedTuple):
    x: int
    y: int


DELTAS = {Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1)}


def signature(new_key, key_hx):
    return frozenset(new_key), frozenset(key_hx)


class Maze:
    def __init__(self, grid: List[List[str]]):
        self.tiles = set()
        self.portals = defaultdict(set)
        self.portal_ends = {}
        self.start = None
        self.end = None
        raw_portals = {}
        for j, row in enumerate(grid):
            for i, c in enumerate(row):
                if c == '#' or c == ' ':
                    continue
                if c == '.':
                    self.tiles.add(Pos(i, j))
                    continue
                if 'A' <= c <= 'Z':
                    raw_portals[Pos(i, j)] = c
                    continue
        for pos1 in raw_portals:
            for d in DELTAS:
                pos2 = Pos(pos1.x + d.x, pos1.y + d.y)
                pos3 = Pos(pos2.x + d.x, pos2.y + d.y)
                if pos2 in raw_portals and pos3 in self.tiles:
                    if d == Pos(-1,0) or d == Pos(0,-1):
                        name = raw_portals[pos2] + raw_portals[pos1]
                    else:
                        name = raw_portals[pos1] + raw_portals[pos2]
                    if name == 'AA':
                        self.start = pos3
                        continue
                    if name == 'ZZ':
                        self.end = pos3
                        continue
                    self.portals[name].add(pos3)
                    self.portal_ends[pos2] = name

    def neighbors(self, pos: Pos) -> Set[Pos]:
        found = set()
        for d in DELTAS:
            possible_neighbor = Pos(pos.x + d.x, pos.y + d.y)
            if possible_neighbor in self.tiles:
                found.add(possible_neighbor)
            if possible_neighbor in self.portal_ends:
                portal_name = self.portal_ends[possible_neighbor]
                ends = set(self.portals[portal_name])
                ends.remove(pos)
                other_end = ends.pop()
                found.add(other_end)
        return found

    def shortest_path(self, start: Pos, end: Pos) -> List:
        frontier = deque()
        visited = set()

        frontier.append((start, [start]))
        visited.add(start)

        while frontier:
            pos, path_hx = frontier.popleft()
            for nn in self.neighbors(pos):
                if nn not in visited:
                    if nn == end:
                        path_hx.append(nn)
                        return path_hx
                    new_hx = list(path_hx)
                    new_hx.append(nn)
                    frontier.append((nn, new_hx))
                    visited.add(nn)
        raise LookupError(f'Not {end} not part of {start}')


MAZE_1 = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""

MAZE_2 = """
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P              
"""

with open('input_day_20.txt') as fp:
    SUBMISSION = fp.read()


def help_test_maze_min(raw: str, expected_path_length: int):
    maze = Maze([list(row) for row in raw.split('\n')])
    assert len(maze.shortest_path(maze.start, maze.end))-1 == expected_path_length


def test_create_maze_details():
    maze = Maze([list(row) for row in MAZE_1.split('\n')])
    assert maze.start == Pos(9,3)
    assert maze.end == Pos(13,17)
    portal = set(maze.portals['BC']).pop()
    assert portal == Pos(2,9)
    assert maze.neighbors(portal) == {Pos(x=9, y=7), Pos(x=3, y=9)}


def test_maze_min_length():
    help_test_maze_min(MAZE_1, 23)
    help_test_maze_min(MAZE_2, 58)


def test_submission():
    help_test_maze_min(SUBMISSION, 644)
