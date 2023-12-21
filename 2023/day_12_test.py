from functools import cache


class Puzzle:
    """
    --- Day 12: Hot Springs ---
    You finally reach the hot springs! You can see steam rising from secluded
    areas attached to the primary, ornate building.

    As you turn to enter, the researcher stops you. "Wait - I thought you were
    looking for the hot springs, weren't you?" You indicate that this definitely
    looks like hot springs to you.

    "Oh, sorry, common mistake! This is actually the onsen! The hot springs are
    next door."

    You look in the direction the researcher is pointing and suddenly notice the
    massive metal helixes towering overhead. "This way!"

    It only takes you a few more steps to reach the main gate of the massive
    fenced-off area containing the springs. You go through the gate and into a
    small administrative building.

    "Hello! What brings you to the hot springs today? Sorry they're not very hot
    right now; we're having a lava shortage at the moment." You ask about the
    missing machine parts for Desert Island.

    "Oh, all of Gear Island is currently offline! Nothing is being manufactured
    at the moment, not until we get more lava to heat our forges. And our
    springs. The springs aren't very springy unless they're hot!"

    "Say, could you go up and see why the lava stopped flowing? The springs are
    too cold for normal operation, but we should be able to find one springy
    enough to launch you up there!"

    There's just one problem - many of the springs have fallen into disrepair,
    so they're not actually sure which springs would even be safe to use! Worse
    yet, their condition records of which springs are damaged (your puzzle
    input) are also damaged! You'll need to help them repair the damaged
    records.

    In the giant field just outside, the springs are arranged into rows. For
    each row, the condition records show every spring and whether it is
    operational (.) or damaged (#). This is the part of the condition records
    that is itself damaged; for some springs, it is simply unknown (?) whether
    the spring is operational or damaged.

    However, the engineer that produced the condition records also duplicated
    some of this information in a different format! After the list of springs
    for a given row, the size of each contiguous group of damaged springs is
    listed in the order those groups appear in the row. This list always
    accounts for every damaged spring, and each number is the entire size of its
    contiguous group (that is, groups are always separated by at least one
    operational spring: #### would always be 4, never 2,2).

    So, condition records with no unknown spring conditions might look like
    this:

    #.#.### 1,1,3
    .#...#....###. 1,1,3
    .#.###.#.###### 1,3,1,6
    ####.#...#... 4,1,1
    #....######..#####. 1,6,5
    .###.##....# 3,2,1

    However, the condition records are partially damaged; some of the springs'
    conditions are actually unknown (?). For example:

    ???.### 1,1,3
    .??..??...?##. 1,1,3
    ?#?#?#?#?#?#?#? 1,3,1,6
    ????.#...#... 4,1,1
    ????.######..#####. 1,6,5
    ?###???????? 3,2,1

    Equipped with this information, it is your job to figure out how many
    different arrangements of operational and broken springs fit the given
    criteria in each row.

    In the first line (???.### 1,1,3), there is exactly one way separate groups
    of one, one, and three broken springs (in that order) can appear in that
    row: the first three unknown springs must be broken, then operational, then
    broken (#.#), making the whole row #.#.###.

    The second line is more interesting: .??..??...?##. 1,1,3 could be a total
    of four different arrangements. The last ? must always be broken (to satisfy
    the final contiguous group of three broken springs), and each ?? must hide
    exactly one of the two broken springs. (Neither ?? could be both broken
    springs or they would form a single contiguous group of two; if that were
    true, the numbers afterward would have been 2,3 instead.) Since each ?? can
    either be #. or .#, there are four possible arrangements of springs.

    The last line is actually consistent with ten different arrangements!
    Because the first number is 3, the first and second ? must both be . (if
    either were #, the first number would have to be 4 or higher). However, the
    remaining run of unknown spring conditions have many different ways they
    could hold groups of two and one broken springs:

    ?###???????? 3,2,1
    .###.##.#...
    .###.##..#..
    .###.##...#.
    .###.##....#
    .###..##.#..
    .###..##..#.
    .###..##...#
    .###...##.#.
    .###...##..#
    .###....##.#

    In this example, the number of possible arrangements for each row is:

    ???.### 1,1,3 - 1 arrangement
    .??..??...?##. 1,1,3 - 4 arrangements
    ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
    ????.#...#... 4,1,1 - 1 arrangement
    ????.######..#####. 1,6,5 - 4 arrangements
    ?###???????? 3,2,1 - 10 arrangements

    Adding all of the possible arrangement counts together produces a total of
    21 arrangements.

    For each row, count all of the different arrangements of operational and
    broken springs that meet the given criteria. What is the sum of those
    counts?

    Your puzzle answer was 7674.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    As you look out at the field of springs, you feel like there are way more
    springs than the condition records list. When you examine the records, you
    discover that they were actually folded up this whole time!

    To unfold the records, on each row, replace the list of spring conditions
    with five copies of itself (separated by ?) and replace the list of
    contiguous groups of damaged springs with five copies of itself (separated
    by ,).

    So, this row:

    .# 1
    Would become:

    .#?.#?.#?.#?.# 1,1,1,1,1

    The first line of the above example would become:

    ???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3

    In the above example, after unfolding, the number of possible arrangements
    for some rows is now much larger:

    ???.### 1,1,3 - 1 arrangement
    .??..??...?##. 1,1,3 - 16384 arrangements
    ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
    ????.#...#... 4,1,1 - 16 arrangements
    ????.######..#####. 1,6,5 - 2500 arrangements
    ?###???????? 3,2,1 - 506250 arrangements

    After unfolding, adding all of the possible arrangement counts together
    produces 525152.

    Unfold your condition records; what is the new sum of possible arrangement
    counts?

    Your puzzle answer was 4443895258186.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open("day_12_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")


SAMPLES = {
    "???.### 1,1,3": (1, 1),
    ".??..??...?##. 1,1,3": (4, 16384),
    "?#?#?#?#?#?#?#? 1,3,1,6": (1, 1),
    "????.#...#... 4,1,1": (1, 16),
    "????.######..#####. 1,6,5": (4, 2500),
    "?###???????? 3,2,1": (10, 506250),
}

MORE_SAMPLES = {
    ".?##??##??..??????? 9,4": 4,  # not 5
    "?.?##??##??..??????? 9,4": 4,  # not 13,
    ".???.????.???????? 1,4,3,1": 30,  # not 81,
}


def possible_arrangements(row_criteria: str, unfold=False, recursive=True):
    state, raw_counts = row_criteria.split(" ")
    faults = tuple(int(d) for d in raw_counts.split(","))
    if unfold:
        faults = faults * 5
        state = "?".join([state] * 5)
    if recursive:
        return recursive_arrangements(faults, state)
    return path_find_possible_arrangements(faults, state)


def path_find_possible_arrangements(faults, state):
    count = 0
    to_process = [(faults, state)]
    while to_process:
        faults, state = to_process.pop()
        # check for complete states
        if len(faults) == 0:
            if state.count("#"):
                continue
            count += 1
            continue
        # check for impossible to complete states
        state = state.strip(".")
        min_len = sum(faults) + len(faults) - 1
        if len(state) < min_len:
            continue
        # delay fault
        if state[0] == "?":
            to_process.append((faults, state[1:]))
        # start fault
        if state[0 : faults[0]].count("."):
            continue
        if faults[0] < len(state) and state[faults[0]] == "#":
            continue
        to_process.append((faults[1:], state[faults[0] + 1 :]))
    return count


@cache
def recursive_arrangements(faults, state):
    state = state.strip(".")
    # base cases
    if len(faults) == 0:
        return 0 if state.count("#") else 1
    if len(state) == 0:
        return 0
    if len(state) < sum(faults) + len(faults) - 1:
        return 0
    if len(state) == faults[0]:
        return 0 if state.count(".") or len(faults) > 1 else 1

    #  recursive cases
    result = 0
    if state[: faults[0]].count(".") == 0 and state[faults[0]] in ".?":
        left = recursive_arrangements(faults[1:], state[faults[0] + 1 :])
        result += left
    if state[0] == "?":
        shift = recursive_arrangements(faults, state[1:])
        result += shift
    return result


def test_possible_arrangements():
    for criteria, counts in SAMPLES.items():
        assert possible_arrangements(criteria) == counts[0]

    for criteria, count in MORE_SAMPLES.items():
        assert possible_arrangements(criteria) == count

    for criteria, counts in SAMPLES.items():
        assert possible_arrangements(criteria, unfold=True) == counts[1]

    my_answer = sum(possible_arrangements(c) for c in RAW_INPUT)
    # 9594 was too high, 7674 is correct - found and fixed bug
    assert my_answer == 7674

    my_answer_2 = sum(possible_arrangements(c, unfold=True) for c in RAW_INPUT)
    assert my_answer_2 == 4443895258186
