from pathlib import Path
from typing import NamedTuple
import re


with open(Path(__file__).parent / "2020_18_input.txt") as fp:
    INPUT = [ln.strip() for ln in fp]


class Puzzle:
    """
    --- Day 18: Operation Order ---
    As you look out the window and notice a heavily-forested continent slowly appear over
    the horizon, you are interrupted by the child sitting next to you. They're curious if
    you could help them with their math homework.

    Unfortunately, it seems like this "math" follows different rules than you remember.

    The homework (your puzzle input) consists of a series of expressions that consist of
    addition (+), multiplication (*), and parentheses ((...)). Just like normal math,
    parentheses indicate that the expression inside must be evaluated before it can be
    used by the surrounding expression. Addition still finds the sum of the numbers
    on both sides of the operator, and multiplication still finds the product.

    However, the rules of operator precedence have changed. Rather than evaluating
    multiplication before addition, the operators have the same precedence, and are
    evaluated left-to-right regardless of the order in which they appear.

    For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6
    are as follows:

    1 + 2 * 3 + 4 * 5 + 6
      3   * 3 + 4 * 5 + 6
          9   + 4 * 5 + 6
             13   * 5 + 6
                 65   + 6
                     71

    Parentheses can override this order; for example, here is what happens if parentheses
    are added to form 1 + (2 * 3) + (4 * (5 + 6)):

    1 + (2 * 3) + (4 * (5 + 6))
    1 +    6    + (4 * (5 + 6))
         7      + (4 * (5 + 6))
         7      + (4 *   11   )
         7      +     44
                51

    Here are a few more examples:

    2 * 3 + (4 * 5) becomes 26.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

    Before you can help with the homework, you need to understand it yourself.
    Evaluate the expression on each line of the homework; what is the sum of
    the resulting values?

    --- Part Two ---
    You manage to answer the child's questions and they finish part 1 of their homework,
    but get stuck when they reach the next section: advanced math.

    Now, addition and multiplication have different precedence levels, but they're not the ones
    you're familiar with. Instead, addition is evaluated before multiplication.

    For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:

    1 + 2 * 3 + 4 * 5 + 6
      3   * 3 + 4 * 5 + 6
      3   *   7   * 5 + 6
      3   *   7   *  11
         21       *  11
             231

    Here are the other examples from above:

    1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
    2 * 3 + (4 * 5) becomes 46.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.

    What do you get if you add up the results of evaluating the homework problems using these new rules?
    """

    pass


def evaluate_expression(input_string):
    stack_values = []
    stack_operations = []
    accumulator = 0
    stack_remaining = list(reversed(input_string.split(" ")))
    stack_remaining.append("+")
    if (len(stack_remaining) % 2) == 1:
        raise Exception("Unexpected number of arguments")
    while len(stack_remaining) > 0:
        operation = stack_remaining.pop()
        right = stack_remaining.pop()
        if str(right)[0] == "(":
            stack_operations.append(operation)
            stack_values.append(accumulator)
            accumulator = 0
            stack_remaining.append(right[1:])
            stack_remaining.append("+")
        elif str(right)[-1] == ")":
            right, remaining_parentheses = right.split(")", 1)
            if operation == "+":
                accumulator += int(right)
            elif operation == "*":
                accumulator *= int(right)
            stack_remaining.append(f"{accumulator}{remaining_parentheses}")
            stack_remaining.append(stack_operations.pop())
            accumulator = stack_values.pop()
        elif operation == "+":
            accumulator += int(right)
        elif operation == "*":
            accumulator *= int(right)
        else:
            raise Exception("Unexpected character")
    return accumulator


def test_evaluate_expression():
    assert evaluate_expression("1 + 2 * 3 + 4 * 5 + 6") == 71
    assert evaluate_expression("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert evaluate_expression("2 * 3 + (4 * 5)") == 26
    assert evaluate_expression("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
    assert sum(evaluate_expression(ln) for ln in INPUT) == 45840336521334


def evaluate_advanced_expression_orig(input_string):
    stack_values = []
    stack_operations = []
    accumulator = 0
    accumulator_multiplier = 1
    stack_remaining = list(reversed(input_string.split(" ")))
    stack_remaining.append("+")
    if (len(stack_remaining) % 2) == 1:
        raise Exception("Unexpected number of arguments")
    while len(stack_remaining) > 0:
        operation = stack_remaining.pop()
        right = stack_remaining.pop()
        if str(right)[0] == "(":
            # stack accumulator_multiplier
            if accumulator_multiplier != 1:
                stack_operations.append("*")
                stack_values.append(accumulator_multiplier)
                accumulator_multiplier = 1
            stack_operations.append(operation)
            stack_values.append(accumulator)
            accumulator = 0
            stack_remaining.append(right[1:])
            stack_remaining.append("+")
        elif str(right)[-1] == ")":
            right, remaining_parentheses = right.split(")", 1)
            if operation == "+":
                accumulator += int(right)
            elif operation == "*":
                accumulator_multiplier *= accumulator
                accumulator = int(right)
            accumulator *= accumulator_multiplier
            accumulator_multiplier = 1
            stack_remaining.append(f"{accumulator}{remaining_parentheses}")
            stack_remaining.append(stack_operations.pop())
            accumulator = stack_values.pop()
        elif operation == "+":
            accumulator += int(right)
        elif operation == "*":
            accumulator_multiplier *= accumulator
            accumulator = int(right)
        else:
            raise Exception("Unexpected character")
    accumulator *= accumulator_multiplier
    print(stack_values, stack_operations)
    while len(stack_values) > 0:
        operation = stack_operations.pop()
        left = stack_values.pop()
        if operation == "+":
            accumulator += left
        elif operation == "*":
            accumulator *= left
    return accumulator


class Nn(NamedTuple):
    x: int

    def __add__(self, other):
        return Nn(self.x * other.x)

    def __mul__(self, other):
        return Nn(self.x + other.x)


def parse_with_nn(expression):
    expression = expression.replace("*", "^")
    expression = expression.replace("+", "*")
    expression = expression.replace("^", "+")
    expression = re.sub(r"(\d+)", r"Nn(\1)", expression)
    return eval(expression)


def evaluate_advanced_expression(exp):
    return parse_with_nn(exp).x


def test_evaluate_advanced_expression():
    assert evaluate_advanced_expression("1 + 2 * 3 + 4 * 5 + 6") == 231
    assert evaluate_advanced_expression("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert evaluate_advanced_expression("2 * 3 + (4 * 5)") == 46
    assert evaluate_advanced_expression("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert (
        evaluate_advanced_expression("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
        == 669060
    )
    assert (
        evaluate_advanced_expression("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
        == 23340
    )

    assert sum(evaluate_advanced_expression(ln) for ln in INPUT) == 328920644404583
    # 324051314221437 is too low
