from typing import NamedTuple
from collections import defaultdict
from queue import PriorityQueue


class Puzzle:
    """
    --- Day 20: A Regular Map ---
    While you were learning about instruction pointers, the Elves made considerable progress. When you look up, you
    discover that the North Pole base construction project has completely surrounded you.

    The area you are in is made up entirely of rooms and doors. The rooms are arranged in a grid, and rooms only
    connect to adjacent rooms when a door is present between them.

    For example, drawing rooms as ., walls as #, doors as | or -, your current position as X, and where north is up,
    the area you're in might look like this:

    #####
    #.|.#
    #-###
    #.|X#
    #####

    You get the attention of a passing construction Elf and ask for a map. "I don't have time to draw out a map of
    this place - it's huge. Instead, I can give you directions to every room in the facility!" He writes down some
    directions on a piece of parchment and runs off. In the example above, the instructions might have been ^WNE$,
    a regular expression or "regex" (your puzzle input).

    The regex matches routes (like WNE for "west, north, east") that will take you from your current room through
    various doors in the facility. In aggregate, the routes will take you through every door in the facility at
    least once; mapping out all of these routes will let you build a proper map and find your way around.

    ^ and $ are at the beginning and end of your regex; these just mean that the regex doesn't match anything
    outside the routes it describes. (Specifically, ^ matches the start of the route, and $ matches the end of it.)
    These characters will not appear elsewhere in the regex.

    The rest of the regex matches various sequences of the characters N (north), S (south), E (east), and W (west).
    In the example above, ^WNE$ matches only one route, WNE, which means you can move west, then north, then east from
    your current position. Sequences of letters like this always match that exact route in the same order.

    Sometimes, the route can branch. A branch is given by a list of options separated by pipes (|) and wrapped in
    parentheses. So, ^N(E|W)N$ contains a branch: after going north, you must choose to go either east or west before
    finishing your route by going north again. By tracing out the possible routes after branching, you can determine
    where the doors are and, therefore, where the rooms are in the facility.

    For example, consider this regex: ^ENWWW(NEEE|SSE(EE|N))$

    This regex begins with ENWWW, which means that from your current position, all routes must begin by moving east,
    north, and then west three times, in that order. After this, there is a branch. Before you consider the branch,
    this is what you know about the map so far, with doors you aren't sure about marked with a ?:

    #?#?#?#?#
    ?.|.|.|.?
    #?#?#?#-#
        ?X|.?
        #?#?#

    After this point, there is (NEEE|SSE(EE|N)). This gives you exactly two options: NEEE and SSE(EE|N). By
    following NEEE, the map now looks like this:

    #?#?#?#?#
    ?.|.|.|.?
    #-#?#?#?#
    ?.|.|.|.?
    #?#?#?#-#
        ?X|.?
        #?#?#

    Now, only SSE(EE|N) remains. Because it is in the same parenthesized group as NEEE, it starts from the same
    room NEEE started in. It states that starting from that point, there exist doors which will allow you to move
    south twice, then east; this ends up at another branch. After that, you can either move east twice or north
    once. This information fills in the rest of the doors:

    #?#?#?#?#
    ?.|.|.|.?
    #-#?#?#?#
    ?.|.|.|.?
    #-#?#?#-#
    ?.?.?X|.?
    #-#-#?#?#
    ?.|.|.|.?
    #?#?#?#?#

    Once you've followed all possible routes, you know the remaining unknown parts are all walls, producing a
    finished map of the facility:

    #########
    #.|.|.|.#
    #-#######
    #.|.|.|.#
    #-#####-#
    #.#.#X|.#
    #-#-#####
    #.|.|.|.#
    #########

    Sometimes, a list of options can have an empty option, like (NEWS|WNSE|). This means that routes at this point
    could effectively skip the options in parentheses and move on immediately. For example, consider this regex
    and the corresponding map:

    ^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$

    ###########
    #.|.#.|.#.#
    #-###-#-#-#
    #.|.|.#.#.#
    #-#####-#-#
    #.#.#X|.#.#
    #-#-#####-#
    #.#.|.|.|.#
    #-###-###-#
    #.|.|.#.|.#
    ###########

    This regex has one main route which, at three locations, can optionally include additional detours and be
    valid: (NEWS|), (WNSE|), and (SWEN|). Regardless of which option is taken, the route continues from the
    position it is left at after taking those steps. So, for example, this regex matches all of the following
    routes (and more that aren't listed here):

    ENNWSWWSSSEENEENNN
    ENNWSWWNEWSSSSEENEENNN
    ENNWSWWNEWSSSSEENEESWENNNN
    ENNWSWWSSSEENWNSEEENNN

    By following the various routes the regex matches, a full map of all of the doors and rooms in the facility
    can be assembled.

    To get a sense for the size of this facility, you'd like to determine which room is furthest from you:
    specifically, you would like to find the room for which the shortest path to that room would require passing
    through the most doors.

    - In the first example (^WNE$), this would be the north-east corner 3 doors away.
    - In the second example (^ENWWW(NEEE|SSE(EE|N))$), this would be the south-east corner 10 doors away.
    - In the third example (^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$), this would be the north-east corner
      18 doors away.

    Here are a few more examples:

    Regex: ^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
    Furthest room requires passing 23 doors

    #############
    #.|.|.|.|.|.#
    #-#####-###-#
    #.#.|.#.#.#.#
    #-#-###-#-#-#
    #.#.#.|.#.|.#
    #-#-#-#####-#
    #.#.#.#X|.#.#
    #-#-#-###-#-#
    #.|.#.|.#.#.#
    ###-#-###-#-#
    #.|.#.|.|.#.#
    #############

    Regex: ^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
    Furthest room requires passing 31 doors

    ###############
    #.|.|.|.#.|.|.#
    #-###-###-#-#-#
    #.|.#.|.|.#.#.#
    #-#########-#-#
    #.#.|.|.|.|.#.#
    #-#-#########-#
    #.#.#.|X#.|.#.#
    ###-#-###-#-#-#
    #.|.#.#.|.#.|.#
    #-###-#####-###
    #.|.#.|.|.#.#.#
    #-#-#####-#-#-#
    #.#.|.|.|.#.|.#
    ###############

    What is the largest number of doors you would be required to pass through to reach a room? That is, find the room
    for which the shortest path from your starting location to that room would require passing through the most doors;
    what is the fewest doors you can pass through to reach it?
    """
    pass


with open('day_20_input.txt') as fp:
    INPUT = fp.read().strip()


def test_input():
    assert INPUT[0] == '^'
    assert INPUT[-1] == '$'
    assert len(INPUT) == 14258


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Maze:
    def __init__(self, directions):
        self.map = defaultdict(set)
        self.distances = defaultdict(int)

        self.follow_directions(Pt(0, 0), directions)

        self.min_y = None
        self.max_y = None
        self.min_x = None
        self.max_x = None
        self.get_map_dimensions()

    DIRECTIONS = {'N': Pt(0, -1), 'S': Pt(0, 1), 'W': Pt(-1, 0), 'E': Pt(1, 0)}

    def get_map_dimensions(self):
        self.min_y = min(pt.y for pt in self.map.keys())
        self.max_y = max(pt.y for pt in self.map.keys())
        self.min_x = min(pt.x for pt in self.map.keys())
        self.max_x = max(pt.x for pt in self.map.keys())

    def follow_directions(self, pt, directions):
        position_queue = []
        for c in directions:
            if c in self.DIRECTIONS:
                next_pt = pt + self.DIRECTIONS[c]
                self.map[pt].add(next_pt)
                self.map[next_pt].add(pt)  # doors work both ways
                new_dist = self.distances[pt] + 1
                self.distances[next_pt] = min(self.distances[next_pt], new_dist) \
                    if self.distances[next_pt] != 0 else new_dist
                pt = next_pt
            elif c == '(':
                position_queue.append(pt)
            elif c == ')':
                pt = position_queue.pop()  # TODO: I don't understand why this works???
            elif c == '|':
                pt = position_queue[-1]

    def overly_complex_follow_directions(self, pt, directions):
        direction_queue = [(pt, directions)]
        while len(direction_queue) > 0:
            pt, directions = direction_queue.pop()
            if directions.count('(') == 0:
                head, rest = directions, ''
            else:
                head, rest = directions.split('(', 1)

            for c in head:
                if c in self.DIRECTIONS:
                    next_pt = pt + self.DIRECTIONS[c]
                    self.map[pt].add(next_pt)
                    self.map[next_pt].add(pt)  # doors work both ways
                    pt = next_pt

            if len(rest) > 0:
                depth = 1
                pos = 0
                opt_start = 0
                options = []
                while depth > 0:
                    c = rest[pos]
                    if c == '(':
                        depth += 1
                    elif c == ')':
                        if depth == 1:
                            options.append((opt_start, pos))
                            opt_start = pos + 1
                        depth -= 1
                    elif depth == 1 and c == '|':
                        options.append((opt_start, pos))
                        opt_start = pos + 1
                    pos += 1
                for opt_start, opt_end in options:
                    direction_queue.append((pt, f'{rest[opt_start:opt_end]}{rest[pos:]}'))

    def find_shortest_path(self, start, end):
        to_explore = PriorityQueue()
        history = {start}
        to_explore.put((0, start))
        while not to_explore.empty():
            dist, new_pt = to_explore.get()
            if new_pt == end:
                return dist
            for p in self.map[new_pt]:
                if p not in history:
                    to_explore.put((dist + 1, p))
                    history.add(p)
        return -1

    def find_farthest_room(self, start):
        distances = []
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                pt = Pt(x, y)
                if pt != start:
                    distances.append(self.find_shortest_path(start, pt))
        return max(distances)

    def print_map(self):
        result = []
        for y in range(self.min_y, self.max_y + 1):
            walls = ['']
            rooms = ['']
            for x in range(self.min_x, self.max_x + 1):
                walls.append('#')
                pt = Pt(x, y)
                up = Pt(x, y - 1)
                if up in self.map[pt]:
                    walls.append('-')
                else:
                    walls.append('#')
                left = Pt(x - 1, y)
                if left in self.map[pt]:
                    rooms.append('|')
                else:
                    rooms.append('#')
                if pt == Pt(0, 0):
                    rooms.append('X')
                else:
                    rooms.append('.')
            walls.append('#')
            rooms.append('#')
            result.append(''.join(walls))
            result.append(''.join(rooms))
        result.append(result[0])
        return result


def test_sample_maze():
    maze = Maze('^ENWWW(NEEE|SSE(EE|N))$')
    maze_map = maze.print_map()
    # print()
    # print('\n'.join(maze_map))
    assert maze_map == ['#########',
                        '#.|.|.|.#',
                        '#-#######',
                        '#.|.|.|.#',
                        '#-#####-#',
                        '#.#.#X|.#',
                        '#-#-#####',
                        '#.|.|.|.#',
                        '#########']
    assert maze.find_farthest_room(Pt(0, 0)) == 10

    maze = Maze('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')
    maze_map = maze.print_map()
    # print()
    # print('\n'.join(maze_map))
    assert maze_map == ['###########',
                        '#.|.#.|.#.#',
                        '#-###-#-#-#',
                        '#.|.|.#.#.#',
                        '#-#####-#-#',
                        '#.#.#X|.#.#',
                        '#-#-#####-#',
                        '#.#.|.|.|.#',
                        '#-###-###-#',
                        '#.|.|.#.|.#',
                        '###########']
    assert maze.find_farthest_room(Pt(0, 0)) == 18

    maze = Maze('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$')
    assert maze.find_farthest_room(Pt(0, 0)) == 23

    maze = Maze('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$')
    assert maze.find_farthest_room(Pt(0, 0)) == 31


def test_puzzle_maze():
    maze = Maze(INPUT)
    assert max(maze.distances.values()) == 4050
    assert sum(1 for v in maze.distances.values() if v >= 1_000) == 8564