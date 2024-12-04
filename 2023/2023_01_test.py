from pathlib import Path


class Puzzle:
    """
    --- Day 1: Trebuchet?! ---
    Something is wrong with global snow production, and you've been selected to take a
    look. The Elves have even given you a map; on it, they've used stars to mark the
    top fifty locations that are likely to be having problems.

    You've been doing this long enough to know that to restore snow operations, you
    need to check all fifty stars by December 25th.

    Collect stars by solving puzzles. Two puzzles will be made available on each day in
    the Advent calendar; the second puzzle is unlocked when you complete the first.
    Each puzzle grants one star. Good luck!

    You try to ask why they can't just use a weather machine ("not powerful enough")
    and where they're even sending you ("the sky") and why your map looks mostly blank
    ("you sure ask a lot of questions") and hang on did you just say the sky ("of
    course, where do you think snow comes from") when you realize that the Elves are
    already loading you into a trebuchet ("please hold still, we need to strap you in").

    As they're making the final adjustments, they discover that their calibration
    document (your puzzle input) has been amended by a very young Elf who was apparently
    just excited to show off her art skills. Consequently, the Elves are having trouble
    reading the values on the document.

    The newly-improved calibration document consists of lines of text; each line
    originally contained a specific calibration value that the Elves now need to
    recover. On each line, the calibration value can be found by combining the first
    digit and the last digit (in that order) to form a single two-digit number.

    For example:

    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet

    In this example, the calibration values of these four lines are 12, 38, 15, and 77.
    Adding these together produces 142.

    Consider your entire calibration document. What is the sum of all of the
    calibration values?

    Your puzzle answer was 55386.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    Your calculation isn't quite right. It looks like some of the digits are
    actually spelled out with letters: one, two, three, four, five, six,
    seven, eight, and nine also count as valid "digits".

    Equipped with this new information, you now need to find the real first
    and last digit on each line. For example:

    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen

    In this example, the calibration values are 29, 83, 13, 24, 42, 14,
    and 76. Adding these together produces 281.

    What is the sum of all of the calibration values?
    """


with open(Path(__file__).parent / "2023_01_input.txt") as fp:
    RAW_INPUT = fp.read()

RAW_SAMPLE = """1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet"""

RAW_SAMPLE_2 = """two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen"""

STRING_TO_DIGIT = {
    "eight": "8",
    "four": "4",
    "five": "5",
    "nine": "9",
    "one": "1",
    "six": "6",
    "seven": "7",
    "three": "3",
    "two": "2",
}


def replace_digit_strings(cal_str):
    """
    BUG: With this approach the last digit might be combined with something like
         123oneight. Parsing forward we would get the one and reject the last ight,
         but if we read from the end we should pull eight as the last digit...
    """

    fixed = ""
    to_check = cal_str
    while to_check:
        no_match = True
        for w, v in STRING_TO_DIGIT.items():
            if w == to_check[: len(w)]:
                fixed += v
                to_check = to_check[len(w) :]
                no_match = False
                break
        if no_match:
            fixed += to_check[:1]
            to_check = to_check[1:]
    return fixed


def find_digit(cal_str, reversed=False):
    to_check = cal_str[::-1] if reversed else cal_str
    while to_check:
        if to_check[0].isdigit():
            return to_check[0]
        for w, v in STRING_TO_DIGIT.items():
            w_test = w[::-1] if reversed else w
            if w_test == to_check[: len(w)]:
                return v
        to_check = to_check[1:]
    return None


def parse_input(raw_string, map_words=False):
    cal_list = raw_string.split("\n")
    if map_words:
        cal_list = [replace_digit_strings(ln) for ln in cal_list]
    digits_only = [[c for c in ln if c.isdigit()] for ln in cal_list]
    return [int(f"{d[0]}{d[-1]}") for d in digits_only]


def parse_input_2(raw_string):
    cal_list = raw_string.split("\n")
    return [int(f"{find_digit(d)}{find_digit(d,reversed=True)}") for d in cal_list]


def test_parse_input():
    parsed_sample = parse_input(RAW_SAMPLE)
    assert parsed_sample == [12, 38, 15, 77]

    parsed_sample = parse_input(RAW_SAMPLE_2, map_words=True)
    assert parsed_sample == [29, 83, 13, 24, 42, 14, 76]

    parsed_sample = parse_input_2(RAW_SAMPLE_2)
    assert parsed_sample == [29, 83, 13, 24, 42, 14, 76]

    # now puzzle input
    parsed_inputs = parse_input(RAW_INPUT)
    assert sum(parsed_inputs) == 55386

    parsed_inputs = parse_input_2(RAW_INPUT)
    assert sum(parsed_inputs) == 54824
    # Initial 54807 was too low, see BUG noted above?
