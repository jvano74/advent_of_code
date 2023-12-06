from typing import NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 3: Gear Ratios ---
    You and the Elf eventually reach a gondola lift station; he says the gondola
    lift will take you up to the water source, but this is as far as he can
    bring you. You go inside.

    It doesn't take long to find the gondolas, but there seems to be a problem:
    they're not moving.

    "Aaah!"

    You turn around to see a slightly-greasy Elf with a wrench and a look of
    surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working
    right now; it'll still be a while before I can fix it." You offer to help.

    The engineer explains that an engine part seems to be missing from the
    engine, but nobody can figure out which one. If you can add up all the part
    numbers in the engine schematic, it should be easy to work out which part is
    missing.

    The engine schematic (your puzzle input) consists of a visual representation
    of the engine. There are lots of numbers and symbols you don't really
    understand, but apparently any number adjacent to a symbol, even diagonally,
    is a "part number" and should be included in your sum. (Periods (.) do not
    count as a symbol.)

    Here is an example engine schematic:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

    In this schematic, two numbers are not part numbers because they are not
    adjacent to a symbol: 114 (top right) and 58 (middle right). Every other
    number is adjacent to a symbol and so is a part number; their sum is 4361.

    Of course, the actual engine schematic is much larger. What is the sum of
    all of the part numbers in the engine schematic?

    Your puzzle answer was 535078.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The engineer finds the missing part and installs it in the engine! As
    the engine springs to life, you jump in the closest gondola, finally
    ready to ascend to the water source.

    You don't seem to be going very fast, though. Maybe something is still
    wrong? Fortunately, the gondola has a phone labeled "help", so you pick
    it up and the engineer answers.

    Before you can explain the situation, she suggests that you look out the
    window. There stands the engineer, holding a phone in one hand and waving
    with the other. You're going so slowly that you haven't even left the
    station. You exit the gondola.

    The missing part wasn't the only issue - one of the gears in the engine is
    wrong. A gear is any * symbol that is adjacent to exactly two part numbers.
    Its gear ratio is the result of multiplying those two numbers together.

    This time, you need to find the gear ratio of every gear and add them all up
    so that the engineer can figure out which gear needs to be replaced.

    Consider the same engine schematic again:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

    In this schematic, there are two gears. The first is in the top left; it has
    part numbers 467 and 35, so its gear ratio is 16345. The second gear is in
    the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a
    gear because it is only adjacent to one part number.) Adding up all of the
    gear ratios produces 467835.

    What is the sum of all of the gear ratios in your engine schematic?

    Your puzzle answer was 75312571.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open("day_03_input.txt") as fp:
    RAW_INPUT = fp.read()


RAW_SAMPLE = """
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
"""


class Pt(NamedTuple):
    x: str
    y: int

    def neighbors(self, width=1):
        neighbors = set()
        y = self.y
        for x in range(self.x - 1, self.x + width + 1):
            neighbors.add(Pt(x, y + 1))
            neighbors.add(Pt(x, y))
            neighbors.add(Pt(x, y - 1))
        return neighbors


class Engine:
    def __init__(self, raw_diagram) -> None:
        self.diagram = dict()
        self.part_num = dict()
        self.parts = defaultdict(lambda: defaultdict(set))
        lines = reversed(raw_diagram.split("\n"))
        y = 0
        for line in lines:
            y += 1
            x = 0
            start = None
            for c in line:
                x += 1
                pt = Pt(x, y)
                if c.isdigit():
                    if start is None:
                        start = pt
                        num = c
                    else:
                        num += c
                    continue
                if start:
                    # end of a digit
                    self.part_num[start] = int(num)
                    start = None
                if not (c == "." or c == " "):
                    self.diagram[pt] = c
            if start:
                # end of a digit
                self.part_num[start] = int(num)
                start = None

    def link_parts(self):
        found_total = 0
        for number_start, number in self.part_num.items():
            width = len(str(number))
            found = False
            for test_point in number_start.neighbors(width=width):
                if test_point in self.diagram:
                    found = True
                    part = self.diagram[test_point]
                    self.parts[part][test_point].add(number)
            if found:
                found_total += number
        return found_total


def mul_set(numbers):
    result = 1
    for number in numbers:
        result *= number
    return result


def find_gear_ratio_sum(parts):
    return sum(
        mul_set(numbers) for part, numbers in parts["*"].items() if len(numbers) > 1
    )


def test_engine():
    sample_engine = Engine(RAW_SAMPLE)
    assert sample_engine.link_parts() == 4361
    assert find_gear_ratio_sum(sample_engine.parts) == 467835
    my_engine = Engine(RAW_INPUT)
    assert my_engine.link_parts() == 535078
    assert find_gear_ratio_sum(my_engine.parts) == 75312571
