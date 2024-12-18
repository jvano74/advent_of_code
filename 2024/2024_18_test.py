from pathlib import Path
from queue import PriorityQueue
from typing import NamedTuple


class Puzzle:
    """
    --- Day 18: RAM Run ---
    You and The Historians look a lot more pixelated than you remember. You're
    inside a computer at the North Pole!

    Just as you're about to check out your surroundings, a program runs up to
    you. "This region of memory isn't safe! The User misunderstood what a
    pushdown automaton is and their algorithm is pushing whole bytes down on top
    of us! Run!"

    The algorithm is fast - it's going to cause a byte to fall into your memory
    space once every nanosecond! Fortunately, you're faster, and by quickly
    scanning the algorithm, you create a list of which bytes will fall (your
    puzzle input) in the order they'll land in your memory space.

    Your memory space is a two-dimensional grid with coordinates that range from
    0 to 70 both horizontally and vertically. However, for the sake of example,
    suppose you're on a smaller grid with coordinates that range from 0 to 6 and
    the following list of incoming byte positions:

    5,4
    4,2
    4,5
    3,0
    2,1
    6,3
    2,4
    1,5
    0,6
    3,3
    2,6
    5,1
    1,2
    5,5
    2,5
    6,5
    1,4
    0,4
    6,4
    1,1
    6,1
    1,0
    0,5
    1,6
    2,0

    Each byte position is given as an X,Y coordinate, where X is the distance
    from the left edge of your memory space and Y is the distance from the top
    edge of your memory space.

    You and The Historians are currently in the top left corner of the memory
    space (at 0,0) and need to reach the exit in the bottom right corner (at
    70,70 in your memory space, but at 6,6 in this example). You'll need to
    simulate the falling bytes to plan out where it will be safe to run; for
    now, simulate just the first few bytes falling into your memory space.

    As bytes fall into your memory space, they make that coordinate corrupted.
    Corrupted memory coordinates cannot be entered by you or The Historians, so
    you'll need to plan your route carefully. You also cannot leave the
    boundaries of the memory space; your only hope is to reach the exit.

    In the above example, if you were to draw the memory space after the first
    12 bytes have fallen (using . for safe and # for corrupted), it would look
    like this:

    ...#...
    ..#..#.
    ....#..
    ...#..#
    ..#..#.
    .#..#..
    #.#....

    You can take steps up, down, left, or right. After just 12 bytes have
    corrupted locations in your memory space, the shortest path from the top
    left corner to the exit would take 22 steps. Here (marked with O) is one
    such path:

    OO.#OOO
    .O#OO#O
    .OOO#OO
    ...#OO#
    ..#OO#.
    .#.O#..
    #.#OOOO

    Simulate the first kilobyte (1024 bytes) falling onto your memory space.
    Afterward, what is the minimum number of steps needed to reach the exit?

    Your puzzle answer was 284.

    --- Part Two ---
    The Historians aren't as used to moving around in this pixelated universe as
    you are. You're afraid they're not going to be fast enough to make it to the
    exit before the path is completely blocked.

    To determine how fast everyone needs to go, you need to determine the first
    byte that will cut off the path to the exit.

    In the above example, after the byte at 1,1 falls, there is still a path to
    the exit:

    O..#OOO
    O##OO#O
    O#OO#OO
    OOO#OO#
    ###OO##
    .##O###
    #.#OOOO

    However, after adding the very next byte (at 6,1), there is no longer a path
    to the exit:

    ...#...
    .##..##
    .#..#..
    ...#..#
    ###..##
    .##.###
    #.#....

    So, in this example, the coordinates of the first byte that prevents the
    exit from being reachable are 6,1.

    Simulate more of the bytes that are about to corrupt your memory space. What
    are the coordinates of the first byte that will prevent the exit from being
    reachable from your starting position? (Provide the answer as two integers
    separated by a comma with no other characters.)

    Your puzzle answer was 51,50.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


SAMPLE = [
    (5, 4),
    (4, 2),
    (4, 5),
    (3, 0),
    (2, 1),
    (6, 3),
    (2, 4),
    (1, 5),
    (0, 6),
    (3, 3),
    (2, 6),
    (5, 1),
    (1, 2),
    (5, 5),
    (2, 5),
    (6, 5),
    (1, 4),
    (0, 4),
    (6, 4),
    (1, 1),
    (6, 1),
    (1, 0),
    (0, 5),
    (1, 6),
    (2, 0),
]

with open(Path(__file__).parent / "2024_18_input.txt") as fp:
    MY_SAMPLE = [
        (int(a), int(b)) for (a, b) in [ln.split(",") for ln in fp.read().split("\n")]
    ]


def test_my_sample():
    assert MY_SAMPLE[:5] == [(67, 61), (15, 16), (11, 26), (39, 1), (3, 27)]
    assert MY_SAMPLE[-5:] == [(46, 25), (28, 38), (18, 66), (2, 11), (39, 4)]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def dist_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def nbhd(self):
        return {self + Pt(-1, 0), self + Pt(1, 0), self + Pt(0, -1), self + Pt(0, 1)}


class Memory:
    def __init__(self, corrupted_bytes, size=70):
        self.max_wall = size
        self.corrupted_bytes = dict()
        for time, (x, y) in enumerate(corrupted_bytes):
            self.corrupted_bytes[Pt(x, y)] = time + 1

    def min_path(self, fixed_time=1024):
        target = Pt(self.max_wall, self.max_wall)

        boundary = PriorityQueue()

        starting_state = Pt(0, 0)
        history = {starting_state: 0}
        boundary.put((0, 0, starting_state, [starting_state]))

        while not boundary.empty():
            _, steps, current_state, path = boundary.get()

            if current_state == target:
                return steps

            for new_state in current_state.nbhd():
                if (
                    new_state.x < 0
                    or new_state.x > self.max_wall
                    or new_state.y < 0
                    or new_state.y > self.max_wall
                ):
                    continue
                if new_state in self.corrupted_bytes and self.corrupted_bytes[
                    new_state
                ] < (fixed_time + 1):
                    continue
                if new_state in path:
                    continue
                if new_state in history:
                    continue

                new_path = path[:]
                new_path.append(new_state)
                boundary.put(
                    (steps + target.dist_to(new_state), steps + 1, new_state, new_path)
                )
                history[new_state] = steps

        return -1

    def find_max_fixed_time(self):
        min_dropped = 0
        max_dropped = len(self.corrupted_bytes)

        while True:
            mid_time = (min_dropped + max_dropped) // 2
            steps_to_pass = self.min_path(fixed_time=mid_time)
            if steps_to_pass == -1:
                max_dropped = mid_time
            else:
                min_dropped = mid_time
            if min_dropped + 1 == max_dropped:
                return [
                    pt
                    for pt, time in self.corrupted_bytes.items()
                    if time == max_dropped
                ][0]


def test_memory_samples():
    sample_memory = Memory(SAMPLE, size=6)
    assert sample_memory.min_path(fixed_time=100) == -1
    assert sample_memory.min_path(fixed_time=12) == 22
    assert sample_memory.find_max_fixed_time() == Pt(6, 1)


def test_my_memory():
    assert len(MY_SAMPLE) == 3450
    my_memory = Memory(MY_SAMPLE)
    assert my_memory.min_path(fixed_time=1024) == 284
    assert my_memory.find_max_fixed_time() == Pt(x=51, y=50)
