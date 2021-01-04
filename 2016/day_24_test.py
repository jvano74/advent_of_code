from typing import NamedTuple
from queue import PriorityQueue
from collections import defaultdict


class Puzzle:
    """
    --- Day 24: Air Duct Spelunking ---
    You've finally met your match; the doors that provide access to the roof are locked tight, and all of the controls
    and related electronics are inaccessible. You simply can't reach them.

    The robot that cleans the air ducts, however, can.

    It's not a very fast little robot, but you reconfigure it to be able to interface with some of the exposed wires
    that have been routed through the HVAC system. If you can direct it to each of those locations, you should be able
    to bypass the security controls.

    You extract the duct layout for this area from some blueprints you acquired and create a map with the relevant
    locations marked (your puzzle input). 0 is your current location, from which the cleaning robot embarks; the other
    numbers are (in no particular order) the locations the robot needs to visit at least once each. Walls are marked
    as #, and open passages are marked as .. Numbers behave like open passages.

    For example, suppose you have a map like the following:

    ###########
    #0.1.....2#
    #.#######.#
    #4.......3#
    ###########

    To reach all of the points of interest as quickly as possible, you would have the robot take the following path:

    0 to 4 (2 steps)
    4 to 1 (4 steps; it can't move diagonally)
    1 to 2 (6 steps)
    2 to 3 (2 steps)

    Since the robot isn't very fast, you need to find it the shortest route. This path is the fewest steps
    (in the above example, a total of 14) required to start at 0 and then visit every other location at least once.

    Given your actual map, and starting from location 0, what is the fewest number of steps required to visit
    every non-0 number marked on the map at least once?

    --- Part Two ---
    Of course, if you leave the cleaning robot somewhere weird, someone is bound to notice.

    What is the fewest number of steps required to start at 0, visit every non-0 number marked on the map at least
    once, and then return to 0?
    """
    pass


SAMPLE = ['###########',
          '#0.1.....2#',
          '#.#######.#',
          '#4.......3#',
          '###########']


with open('day_24_input.txt') as fp:
    INPUTS = [line.strip() for line in fp]


with open('day_24_simplified_input.txt') as fp:
    S_INPUTS = [line.strip() for line in fp]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Maze:
    def __init__(self, raw_input):
        self.grid = set()
        self.grid_removed = 0
        self.goals = {}
        self.goals_map = defaultdict(lambda: defaultdict(int))
        self.dead_ends = 0
        self.map_trim_iterations = 0
        self.map_dead_ends = 0
        self.map_no_stops = 0
        self.map_loops = 0
        self.map = defaultdict(lambda: defaultdict(int))
        self.max_x = 0
        self.max_y = 0

        for y, line in enumerate(raw_input):
            for x, v in enumerate(line):
                if v != '#' and v != 'x':
                    self.max_x = max(x, self.max_x)
                    self.max_y = max(y, self.max_y)
                    pt = Pt(x, y)
                    self.grid.add(pt)
                    if v != '.':
                        self.goals[pt] = v

    def prune_grid(self):
        modified = True
        while modified:
            modified = False
            to_remove = set()
            for pt in self.grid:
                if pt not in self.goals and len(self.neighbors(pt)) <= 1:
                    to_remove.add(pt)
            if len(to_remove) > 0:
                modified = True
                self.grid_removed += len(to_remove)
                self.grid = self.grid - to_remove

    def print_grid(self, include_goals=False, include_map=False):
        result = []
        for y in range(self.max_y + 2):
            line = []
            for x in range(self.max_x + 2):
                pt = Pt(x, y)
                line.append('.' if pt in self.grid else '#')
                if include_map and pt in self.map:
                    line[-1] = '+'
                if include_goals and pt in self.goals:
                    line[-1] = self.goals[pt]
            result.append(''.join(line))
        return result

    def neighbors(self, pt):
        nbs = set()
        for delta in [Pt(1, 0), Pt(0, -1), Pt(-1, 0), Pt(0, 1)]:
            new_pt = pt + delta
            if new_pt in self.grid:
                nbs.add(new_pt)
        return nbs

    def next_step(self, current_pt, prev_pt):
        choices = self.neighbors(current_pt) - {prev_pt}
        if len(choices) == 1:
            return choices.pop()
        return current_pt

    def build_map(self, trim_map=True):
        first_pass_choices = defaultdict(set)
        for pt in self.grid:
            neighbors = self.neighbors(pt)
            if len(neighbors) > 2 or pt in self.goals:
                first_pass_choices[pt] = first_pass_choices[pt].union(neighbors)
        # now follow first_pass_choices to end
        for pt, neighbors in first_pass_choices.items():
            for current_pt in neighbors:
                prev_pt = pt
                dist = 1
                while current_pt not in first_pass_choices:
                    current_pt, prev_pt = self.next_step(current_pt, prev_pt), current_pt
                    if current_pt == prev_pt:
                        break
                    dist += 1
                if current_pt in first_pass_choices:
                    self.map[pt][current_pt] = dist
                else:
                    self.dead_ends += 1  # skip mapping dead ends
        # points going to dead ends now may just be normal path so we should prune these
        while trim_map:
            self.map_trim_iterations += 1
            trim_map = False
            for pt, neighbors in [t for t in self.map.items()]:
                if pt not in self.goals:
                    if len(neighbors) == 1:
                        self.map.pop(pt)
                        self.map_dead_ends += 1
                        trim_map = True
                    elif len(neighbors) == 2:
                        n = [pt for pt in neighbors]
                        curr_dist = self.map[n[0]][n[1]]
                        dist_via_pt = self.map[pt].pop(n[0]) + self.map[pt].pop(n[1])
                        new_dist = min(curr_dist, dist_via_pt)
                        self.map[n[0]][n[1]] = new_dist
                        self.map[n[1]][n[0]] = new_dist
                        # clear remaining references to pt
                        if pt in self.map[n[0]]:
                            self.map[n[0]].pop(pt)
                        if pt in self.map[n[1]]:
                            self.map[n[1]].pop(pt)
                        self.map.pop(pt)
                        self.map_no_stops += 1
                        trim_map = True
                    elif pt in neighbors:
                        self.map[pt].pop(pt)
                        self.map_loops += 1
                        trim_map = True

    def shortest_dist(self, start, end):
        # return self.shortest_map_dist(start, end)[0]
        return self.shortest_grid_dist(start, end)

    def shortest_grid_dist(self, start, end):
        if start not in self.grid:
            raise Exception(f'Start {start} not in grid')
        if end not in self.grid:
            raise Exception(f'End {end} not in grid')
        boundary = PriorityQueue()
        boundary.put((0, start))
        points_visited = set(start)
        while not boundary.empty():
            moves, pt = boundary.get()
            if pt == end:
                return moves
            for new_pt in self.neighbors(pt):
                if new_pt not in points_visited:
                    points_visited.add(new_pt)
                    boundary.put((moves + 1, new_pt))
        raise Exception(f'Unable to get from {start} to {end}')

    def shortest_map_dist(self, start, end):
        if start not in self.map:
            raise Exception(f'Start {start} not in map')
        if end not in self.map:
            raise Exception(f'End {end} not in map')
        boundary = PriorityQueue()
        boundary.put((0, start, [start]))
        points_visited = set(start)
        while not boundary.empty():
            moves, pt, path = boundary.get()
            if pt == end:
                return moves, path
            for new_pt in self.map[pt]:
                if new_pt not in points_visited:  # previously used not in path
                    points_visited.add(new_pt)
                    new_path = path.copy()
                    new_path.append(new_pt)
                    boundary.put((moves + self.map[pt][new_pt], new_pt, new_path))
        raise Exception(f'Unable to get from {start} to {end}')

    def build_goal_map(self):
        for start_goal, start_goal_id in self.goals.items():
            for end_goal, end_goal_id in self.goals.items():
                if start_goal != end_goal and self.goals_map[start_goal_id][end_goal_id] == 0:
                    goal_dist = self.shortest_dist(start_goal, end_goal)
                    self.goals_map[start_goal_id][end_goal_id] = goal_dist
                    self.goals_map[end_goal_id][start_goal_id] = goal_dist

    def shortest_path_to_goals(self, start, return_to_start=False):
        if start not in self.goals_map:
            raise Exception(f'Start {start} not in goal map')
        boundary = PriorityQueue()
        boundary.put((0, start, [start]))
        while not boundary.empty():
            moves, goal, path = boundary.get()
            if set(path) == set(self.goals.values()) and (goal == start or not return_to_start):
                return moves, path
            for new_goal in self.goals_map[goal]:
                new_path = path.copy()
                new_path.append(new_goal)
                boundary.put((moves + self.goals_map[goal][new_goal], new_goal, new_path))


def test_sample_get_goals():
    sample_maze = Maze(SAMPLE)
    # print()
    # print('\n'.join(sample_maze.print_grid(include_goals=True)))
    sample_maze.build_map()
    sample_maze.build_goal_map()
    assert len(sample_maze.grid) == 20
    assert len(sample_maze.goals) == 5
    assert sample_maze.dead_ends == 0
    assert sample_maze.map[Pt(1, 1)][Pt(1, 3)] == 2
    assert sample_maze.map[Pt(9, 1)][Pt(3, 1)] == 6
    assert sample_maze.shortest_dist(Pt(9, 1), Pt(1, 3)) == (10, [Pt(x=9, y=1), Pt(x=9, y=3), Pt(x=1, y=3)])
    assert sample_maze.shortest_path_to_goals('0') == (14, ['0', '4', '0', '1', '2', '3'])


def test_puzzle_get_goals():
    puzzle_maze = Maze(INPUTS)
    # puzzle_maze = Maze(S_INPUTS)
    check_stats = False
    print_puzzle = False

    if check_stats:
        assert len(puzzle_maze.grid) == 3833
        assert len(puzzle_maze.goals) == 8

    puzzle_maze.prune_grid()
    if check_stats:
        assert len(puzzle_maze.grid) == 3091
        assert puzzle_maze.grid_removed == 3833 - 3091
        assert len(puzzle_maze.goals) == 8

    puzzle_maze.build_map()
    if check_stats:
        assert puzzle_maze.dead_ends == 0  # without pruning was 193
        assert puzzle_maze.map_dead_ends == 6  # without pruning was 28
        assert puzzle_maze.map_no_stops == 80  # without pruning was 190
        assert puzzle_maze.map_loops == 2  # without pruning was 1
        assert puzzle_maze.map_trim_iterations == 4
        assert len(puzzle_maze.map) == 612  # 630  # nodes, down from 845 without trimming

    puzzle_maze.build_goal_map()

    if print_puzzle:
        print()
        print('\n'.join(puzzle_maze.print_grid(include_goals=True, include_map=True)))

    assert puzzle_maze.shortest_path_to_goals('0') == (502, ['0', '1', '7', '6', '3', '2', '4', '5'])
    # Looks like I was making things way too complicated...
    assert puzzle_maze.shortest_path_to_goals('0', return_to_start=True) == (724, ['0', '1', '7', '6',
                                                                                   '3', '2', '5', '4', '0'])
