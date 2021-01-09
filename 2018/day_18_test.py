from typing import NamedTuple


class Puzzle:
    """
    --- Day 18: Settlers of The North Pole ---
    On the outskirts of the North Pole base construction project, many Elves are collecting lumber.

    The lumber collection area is 50 acres by 50 acres; each acre can be either open ground (.), trees (|), or a
    lumberyard (#). You take a scan of the area (your puzzle input).

    Strange magic is at work here: each minute, the landscape looks entirely different. In exactly one minute, an open
    acre can fill with trees, a wooded acre can be converted to a lumberyard, or a lumberyard can be cleared to open
    ground (the lumber having been sent to other projects).

    The change to each acre is based entirely on the contents of that acre as well as the number of open, wooded, or
    lumberyard acres adjacent to it at the start of each minute. Here, "adjacent" means any of the eight acres
    surrounding that acre. (Acres on the edges of the lumber collection area might have fewer than eight adjacent
    acres; the missing acres aren't counted.)

    In particular:

    - An open acre will become filled with trees if three or more adjacent acres contained trees.
      Otherwise, nothing happens.
    - An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards.
      Otherwise, nothing happens.
    - An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard
      and at least one acre containing trees. Otherwise, it becomes open.

    These changes happen across all acres simultaneously, each of them using the state of all acres at the beginning
    of the minute and changing to their new form by the end of that same minute. Changes that happen during the
    minute don't affect each other.

    For example, suppose the lumber collection area is instead only 10 by 10 acres with this initial configuration:

    Initial state:
    .#.#...|#.
    .....#|##|
    .|..|...#.
    ..|#.....#
    #.#|||#|#|
    ...#.||...
    .|....|...
    ||...#|.#|
    |.||||..|.
    ...#.|..|.

    After 1 minute:
    .......##.
    ......|###
    .|..|...#.
    ..|#||...#
    ..##||.|#|
    ...#||||..
    ||...|||..
    |||||.||.|
    ||||||||||
    ....||..|.

    After 2 minutes:
    .......#..
    ......|#..
    .|.|||....
    ..##|||..#
    ..###|||#|
    ...#|||||.
    |||||||||.
    ||||||||||
    ||||||||||
    .|||||||||

    After 3 minutes:
    .......#..
    ....|||#..
    .|.||||...
    ..###|||.#
    ...##|||#|
    .||##|||||
    ||||||||||
    ||||||||||
    ||||||||||
    ||||||||||

    After 4 minutes:
    .....|.#..
    ...||||#..
    .|.#||||..
    ..###||||#
    ...###||#|
    |||##|||||
    ||||||||||
    ||||||||||
    ||||||||||
    ||||||||||

    After 5 minutes:
    ....|||#..
    ...||||#..
    .|.##||||.
    ..####|||#
    .|.###||#|
    |||###||||
    ||||||||||
    ||||||||||
    ||||||||||
    ||||||||||

    After 6 minutes:
    ...||||#..
    ...||||#..
    .|.###|||.
    ..#.##|||#
    |||#.##|#|
    |||###||||
    ||||#|||||
    ||||||||||
    ||||||||||
    ||||||||||

    After 7 minutes:
    ...||||#..
    ..||#|##..
    .|.####||.
    ||#..##||#
    ||##.##|#|
    |||####|||
    |||###||||
    ||||||||||
    ||||||||||
    ||||||||||

    After 8 minutes:
    ..||||##..
    ..|#####..
    |||#####|.
    ||#...##|#
    ||##..###|
    ||##.###||
    |||####|||
    ||||#|||||
    ||||||||||
    ||||||||||

    After 9 minutes:
    ..||###...
    .||#####..
    ||##...##.
    ||#....###
    |##....##|
    ||##..###|
    ||######||
    |||###||||
    ||||||||||
    ||||||||||

    After 10 minutes:
    .||##.....
    ||###.....
    ||##......
    |##.....##
    |##.....##
    |##....##|
    ||##.####|
    ||#####|||
    ||||#|||||
    ||||||||||

    After 10 minutes, there are 37 wooded acres and 31 lumberyards. Multiplying the number of wooded acres by the
    number of lumberyards gives the total resource value after ten minutes: 37 * 31 = 1147.

    What will the total resource value of the lumber collection area be after 10 minutes?

    --- Part Two ---
    This important natural resource will need to last for at least thousands of years. Are the Elves collecting
    this lumber sustainably?

    What will the total resource value of the lumber collection area be after 1_000_000_000 minutes?
    """
    pass


with open('day_18_input.txt') as fp:
    INPUTS = [ln.strip() for ln in fp]


def test_input():
    assert len(INPUTS[0]) == 50
    assert INPUTS[0].count('|') == 10
    assert INPUTS[0].count('#') == 4
    assert INPUTS[0].count('.') == 36


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Forest:
    def __init__(self, raw_map, track_hx=True):
        self.track_hx = track_hx
        self.hx = {}
        self.time = 0
        self.map = {}
        self.max_x = 0
        self.max_y = len(raw_map)
        for y, line in enumerate(raw_map):
            self.max_x = max(self.max_x, len(line))
            for x, c in enumerate(line):
                self.map[Pt(x, y)] = c

    def print_map(self, to_screen=True):
        results = []
        for y in range(self.max_y):
            line = []
            for x in range(self.max_x):
                line.append(self.map[Pt(x, y)])
            results.append(''.join(line))
        if to_screen:
            print()
            print(f'After {self.time} minutes:')
            print('\n'.join(results))
        return results

    def neighbors(self, pt):
        results = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                new_pt = pt + Pt(x, y)
                if new_pt in self.map and new_pt != pt:
                    results.append(self.map[new_pt])
        return results

    def tick(self):
        new_map = {}
        for pt, val in self.map.items():
            nbs = self.neighbors(pt)
            if val == '.':
                new_map[pt] = '|' if nbs.count('|') >= 3 else '.'
            elif val == '|':
                new_map[pt] = '#' if nbs.count('#') >= 3 else '|'
            elif val == '#':
                new_map[pt] = '#' if nbs.count('#') >= 1 and nbs.count('|') >= 1 else '.'
        self.time += 1
        if self.track_hx:
            state = '/'.join(self.print_map(to_screen=False))
            if state in self.hx:
                return 1, f'at t={self.time} looped back to t={self.hx[state]}'
            else:
                self.hx[state] = self.time
        if self.map == new_map:
            return 1
        self.map = new_map
        return 0

    def run_till(self, max_time):
        while True:
            if self.time >= max_time:
                return self.time, self.resource_value()
            result = self.tick()
            if result != 0:
                return result

    def resource_value(self):
        number_wooded = sum(1 for v in self.map.values() if v == '|')
        number_lumberyards = sum(1 for v in self.map.values() if v == '#')
        return number_wooded * number_lumberyards


SAMPLE = ['.#.#...|#.',
          '.....#|##|',
          '.|..|...#.',
          '..|#.....#',
          '#.#|||#|#|',
          '...#.||...',
          '.|....|...',
          '||...#|.#|',
          '|.||||..|.',
          '...#.|..|.']


def test_forest():
    forest = Forest(SAMPLE)
    # forest.print_map()
    for _ in range(10):
        forest.tick()
        # forest.print_map()
    assert forest.resource_value() == 1147


def test_puzzle_forest():
    forest = Forest(INPUTS)
    # forest.print_map()
    for _ in range(10):
        forest.tick()
        # forest.print_map()
    assert forest.resource_value() == 486878


def test_puzzle_forest2():
    forest = Forest(INPUTS, track_hx=True)
    find_loop = False
    if find_loop:
        result = forest.run_till(1_000)  # want to get to 1_000_000_000
        assert result == (1, 'at t=526 looped back to t=498')
    period = 526 - 498
    offset = (1_000_000_000 - 498) % 28
    assert period == 28
    assert offset == 26
    result = forest.run_till(498 + 26)  # should be same as at 1_000_000_000
    assert result == (524, 190836)
