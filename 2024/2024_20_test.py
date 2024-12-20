from pathlib import Path
from typing import NamedTuple
from functools import cache
from collections import defaultdict


class Puzzle:
    """
    --- Day 20: Race Condition ---
    The Historians are quite pixelated again. This time, a massive, black
    building looms over you - you're right outside the CPU!

    While The Historians get to work, a nearby program sees that you're idle and
    challenges you to a race. Apparently, you've arrived just in time for the
    frequently-held race condition festival!

    The race takes place on a particularly long and twisting code path; programs
    compete to see who can finish in the fewest picoseconds. The winner even
    gets their very own mutex!

    They hand you a map of the racetrack (your puzzle input). For example:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############

    The map consists of track (.) - including the start (S) and end (E)
    positions (both of which also count as track) - and walls (#).

    When a program runs through the racetrack, it starts at the start position.
    Then, it is allowed to move up, down, left, or right; each such move takes 1
    picosecond. The goal is to reach the end position as quickly as possible. In
    this example racetrack, the fastest time is 84 picoseconds.

    Because there is only a single path from the start to the end and the
    programs all go the same speed, the races used to be pretty boring. To make
    things more interesting, they introduced a new rule to the races: programs
    are allowed to cheat.

    The rules for cheating are very strict. Exactly once during a race, a
    program may disable collision for up to 2 picoseconds. This allows the
    program to pass through walls as if they were regular track. At the end of
    the cheat, the program must be back on normal track again; otherwise, it
    will receive a segmentation fault and get disqualified.

    So, a program could complete the course in 72 picoseconds (saving 12
    picoseconds) by cheating for the two moves marked 1 and 2:

    ###############
    #...#...12....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############

    Or, a program could complete the course in 64 picoseconds (saving 20
    picoseconds) by cheating for the two moves marked 1 and 2:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...12..#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############

    This cheat saves 38 picoseconds:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.####1##.###
    #...###.2.#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############

    This cheat saves 64 picoseconds and takes the program directly to the end:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..21...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############

    Each cheat has a distinct start position (the position where the cheat is
    activated, just before the first move that is allowed to go through walls)
    and end position; cheats are uniquely identified by their start position and
    end position.

    In this example, the total number of cheats (grouped by the amount of time
    they save) are as follows:

    There are 14 cheats that save 2 picoseconds.
    There are 14 cheats that save 4 picoseconds.
    There are 2 cheats that save 6 picoseconds.
    There are 4 cheats that save 8 picoseconds.
    There are 2 cheats that save 10 picoseconds.
    There are 3 cheats that save 12 picoseconds.
    There is one cheat that saves 20 picoseconds.
    There is one cheat that saves 36 picoseconds.
    There is one cheat that saves 38 picoseconds.
    There is one cheat that saves 40 picoseconds.
    There is one cheat that saves 64 picoseconds.

    You aren't sure what the conditions of the racetrack will be like, so to
    give yourself as many options as possible, you'll need a list of the best
    cheats. How many cheats would save you at least 100 picoseconds?

    Your puzzle answer was 1307.

    --- Part Two ---

    The programs seem perplexed by your list of cheats. Apparently, the
    two-picosecond cheating rule was deprecated several milliseconds ago! The
    latest version of the cheating rule permits a single cheat that instead
    lasts at most 20 picoseconds.

    Now, in addition to all the cheats that were possible in just two
    picoseconds, many more cheats are possible. This six-picosecond cheat saves
    76 picoseconds:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #1#####.#.#.###
    #2#####.#.#...#
    #3#####.#.###.#
    #456.E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############

    Because this cheat has the same start and end positions as the one above,
    it's the same cheat, even though the path taken during the cheat is
    different:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S12..#.#.#...#
    ###3###.#.#.###
    ###4###.#.#...#
    ###5###.#.###.#
    ###6.E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############

    Cheats don't need to use all 20 picoseconds; cheats can last any amount of
    time up to and including 20 picoseconds (but can still only end when the
    program is on normal track). Any cheat time not used is lost; it can't be
    saved for another cheat later. If cheat mode is active when the end position
    is reached, cheat mode ends automatically.

    You'll still need a list of the best cheats, but now there are even more to
    choose between. Here are the quantities of cheats in this example that save
    50 picoseconds or more:

    There are 32 cheats that save 50 picoseconds.
    There are 31 cheats that save 52 picoseconds.
    There are 29 cheats that save 54 picoseconds.
    There are 39 cheats that save 56 picoseconds.
    There are 25 cheats that save 58 picoseconds.
    There are 23 cheats that save 60 picoseconds.
    There are 20 cheats that save 62 picoseconds.
    There are 19 cheats that save 64 picoseconds.
    There are 12 cheats that save 66 picoseconds.
    There are 14 cheats that save 68 picoseconds.
    There are 12 cheats that save 70 picoseconds.
    There are 22 cheats that save 72 picoseconds.
    There are 4 cheats that save 74 picoseconds.
    There are 3 cheats that save 76 picoseconds.

    Find the best cheats using the updated cheating rules. How many cheats would
    save you at least 100 picoseconds?

    Your puzzle answer was 986545.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


SAMPLE_TRACK = [
    "###############",
    "#...#...#.....#",
    "#.#.#.#.#.###.#",
    "#S#...#.#.#...#",
    "#######.#.#.###",
    "#######.#.#...#",
    "#######.#.###.#",
    "###..E#...#...#",
    "###.#######.###",
    "#...###...#...#",
    "#.#####.#.###.#",
    "#.#...#.#.#...#",
    "#.#.#.#.#.#.###",
    "#...#...#...###",
    "###############",
]


with open(Path(__file__).parent / "2024_20_input.txt") as fp:
    TRACK = fp.read().split("\n")


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def dist_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def nbhd(self, r=1):
        nbhd = set()
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if abs(dx) + abs(dy) <= r:
                    nbhd.add(self + Pt(dx, dy))
        return nbhd


class Track:
    def __init__(self, track_map):
        self.track = {}
        self.race = []

        for y, raw_line in enumerate(track_map):
            for x, c in enumerate(raw_line):
                if c == "#":
                    continue
                self.track[Pt(x, y)] = -1
                if c == "S":
                    self.start = Pt(x, y)
                elif c == "E":
                    self.end = Pt(x, y)
        dist = 0
        pt = self.start
        self.track[pt] = dist
        while pt != self.end:
            for next_pt in pt.nbhd():
                if next_pt not in self.track:
                    continue
                if self.track[next_pt] != -1:
                    continue
                pt = next_pt
                dist += 1
                self.track[pt] = dist
        for key, time in self.track.items():
            self.race.append((time, key))
        self.race.sort()

    def find_cheats(self, min_savings, cheat_length=2):
        unique_cheats = defaultdict(set)
        cheat_ranking = defaultdict(set)
        for time, current_pt in self.race:
            for cheat_end in current_pt.nbhd(r=cheat_length):
                if cheat_end not in self.track:
                    continue
                savings = self.track[cheat_end] - (time + cheat_end.dist_to(current_pt))
                if savings >= min_savings:
                    unique_cheats[(current_pt, cheat_end)].add(savings)

        for cheat, savings in unique_cheats.items():
            cheat_ranking[min(savings)].add(cheat)

        return {savings: len(cheats) for savings, cheats in cheat_ranking.items()}


def test_track():
    sample_track = Track(SAMPLE_TRACK)
    assert max(sample_track.track.values()) == 84
    assert sample_track.find_cheats(2) == {
        2: 14,
        4: 14,
        8: 4,
        6: 2,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }
    new_cheats = sample_track.find_cheats(50, cheat_length=20)
    print(new_cheats)
    assert new_cheats == {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }


def test_my_track():
    track = Track(TRACK)
    assert sum(track.find_cheats(100).values()) == 1307
    assert sum(track.find_cheats(100, cheat_length=20).values()) == 986545
    # First attempt 1007410 is too high - not surprised, same issue with sample
    # Finally figured out issue was the starting point was the valid location on track
    # not the first cheat location, so after updating how I counted unique cheats got
    # correct answer of 986545
