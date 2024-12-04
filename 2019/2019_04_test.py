class Puzzle:
    """
    --- Day 4: Secure Container ---
    You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the
    password on a sticky note, but someone threw it out.

    However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same
    (like 111123 or 135679).
    Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).
    How many different passwords within the range given in your puzzle input meet these criteria?

    Your puzzle answer was 1764.

    --- Part Two ---
    An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger
    group of matching digits.

    Given this additional criterion, but still ignoring the range rule, the following are now true:

    112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
    How many different passwords within the range given in your puzzle input meet all of the criteria?

    Your puzzle answer was 1196.
    """
    pass


def password_is_valid(password: int) -> bool:
    password = str(password)
    previous = -1
    run_len = 0
    double = False
    for p in password:
        if previous > int(p):
            return False
        if previous == int(p):
            run_len += 1
        else:
            if run_len == 1:
                double = True
            run_len = 0
        previous = int(p)
    if run_len == 1:
        double = True
    return double


def test_password_is_valid_returns_true_when_input_has_repeated_string():
    assert password_is_valid(123455)


def test_password_is_valid_returns_false_when_input_has_no_repeated_string():
    assert not password_is_valid(123456)


def test_password_is_valid_returns_false_when_input_has_only_repeated_string_longer_than_2():
    assert not password_is_valid(122256)


def test_password_is_valid_returns_true_if_values_do_not_decrease():
    assert password_is_valid(124456)


def test_password_is_valid_returns_false_if_values_do_decrease():
    assert not password_is_valid(123450)


MYINPUT_MIN = 152085
MYINPUT_MAX = 670283


def test_submission():
    assert sum([1 if password_is_valid(d) else 0 for d in range(MYINPUT_MIN, MYINPUT_MAX+1)]) == 1196 # orig 1764
