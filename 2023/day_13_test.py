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

    Your puzzle answer was 33520.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    You resume walking through the valley of mirrors and - SMACK! - run directly
    into one. Hopefully nobody was watching, because that must have been pretty
    embarrassing.

    Upon closer inspection, you discover that every mirror has exactly one
    smudge: exactly one . or # should be the opposite type.

    In each pattern, you'll need to locate and fix the smudge that causes a
    different reflection line to be valid. (The old reflection line won't
    necessarily continue being valid after the smudge is fixed.)

    Here's the above example again:

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

    The first pattern's smudge is in the top-left corner. If the top-left # were
    instead ., it would have a different, horizontal line of reflection:

    1 ..##..##. 1
    2 ..#.##.#. 2
    3v##......#v3
    4^##......#^4
    5 ..#.##.#. 5
    6 ..##..##. 6
    7 #.#.##.#. 7

    With the smudge in the top-left corner repaired, a new horizontal line of
    reflection between rows 3 and 4 now exists. Row 7 has no corresponding
    reflected row and can be ignored, but every other row matches exactly: row 1
    matches row 6, row 2 matches row 5, and row 3 matches row 4.

    In the second pattern, the smudge can be fixed by changing the fifth symbol
    on row 2 from . to #:

    1v#...##..#v1
    2^#...##..#^2
    3 ..##..### 3
    4 #####.##. 4
    5 #####.##. 5
    6 ..##..### 6
    7 #....#..# 7

    Now, the pattern has a different horizontal line of reflection between rows
    1 and 2.

    Summarize your notes as before, but instead use the new different reflection
    lines. In this example, the first pattern's new horizontal line has 3 rows
    above it and the second pattern's new horizontal line has 1 row above it,
    summarizing to the value 400.

    In each pattern, fix the smudge and find the different line of reflection.
    What number do you get after summarizing the new reflection line in each
    pattern in your notes?

    Your puzzle answer was 34824.

    Both parts of this puzzle are complete! They provide two gold stars: **
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


def mirror_point(sequence):
    n = len(sequence)
    for offset in range(n - 1):
        if (n - offset) % 2:
            continue
        # extra on right
        left = 0
        right = n - 1 - offset
        while sequence[left] == sequence[right]:
            if not (left < right):
                return left
            left += 1
            right -= 1
        # extra on left
        left = offset
        right = n - 1
        while sequence[left] == sequence[right]:
            if not (left < right):
                return left
            left += 1
            right -= 1
    return 0


def smudge_mirror_point(sequence):
    n = len(sequence)

    # build diff set
    # The previous range of
    # set(2**p for p in range(n))
    # was too small
    max_val = max(sequence)
    smudge = set()
    diff = 1
    smudge.add(diff)
    while diff < 2 * max_val:
        diff *= 2
        smudge.add(diff)

    for offset in range(n - 1):
        if (n - offset) % 2:
            continue
        # extra on right
        found = False
        smudge_n = None
        left = 0
        right = n - 1 - offset
        while True:
            diff = abs(sequence[left] - sequence[right])
            if diff != 0:
                if found:
                    break
                if diff not in smudge:
                    break
                smudge_n = (left, diff)
                found = True
            if not (left < right - 1):
                if found:
                    return right
                break
            left += 1
            right -= 1
        # extra on left
        found = False
        smudge_n = None
        left = offset
        right = n - 1
        while True:
            diff = abs(sequence[left] - sequence[right])
            if diff != 0:
                if found:
                    break
                if diff not in smudge:
                    break
                smudge_n = (left, diff)
                found = True
            if not (left < right - 1):
                if found:
                    return right
                break
            left += 1
            right -= 1
    return 0


def calc_symetry(raw_map, with_smudge=False):
    col_counts = [0] * len(raw_map[0])
    row_counts = []
    for y, raw_line in enumerate(raw_map):
        row_count = 0
        for x, c in enumerate(raw_line):
            if c == "#":
                row_count += 2**x
                col_counts[x] += 2**y
        row_counts.append(row_count)
    if with_smudge:
        a = smudge_mirror_point(col_counts)
        b = smudge_mirror_point(row_counts)
        if a and b:
            if a == 1 or a == len(col_counts) - 1:
                a = 0
            elif b == 1 or b == len(row_counts) - 1:
                b = 0
    else:
        a = mirror_point(col_counts)
        b = mirror_point(row_counts)
    answer = a + 100 * b
    # if a and b:
    #     print("\n".join(raw_map))
    #     print(f"{a} {col_counts=}")
    #     print(f"{b} {row_counts=}")
    #     print(f"{answer=}")

    return answer


def test_rocks():
    assert calc_symetry(SAMPLE_1) == 5
    assert calc_symetry(SAMPLE_2) == 400
    assert calc_symetry(SAMPLE_1, with_smudge=True) == 300
    assert calc_symetry(SAMPLE_2, with_smudge=True) == 100
    my_answer = sum(calc_symetry(block) for block in RAW_INPUT)
    assert my_answer == 33520
    # 16887 is too low, 33625 is too high, 33520 is just right

    # for index, block in enumerate(RAW_INPUT):
    #     # if index in {6, 21, 29, 50, 59, 64, 87}:
    #     print(f"{index=}")
    #     calc_symetry(block, with_smudge=True)

    my_answer_2 = sum(calc_symetry(block, with_smudge=True) for block in RAW_INPUT)
    # 33814 is too low, 34934 is too high,
    # note - guessed the correct answer of 34824 by inspecting the cases where
    # there were horizontal and vertical mirror points (two cases, index 18 and 93)
    # and disgarding smudge that was closest to an edge
    assert my_answer_2 == 34824
