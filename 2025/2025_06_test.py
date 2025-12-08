from pathlib import Path
from typing import List
from math import prod


class Puzzle:
    """
    --- Day 6: Trash Compactor ---
    After helping the Elves in the kitchen, you were taking a break and helping
    them re-enact a movie scene when you over-enthusiastically jumped into the
    garbage chute!

    A brief fall later, you find yourself in a garbage smasher. Unfortunately,
    the door's been magnetically sealed.

    As you try to find a way out, you are approached by a family of cephalopods!
    They're pretty sure they can get the door open, but it will take some time.
    While you wait, they're curious if you can help the youngest cephalopod with
    her math homework.

    Cephalopod math doesn't look that different from normal math. The math
    worksheet (your puzzle input) consists of a list of problems; each problem
    has a group of numbers that need to either be either added (+) or multiplied
    (*) together.

    However, the problems are arranged a little strangely; they seem to be
    presented next to each other in a very long horizontal list. For example:

    123 328  51 64
    45 64  387 23
    6 98  215 314
    *   +   *   +

    Each problem's numbers are arranged vertically; at the bottom of the problem
    is the symbol for the operation that needs to be performed. Problems are
    separated by a full column of only spaces. The left/right alignment of
    numbers within each problem can be ignored.

    So, this worksheet contains four problems:

    123 * 45 * 6 = 33210
    328 + 64 + 98 = 490
    51 * 387 * 215 = 4243455
    64 + 23 + 314 = 401

    To check their work, cephalopod students are given the grand total of adding
    together all of the answers to the individual problems. In this worksheet,
    the grand total is 33210 + 490 + 4243455 + 401 = 4277556.

    Of course, the actual worksheet is much wider. You'll need to make sure to
    unroll it completely so that you can read the problems clearly.

    Solve the problems on the math worksheet. What is the grand total found by
    adding together all of the answers to the individual problems?

    Your puzzle answer was 4719804927602.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The big cephalopods come back to check on how things are going. When they
    see that your grand total doesn't match the one expected by the worksheet,
    they realize they forgot to explain how to read cephalopod math.

    Cephalopod math is written right-to-left in columns. Each number is given in
    its own column, with the most significant digit at the top and the least
    significant digit at the bottom. (Problems are still separated with a column
    consisting only of spaces, and the symbol at the bottom of the problem is
    still the operator to use.)

    Here's the example worksheet again:

    123 328  51 64
     45 64  387 23
      6 98  215 314
    *   +   *   +

    Reading the problems right-to-left one column at a time, the problems are
    now quite different:

    The rightmost problem is 4 + 431 + 623 = 1058
    The second problem from the right is 175 * 581 * 32 = 3253600
    The third problem from the right is 8 + 248 + 369 = 625
    Finally, the leftmost problem is 356 * 24 * 1 = 8544
    Now, the grand total is 1058 + 3253600 + 625 + 8544 = 3263827.

    Solve the problems on the math worksheet again. What is the grand total
    found by adding together all of the answers to the individual problems?

    Your puzzle answer was 9608327000261.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open(Path(__file__).parent / "2025_06_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")
    RAW_INPUT.pop()

SAMPLE = ["123 328  51 64 ", " 45 64  387 23 ", "  6 98  215 314", "*   +   *   +  "]


def do_math(input_list: List[str]) -> int:
    ops = [c for c in input_list.pop().split(" ") if c != ""]
    running_total = [int(c) for c in input_list.pop().split(" ") if c != ""]
    while input_list:
        next_numbers = [int(c) for c in input_list.pop().split(" ") if c != ""]
        for i, nn in enumerate(next_numbers):
            if ops[i] == "*":
                running_total[i] *= nn
            elif ops[i] == "+":
                running_total[i] += nn
    return sum(running_total)


def test_math():
    assert do_math(SAMPLE) == 4277556
    assert do_math(RAW_INPUT) == 4719804927602


def do_more_math(input_list: List[str]) -> int:
    ops = input_list.pop()
    raw_array = [[] for c in ops]
    for raw_ln in input_list:
        for row, c in enumerate(raw_ln):
            raw_array[row].append(c)
    digit_array = ["".join(row) for row in raw_array]
    running_sum = 0
    op_list = []
    for op, number in zip(reversed(ops), reversed(digit_array)):
        if number.strip() == "":
            op_list = []
        else:
            op_list.append(int(number))
        if op == "*":
            running_sum += prod(op_list)
        if op == "+":
            running_sum += sum(op_list)
    return running_sum


def test_more_math():
    assert do_more_math(SAMPLE) == 3263827
    assert do_more_math(RAW_INPUT) == 9608327000261
