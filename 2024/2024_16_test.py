from queue import PriorityQueue
from pathlib import Path
from typing import NamedTuple


class Puzzle:
    """
    --- Day 16: Reindeer Maze ---
    It's time again for the Reindeer Olympics! This year, the big event is the
    Reindeer Maze, where the Reindeer compete for the lowest score.

    You and The Historians arrive to search for the Chief right as the event is
    about to start. It wouldn't hurt to watch a little, right?

    The Reindeer start on the Start Tile (marked S) facing East and need to
    reach the End Tile (marked E). They can move forward one tile at a time
    (increasing their score by 1 point), but never into a wall (#). They can
    also rotate clockwise or counterclockwise 90 degrees at a time (increasing
    their score by 1000 points).

    To figure out the best place to sit, you start by grabbing a map (your
    puzzle input) from a nearby kiosk. For example:

    ###############
    #.......#....E#
    #.#.###.#.###.#
    #.....#.#...#.#
    #.###.#####.#.#
    #.#.#.......#.#
    #.#.#####.###.#
    #...........#.#
    ###.#.#####.#.#
    #...#.....#.#.#
    #.#.#.###.#.#.#
    #.....#...#.#.#
    #.###.#.#.#.#.#
    #S..#.....#...#
    ###############

    There are many paths through this maze, but taking any of the best paths
    would incur a score of only 7036. This can be achieved by taking a total of
    36 steps forward and turning 90 degrees a total of 7 times:


    ###############
    #.......#....E#
    #.#.###.#.###^#
    #.....#.#...#^#
    #.###.#####.#^#
    #.#.#.......#^#
    #.#.#####.###^#
    #..>>>>>>>>v#^#
    ###^#.#####v#^#
    #>>^#.....#v#^#
    #^#.#.###.#v#^#
    #^....#...#v#^#
    #^###.#.#.#v#^#
    #S..#.....#>>^#
    ###############

    Here's a second example:

    #################
    #...#...#...#..E#
    #.#.#.#.#.#.#.#.#
    #.#.#.#...#...#.#
    #.#.#.#.###.#.#.#
    #...#.#.#.....#.#
    #.#.#.#.#.#####.#
    #.#...#.#.#.....#
    #.#.#####.#.###.#
    #.#.#.......#...#
    #.#.###.#####.###
    #.#.#...#.....#.#
    #.#.#.#####.###.#
    #.#.#.........#.#
    #.#.#.#########.#
    #S#.............#
    #################

    In this maze, the best paths cost 11048 points; following one such path
    would look like this:

    #################
    #...#...#...#..E#
    #.#.#.#.#.#.#.#^#
    #.#.#.#...#...#^#
    #.#.#.#.###.#.#^#
    #>>v#.#.#.....#^#
    #^#v#.#.#.#####^#
    #^#v..#.#.#>>>>^#
    #^#v#####.#^###.#
    #^#v#..>>>>^#...#
    #^#v###^#####.###
    #^#v#>>^#.....#.#
    #^#v#^#####.###.#
    #^#v#^........#.#
    #^#v#^#########.#
    #S#>>^..........#
    #################

    Note that the path shown above includes one 90 degree turn as the very first
    move, rotating the Reindeer from facing East to facing North.

    Analyze your map carefully. What is the lowest score a Reindeer could
    possibly get?

    Your puzzle answer was 106512.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    Now that you know what the best paths look like, you can figure out the best
    spot to sit.

    Every non-wall tile (S, ., or E) is equipped with places to sit along the
    edges of the tile. While determining which of these tiles would be the best
    spot to sit depends on a whole bunch of factors (how comfortable the seats
    are, how far away the bathrooms are, whether there's a pillar blocking your
    view, etc.), the most important factor is whether the tile is on one of the
    best paths through the maze. If you sit somewhere else, you'd miss all the
    action!

    So, you'll need to determine which tiles are part of any best path through
    the maze, including the S and E tiles.

    In the first example, there are 45 tiles (marked O) that are part of at
    least one of the various best paths through the maze:

    ###############
    #.......#....O#
    #.#.###.#.###O#
    #.....#.#...#O#
    #.###.#####.#O#
    #.#.#.......#O#
    #.#.#####.###O#
    #..OOOOOOOOO#O#
    ###O#O#####O#O#
    #OOO#O....#O#O#
    #O#O#O###.#O#O#
    #OOOOO#...#O#O#
    #O###.#.#.#O#O#
    #O..#.....#OOO#
    ###############

    In the second example, there are 64 tiles that are part of at least one of
    the best paths:

    #################
    #...#...#...#..O#
    #.#.#.#.#.#.#.#O#
    #.#.#.#...#...#O#
    #.#.#.#.###.#.#O#
    #OOO#.#.#.....#O#
    #O#O#.#.#.#####O#
    #O#O..#.#.#OOOOO#
    #O#O#####.#O###O#
    #O#O#..OOOOO#OOO#
    #O#O###O#####O###
    #O#O#OOO#..OOO#.#
    #O#O#O#####O###.#
    #O#O#OOOOOOO..#.#
    #O#O#O#########.#
    #O#OOO..........#
    #################

    Analyze your map further. How many tiles are part of at least one of the
    best paths through the maze?

    Your puzzle answer was 563.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


SAMPLE_MAP = [
    "###############",
    "#.......#....E#",
    "#.#.###.#.###.#",
    "#.....#.#...#.#",
    "#.###.#####.#.#",
    "#.#.#.......#.#",
    "#.#.#####.###.#",
    "#...........#.#",
    "###.#.#####.#.#",
    "#...#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.....#...#.#.#",
    "#.###.#.#.#.#.#",
    "#S..#.....#...#",
    "###############",
]

with open(Path(__file__).parent / "2024_16_input.txt") as fp:
    MY_MAP = fp.read().split("\n")


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def nbhd(self):
        return {self + Pt(-1, 0), self + Pt(1, 0), self + Pt(0, -1), self + Pt(0, 1)}


class Pos(NamedTuple):
    pt: Pt
    direction: str

    def step(self):
        return Pos(self.pt + DIRECTIONS[self.direction], self.direction)

    def nbhd(self):
        return (
            (1, Pos(self.pt + DIRECTIONS[self.direction], self.direction)),
            (1000, Pos(self.pt, CW_ROTATION[self.direction])),
            (1000, Pos(self.pt, CCW_ROTATION[self.direction])),
        )


DIRECTIONS = {
    "^": Pt(0, -1),
    ">": Pt(1, 0),
    "<": Pt(-1, 0),
    "v": Pt(0, 1),
}

CW_ROTATION = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",
}

CCW_ROTATION = {
    "^": "<",
    "<": "v",
    "v": ">",
    ">": "^",
}


class ReindeerMaze:
    def __init__(self, raw_map, prune_dead_ends=False):
        self.walls = set()
        self.x_max = 0
        self.y_max = 0

        for y, raw_line in enumerate(raw_map):
            self.y_max = max(y, self.y_max)
            for x, c in enumerate(raw_line):
                self.x_max = max(x, self.x_max)
                match c:
                    case "S":
                        self.start = Pt(x, y)
                        self.start_dir = ">"
                    case "E":
                        self.end = Pt(x, y)
                    case "#":
                        self.walls.add(Pt(x, y))

        if prune_dead_ends:
            self.dead_ends = set()
            self.paths = set()
            self.junctions = set()
            for y in range(self.y_max + 1):
                for x in range(self.x_max + 1):
                    pt = Pt(x, y)
                    if pt == self.start:
                        continue
                    if pt == self.end:
                        continue
                    if pt in self.walls:
                        continue
                    nbhd = len(pt.nbhd() & self.walls)
                    if nbhd <= 1:
                        self.junctions.add(pt)
                    elif nbhd == 2:
                        self.paths.add(pt)
                    elif nbhd == 3:
                        self.dead_ends.add(pt)
            pruning = self.dead_ends.copy()
            while pruning:
                dead_end = pruning.pop()
                new_dead_ends = dead_end.nbhd() & self.paths
                self.paths -= new_dead_ends
                self.dead_ends |= new_dead_ends
                pruning |= new_dead_ends

            self.walls |= self.dead_ends

    def display(self, good_seats=None):
        if good_seats is None:
            good_seats = set()

        for y in range(self.y_max + 1):
            raw_line = []
            for x in range(self.x_max + 1):
                pt = Pt(x, y)
                if pt in good_seats:
                    raw_line.append("O")
                elif pt == self.start:
                    raw_line.append("S")
                elif pt == self.end:
                    raw_line.append("E")
                elif pt in self.walls:
                    raw_line.append("#")
                else:
                    raw_line.append(".")
            print("".join(raw_line))

    def navigate(self, max_score=None, find_all=False):
        boundary = PriorityQueue()

        starting_state = Pos(pt=self.start, direction=self.start_dir)
        history = {starting_state: 0}
        boundary.put((0, starting_state, [starting_state]))

        successful_paths = []

        while boundary:
            score, current_state, path = boundary.get()

            if max_score is not None:
                if score > max_score:
                    break
                delta = current_state.pt - self.end
                min_possible = (
                    score
                    + abs(delta.x)
                    + abs(delta.y)
                    + (0 if delta.x == 0 or delta.y == 0 else 1000)
                )
                if min_possible > max_score:
                    continue

            if current_state.pt == self.end:
                if find_all:
                    max_score = score
                    successful_paths.append(path)
                    continue
                return score
            for move_cost, new_state in current_state.nbhd():
                if new_state.pt in self.walls:
                    continue
                if new_state in path:
                    continue
                if new_state in history and not find_all:
                    continue

                new_score = score + move_cost
                if new_state in history and new_score > history[new_state]:
                    continue

                new_path = path[:]
                new_path.append(new_state)
                boundary.put((new_score, new_state, new_path))
                history[new_state] = new_score

        good_seats = set()
        good_seats.add(self.end)
        for route in successful_paths:
            for step in route:
                good_seats.add(step.pt)
        # self.display(good_seats)
        return len(good_seats)


LARGER_MAP = [
    "#################",
    "#...#...#...#..E#",
    "#.#.#.#.#.#.#.#^#",
    "#.#.#.#...#...#^#",
    "#.#.#.#.###.#.#^#",
    "#>>v#.#.#.....#^#",
    "#^#v#.#.#.#####^#",
    "#^#v..#.#.#>>>>^#",
    "#^#v#####.#^###.#",
    "#^#v#..>>>>^#...#",
    "#^#v###^#####.###",
    "#^#v#>>^#.....#.#",
    "#^#v#^#####.###.#",
    "#^#v#^........#.#",
    "#^#v#^#########.#",
    "#S#>>^..........#",
    "#################",
]


def test_part_1():
    sample_maze = ReindeerMaze(SAMPLE_MAP)
    assert sample_maze.navigate() == 7036
    larger_maze = ReindeerMaze(LARGER_MAP)
    assert larger_maze.navigate() == 11048


def test_my_part_1():
    my_maze = ReindeerMaze(MY_MAP)
    assert my_maze.navigate() == 106512


def test_part_2():
    sample_maze = ReindeerMaze(SAMPLE_MAP, prune_dead_ends=True)
    assert sample_maze.navigate(find_all=True) == 45
    larger_maze = ReindeerMaze(LARGER_MAP, prune_dead_ends=True)
    assert larger_maze.navigate(find_all=True) == 64


def test_my_part_2():
    my_maze = ReindeerMaze(MY_MAP, prune_dead_ends=True)
    my_maze.display()
    assert my_maze.navigate(find_all=True) == 563
