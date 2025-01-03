from pathlib import Path


class Puzzle:
    """
    --- Day 9: Explosives in Cyberspace ---
    Wandering around a secure area, you come across a datalink port to a new
    part of the network. After briefly scanning it for interesting files, you
    find one file in particular that catches your attention. It's compressed
    with an experimental format, but fortunately, the documentation for the
    format is nearby.

    The format compresses a sequence of characters. Whitespace is ignored. To
    indicate that some sequence should be repeated, a marker is added to the
    file, like (10x2). To decompress this marker, take the subsequent 10
    characters and repeat them 2 times. Then, continue reading the file after
    the repeated data. The marker itself is not included in the decompressed
    output.

    If parentheses or other characters appear within the data referenced by a
    marker, that's okay - treat it like normal data, not a marker, and then
    resume looking for markers after the decompressed section.

    For example:

    - ADVENT contains no markers and decompresses to itself with no changes,
      resulting in a decompressed length of 6.

    - A(1x5)BC repeats only the B a total of 5 times, becoming ABBBBBC
      for a decompressed length of 7.

    - (3x3)XYZ becomes XYZXYZXYZ for a decompressed length of 9.

    - A(2x2)BCD(2x2)EFG doubles the BC and EF, becoming ABCBCDEFEFG for a
      decompressed length of 11.

    - (6x1)(1x3)A simply becomes (1x3)A - the (1x3) looks like a marker, but
      because it's within a data section of another marker, it is not treated
      any differently from the A that comes after it. It has a decompressed
      length of 6.

    - X(8x2)(3x3)ABCY becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of
      18), because the decompressed data from the (8x2) marker (the (3x3)ABC) is
      skipped and not processed further.

    What is the decompressed length of the file (your puzzle input)? Don't count
    whitespace.

    Your puzzle answer was 183269.

    --- Part Two ---
    Apparently, the file actually uses version two of the format.

    In version two, the only difference is that markers within decompressed data
    are decompressed. This, the documentation explains, provides much more
    substantial compression capabilities, allowing many-gigabyte files to be
    stored in only a few kilobytes.

    For example:

    - (3x3)XYZ still becomes XYZXYZXYZ, as the decompressed section contains no
      markers.

    - X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY, because the decompressed
      data from the (8x2) marker is then further decompressed, thus triggering
      the (3x3) marker twice for a total of six ABC sequences.

    - (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A
      repeated 241920 times.

    - (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445
      characters long.

    Unfortunately, the computer you brought probably doesn't have enough memory
    to actually decompress the file; you'll have to come up with another way to
    get its decompressed length.

    What is the decompressed length of the file using this improved format?

    Your puzzle answer was 11317278863.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """

    pass


SAMPLE = [
    "ADVENT",
    "A(1x5)BC",
    "(3x3)XYZ",
    "A(2x2)BCD(2x2)EFG",
    "(6x1)(1x3)A",
    "X(8x2)(3x3)ABCY",
]
SAMPLE_RESULT = [
    "ADVENT",
    "ABBBBBC",
    "XYZXYZXYZ",
    "ABCBCDEFEFG",
    "(1x3)A",
    "X(3x3)ABC(3x3)ABCY",
]

with open(Path(__file__).parent / "2016_09_input.txt") as f:
    INPUT = f.read().strip()


def decompress(in_string, out_string=""):
    if in_string.count("(") == 0:
        return in_string

    head, rest = in_string.split("(", 1)
    out_string += head
    inst, rest = rest.split(")", 1)
    chunk_size, repeat = inst.split("x")
    chunk = rest[: int(chunk_size)]
    out_string += chunk * int(repeat)
    rest = rest[int(chunk_size) :]
    return out_string + decompress(rest)


def test_decompress():
    for raw, out in zip(SAMPLE, SAMPLE_RESULT):
        assert decompress(raw) == out
    assert len(decompress(INPUT)) == 183269


def parse_first(remaining_string, result_len=0):
    if remaining_string.count("(") == 0:
        return "", result_len + len(remaining_string)
    head, tail = remaining_string.split("(", 1)
    return f"({tail}", result_len + len(head)


def test_parse_first():
    assert parse_first("") == ("", 0)
    assert parse_first("123asd") == ("", 6)
    assert parse_first("(1x4)asd", 4) == ("(1x4)asd", 4)
    assert parse_first("123(1x3)asd", 7) == ("(1x3)asd", 10)
    assert parse_first("123(4x1)as(4x1)d") == ("(4x1)as(4x1)d", 3)


def parse_repeat(remaining_string):
    if remaining_string[0] != "(":
        raise Exception("Invalid input string")
    inst, remaining = remaining_string[1:].split(")", 1)
    chunk_size, repeat_count = [int(d) for d in inst.split("x")]
    return remaining[chunk_size:], remaining[:chunk_size], repeat_count


def test_parse_repeat():
    assert parse_repeat("(1x4)asd") == ("sd", "a", 4)
    assert parse_repeat("(2x3)asd") == ("d", "as", 3)
    assert parse_repeat("(5x2)(5x1)asdfg") == ("asdfg", "(5x1)", 2)
    assert parse_repeat("(27x12)(20x12)(13x14)(7x10)(1x12)A") == (
        "",
        "(20x12)(13x14)(7x10)(1x12)A",
        12,
    )


def decompress2_len(remaining_string, result_len=0):
    repeating_stuff, result_len = parse_first(remaining_string, result_len)
    if repeating_stuff == "":
        return result_len
    remaining, chunk, repeat_count = parse_repeat(repeating_stuff)
    if chunk.count("(") == 0:
        return decompress2_len(remaining, result_len + repeat_count * len(chunk))
    expanded_chunk_cnt = decompress2_len(chunk)
    return decompress2_len(remaining, result_len + repeat_count * expanded_chunk_cnt)


def test_decompress2_len():
    assert decompress2_len("(3x3)XYZ") == 9
    assert decompress2_len("X(8x2)(3x3)ABCY") == 20
    assert decompress2_len("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920
    assert (
        decompress2_len("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN")
        == 445
    )
    assert decompress2_len(INPUT) == 11317278863
