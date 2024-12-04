from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 8: I Heard You Like Registers ---
    You receive a signal directly from the CPU. Because of your recent assistance with jump instructions,
    it would like you to compute the result of a series of unusual register instructions.

    Each instruction consists of several parts: the register to modify, whether to increase or decrease
    that register's value, the amount by which to increase or decrease it, and a condition.

    If the condition fails, skip the instruction without modifying the register.
    The registers all start at 0.

    The instructions look like this:

    b inc 5 if a > 1
    a inc 1 if b < 5
    c dec -10 if a >= 1
    c inc -20 if c == 10

    These instructions would be processed as follows:

    Because a starts at 0, it is not greater than 1, and so b is not modified.
    a is increased by 1 (to 1) because b is less than 5 (it is 0).
    c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
    c is increased by -20 (to -10) because c is equal to 10.
    After this process, the largest value in any register is 1.

    You might also encounter <= (less than or equal to) or != (not equal to).
    However, the CPU doesn't have the bandwidth to tell you what all the registers are named,
    and leaves that to you to determine.

    What is the largest value in any register after completing the instructions in your puzzle input?

    --- Part Two ---
    To be safe, the CPU also needs to know the highest value held in any register during this process so
    that it can decide how much memory to allocate to these operations. For example, in the above instructions,
    the highest value ever held was 10 (in register c after the third instruction was evaluated).
    """

    pass


SAMPLE = [
    "b inc 5 if a > 1",
    "a inc 1 if b < 5",
    "c dec -10 if a >= 1",
    "c inc -20 if c == 10",
]

with open(Path(__file__).parent / "2017_08_input.txt") as fp:
    INPUT = [line.strip() for line in fp]


def process_registers(instructions):
    registers = defaultdict(int)
    max_reg_value = 0
    for inst in instructions:
        change, condition = inst.split(" if ")
        check_loc, comparison, value = condition.split(" ")

        if comparison == "<":
            ok = registers[check_loc] < int(value)
        elif comparison == ">":
            ok = registers[check_loc] > int(value)
        elif comparison == "<=":
            ok = registers[check_loc] <= int(value)
        elif comparison == ">=":
            ok = registers[check_loc] >= int(value)
        elif comparison == "==":
            ok = registers[check_loc] == int(value)
        elif comparison == "!=":
            ok = registers[check_loc] != int(value)

        if ok:
            change_loc, direction, value = change.split(" ")
            if direction == "inc":
                registers[change_loc] += int(value)
            elif direction == "dec":
                registers[change_loc] -= int(value)
            max_reg_value = max(registers[change_loc], max_reg_value)
    return registers, max_reg_value


def test_process_registers():
    sample_result = process_registers(SAMPLE)
    assert max(v for k, v in sample_result[0].items()) == 1
    assert sample_result[1] == 10
    #
    puzzle_result = process_registers(INPUT)
    assert max(v for k, v in puzzle_result[0].items()) == 4647
    assert puzzle_result[1] == 5590
