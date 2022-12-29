from __future__ import annotations
from heapq import heappush, heappop
from typing import NamedTuple, Set
from collections import defaultdict


class Puzzle:
    """
    --- Day 24: Blizzard Basin ---
    With everything replanted for next year (and with elephants and monkeys to
    tend the grove), you and the Elves leave for the extraction point.

    Partway up the mountain that shields the grove is a flat, open area that
    serves as the extraction point. It's a bit of a climb, but nothing the
    expedition can't handle.

    At least, that would normally be true; now that the mountain is covered in
    snow, things have become more difficult than the Elves are used to.

    As the expedition reaches a valley that must be traversed to reach the
    extraction site, you find that strong, turbulent winds are pushing small
    blizzards of snow and sharp ice around the valley. It's a good thing
    everyone packed warm clothes! To make it across safely, you'll need to find
    a way to avoid them.

    Fortunately, it's easy to see all of this from the entrance to the valley,
    so you make a map of the valley and the blizzards (your puzzle input). For
    example:

    #.#####
    #.....#
    #>....#
    #.....#
    #...v.#
    #.....#
    #####.#

    The walls of the valley are drawn as #; everything else is ground. Clear
    ground - where there is currently no blizzard - is drawn as .. Otherwise,
    blizzards are drawn with an arrow indicating their direction of motion: up
    (^), down (v), left (<), or right (>).

    The above map includes two blizzards, one moving right (>) and one moving
    down (v). In one minute, each blizzard moves one position in the direction
    it is pointing:

    #.#####
    #.....#
    #.>...#
    #.....#
    #.....#
    #...v.#
    #####.#

    Due to conservation of blizzard energy, as a blizzard reaches the wall of
    the valley, a new blizzard forms on the opposite side of the valley moving
    in the same direction. After another minute, the bottom downward-moving
    blizzard has been replaced with a new downward-moving blizzard at the top of
    the valley instead:

    #.#####
    #...v.#
    #..>..#
    #.....#
    #.....#
    #.....#
    #####.#

    Because blizzards are made of tiny snowflakes, they pass right through each
    other. After another minute, both blizzards temporarily occupy the same
    position, marked 2:

    #.#####
    #.....#
    #...2.#
    #.....#
    #.....#
    #.....#
    #####.#

    After another minute, the situation resolves itself, giving each blizzard
    back its personal space:

    #.#####
    #.....#
    #....>#
    #...v.#
    #.....#
    #.....#
    #####.#

    Finally, after yet another minute, the rightward-facing blizzard on the
    right is replaced with a new one on the left facing the same direction:

    #.#####
    #.....#
    #>....#
    #.....#
    #...v.#
    #.....#
    #####.#

    This process repeats at least as long as you are observing it, but probably
    forever.

    Here is a more complex example:

    #.######
    #>>.<^<#
    #.<..<<#
    #>v.><>#
    #<^v^^>#
    ######.#

    Your expedition begins in the only non-wall position in the top row and
    needs to reach the only non-wall position in the bottom row. On each minute,
    you can move up, down, left, or right, or you can wait in place. You and the
    blizzards act simultaneously, and you cannot share a position with a
    blizzard.

    In the above example, the fastest way to reach your goal requires 18 steps.
    Drawing the position of the expedition as E, one way to achieve this is:

    Initial state:
    #E######
    #>>.<^<#
    #.<..<<#
    #>v.><>#
    #<^v^^>#
    ######.#

    Minute 1, move down:
    #.######
    #E>3.<.#
    #<..<<.#
    #>2.22.#
    #>v..^<#
    ######.#

    Minute 2, move down:
    #.######
    #.2>2..#
    #E^22^<#
    #.>2.^>#
    #.>..<.#
    ######.#

    Minute 3, wait:
    #.######
    #<^<22.#
    #E2<.2.#
    #><2>..#
    #..><..#
    ######.#

    Minute 4, move up:
    #.######
    #E<..22#
    #<<.<..#
    #<2.>>.#
    #.^22^.#
    ######.#

    Minute 5, move right:
    #.######
    #2Ev.<>#
    #<.<..<#
    #.^>^22#
    #.2..2.#
    ######.#

    Minute 6, move right:
    #.######
    #>2E<.<#
    #.2v^2<#
    #>..>2>#
    #<....>#
    ######.#

    Minute 7, move down:
    #.######
    #.22^2.#
    #<vE<2.#
    #>>v<>.#
    #>....<#
    ######.#

    Minute 8, move left:
    #.######
    #.<>2^.#
    #.E<<.<#
    #.22..>#
    #.2v^2.#
    ######.#

    Minute 9, move up:
    #.######
    #<E2>>.#
    #.<<.<.#
    #>2>2^.#
    #.v><^.#
    ######.#

    Minute 10, move right:
    #.######
    #.2E.>2#
    #<2v2^.#
    #<>.>2.#
    #..<>..#
    ######.#

    Minute 11, wait:
    #.######
    #2^E^2>#
    #<v<.^<#
    #..2.>2#
    #.<..>.#
    ######.#

    Minute 12, move down:
    #.######
    #>>.<^<#
    #.<E.<<#
    #>v.><>#
    #<^v^^>#
    ######.#

    Minute 13, move down:
    #.######
    #.>3.<.#
    #<..<<.#
    #>2E22.#
    #>v..^<#
    ######.#

    Minute 14, move right:
    #.######
    #.2>2..#
    #.^22^<#
    #.>2E^>#
    #.>..<.#
    ######.#

    Minute 15, move right:
    #.######
    #<^<22.#
    #.2<.2.#
    #><2>E.#
    #..><..#
    ######.#

    Minute 16, move right:
    #.######
    #.<..22#
    #<<.<..#
    #<2.>>E#
    #.^22^.#
    ######.#

    Minute 17, move down:
    #.######
    #2.v.<>#
    #<.<..<#
    #.^>^22#
    #.2..2E#
    ######.#

    Minute 18, move down:
    #.######
    #>2.<.<#
    #.2v^2<#
    #>..>2>#
    #<....>#
    ######E#

    What is the fewest number of minutes required to avoid the blizzards and
    reach the goal?

    Your puzzle answer was 225.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    As the expedition reaches the far side of the valley, one of the Elves looks
    especially dismayed:

    He forgot his snacks at the entrance to the valley!

    Since you're so good at dodging blizzards, the Elves humbly request that you
    go back for his snacks. From the same initial conditions, how quickly can
    you make it from the start to the goal, then back to the start, then back to
    the goal?

    In the above example, the first trip to the goal takes 18 minutes, the trip
    back to the start takes 23 minutes, and the trip back to the goal again
    takes 13 minutes, for a total time of 54 minutes.

    What is the fewest number of minutes required to reach the goal, go back to
    the start, then reach the goal again?

    Your puzzle answer was 711.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


SAMPLE_MAP = [
    "#.######",
    "#>>.<^<#",
    "#.<..<<#",
    "#>v.><>#",
    "#<^v^^>#",
    "######.#",
]

with open("day_24_input.txt") as fp:
    MY_MAP = [line.strip() for line in fp]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Pt) -> Pt:
        return Pt(x=self.x + other.x, y=self.y + other.y)

    def __neg__(self) -> Pt:
        return Pt(x=-self.x, y=-self.y)

    def __sub__(self, other: Pt) -> Pt:
        return Pt(x=self.x - other.x, y=self.y - other.y)

    def nbhd(self) -> Set[Pt]:
        return {
            self,
            self + Pt(0, -1),
            self + Pt(0, 1),
            self + Pt(-1, 0),
            self + Pt(1, 0),
        }


class T(NamedTuple):
    pos: Pt
    time: int


class State(NamedTuple):
    pos: Pt
    board: int

    def dist_to_goal(self, goal: Pt):
        return abs(self.pos.x - goal.x) + abs(self.pos.y - goal.y)

    def priority(self, time: int, goal: Pt):
        return (time, self.dist_to_goal(goal=goal))

    @staticmethod
    def create(time: int, pos: Pt, max_t: int) -> State:
        return State(pos=pos, board=time % max_t)

    def next_moves(self, storms, max_t: int):
        next_board = (self.board + 1) % max_t
        return [
            State(pos=p, board=next_board)
            for p in self.pos.nbhd()
            if T(pos=p, time=next_board) not in storms
        ]


class BlizzardBasin:
    def __init__(self, map) -> None:
        self.max_x = len(map[0]) - 2
        self.max_y = len(map) - 2
        self.max_t = self.max_x * self.max_y

        self.start = Pt(0, -1)
        self.end = Pt(self.max_x - 1, self.max_y)

        storms = defaultdict(list)
        for t in range(self.max_t):
            storms[T(pos=Pt(0, -2), time=t)].append("#")
        for y, row in enumerate(map):
            for x, c in enumerate(row):
                match c:
                    case "#":
                        for t in range(self.max_t):
                            storms[T(pos=Pt(x - 1, y - 1), time=t)].append("#")
                    case ">":
                        for t in range(self.max_t):
                            storms[
                                T(pos=Pt((x - 1 + t) % self.max_x, y - 1), time=t)
                            ].append(">")
                    case "<":
                        for t in range(self.max_t):
                            storms[
                                T(pos=Pt((x - 1 - t) % self.max_x, y - 1), time=t)
                            ].append("<")
                    case "^":
                        for t in range(self.max_t):
                            storms[
                                T(pos=Pt(x - 1, (y - 1 - t) % self.max_y), time=t)
                            ].append("^")
                    case "v":
                        for t in range(self.max_t):
                            storms[
                                T(pos=Pt(x - 1, (y - 1 + t) % self.max_y), time=t)
                            ].append("v")
                    case ".":
                        pass
        self.storms = dict(storms)

    def display(self, state):
        grid = []
        for y in range(-1, self.max_y + 1):
            line = []
            for x in range(-1, self.max_x + 1):
                stpt = T(pos=Pt(x, y), time=state.board)
                c = "."
                if stpt.pos == state.pos:
                    c = "E"
                if stpt.pos == self.end:
                    c = "x"
                if stpt in self.storms:
                    stm = self.storms[stpt]
                    nc = stm[0] if len(stm) == 1 else f"{len(stm)}"
                    c = nc if c == "." else "X"
                line.append(c)
            grid.append("".join(line))
        return grid

    def find_shortest_time(
        self,
        time=0,
        start_pt=None,
        goal=None,
        track_path=False,
        print_status=False,
        print_freq=100_000,
    ):
        if start_pt is None:
            start_pt = self.start

        if goal is None:
            goal = self.end

        state = State.create(time=time, pos=start_pt, max_t=self.max_t)
        priority = state.priority(time=time, goal=goal)
        if track_path:
            path = [state]
        else:
            path = None

        history = set()
        exploring = []
        heappush(exploring, (priority, state, path))

        steps = 0
        while exploring:
            priority, state, path = heappop(exploring)
            time = priority[0]

            if print_status and steps % print_freq == 0:
                print(f"steps={steps} priority={priority} exploring={len(exploring)}")
            steps += 1

            if state in history:
                continue
            history.add(state)

            if state.pos == goal:
                return time, path

            for next_state in state.next_moves(storms=self.storms, max_t=self.max_t):
                if track_path:
                    next_path = path[:]
                    next_path.append(next_state)
                else:
                    next_path = None
                priority = next_state.priority(time=time + 1, goal=goal)
                heappush(exploring, (priority, next_state, next_path))
        raise Exception("Can't get there")

    def find_shortest_loop_back_time(self):
        time = 0
        time, _ = self.find_shortest_time(time=time, start_pt=self.start, goal=self.end)
        print(f"first finish {time}")
        # head back
        time, _ = self.find_shortest_time(time=time, start_pt=self.end, goal=self.start)
        print(f"first return {time}")
        # and out
        time, _ = self.find_shortest_time(time=time, start_pt=self.start, goal=self.end)
        print(f"second finish {time}")
        return time


def test_sample_blizzard():
    sample = BlizzardBasin(SAMPLE_MAP)
    min_time, min_path = sample.find_shortest_time(track_path=True)
    # print(min_path)
    # for state in min_path:
    #     print(state)
    #     print("\n".join(sample.display(state)))
    assert min_time == 18
    min_time = sample.find_shortest_loop_back_time()
    assert min_time == 54


def test_my_blizzard():
    my_blizzard = BlizzardBasin(MY_MAP)
    min_time, _ = my_blizzard.find_shortest_time()
    assert min_time == 225
    min_time = my_blizzard.find_shortest_loop_back_time()
    # assert min_time == 469
    # 469 is too low, had bug with correctly replacing self.end with goal
    assert min_time == 711


if __name__ == "__main__":
    my_blizzard = BlizzardBasin(MY_MAP)
    # min_time, _ = my_blizzard.find_shortest_time(print_status=True)
    min_time = my_blizzard.find_shortest_loop_back_time()
    print(f"min_time={min_time}")
