from typing import Set, Dict, List, NamedTuple
from collections import namedtuple, deque
from queue import PriorityQueue


class Puzzle:
    """
    --- Day 18: Many-Worlds Interpretation ---
    As you approach Neptune, a planetary security system detects you and activates a giant tractor beam on Triton!
    You have no choice but to land.

    A scan of the local area reveals only one interesting feature: a massive underground vault. You generate a map of
    the tunnels (your puzzle input). The tunnels are too narrow to move diagonally.

    Only one entrance (marked @) is present among the open passages (marked .) and stone walls (#), but you also
    detect an assortment of keys (shown as lowercase letters) and doors (shown as uppercase letters). Keys of a
    given letter open the door of the same letter: a opens A, b opens B, and so on. You aren't sure which key you
    need to disable the tractor beam, so you'll need to collect all of them.

    For example, suppose you have the following map:

    #########
    #b.A.@.a#
    #########
    Starting from the entrance (@), you can only access a large door (A) and a key (a). Moving toward the door
    doesn't help you, but you can move 2 steps to collect the key, unlocking A in the process:

    #########
    #b.....@#
    #########

    Then, you can move 6 steps to collect the only other key, b:

    #########
    #@......#
    #########

    So, collecting every key took a total of 8 steps.

    Here is a larger example:

    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################

    The only reasonable move is to take key a and unlock door A:

    ########################
    #f.D.E.e.C.b.....@.B.c.#
    ######################.#
    #d.....................#
    ########################

    Then, do the same with key b:

    ########################
    #f.D.E.e.C.@.........c.#
    ######################.#
    #d.....................#
    ########################

    ...and the same with key c:

    ########################
    #f.D.E.e.............@.#
    ######################.#
    #d.....................#
    ########################

    Now, you have a choice between keys d and e. While key e is closer, collecting it now would be slower in the long
    run than collecting key d first, so that's the best choice:

    ########################
    #f...E.e...............#
    ######################.#
    #@.....................#
    ########################

    Finally, collect key e to unlock door E, then collect key f, taking a grand total of 86 steps.

    Here are a few more examples:

    ########################
    #...............b.C.D.f#
    #.######################
    #.....@.a.B.c.d.A.e.F.g#
    ########################

    Shortest path is 132 steps: b, a, c, d, f, e, g

    #################
    #i.G..c...e..H.p#
    ########.########
    #j.A..b...f..D.o#
    ########@########
    #k.E..a...g..B.n#
    ########.########
    #l.F..d...h..C.m#
    #################

    Shortest paths are 136 steps;
    one is: a, f, b, j, g, n, h, d, l, o, e, p, c, i, k, m

    ########################
    #@..............ac.GI.b#
    ###d#e#f################
    ###A#B#C################
    ###g#h#i################
    ########################

    Shortest paths are 81 steps; one is: a, c, f, i, d, g, b, e, h

    How many steps is the shortest path that collects all of the keys?

    Your puzzle answer was 3270.

    --- Part Two ---

    You arrive at the vault only to discover that there is not one vault, but four - each with its own entrance.

    On your map, find the area in the middle that looks like this:

    ...
    .@.
    ...

    Update your map to instead use the correct data:

    @#@
    ###
    @#@

    This change will split your map into four separate sections, each with its own entrance:

    #######       #######
    #a.#Cd#       #a.#Cd#
    ##...##       ##@#@##
    ##.@.##  -->  #######
    ##...##       ##@#@##
    #cB#Ab#       #cB#Ab#
    #######       #######

    Because some of the keys are for doors in other vaults, it would take much too long to collect all of the keys
    by yourself. Instead, you deploy four remote-controlled robots. Each starts at one of the entrances (@).

    Your goal is still to collect all of the keys in the fewest steps, but now, each robot has its own position and
    can move independently. You can only remotely control a single robot at a time. Collecting a key instantly
    unlocks any corresponding doors, regardless of the vault in which the key or door is found.

    For example, in the map above, the top-left robot first collects key a, unlocking door A in the bottom-right vault:

    #######
    #@.#Cd#
    ##.#@##
    #######
    ##@#@##
    #cB#.b#
    #######

    Then, the bottom-right robot collects key b, unlocking door B in the bottom-left vault:

    #######
    #@.#Cd#
    ##.#@##
    #######
    ##@#.##
    #c.#.@#
    #######

    Then, the bottom-left robot collects key c:

    #######
    #@.#.d#
    ##.#@##
    #######
    ##.#.##
    #@.#.@#
    #######

    Finally, the top-right robot collects key d:

    #######
    #@.#.@#
    ##.#.##
    #######
    ##.#.##
    #@.#.@#
    #######

    In this example, it only took 8 steps to collect all of the keys.

    Sometimes, multiple robots might have keys available, or a robot might have to wait for multiple keys to
    be collected:

    ###############
    #d.ABC.#.....a#
    ######@#@######
    ###############
    ######@#@######
    #b.....#.....c#
    ###############

    First, the top-right, bottom-left, and bottom-right robots take turns collecting keys a, b, and c, a total
    of 6 + 6 + 6 = 18 steps. Then, the top-left robot can access key d, spending another 6 steps; collecting
    all of the keys here takes a minimum of 24 steps.

    Here's a more complex example:

    #############
    #DcBa.#.GhKl#
    #.###@#@#I###
    #e#d#####j#k#
    ###C#@#@###J#
    #fEbA.#.FgHi#
    #############

    Top-left robot collects key a.
    Bottom-left robot collects key b.
    Top-left robot collects key c.
    Bottom-left robot collects key d.
    Top-left robot collects key e.
    Bottom-left robot collects key f.
    Bottom-right robot collects key g.
    Top-right robot collects key h.
    Bottom-right robot collects key i.
    Top-right robot collects key j.
    Bottom-right robot collects key k.
    Top-right robot collects key l.

    In the above example, the fewest steps to collect all of the keys is 32.

    Here's an example with more choices:

    #############
    #g#f.D#..h#l#
    #F###e#E###.#
    #dCba@#@BcIJ#
    #############
    #nK.L@#@G...#
    #M###N#H###.#
    #o#m..#i#jk.#
    #############

    One solution with the fewest steps is:

    Top-left robot collects key e.
    Top-right robot collects key h.
    Bottom-right robot collects key i.
    Top-left robot collects key a.
    Top-left robot collects key b.
    Top-right robot collects key c.
    Top-left robot collects key d.
    Top-left robot collects key f.
    Top-left robot collects key g.
    Bottom-right robot collects key k.
    Bottom-right robot collects key j.
    Top-right robot collects key l.
    Bottom-left robot collects key n.
    Bottom-left robot collects key m.
    Bottom-left robot collects key o.

    This example requires at least 72 steps to collect all keys.

    After updating your map and using the remote-controlled robots, what is the fewest steps necessary
    to collect all of the keys?

    Your puzzle answer was 1628.
    """
    pass


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
            for i, c in enumerate(row):
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

    def shortest_path(self, start: Pos, end: Pos) -> tuple:
        frontier = deque()
        visited = set()

        frontier.append((start, [start], set()))
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
        robots = {f'@{ri}' for ri, _ in enumerate(self.start)}
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


with open('day_18_input.txt') as fp:
    SUBMISSION = fp.read()


with open('day_18_input_pt2.txt') as fp:
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
