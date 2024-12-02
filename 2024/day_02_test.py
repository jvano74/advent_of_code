from typing import List
from collections import defaultdict


class Puzzle:
    """
    --- Day 2: Red-Nosed Reports ---
    Fortunately, the first location The Historians want to search isn't a long
    walk from the Chief Historian's office.

    While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain
    no sign of the Chief Historian, the engineers there run up to you as soon as
    they see you. Apparently, they still talk about the time Rudolph was saved
    through molecular synthesis from a single electron.

    They're quick to add that - since you're already here - they'd really
    appreciate your help analyzing some unusual data from the Red-Nosed reactor.
    You turn to check if The Historians are waiting for you, but they seem to
    have already divided into groups that are currently searching every corner
    of the facility. You offer to help with the unusual data.

    The unusual data (your puzzle input) consists of many reports, one report
    per line. Each report is a list of numbers called levels that are separated
    by spaces. For example:

    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9

    This example data contains six reports each containing five levels.

    The engineers are trying to figure out which reports are safe. The Red-Nosed
    reactor safety systems can only tolerate levels that are either gradually
    increasing or gradually decreasing. So, a report only counts as safe if both
    of the following are true:

    The levels are either all increasing or all decreasing.
    Any two adjacent levels differ by at least one and at most three.
    In the example above, the reports can be found safe or unsafe by checking
    those rules:

    7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
    1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
    9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
    1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
    8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
    1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.

    So, in this example, 2 reports are safe.

    Analyze the unusual data from the engineers. How many reports are safe?

    Your puzzle answer was 369.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The engineers are surprised by the low number of safe reports until they
    realize they forgot to tell you about the Problem Dampener.

    The Problem Dampener is a reactor-mounted module that lets the reactor
    safety systems tolerate a single bad level in what would otherwise be a safe
    report. It's like the bad level never happened!

    Now, the same rules apply as before, except if removing a single level from
    an unsafe report would make it safe, the report instead counts as safe.

    More of the above example's reports are now safe:

    7 6 4 2 1: Safe without removing any level.
    1 2 7 8 9: Unsafe regardless of which level is removed.
    9 7 6 2 1: Unsafe regardless of which level is removed.
    1 3 2 4 5: Safe by removing the second level, 3.
    8 6 4 4 1: Safe by removing the third level, 4.
    1 3 6 7 9: Safe without removing any level.
    Thanks to the Problem Dampener, 4 reports are actually safe!

    Update your analysis by handling situations where the Problem Dampener can
    remove a single level from unsafe reports. How many reports are now safe?

    Your puzzle answer was 428.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


with open("day_02_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")

SAMPLE = ["7 6 4 2 1", "1 2 7 8 9", "9 7 6 2 1", "1 3 2 4 5", "8 6 4 4 1", "1 3 6 7 9"]


def prep_report(report: str) -> List[int]:
    return [int(d) for d in report.split(" ")]


SAMPLE = [prep_report(r) for r in SAMPLE]


def orig_report_is_safe(levels: List[int]) -> bool:
    if levels[0] > levels[1]:
        levels = [-d for d in levels]
        negated = True
    else:
        negated = False
    for pos, next_level in enumerate(levels):
        if pos == 0:
            current_level = next_level
            continue
        if 0 < next_level - current_level < 4:
            current_level = next_level
            continue
        return False
    return True


def report_is_safe(levels: List[int], tolerance: int = 0) -> bool:
    up, down, fail = [], [], []
    for pos, next_level in enumerate(levels):
        if pos == 0:
            current_level = next_level
            continue
        delta = next_level - current_level
        current_level = next_level
        if not (0 < abs(delta) < 4):
            fail.append(pos)
        elif delta > 0:
            up.append(pos)
        else:
            down.append(pos)
    if len(fail) == 0:
        if len(up) == 0 or len(down) == 0:
            return True
        if tolerance == 0:
            return False

        if len(up) > len(down):
            new_levels = [lvl for pos, lvl in enumerate(levels) if pos + 1 != down[0]]
            if report_is_safe(new_levels):
                return True
            new_levels = [lvl for pos, lvl in enumerate(levels) if pos != down[0]]
            return report_is_safe(new_levels)
        new_levels = [lvl for pos, lvl in enumerate(levels) if pos + 1 != up[0]]
        if report_is_safe(new_levels):
            return True
        new_levels = [lvl for pos, lvl in enumerate(levels) if pos != up[0]]
        return report_is_safe(new_levels)

    if tolerance == 0:
        return False

    new_levels = [lvl for pos, lvl in enumerate(levels) if pos + 1 != fail[0]]
    if report_is_safe(new_levels):
        return True
    new_levels = [lvl for pos, lvl in enumerate(levels) if pos != fail[0]]
    return report_is_safe(new_levels)


def test_report_is_safe():
    assert orig_report_is_safe(SAMPLE[0]) == True
    assert orig_report_is_safe(SAMPLE[1]) == False
    assert orig_report_is_safe(SAMPLE[2]) == False
    assert orig_report_is_safe(SAMPLE[3]) == False
    assert orig_report_is_safe(SAMPLE[4]) == False
    assert orig_report_is_safe(SAMPLE[5]) == True
    assert sum(1 if orig_report_is_safe(rep) else 0 for rep in SAMPLE) == 2

    assert report_is_safe(SAMPLE[0]) == True
    assert report_is_safe(SAMPLE[1]) == False
    assert report_is_safe(SAMPLE[2]) == False
    assert report_is_safe(SAMPLE[3]) == False
    assert report_is_safe(SAMPLE[4]) == False
    assert report_is_safe(SAMPLE[5]) == True
    assert sum(1 if report_is_safe(rep) else 0 for rep in SAMPLE) == 2
    # now try my input
    my_input = [prep_report(raw) for raw in RAW_INPUT]
    assert sum(1 if report_is_safe(rep) else 0 for rep in my_input) == 369


def test_tolerant_report_is_safe():
    assert report_is_safe(SAMPLE[0], tolerance=1) == True
    assert report_is_safe(SAMPLE[1], tolerance=1) == False
    assert report_is_safe(SAMPLE[2], tolerance=1) == False
    assert report_is_safe(SAMPLE[3], tolerance=1) == True
    assert report_is_safe(SAMPLE[4], tolerance=1) == True
    assert report_is_safe(SAMPLE[5], tolerance=1) == True
    assert sum(1 if report_is_safe(r, tolerance=1) else 0 for r in SAMPLE) == 4
    # now try my input
    my_input = [prep_report(raw) for raw in RAW_INPUT]
    assert sum(1 if report_is_safe(rep, tolerance=1) else 0 for rep in my_input) == 428
    # First got 423 but was too low,
    # updated to try both cases for up and down got correct answer of 428
