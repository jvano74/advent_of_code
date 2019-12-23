from typing import Set, Tuple, List, NamedTuple
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
        self.portal_down = {}
        self.portal_up = {}
        self.start = None
        self.end = None
        raw_portals = {}
        self.hole_min = None
        self.hole_max = None
        for j, row in enumerate(grid):
            for i, c in enumerate(row):
                if c == '#' or c == ' ':
                    continue
                if c == 'h':
                    self.hole_min = Pos(i, j)
                    continue
                if c == 'e':
                    self.hole_max = Pos(i, j)
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
                    inner = self.is_inner(pos2)
                    if d == Pos(-1, 0) or d == Pos(0, -1):
                        name = raw_portals[pos2] + raw_portals[pos1]
                    else:
                        name = raw_portals[pos1] + raw_portals[pos2]
                    if name == 'AA':
                        self.start = (pos3, 0)
                        continue
                    if name == 'ZZ':
                        self.end = (pos3, 0)
                        continue
                    self.portals[name].add(pos3)
                    self.portal_ends[pos2] = name
                    if inner:
                        self.portal_down[pos2] = name
                    else:
                        self.portal_up[pos2] = name

    def is_inner(self, pos):
        if self.hole_min is None or self.hole_max is None:
            return False
        if self.hole_min.y <= pos.y <= self.hole_max.y:
            if self.hole_min.x <= pos.x <= self.hole_max.x:
                return True
        return False

    def neighbors(self, poslvl: Tuple[Pos,int]) -> Set[Tuple[Pos,int]]:
        found = set()
        pos, lvl = poslvl
        for d in DELTAS:
            possible_neighbor = Pos(pos.x + d.x, pos.y + d.y)
            if possible_neighbor in self.tiles:
                found.add((possible_neighbor,lvl))
                continue
            if lvl == 0 and possible_neighbor in self.portal_up:
                continue
            if possible_neighbor in self.portal_ends:
                portal_name = self.portal_ends[possible_neighbor]
                ends = set(self.portals[portal_name])
                ends.remove(pos)
                other_end = ends.pop()
                if possible_neighbor in self.portal_up:
                    found.add((other_end, lvl - 1))
                else:
                    found.add((other_end, lvl + 1))
        return found

    def shortest_path(self, start: Tuple[Pos,int], end: Tuple[Pos,int]) -> List[Tuple[Pos,int]]:
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
  #####h B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G e###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""

MAZE_3 = """
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#h   F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P     e#.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M
"""

with open('input_day_20.txt') as fp:
    SUBMISSION = fp.read()


def help_test_maze_min(raw: str, expected_path_length: int):
    maze = Maze([list(row) for row in raw.split('\n')])
    # print(maze.hole_min,maze.hole_max)
    # print(maze.portal_down)
    # print(maze.portal_up)
    # assert False
    path = maze.shortest_path(maze.start, maze.end)
    print(path)
    assert len(path)-1 == expected_path_length


def test_create_maze_details():
    maze = Maze([list(row) for row in MAZE_1.split('\n')])
    assert maze.start == (Pos(9, 3), 0)
    assert maze.end == (Pos(13, 17), 0)
    portal = set(maze.portals['BC']).pop()
    assert portal == Pos(2, 9)
    assert maze.neighbors((portal, 0)) == {(Pos(x=3, y=9), 0)}
    assert maze.neighbors((portal, 1)) == {(Pos(x=9, y=7), 0), (Pos(x=3, y=9), 1)}


def test_maze_min_length():
    help_test_maze_min(MAZE_1, 26)
    help_test_maze_min(MAZE_3, 396)


def test_submission():
    help_test_maze_min(SUBMISSION, 7798)
