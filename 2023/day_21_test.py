from typing import NamedTuple


class Puzzle:
    """
    --- Day 21: Step Counter ---
    You manage to catch the airship right as it's dropping someone else off on
    their all-expenses-paid trip to Desert Island! It even helpfully drops you
    off near the gardener and his massive farm.

    "You got the sand flowing again! Great work! Now we just need to wait until
    we have enough sand to filter the water for Snow Island and we'll have snow
    again in no time."

    While you wait, one of the Elves that works with the gardener heard how good
    you are at solving problems and would like your help. He needs to get his
    steps in for the day, and so he'd like to know which garden plots he can
    reach with exactly his remaining 64 steps.

    He gives you an up-to-date map (your puzzle input) of his starting position
    (S), garden plots (.), and rocks (#). For example:

    ...........
    .....###.#.
    .###.##..#.
    ..#.#...#..
    ....#.#....
    .##..S####.
    .##..#...#.
    .......##..
    .##.#.####.
    .##..##.##.
    ...........

    The Elf starts at the starting position (S) which also counts as a garden
    plot. Then, he can take one step north, south, east, or west, but only onto
    tiles that are garden plots. This would allow him to reach any of the tiles
    marked O:

    ...........
    .....###.#.
    .###.##..#.
    ..#.#...#..
    ....#O#....
    .##.OS####.
    .##..#...#.
    .......##..
    .##.#.####.
    .##..##.##.
    ...........

    Then, he takes a second step. Since at this point he could be at either tile
    marked O, his second step would allow him to reach any garden plot that is
    one step north, south, east, or west of any tile that he could have reached
    after the first step:

    ...........
    .....###.#.
    .###.##..#.
    ..#.#O..#..
    ....#.#....
    .##O.O####.
    .##.O#...#.
    .......##..
    .##.#.####.
    .##..##.##.
    ...........

    After two steps, he could be at any of the tiles marked O above, including
    the starting position (either by going north-then-south or by going
    west-then-east).

    A single third step leads to even more possibilities:

    ...........
    .....###.#.
    .###.##..#.
    ..#.#.O.#..
    ...O#O#....
    .##.OS####.
    .##O.#...#.
    ....O..##..
    .##.#.####.
    .##..##.##.
    ...........

    He will continue like this until his steps for the day have been exhausted.
    After a total of 6 steps, he could reach any of the garden plots marked O:

    ...........
    .....###.#.
    .###.##.O#.
    .O#O#O.O#..
    O.O.#.#.O..
    .##O.O####.
    .##.O#O..#.
    .O.O.O.##..
    .##.#.####.
    .##O.##.##.
    ...........

    In this example, if the Elf's goal was to get exactly 6 more steps today, he
    could use them to reach any of 16 garden plots.

    However, the Elf actually needs to get 64 steps today, and the map he's
    handed you is much larger than the example map.

    Starting from the garden plot marked S on your map, how many garden plots
    could the Elf reach in exactly 64 steps?

    Your puzzle answer was 3746.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The Elf seems confused by your answer until he realizes his mistake: he was
    reading from a list of his favorite numbers that are both perfect squares
    and perfect cubes, not his step counter.

    The actual number of steps he needs to get today is exactly 26501365.

    He also points out that the garden plots and rocks are set up so that the
    map repeats infinitely in every direction.

    So, if you were to look one additional map-width or map-height out from the
    edge of the example map above, you would find that it keeps repeating:

    .................................
    .....###.#......###.#......###.#.
    .###.##..#..###.##..#..###.##..#.
    ..#.#...#....#.#...#....#.#...#..
    ....#.#........#.#........#.#....
    .##...####..##...####..##...####.
    .##..#...#..##..#...#..##..#...#.
    .......##.........##.........##..
    .##.#.####..##.#.####..##.#.####.
    .##..##.##..##..##.##..##..##.##.
    .................................
    .................................
    .....###.#......###.#......###.#.
    .###.##..#..###.##..#..###.##..#.
    ..#.#...#....#.#...#....#.#...#..
    ....#.#........#.#........#.#....
    .##...####..##..S####..##...####.
    .##..#...#..##..#...#..##..#...#.
    .......##.........##.........##..
    .##.#.####..##.#.####..##.#.####.
    .##..##.##..##..##.##..##..##.##.
    .................................
    .................................
    .....###.#......###.#......###.#.
    .###.##..#..###.##..#..###.##..#.
    ..#.#...#....#.#...#....#.#...#..
    ....#.#........#.#........#.#....
    .##...####..##...####..##...####.
    .##..#...#..##..#...#..##..#...#.
    .......##.........##.........##..
    .##.#.####..##.#.####..##.#.####.
    .##..##.##..##..##.##..##..##.##.
    .................................

    This is just a tiny three-map-by-three-map slice of the
    inexplicably-infinite farm layout; garden plots and rocks repeat as far as
    you can see. The Elf still starts on the one middle tile marked S, though -
    every other repeated S is replaced with a normal garden plot (.).

    Here are the number of reachable garden plots in this new infinite version
    of the example map for different numbers of steps:

    In exactly 6 steps, he can still reach 16 garden plots.
    In exactly 10 steps, he can reach any of 50 garden plots.
    In exactly 50 steps, he can reach 1594 garden plots.
    In exactly 100 steps, he can reach 6536 garden plots.
    In exactly 500 steps, he can reach 167004 garden plots.
    In exactly 1000 steps, he can reach 668697 garden plots.
    In exactly 5000 steps, he can reach 16733044 garden plots.

    However, the step count the Elf needs is much larger! Starting from the
    garden plot marked S on your infinite map, how many garden plots could the
    Elf reach in exactly 26501365 steps?

    Your puzzle answer was 623540829615589.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open("day_21_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")

SAMPLE = [
    "...........",
    ".....###.#.",
    ".###.##..#.",
    "..#.#...#..",
    "....#.#....",
    ".##..S####.",
    ".##..#...#.",
    ".......##..",
    ".##.#.####.",
    ".##..##.##.",
    "...........",
]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def neighbors(self):
        return {
            Pt(self.x + 1, self.y + 0),
            Pt(self.x + 0, self.y + 1),
            Pt(self.x - 1, self.y + 0),
            Pt(self.x + 0, self.y - 1),
        }


class Garden:
    def __init__(self, raw_map) -> None:
        self.map = set()
        self.x_max = 0
        self.y_max = 0
        for y, raw_row in enumerate(raw_map):
            self.y_max = max(y, self.x_max)
            for x, c in enumerate(raw_row):
                self.x_max = max(x, self.x_max)
                pt = Pt(x, y)
                if c == "#":
                    self.map.add(pt)
                elif c == "S":
                    self.start = pt

    def step_range(
        self, generations=1, boundary=None, finite_board=True, fit_count=False
    ):
        if boundary is None:
            boundary = {
                self.start,
            }
        counts = [0]
        even_odd = [boundary, set()]
        for n in range(generations):
            new_boundary = set()
            for pt in boundary:
                for nbh in pt.neighbors():
                    if finite_board and (
                        nbh.x < 0
                        or nbh.y < 0
                        or self.x_max < nbh.x
                        or self.x_max < nbh.x
                    ):
                        continue
                    nbh_mod = Pt(nbh.x % (self.x_max + 1), nbh.y % (self.y_max + 1))
                    if nbh_mod not in self.map and nbh not in even_odd[(n + 1) % 2]:
                        new_boundary.add(nbh)
                        even_odd[(n + 1) % 2].add(nbh)
            boundary = new_boundary
            counts.append(len(even_odd[(n + 1) % 2]))
        if fit_count:
            return counts
        return len(even_odd[generations % 2])


def extrapolate_second_diff(x, dx, y, dy, second_diff, number_of_cycles):
    for _ in range(number_of_cycles):
        x += dx
        dy += second_diff
        y += dy
    return x, y, dy


def test_garden():
    # part 1
    sample = Garden(SAMPLE)
    count = sample.step_range(6)
    assert count == 16

    my_garden = Garden(RAW_INPUT)
    count = my_garden.step_range(64)
    assert count == 3746

    # part 2
    for steps, expected in [
        (6, 16),
        (10, 50),
        (50, 1594),
        (100, 6536),
        # (500, 167004),
        # (1000, 668697),
        # (5000, 16733044),
    ]:
        count = sample.step_range(steps, finite_board=False)
        # print(f"{steps=} {count} == {expected}")
        assert count == expected

    TOTAL_STEPS = 26501365
    # In order to get to the this total step count we will need
    # to somehow optimize
    #
    # If there were no obstacles the count would grow as a quadratic function
    # so we start checking if there is a quadratic growth if we take steps
    # in multiples of the grid size (don't forget that length is +1 since x_min,
    # y_min start at 0)
    # print(f"{my_garden.x_max+1=} {my_garden.y_max+1=}")
    GRID_SIZE = my_garden.x_max + 1
    STARTING_OFFSET = TOTAL_STEPS % GRID_SIZE

    steps = 1000
    count_fit = my_garden.step_range(steps, finite_board=False, fit_count=True)

    # print("i, count_fit[i], delta -> delta-old_delta")
    # old_delta = 0
    # for i in range(STARTING_OFFSET, steps, GRID_SIZE):
    #     delta = count_fit[i] - count_fit[i - GRID_SIZE]
    #     print(f"{i}, {count_fit[i]}, {delta} -> {delta-old_delta}")
    #     old_delta = delta
    # looks like the 2nd delta is constant at 469 every 131 steps, lets check with correct initial offset
    SECOND_DIFF = 30472
    # print(f"{extrapolate_second_diff(327, GRID_SIZE, 95591, 61087, 30472, 1)=}")
    # print(f"{extrapolate_second_diff(327, GRID_SIZE, 95591, 61087, 30472, 2)=}")
    # print(f"{extrapolate_second_diff(327, GRID_SIZE, 95591, 61087, 30472, 3)=}")
    ITERATIONS = (TOTAL_STEPS - 327) // GRID_SIZE
    TOTAL_PLOTS = extrapolate_second_diff(
        327, GRID_SIZE, 95591, 61087, SECOND_DIFF, ITERATIONS
    )
    # print(f"{TOTAL_PLOTS=}")
    assert TOTAL_PLOTS[1] == 623540829615589
