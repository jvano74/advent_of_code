class Puzzle:
    """--- Day 13: Point of Incidence ---
    With your help, the hot springs team locates an appropriate spring which
    launches you neatly and precisely up to the edge of Lava Island.

    There's just one problem: you don't see any lava.

    You do see a lot of ash and igneous rock; there are even what look like gray
    mountains scattered around. After a while, you make your way to a nearby
    cluster of mountains only to discover that the valley between them is
    completely full of large mirrors. Most of the mirrors seem to be aligned in
    a consistent way; perhaps you should head in that direction?

    As you move through the valley of mirrors, you find that several of them
    have fallen from the large metal frames keeping them in place. The mirrors
    are extremely flat and shiny, and many of the fallen mirrors have lodged
    into the ash at strange angles. Because the terrain is all one color, it's
    hard to tell where it's safe to walk or where you're about to run into a
    mirror.

    You note down the patterns of ash (.) and rocks (#) that you see as you walk
    (your puzzle input); perhaps by carefully analyzing these patterns, you can
    figure out where the mirrors are!

    For example:

    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.

    #...##..#
    #....#..#
    ..##..###
    #####.##.
    #####.##.
    ..##..###
    #....#..#

    To find the reflection in each pattern, you need to find a perfect
    reflection across either a horizontal line between two rows or across a
    vertical line between two columns.

    In the first pattern, the reflection is across a vertical line between two
    columns; arrows on each of the two columns point at the line between the
    columns:

    123456789
        ><
    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.
        ><
    123456789

    In this pattern, the line of reflection is the vertical line between columns
    5 and 6. Because the vertical line is not perfectly in the middle of the
    pattern, part of the pattern (column 1) has nowhere to reflect onto and can
    be ignored; every other column has a reflected column within the pattern and
    must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches
    7, and 5 matches 6.

    The second pattern reflects across a horizontal line instead:

    1 #...##..# 1
    2 #....#..# 2
    3 ..##..### 3
    4v#####.##.v4
    5^#####.##.^5
    6 ..##..### 6
    7 #....#..# 7

    This pattern reflects across the horizontal line between rows 4 and 5. Row 1
    would reflect with a hypothetical row 8, but since that's not in the
    pattern, row 1 doesn't need to match anything. The remaining rows match: row
    2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

    To summarize your pattern notes, add up the number of columns to the left of
    each vertical line of reflection; to that, also add 100 multiplied by the
    number of rows above each horizontal line of reflection. In the above
    example, the first pattern's vertical line has 5 columns to its left and the
    second pattern's horizontal line has 4 rows above it, a total of 405.

    Find the line of reflection in each of the patterns in your notes. What
    number do you get after summarizing all of your notes?

    """


with open("day_13_input.txt") as fp:
    RAW_INPUT = [
        [raw_line for raw_line in raw_block.split("\n")]
        for raw_block in fp.read().split("\n\n")
    ]

SAMPLE_1 = [
    "#.##..##.",
    "..#.##.#.",
    "##......#",
    "##......#",
    "..#.##.#.",
    "..##..##.",
    "#.#.##.#.",
]

SAMPLE_2 = [
    "#...##..#",
    "#....#..#",
    "..##..###",
    "#####.##.",
    "#####.##.",
    "..##..###",
    "#....#..#",
]


def convolution(sequence):
    n = len(sequence)
    for offset in range(n):
        left = offset
        right = n - 1
        while sequence[left] == sequence[right]:
            if left == n - 1:
                return 0
            if not (left < right):
                return left
            left += 1
            right -= 1


def calc_symetry(raw_map):
    col_counts = [0] * len(raw_map[0])
    row_counts = []
    for y, raw_line in enumerate(raw_map):
        row_count = 0
        for x, c in enumerate(raw_line):
            if c == "#":
                row_count += 2**x
                col_counts[x] += 2**y
        row_counts.append(row_count)
    return convolution(col_counts) + 100 * convolution(row_counts)


class Rocks:
    def __init__(self, raw_map) -> None:
        self.col_counts = [0] * len(raw_map[0])
        self.row_counts = []
        for y, raw_line in enumerate(raw_map):
            row_count = 0
            for x, c in enumerate(raw_line):
                if c == "#":
                    row_count += 2**x
                    self.col_counts[x] += 2**y
            self.row_counts.append(row_count)

    def score(self):
        return convolution(self.col_counts) + 100 * convolution(self.row_counts)


def test_rocks():
    sample_1 = Rocks(SAMPLE_1)
    assert sample_1.score() == 5
    assert calc_symetry(SAMPLE_1) == 5
    sample_2 = Rocks(SAMPLE_2)
    assert sample_2.score() == 400
    assert calc_symetry(SAMPLE_2) == 400
    print()


test_rocks()
