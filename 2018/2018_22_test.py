from typing import NamedTuple
from queue import PriorityQueue


class Puzzle:
    """
    --- Day 22: Mode Maze ---
    This is it, your final stop: the year -483. It's snowing and dark outside; the only light you can see is coming
    from a small cottage in the distance. You make your way there and knock on the door.

    A portly man with a large, white beard answers the door and invites you inside. For someone living near the North
    Pole in -483, he must not get many visitors, but he doesn't act surprised to see you. Instead, he offers you some
    milk and cookies.

    After talking for a while, he asks a favor of you. His friend hasn't come back in a few hours, and he's not sure
    where he is. Scanning the region briefly, you discover one life signal in a cave system nearby; his friend must
    have taken shelter there. The man asks if you can go there to retrieve his friend.

    The cave is divided into square regions which are either dominantly rocky, narrow, or wet (called its type). Each
    region occupies exactly one coordinate in X,Y format where X and Y are integers and zero or greater. (Adjacent
    regions can be the same type.)

    The scan (your puzzle input) is not very detailed: it only reveals the depth of the cave system and the
    coordinates of the target. However, it does not reveal the type of each region. The mouth of the cave is at 0,0.

    The man explains that due to the unusual geology in the area, there is a method to determine any region's type
    based on its erosion level. The erosion level of a region can be determined from its geologic index. The geologic
    index can be determined using the first rule that applies from the list below:

    - The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    - The region at the coordinates of the target has a geologic index of 0.
    - If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    - If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    - Otherwise, the region's geologic index is the result of multiplying the erosion levels of the regions
      at X-1,Y and X,Y-1.

    A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183. Then:

    - If the erosion level modulo 3 is 0, the region's type is rocky.
    - If the erosion level modulo 3 is 1, the region's type is wet.
    - If the erosion level modulo 3 is 2, the region's type is narrow.

    For example, suppose the cave system's depth is 510 and the target's coordinates are 10,10. Using % to represent
    the modulo operator, the cavern would look as follows:

    - At 0,0, the geologic index is 0. The erosion level is (0 + 510) % 20183 = 510.
      The type is 510 % 3 = 0, rocky.
    - At 1,0, because the Y coordinate is 0, the geologic index is 1 * 16807 = 16807.
      The erosion level is (16807 + 510) % 20183 = 17317. The type is 17317 % 3 = 1, wet.
    - At 0,1, because the X coordinate is 0, the geologic index is 1 * 48271 = 48271.
      The erosion level is (48271 + 510) % 20183 = 8415. The type is 8415 % 3 = 0, rocky.
    - At 1,1, neither coordinate is 0 and it is not the coordinate of the target, so the geologic index is
      the erosion level of 0,1 (8415) times the erosion level of 1,0 (17317), 8415 * 17317 = 145722555.
      The erosion level is (145722555 + 510) % 20183 = 1805. The type is 1805 % 3 = 2, narrow.
    - At 10,10, because they are the target's coordinates, the geologic index is 0.
      The erosion level is (0 + 510) % 20183 = 510. The type is 510 % 3 = 0, rocky.

    Drawing this same cave system with rocky as ., wet as =, narrow as |, the mouth as M, the target as T, with 0,0
    in the top-left corner, X increasing to the right, and Y increasing downward,
    the top-left corner of the map looks like this:

    M=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Before you go in, you should determine the risk level of the area. For the rectangle that has a top-left corner
    of region 0,0 and a bottom-right corner of the region containing the target, add up the risk level of each
    individual region: 0 for rocky regions, 1 for wet regions, and 2 for narrow regions.

    In the cave system above, because the mouth is at 0,0 and the target is at 10,10, adding up the risk level of all
    regions with an X coordinate from 0 to 10 and a Y coordinate from 0 to 10, this total is 114.

    What is the total risk level for the smallest rectangle that includes 0,0 and the target's coordinates?

    --- Part Two ---
    Okay, it's time to go rescue the man's friend.

    As you leave, he hands you some tools: a torch and some climbing gear. You can't equip both tools at once, but
    you can choose to use neither.

    Tools can only be used in certain regions:

    - In rocky regions, you can use the climbing gear or the torch.
      You cannot use neither (you'll likely slip and fall).

    - In wet regions, you can use the climbing gear or neither tool.
      You cannot use the torch (if it gets wet, you won't have a light source).

    - In narrow regions, you can use the torch or neither tool.
      You cannot use the climbing gear (it's too bulky to fit).

    You start at 0,0 (the mouth of the cave) with the torch equipped and must reach the target coordinates as
    quickly as possible. The regions with negative X or Y are solid rock and cannot be traversed. The fastest
    route might involve entering regions beyond the X or Y coordinate of the target.

    You can move to an adjacent region (up, down, left, or right; never diagonally) if your currently equipped
    tool allows you to enter that region. Moving to an adjacent region takes one minute. (For example, if you
    have the torch equipped, you can move between rocky and narrow regions, but cannot enter wet regions.)

    You can change your currently equipped tool or put both away if your new equipment would be valid for
    your current region. Switching to using the climbing gear, torch, or neither always takes seven minutes,
    regardless of which tools you start with. (For example, if you are in a rocky region, you can switch from
    the torch to the climbing gear, but you cannot switch to neither.)

    Finally, once you reach the target, you need the torch equipped before you can find him in the dark. The
    target is always in a rocky region, so if you arrive there with climbing gear equipped, you will need to
    spend seven minutes switching to your torch.

    For example, using the same cave system as above, starting in the top left corner (0,0) and moving to the
    bottom right corner (the target, 10,10) as quickly as possible, one possible route is as follows, with
    your current position marked X:

    Initially:
    X=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Down:
    M=.|=.|.|=.|=|=.
    X|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Right:
    M=.|=.|.|=.|=|=.
    .X=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Switch from using the torch to neither tool:
    M=.|=.|.|=.|=|=.
    .X=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Right 3:
    M=.|=.|.|=.|=|=.
    .|=|X|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Switch from using neither tool to the climbing gear:
    M=.|=.|.|=.|=|=.
    .|=|X|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Down 7:
    M=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..X==..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Right:
    M=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..=X=..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Down 3:
    M=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||.X.|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Right:
    M=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||..X|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Down:
    M=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.X..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Right 4:
    M=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===T===||
    =|||...|==..|=.|
    =.=|=.=..=X||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Up 2:
    M=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===X===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||

    Switch from using the climbing gear to the torch:
    M=.|=.|.|=.|=|=.
    .|=|=|||..|.=...
    .==|....||=..|==
    =.|....|.==.|==.
    =|..==...=.|==..
    =||.=.=||=|=..|=
    |.=.===|||..=..|
    |..==||=.|==|===
    .=..===..=|.|||.
    .======|||=|=.|=
    .===|=|===X===||
    =|||...|==..|=.|
    =.=|=.=..=.||==|
    ||=|=...|==.=|==
    |=.=||===.|||===
    ||.|==.|.|.||=||
    This is tied with other routes as the fastest way to reach the target: 45 minutes. In it, 21 minutes are spent
    switching tools (three times, seven minutes each) and the remaining 24 minutes are spent moving.

    What is the fewest number of minutes you can take to reach the target?

    --------------
    puzzle inputs:

    depth: 8103
    target: 9,758
    """
    pass


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class State(NamedTuple):
    loc: Pt
    equipped: str

    def move(self, delta):
        return 1, State(loc=(self.loc + delta), equipped=self.equipped)

    def change_equip(self, new_item):
        return 7, State(loc=self.loc, equipped=new_item)

    def min_time_distance(self, other):
        min_additional_steps = self.loc.distance(other.loc)
        min_change_time = 0 if self.equipped == other.equipped else 7
        return min_additional_steps + min_change_time


class Cave:
    def __init__(self, depth, target_pt, grid_size):
        self.depth = depth
        self.target_pt = target_pt
        self.grid_size = grid_size
        self.geologic_index = {Pt(0, 0): 0, target_pt: 0}
        for y in range(0, grid_size.y):
            self.geologic_index[Pt(0, y)] = 48271 * y
        for x in range(0, grid_size.x):
            self.geologic_index[Pt(x, 0)] = 16807 * x
        for y in range(1, grid_size.y):
            for x in range(1, grid_size.x):
                pt = Pt(x, y)
                if pt not in self.geologic_index:
                    el_1 = self.erosion_level(pt + Pt(-1, 0))
                    el_2 = self.erosion_level(pt + Pt(0, -1))
                    self.geologic_index[pt] = el_1 * el_2

    def erosion_level(self, pt):
        return (self.geologic_index[pt] + self.depth) % 20183

    def type(self, pt):
        el_mod_3 = self.erosion_level(pt) % 3
        if el_mod_3 == 0:
            return '.'
        if el_mod_3 == 1:
            return '='
        if el_mod_3 == 2:
            return '|'

    def print_cave(self, min_pt, max_pt, as_map=False):
        result = []
        cave_map = {}
        for y in range(min_pt.y, max_pt.y):
            line = []
            for x in range(min_pt.x, max_pt.x):
                pt = Pt(x, y)
                cave_map[pt] = self.type(pt)
                if pt == Pt(0, 0):
                    line.append('M')
                elif pt == self.target_pt:
                    line.append('T')
                else:
                    line.append(self.type(pt))
            result.append(''.join(line))
        if as_map:
            return cave_map
        return result

    def risk_level(self, min_pt, max_pt):
        risk = 0
        for y in range(min_pt.y, max_pt.y + 1):
            for x in range(min_pt.x, max_pt.x + 1):
                pt = Pt(x, y)
                risk += self.erosion_level(pt) % 3
        return risk


class ExploreCave:
    def __init__(self, cave_map, target_pt, start_pt=None):
        """
        Cave map is dict of loc with value equal to type
        """
        self.map = cave_map
        self.target_pt = target_pt

        if start_pt is None:
            self.start_pt = Pt(0, 0)
        else:
            self.start_pt = start_pt

        max_x = max(pt.x for pt in cave_map)
        max_y = max(pt.x for pt in cave_map)
        self.map_size = Pt(max_x + 1, max_y + 1)

    def print_cave(self, min_pt, max_pt, route=None):
        if route is not None:
            path = {s.loc for s in route}
        else:
            path = set()
        path_taken = {'.': '*', '=': '-', '|': '!'}

        result = []
        for y in range(min_pt.y, max_pt.y):
            line = []
            for x in range(min_pt.x, max_pt.x):
                pt = Pt(x, y)
                if pt == self.start_pt:
                    line.append('M')
                elif pt == self.target_pt:
                    line.append('T')
                else:
                    line.append(self.map[pt])
                    if pt in path:
                        line[-1] = path_taken[line[-1]]
            result.append(''.join(line))
        return result

    #    Recap of types : . rock, = wet, | narrow
    safe_states = {('T', '.'), ('T', '|'),  # T = torch
                   ('G', '.'), ('G', '='),  # G = climbing gear
                   ('N', '|'), ('N', '=')}  # N = neither

    safe_gear_transitions = {('.', 'T'): 'G', ('.', 'G'): 'T',
                             ('|', 'T'): 'N', ('|', 'N'): 'T',
                             ('=', 'G'): 'N', ('=', 'N'): 'G'}

    def get_neighbors(self, state, search_grid):
        """
        returns list of (additional_time, new_state)
        """
        neighbors = []

        current_loc = state.loc
        current_equip = state.equipped
        current_type = self.map[current_loc]

        new_gear = self.safe_gear_transitions[(current_type, current_equip)]
        neighbors.append(state.change_equip(new_gear))

        for direction in [Pt(1, 0), Pt(-1, 0), Pt(0, 1), Pt(0, -1)]:
            potential_loc = current_loc + direction
            if 0 <= potential_loc.x < search_grid.x and 0 <= potential_loc.y < search_grid.y:
                potential_type = self.map[potential_loc]
                if (current_equip, potential_type) in self.safe_states:
                    neighbors.append(state.move(direction))

        return neighbors

    def navigate(self, search_area=None, max_time=None):
        if search_area is None:
            search_area = self.map_size
        starting_state = State(loc=self.start_pt, equipped='T')
        target_state = State(loc=self.target_pt, equipped='T')
        boundary = PriorityQueue()
        boundary.put((0, starting_state, [starting_state]))
        history = {starting_state}
        while not boundary.empty():
            duration, current_state, path = boundary.get()
            if current_state == target_state:
                return duration, path
            for delta_t, new_state in self.get_neighbors(current_state, search_area):
                new_duration = duration + delta_t
                if new_state in history:
                    pass  # already been here, no value returning
                elif new_state in path:
                    pass  # already been here, no value returning
                elif max_time is not None and new_duration + target_state.min_time_distance(new_state) > max_time:
                    pass  # too far behind, not able to finish by max_time so prune
                else:
                    new_path = path[:]
                    new_path.append(new_state)
                    boundary.put((new_duration, new_state, new_path))
                    if delta_t == 1:  # if == 7 might get here faster via a different path
                        history.add(new_state)
        return -1, []


def test_cave():
    sample_cave = Cave(510, Pt(10, 10), Pt(16, 16))
    print()
    print('\n'.join(sample_cave.print_cave(Pt(0, 0), Pt(16, 16))))
    assert sample_cave.risk_level(Pt(0, 0), Pt(10, 10)) == 114
    explore = ExploreCave(sample_cave.print_cave(Pt(0, 0), Pt(16, 16), as_map=True), Pt(10, 10))
    time, route = explore.navigate()
    assert time == 45


def test_puzzle_cave():
    """
    depth: 8103
    target: 9, 758
    """
    cave_map_min = Pt(x=0, y=0)
    cave_map_max = Pt(x=1500, y=1500)
    depth = 8103
    target = Pt(x=9, y=758)

    puzzle_cave = Cave(depth, target, cave_map_max)
    assert puzzle_cave.risk_level(cave_map_min, target) == 7743

    explore = ExploreCave(puzzle_cave.print_cave(cave_map_min, cave_map_max, as_map=True), target)

    # note min time would be 9 + 758 = 767 w/o equipment changes but can't go that fast

    time, route = explore.navigate(search_area=Pt(x=10, y=800))
    assert time == 1107
    # with limited grid size of 10, 800 we can get to target in 1107
    # if we expand the area we may be able to speed up

    # using above time and adding a max_time to prune growth of search tree
    time, route = explore.navigate(search_area=Pt(x=1200, y=1200), max_time=1107)

    # route_max_x = max(s.loc.x for s in route)
    # route_max_y = max(s.loc.y for s in route)
    # print()
    # print('\n'.join(explore.print_cave(Pt(0, 0), Pt(route_max_x + 1, route_max_y + 2), route)))
    # print()
    # print(route)
    # equipment_changes = sum(1 if route[t-1].equipped != s.equipped else 0 for t, s in enumerate(route) if t > 0)
    # assert equipment_changes == 8
    # assert len(route) - 8 == (9 + 758) + 221

    assert route[-1] == State(loc=target, equipped='T')
    assert time == 1029  # finally the right answer...
    # Main bug that was in code was adding points to history to prune visiting too soon - namely when adding
    # a longer +7 min equipment changes this ended up pruning a shorter path to this point.
