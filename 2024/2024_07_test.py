from pathlib import Path
from typing import List, NamedTuple
from collections import defaultdict


class Puzzle:
    """
        --- Day 7: Bridge Repair ---
        The Historians take you to a familiar rope bridge over a river in the middle
        of a jungle. The Chief isn't on this side of the bridge, though; maybe he's
        on the other side?

        When you go to cross the bridge, you notice a group of engineers trying to
        repair it. (Apparently, it breaks pretty frequently.) You won't be able to
        cross until it's fixed.

        You ask how long it'll take; the engineers tell you that it only needs final
        calibrations, but some young elephants were playing nearby and stole all the
        operators from their calibration equations! They could finish the
        calibrations if only someone could determine which test values could
        possibly be produced by placing any combination of operators into their
        calibration equations (your puzzle input).

        For example:

        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20

        Each line represents a single equation. The test value appears before the
        colon on each line; it is your job to determine whether the remaining
        numbers can be combined with operators to produce the test value.

        Operators are always evaluated left-to-right, not according to precedence
        rules. Furthermore, numbers in the equations cannot be rearranged. Glancing
        into the jungle, you can see elephants holding two different types of
        operators: add (+) and multiply (*).

        Only three of the above equations can be made true by inserting operators:

        190: 10 19 has only one position that accepts an operator: between 10 and
        19. Choosing + would give 29, but choosing * would give the test value (10 *
        19 = 190).

        3267: 81 40 27 has two positions for operators. Of the four possible
        configurations of the operators, two cause the right side to match the test
        value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated
        left-to-right)!

        292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

        The engineers just need the total calibration result, which is the sum of
        the test values from just the equations that could possibly be true. In the
        above example, the sum of the test values for the three equations listed
        above is 3749.

        Determine which equations could possibly be true. What is their total calibration result?

    Your puzzle answer was 8401132154762.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---

    The engineers seem concerned; the total calibration result you gave them is
    nowhere close to being within safety tolerances. Just then, you spot your
    mistake: some well-hidden elephants are holding a third type of operator.

    The concatenation operator (||) combines the digits from its left and right
    inputs into a single number. For example, 12 || 345 would become 12345. All
    operators are still evaluated left-to-right.

    Now, apart from the three equations that could be made true using only addition
    and multiplication, the above example has three more equations that can be made
    true by inserting operators:

    156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
    7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
    192: 17 8 14 can be made true using 17 || 8 + 14.

    Adding up all six test values (the three that could be made before using only +
    and * plus the new three that can now be made by also using ||) produces the new
    total calibration result of 11387.

    Using your new knowledge of elephant hiding spots, determine which equations
    could possibly be true. What is their total calibration result?

    Your puzzle answer was 95297119227552.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


with open(Path(__file__).parent / "2024_07_input.txt") as fp:
    MY_INPUTS = {
        int(raw_ans): [int(raw_in) for raw_in in raw_inputs.split(" ")]
        for (raw_ans, raw_inputs) in [ln.split(": ") for ln in fp.read().split("\n")]
    }

SAMPLE_INPUTS = {
    190: [10, 19],
    3267: [81, 40, 27],
    83: [17, 5],
    156: [15, 6],
    7290: [6, 8, 6, 15],
    161011: [16, 10, 13],
    192: [17, 8, 14],
    21037: [9, 7, 18, 13],
    292: [11, 6, 16, 20],
}


def inputs_check(answer: int, inputs: List[int], enhanced=False) -> bool:
    to_check = [inputs[::-1]]
    while to_check:
        inputs = to_check.pop()
        if len(inputs) == 1:
            if answer == inputs[0]:
                return True
            continue
        first = inputs.pop()
        second = inputs.pop()
        if first + second <= answer:
            inputs_with_sum = inputs[:]
            inputs_with_sum.append(first + second)
            to_check.append(inputs_with_sum)
        if first * second <= answer:
            inputs_with_prod = inputs[:]
            inputs_with_prod.append(first * second)
            to_check.append(inputs_with_prod)
        if enhanced and int(f"{first}{second}") <= answer:
            inputs_with_concat = inputs[:]
            inputs_with_concat.append(int(f"{first}{second}"))
            to_check.append(inputs_with_concat)
    return False


def sum_valid_inputs(input_dict, enhanced=False) -> int:
    return sum(
        answer
        for answer, inputs in input_dict.items()
        if inputs_check(answer, inputs, enhanced)
    )


def test_input_check():
    expected_test_results = {
        190: True,
        3267: True,
        83: False,
        156: False,
        7290: False,
        161011: False,
        192: False,
        21037: False,
        292: True,
    }
    for answer, inputs in SAMPLE_INPUTS.items():
        assert inputs_check(answer, inputs) == expected_test_results[answer]
    assert sum_valid_inputs(SAMPLE_INPUTS) == 3749
    assert sum_valid_inputs(MY_INPUTS) == 8401132154762


def test_enhanced_input_check():
    expected_test_results = {
        190: True,
        3267: True,
        83: False,
        156: True,
        7290: True,
        161011: False,
        192: True,
        21037: False,
        292: True,
    }
    for answer, inputs in SAMPLE_INPUTS.items():
        assert (
            inputs_check(answer, inputs, enhanced=True) == expected_test_results[answer]
        )
    assert sum_valid_inputs(SAMPLE_INPUTS, enhanced=True) == 11387
    assert sum_valid_inputs(MY_INPUTS, enhanced=True) == 95297119227552
