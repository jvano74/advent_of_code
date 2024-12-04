from typing import List, NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 4: Ceres Search ---

    "Looks like the Chief's not here. Next!" One of The Historians pulls out a
    device and pushes the only button on it. After a brief flash, you recognize
    the interior of the Ceres monitoring station!

    As the search for the Chief continues, a small Elf who lives on the station
    tugs on your shirt; she'd like to know if you could help her with her word
    search (your puzzle input). She only has to find one word: XMAS.

    This word search allows words to be horizontal, vertical, diagonal, written
    backwards, or even overlapping other words. It's a little unusual, though,
    as you don't merely need to find one instance of XMAS - you need to find all
    of them. Here are a few ways XMAS might appear, where irrelevant characters
    have been replaced with .:

    ..X...
    .SAMX.
    .A..A.
    XMAS.S
    .X....

    The actual word search will be full of letters instead. For example:

    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX

    In this word search, XMAS occurs a total of 18 times; here's the same word
    search again, but where letters not involved in any XMAS have been replaced
    with .:

    ....XXMAS.
    .SAMXMS...
    ...S..A...
    ..A.A.MS.X
    XMASAMX.MM
    X.....XA.A
    S.S.S.S.SS
    .A.A.A.A.A
    ..M.M.M.MM
    .X.X.XMASX

    Take a look at the little Elf's word search. How many times does XMAS appear?

    Your puzzle answer was 2642.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---

    The Elf looks quizzically at you. Did you misunderstand the assignment?

    Looking for the instructions, you flip over the word search to find that
    this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're
    supposed to find two MAS in the shape of an X. One way to achieve that is
    like this:

    M.S
    .A.
    M.S

    Irrelevant characters have again been replaced with . in the above diagram.
    Within the X, each MAS can be written forwards or backwards.

    Here's the same example from before, but this time all of the X-MASes have
    been kept instead:

    .M.S......
    ..A..MSMS.
    .M.S.MAA..
    ..A.ASMSM.
    .M.S.M....
    ..........
    S.S.S.S.S.
    .A.A.A.A..
    M.M.M.M.M.
    ..........

    In this example, an X-MAS appears 9 times.

    Flip the word search from the instructions back over to the word search side
    and try again. How many times does an X-MAS appear?

    """


with open("day_04_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")

SAMPLE = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


DELTAS = {
    Pt(1, 0),
    Pt(-1, 0),
    Pt(0, 1),
    Pt(0, -1),
    Pt(1, 1),
    Pt(-1, 1),
    Pt(-1, -1),
    Pt(1, -1),
}


class WordSearch:
    def __init__(self, raw_rows: List[str]):
        self.letters = defaultdict(set)
        for j, row in enumerate(raw_rows):
            for i, c in enumerate(row):
                self.letters[c].add(Pt(i, j))

    def find(self, word="XMAS") -> List[List[Pt]]:
        found = []
        for starting_loc in self.letters[word[0]]:
            for delta in DELTAS:
                loc_to_check = starting_loc + delta
                if loc_to_check in self.letters[word[1]]:
                    found.append([delta, starting_loc, loc_to_check])

        for next_letter in word[2:]:
            next_level = []
            for partial_word in found:
                loc_to_check = partial_word[-1] + partial_word[0]
                if loc_to_check in self.letters[next_letter]:
                    new_partial = partial_word[:]
                    new_partial.append(loc_to_check)
                    next_level.append(new_partial)
            found = next_level
        return found

    def find_x(self) -> List[List[Pt]]:
        x_mas = defaultdict(list)
        for mas in self.find("MAS"):
            mas_dir = mas[0]
            if mas_dir.x != 0 and mas_dir.y != 0:
                a_loc = mas[2]
                x_mas[a_loc].append(mas_dir)
        total_found = 0
        for mas_list in x_mas.values():
            match len(mas_list):
                case 1:
                    pass
                case 2:
                    total_found += 1
                case 4:
                    raise Exception("What?")
                case 3:
                    raise Exception("What?")

        return total_found


def test_word_search_find():
    sample = WordSearch(SAMPLE)
    assert len(sample.find()) == 18
    my_puzzle = WordSearch(RAW_INPUT)
    assert len(my_puzzle.find()) == 2642


def test_word_search_find_x():
    sample = WordSearch(SAMPLE)
    assert sample.find_x() == 9
    my_puzzle = WordSearch(RAW_INPUT)
    assert my_puzzle.find_x() == 1974
    # Initial result was 2001 which was too high,
    # turns out we only want diagonals which gives 1974
