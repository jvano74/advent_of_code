from pathlib import Path
from typing import NamedTuple
from functools import cache
from collections import defaultdict


class Puzzle:
    """
    --- Day 19: Linen Layout ---
    Today, The Historians take you up to the hot springs on Gear Island! Very
    suspiciously, absolutely nothing goes wrong as they begin their careful
    search of the vast field of helixes.

    Could this finally be your chance to visit the onsen next door? Only one way
    to find out.

    After a brief conversation with the reception staff at the onsen front desk,
    you discover that you don't have the right kind of money to pay the
    admission fee. However, before you can leave, the staff get your attention.
    Apparently, they've heard about how you helped at the hot springs, and
    they're willing to make a deal: if you can simply help them arrange their
    towels, they'll let you in for free!

    Every towel at this onsen is marked with a pattern of colored stripes. There
    are only a few patterns, but for any particular pattern, the staff can get
    you as many towels with that pattern as you need. Each stripe can be white
    (w), blue (u), black (b), red (r), or green (g). So, a towel with the
    pattern ggr would have a green stripe, a green stripe, and then a red
    stripe, in that order. (You can't reverse a pattern by flipping a towel
    upside-down, as that would cause the onsen logo to face the wrong way.)

    The Official Onsen Branding Expert has produced a list of designs - each a
    long sequence of stripe colors - that they would like to be able to display.
    You can use any towels you want, but all of the towels' stripes must exactly
    match the desired design. So, to display the design rgrgr, you could use two
    rg towels and then an r towel, an rgr towel and then a gr towel, or even a
    single massive rgrgr towel (assuming such towel patterns were actually
    available).

    To start, collect together all of the available towel patterns and the list
    of desired designs (your puzzle input). For example:

    r, wr, b, g, bwu, rb, gb, br

    brwrr
    bggr
    gbbr
    rrbgbr
    ubwu
    bwurrg
    brgr
    bbrgwb

    The first line indicates the available towel patterns; in this example, the
    onsen has unlimited towels with a single red stripe (r), unlimited towels
    with a white stripe and then a red stripe (wr), and so on.

    After the blank line, the remaining lines each describe a design the onsen
    would like to be able to display. In this example, the first design (brwrr)
    indicates that the onsen would like to be able to display a black stripe, a
    red stripe, a white stripe, and then two red stripes, in that order.

    Not all designs will be possible with the available towels. In the above
    example, the designs are possible or impossible as follows:

    brwrr can be made with a br towel, then a wr towel, and then finally an r towel.
    bggr can be made with a b towel, two g towels, and then an r towel.
    gbbr can be made with a gb towel and then a br towel.
    rrbgbr can be made with r, rb, g, and br.
    ubwu is impossible.
    bwurrg can be made with bwu, r, r, and g.
    brgr can be made with br, g, and r.
    bbrgwb is impossible.

    In this example, 6 of the eight designs are possible with the available
    towel patterns.

    To get into the onsen as soon as possible, consult your list of towel
    patterns and desired designs carefully. How many designs are possible?

    Your puzzle answer was 216.

    --- Part Two ---

    The staff don't really like some of the towel arrangements you came up with.
    To avoid an endless cycle of towel rearrangement, maybe you should just give
    them every possible option.

    Here are all of the different ways the above example's designs can be made:

    brwrr can be made in two different ways: b, r, wr, r or br, wr, r.

    bggr can only be made with b, g, g, and r.

    gbbr can be made 4 different ways:

    g, b, b, r
    g, b, br
    gb, b, r
    gb, br

    rrbgbr can be made 6 different ways:

    r, r, b, g, b, r
    r, r, b, g, br
    r, r, b, gb, r
    r, rb, g, b, r
    r, rb, g, br
    r, rb, gb, r

    bwurrg can only be made with bwu, r, r, and g.

    brgr can be made in two different ways: b, r, g, r or br, g, r.

    ubwu and bbrgwb are still impossible.

    Adding up all of the ways the towels in this example could be arranged into
    the desired designs yields 16 (2 + 1 + 4 + 6 + 1 + 2).

    They'll let you into the onsen as soon as you have the list. What do you get
    if you add up the number of different ways you could make each design?

    Your puzzle answer was 603191454138773.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


SAMPLE_TOWELS = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]

SAMPLE_DESIGNS = [
    "brwrr",
    "bggr",
    "gbbr",
    "rrbgbr",
    "ubwu",
    "bwurrg",
    "brgr",
    "bbrgwb",
]


with open(Path(__file__).parent / "2024_19_input.txt") as fp:
    TOWELS, DESIGNS = fp.read().split("\n\n")
    TOWELS = TOWELS.split(", ")
    DESIGNS = DESIGNS.split("\n")


def test_puzzle_input():
    assert TOWELS[:5] == ["gurwuurg", "ugwrrbuw", "ubr", "bbrurww", "wgw"]
    assert DESIGNS[:5] == [
        "gwwwgrbuwgrbgbwubrbwguwgubrwwurwrbrgwurgwgguww",
        "wwbwbbwubrbruubrwugurrbuuwuuwbrguubbwwbugbbgu",
        "gbwrrgruuurugwwurgwguguugbrggbrwugbugubuggu",
        "uwbrwbwubwbrbgbugubbugwwgwbrrrwuurgwbgrurbwbub",
        "ggwgburrurgwubwbbgrwuwwwwbugwrubguurrgrbbrwrggbrgwwg",
    ]


def make_palette(patterns):
    # palette = defaultdict(set)
    # for pattern in patterns:
    #     palette[pattern[0]].add(pattern)
    # return dict(palette)
    return tuple(sorted(patterns))


@cache
def make_match(palette, design, all_combos=False, detect_overrun=False):
    version_count = 0
    boundary = [(design, [])]
    while boundary:
        remaining_design, build = boundary.pop()
        if remaining_design == "":
            if not all_combos:
                return 1
            version_count += 1
            continue
        for option in palette:
            if len(remaining_design) < len(option):
                if (
                    detect_overrun
                    and remaining_design == option[: len(remaining_design)]
                ):
                    return -1
            if option == remaining_design[: len(option)]:
                new_build = build[:]
                new_build.append(option)
                boundary.append((remaining_design[len(option) :], new_build))
    return version_count


def test_match():
    sample_palette = make_palette(SAMPLE_TOWELS)
    sample_matches = [make_match(sample_palette, design) for design in SAMPLE_DESIGNS]
    assert sum(sample_matches) == 6
    palette = make_palette(TOWELS)
    assert sum(make_match(palette, design) for design in DESIGNS) == 216


def find_factor_towels(towels):
    forward_factors = set()
    end_factors = set()
    full_factors = set()
    for towel in towels:
        passing_forward = True
        passing_end = True
        for test_towel in towels:
            if towel not in test_towel:
                continue
            if towel != test_towel[: len(towel)]:
                passing_forward = False
            if towel != test_towel[-len(towel) :]:
                passing_end = False
            if not passing_forward and not passing_end:
                break
        if passing_forward and passing_end:
            full_factors.add(towel)
        elif passing_forward:
            forward_factors.add(towel)
        elif passing_end:
            end_factors.add(towel)
    palette = make_palette(towels)
    full_factor_dict = {}
    for fac in full_factors:
        multiplicity = make_match(palette, fac, all_combos=True, detect_overrun=True)
        if multiplicity > 0:
            full_factor_dict[fac] = multiplicity

    new_palette = make_palette(set(towels) - set(full_factor_dict.keys()))
    return (full_factor_dict, forward_factors, end_factors, new_palette)


def test_find_factor_towels():
    # SAMPLE_TOWELS = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]
    sample_towel_factors = find_factor_towels(SAMPLE_TOWELS)
    assert sample_towel_factors == (
        {"bwu": 1, "wr": 1},
        {"g"},
        set(),
        ("b", "br", "g", "gb", "r", "rb"),
    )
    towel_factors = find_factor_towels(TOWELS)
    assert [len(fac) for fac in towel_factors] == [3, 29, 13, 444]


def make_fast_match(factors, design):
    new_design = design
    full_factor_dict, forward_factors, end_factors, palette = factors
    version_count = 1
    for factor, factor_multiple in full_factor_dict.items():
        split_design = new_design.split(factor)
        version_count *= factor_multiple ** (len(split_design) - 1)
        new_design = "|".join(split_design)

    for factor in forward_factors:
        split_design = new_design.split(factor)
        new_design = f"|{factor}".join(split_design)

    for factor in end_factors:
        split_design = new_design.split(factor)
        new_design = f"{factor}|".join(split_design)

    for remaining in new_design.split("|"):
        version_count *= make_match(palette, remaining, all_combos=True)

    return version_count


def test_fast_match():
    sample_palette = make_palette(SAMPLE_TOWELS)
    assert make_match(sample_palette, "", all_combos=True) == 1
    sample_matches = [
        make_match(sample_palette, design, all_combos=True) for design in SAMPLE_DESIGNS
    ]
    assert sum(sample_matches) == 16

    sample_factors = find_factor_towels(SAMPLE_TOWELS)
    assert make_fast_match(sample_factors, "rrbgbr") == 6
    sample_matches = [
        make_fast_match(sample_factors, design) for design in SAMPLE_DESIGNS
    ]
    assert sum(sample_matches) == 16

    # The above approach worked but was not nearly fast enough - even after adding
    # the @cache to the base factor count.  So comment out testing of full TOWELS

    # towel_factors = find_factor_towels(TOWELS)
    # assert sum(make_fast_match(towel_factors, design) for design in DESIGNS) == 6

    # and move on to idea from watching someone else who used recursion and
    # simple look back


@cache
def recursive_match(towels, design):
    if design == "":
        return 1
    total = 0
    for towel in towels:
        pattern_start = len(design) - len(towel)
        if pattern_start < 0:
            continue
        if towel == design[pattern_start:]:
            total += recursive_match(towels, design[:pattern_start])
    return total


def test_recursive_match():
    # assert recursive_match(tuple(SAMPLE_TOWELS), "") == 1
    assert recursive_match(tuple(SAMPLE_TOWELS), "rrbgbr") == 6

    sample_matches = [
        recursive_match(tuple(SAMPLE_TOWELS), design) for design in SAMPLE_DESIGNS
    ]
    assert sum(sample_matches) == 16

    assert (
        sum(recursive_match(tuple(TOWELS), design) for design in DESIGNS)
        == 603191454138773
    )
