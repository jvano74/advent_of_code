from pathlib import Path
from typing import List
import re


class Puzzle:
    """
    --- Day 3: Mull It Over ---
    "Our computers are having issues, so I have no idea if we have any Chief
    Historians in stock! You're welcome to check the warehouse, though," says
    the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The
    Historians head out to take a look.

    The shopkeeper turns to you. "Any chance you can see why our computers are
    having issues again?"

    The computer appears to be trying to run a program, but its memory (your
    puzzle input) is corrupted. All of the instructions have been jumbled up!

    It seems like the goal of the program is just to multiply some numbers. It
    does that with instructions like mul(X,Y), where X and Y are each 1-3 digit
    numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of
    2024. Similarly, mul(123,4) would multiply 123 by 4.

    However, because the program's memory has been corrupted, there are also
    many invalid characters that should be ignored, even if they look like part
    of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2
    , 4 ) do nothing.

    For example, consider the following section of corrupted memory:

    xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

    Only the following four sections are real mul instructions:

    xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
     mul(2,4)                    mul(5,5)                mul(11,8)mul(8,5)

    Adding up the result of each instruction produces
    (2*4 + 5*5 + 11*8 + 8*5) = 161

    Scan the corrupted memory for uncorrupted mul instructions. What do you get
    if you add up all of the results of the multiplications?

    Your puzzle answer was 187833789.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---

    As you scan through the corrupted memory, you notice that some of the
    conditional statements are also still intact. If you handle some of the
    uncorrupted conditional statements in the program, you might be able to get
    an even more accurate result.

    There are two new instructions you'll need to handle:

    The do() instruction enables future mul instructions.

    The don't() instruction disables future mul instructions.

    Only the most recent do() or don't() instruction applies. At the beginning
    of the program, mul instructions are enabled.

    For example:

    xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

    This corrupted memory is similar to the example from before, but this time
    the mul(5,5) and mul(11,8) instructions are disabled because there is a
    don't() instruction before them. The other mul instructions function
    normally, including the one at the end that gets re-enabled by a do()
    instruction.

    This time, the sum of the results is (2*4 + 8*5) = 48

    Handle the new instructions; what do you get if you add up all of the
    results of just the enabled multiplications?

    Your puzzle answer was 94455185.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


with open(Path(__file__).parent / "2024_03_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")

SAMPLE1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
SAMPLE2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def find_mul(memory: str) -> int:
    matches = re.findall("mul\((\d*),(\d*)\)", memory)
    return sum(int(a) * int(b) for a, b in matches)


def test_find_mul():
    assert find_mul("mul(4*") == 0
    assert find_mul("mul(6,9!") == 0
    assert find_mul("?(12,34)") == 0
    assert find_mul("mul ( 2 , 4 )") == 0
    assert find_mul(SAMPLE1) == 161
    assert find_mul("".join(RAW_INPUT)) == 187833789


def find_mul2(memory: str) -> int:
    matches = re.findall("mul\((\d*),(\d*)\)|(do)\(\)|(don't)\(\)", memory)
    enabled = True
    total = 0
    for a, b, on, off in matches:
        if len(on):
            enabled = True
        elif len(off):
            enabled = False
        elif enabled and len(a) and len(b):
            total += int(a) * int(b)
    return total


def test_find_mul2():
    assert find_mul2(SAMPLE2) == 48
    assert find_mul2("".join(RAW_INPUT)) == 94455185
