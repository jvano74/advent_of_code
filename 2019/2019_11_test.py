from pathlib import Path
from typing import List, NamedTuple
from collections import defaultdict
import pytest


class Puzzle:
    """
    --- Day 11: Space Police ---
    On the way to Jupiter, you're pulled over by the Space Police.

    "Attention, unmarked spacecraft! You are in violation of Space Law! All spacecraft must have a clearly visible
    registration identifier! You have 24 hours to comply or be sent to Space Jail!"

    Not wanting to be sent to Space Jail, you radio back to the Elves on Earth for help. Although it takes almost three
    hours for their reply signal to reach you, they send instructions for how to power up the emergency hull painting
    robot and even provide a small Intcode program (your puzzle input) that will cause it to paint your ship
    appropriately.

    There's just one problem: you don't have an emergency hull painting robot.

    You'll need to build a new emergency hull painting robot. The robot needs to be able to move around on the grid
    of square panels on the side of your ship, detect the color of its current panel, and paint its current panel
    black or white. (All of the panels are currently black.)

    The Intcode program will serve as the brain of the robot. The program uses input instructions to access the
    robot's camera: provide 0 if the robot is over a black panel or 1 if the robot is over a white panel. Then,
    the program will output two values:

    First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the
    panel black, and 1 means to paint the panel white.

    Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90
    degrees, and 1 means it should turn right 90 degrees.

    After the robot turns, it should always move forward exactly one panel. The robot starts facing up.

    The robot will continue running for a while like this and halt when it is finished drawing. Do not restart the
    Intcode computer inside the robot during this process.

    For example, suppose the robot is about to start running. Drawing black panels as ., white panels as #, and the
    robot pointing the direction it is facing (< ^ > v), the initial state and region near the robot looks like this:

    .....
    .....
    ..^..
    .....
    .....

    The panel under the robot (not visible here because a ^ is shown instead) is also black, and so any input
    instructions at this point should be provided 0. Suppose the robot eventually outputs 1 (paint white) and
    then 0 (turn left). After taking these actions and moving forward one panel, the region now looks like this:

    .....
    .....
    .<#..
    .....
    .....

    Input instructions should still be provided 0. Next, the robot might output 0 (paint black) and
    then 0 (turn left):

    .....
    .....
    ..#..
    .v...
    .....

    After more outputs (1,0, 1,0):

    .....
    .....
    ..^..
    .##..
    .....

    The robot is now back where it started, but because it is now on a white panel, input instructions should be
    provided 1. After several more outputs (0,1, 1,0, 1,0), the area looks like this:

    .....
    ..<#.
    ...#.
    .##..
    .....

    Before you deploy the robot, you should probably have an estimate of the area it will cover: specifically, you
    need to know the number of panels it paints at least once, regardless of color. In the example above, the robot
    painted 6 panels at least once. (It painted its starting panel twice, but that panel is still only counted once;
    it also never painted the panel it ended on.)

    Build a new emergency hull painting robot and run the Intcode program on it. How many panels does it paint at
    least once?

    Your puzzle answer was 2319.

    --- Part Two ---
    You're not sure what it's trying to paint, but it's definitely not a registration identifier. The Space Police
    are getting impatient.

    Checking your external ship cameras again, you notice a white panel marked "emergency hull painting robot starting
    panel". The rest of the panels are still black, but it looks like the robot was expecting to start on a white
    panel, not a black one.

    Based on the Space Law Space Brochure that the Space Police attached to one of your windows, a valid registration
    identifier is always eight capital letters. After starting the robot on a single white panel instead, what
    registration identifier does it paint on your hull?

    Your puzzle answer was UERPRFGJ.
    """

    pass


class Point(NamedTuple):
    x: int
    y: int


DIRECTION = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]
HALT = 99
ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUAL = 8
BASE = 9


class Program:
    def __init__(self, program):
        self.head = 0
        self.relative_base = 0
        self.disk = list(program)
        self.memory = list(program)
        self.input = []
        self.output = []
        self.opt_hx = []

    def reset(self):
        self.head = 0
        self.relative_base = 0
        self.memory = list(self.disk)
        self.input = []
        self.output = []
        self.opt_hx = []

    def process(self, op_code, modes):
        if op_code in [INPUT, OUTPUT, BASE]:
            self.process_one_parameter_operation(modes, op_code)
        elif op_code in [JUMP_IF_TRUE, JUMP_IF_FALSE]:
            self.process_two_parameter_operation(modes, op_code)
        elif op_code in [ADD, MULTIPLY, LESS_THAN, EQUAL]:
            self.process_three_parameter_operation(modes, op_code)
        else:
            raise SyntaxError(f"Unknown optcode {op_code}\nOpt Hx:\n{self.opt_hx}")

    def read_memory(self, pos):
        if len(self.memory) - 1 < pos:
            self.memory.extend([0] * (pos + 1 - len(self.memory)))
        return self.memory[pos]

    def write_memory(self, pos, mode, val):
        if mode == 2:
            pos += self.relative_base
        if len(self.memory) - 1 < pos:
            self.memory.extend([0] * (pos + 1 - len(self.memory)))
        self.memory[pos] = val

    def get_val(self, offset=1, mode=0):
        val = self.read_memory(self.head + offset)
        if mode == 0:
            return self.read_memory(val)
        if mode == 2:
            return self.read_memory(self.relative_base + val)
        return val

    def process_one_parameter_operation(self, modes, op_code):
        if op_code == INPUT:
            if len(self.input) == 0:
                return
            mem_loc = self.memory[self.head + 1]
            self.write_memory(mem_loc, modes % 10, self.input.pop(0))
        elif op_code == OUTPUT:
            self.output.append(self.get_val(1, modes % 10))
        elif op_code == BASE:
            self.relative_base += self.get_val(1, modes % 10)
        else:
            raise SyntaxError(f"Unknown op_code {op_code}")
        self.head += 2

    def process_two_parameter_operation(self, modes, op_code):
        reg_a = self.get_val(1, modes % 10)
        modes //= 10
        reg_b = self.get_val(2, modes % 10)
        if op_code == JUMP_IF_TRUE:
            if reg_a:
                self.head = reg_b
                return
        elif op_code == JUMP_IF_FALSE:
            if not reg_a:
                self.head = reg_b
                return
        else:
            raise SyntaxError(f"Unknown op_code {op_code}")
        self.head += 3

    def process_three_parameter_operation(self, modes, op_code):
        reg_a = self.get_val(1, modes % 10)
        modes //= 10
        reg_b = self.get_val(2, modes % 10)
        modes //= 10
        mem_loc = self.memory[self.head + 3]
        if op_code == ADD:
            self.write_memory(mem_loc, modes % 10, reg_a + reg_b)
        elif op_code == MULTIPLY:
            self.write_memory(mem_loc, modes % 10, reg_a * reg_b)
        elif op_code == LESS_THAN:
            self.write_memory(mem_loc, modes % 10, 1 if reg_a < reg_b else 0)
        elif op_code == EQUAL:
            self.write_memory(mem_loc, modes % 10, 1 if reg_a == reg_b else 0)
        else:
            raise SyntaxError(f"Unknown op_code {op_code}")
        self.head += 4

    def run(self, std_in: List[int] = None) -> int:
        if std_in is not None:
            self.input = std_in
        while True:
            op_code = self.memory[self.head] % 100
            modes = self.memory[self.head] // 100
            if op_code == HALT:
                return 0
            if op_code == INPUT and len(self.input) == 0:
                return -1
            self.process(op_code, modes)


with open(Path(__file__).parent / "2019_11_input.txt") as fp:
    raw = fp.read()
SRC = [int(d) for d in raw.split(",")]
PAINT = Program(SRC)


class Robot:
    def __init__(self, program):
        self.program = program
        self.grid = defaultdict(int)
        self.loc = Point(0, 0)
        self.min = Point(0, 0)
        self.max = Point(0, 0)
        self.orientation = 0

    def move(self):
        steps = 0
        painted = set()
        while True:
            color = self.grid[self.loc]
            self.program.input.append(color)
            steps += 1
            # if steps % 10 == 0 and steps < 100:
            #     print()
            #     print(steps, self.min, self.max)
            #     self.draw()
            #     print()
            if self.program.run() == 0:
                return steps, len(painted), len(self.grid)
            self.grid[self.loc] = self.program.output.pop(0)
            painted.add(self.loc)
            self.orientation = (
                self.orientation + 2 * self.program.output.pop(0) - 1
            ) % 4
            delta = DIRECTION[self.orientation]
            self.loc = Point(self.loc.x + delta.x, self.loc.y + delta.y)
            self.min = Point(min(self.min.x, self.loc.x), min(self.min.y, self.loc.y))
            self.max = Point(max(self.max.x, self.loc.x), max(self.max.y, self.loc.y))

    def draw(self):
        for y in range(self.max.y, self.min.y - 1, -1):
            for x in range(self.min.x, self.max.x + 1):
                if Point(x, y) == self.loc:
                    print("@", end="")
                elif self.grid[Point(x, y)] == 0:
                    print("_", end="")
                else:
                    print("▮", end="")
            print()


def test_program():
    assert PAINT.run() == -1 and PAINT.output == []
    assert PAINT.run([1]) == -1 and PAINT.output == [0, 1]


def test_submission():
    PAINT.reset()
    robot = Robot(PAINT)
    assert robot.move() == (9331, 2319, 2329)


def test_submission2():
    PAINT.reset()
    robot = Robot(PAINT)
    robot.grid[Point(0, 0)] = 1
    assert robot.move() == (249, 248, 249)
    print()
    assert robot.draw() is None


def test_program2():
    error_program = Program([555])
    with pytest.raises(SyntaxError):
        error_program.run([])
    p1 = Program([1, 0, 0, 0, 99])
    assert p1.run([]) == 0 and p1.memory == [2, 0, 0, 0, 99]
    p2 = Program([2, 3, 0, 3, 99])
    assert p2.run([]) == 0 and p2.memory == [2, 3, 0, 6, 99]
    p3 = Program([2, 4, 4, 5, 99, 0])
    assert p3.run([]) == 0 and p3.memory == [2, 4, 4, 5, 99, 9801]
    p4 = Program([1, 1, 1, 4, 99, 5, 6, 0, 99])
    assert p4.run([]) == 0 and p4.memory == [30, 1, 1, 4, 2, 5, 6, 0, 99]
    # IO TESTS
    io = Program([3, 0, 4, 0, 99])
    assert io.run([12]) == 0 and io.output == [12] and io.memory == [12, 0, 4, 0, 99]
    # COMPARE TESTS
    p5 = Program([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
    assert p5.run([8]) == 0 and p5.output == [1]
    p5.reset()
    assert p5.run([7]) == 0 and p5.output == [0]
    p6 = Program([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
    assert p6.run([7]) == 0 and p6.output == [1]
    p6.reset()
    assert p6.run([8]) == 0 and p6.output == [0]
    p7 = Program([3, 3, 1108, -1, 8, 3, 4, 3, 99])
    assert p7.run([8]) == 0 and p7.output == [1]
    p8 = Program([3, 3, 1107, -1, 8, 3, 4, 3, 99])
    assert p8.run([7]) == 0 and p8.output == [1]
    p8.reset()
    assert p8.run([8]) == 0 and p8.output == [0]
    # JUMP TESTS
    pjump1 = Program([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9])
    assert pjump1.run([0]) == 0 and pjump1.output == [0]
    pjump1.reset()
    assert pjump1.run([4]) == 0 and pjump1.output == [1]
    pjump2 = Program([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
    assert pjump2.run([0]) == 0 and pjump2.output == [0]
    pjump2.reset()
    assert pjump2.run([7]) == 0 and pjump2.output == [1]
    pbig = Program(
        [
            3,
            21,
            1008,
            21,
            8,
            20,
            1005,
            20,
            22,
            107,
            8,
            21,
            20,
            1006,
            20,
            31,
            1106,
            0,
            36,
            98,
            0,
            0,
            1002,
            21,
            125,
            20,
            4,
            20,
            1105,
            1,
            46,
            104,
            999,
            1105,
            1,
            46,
            1101,
            1000,
            1,
            20,
            4,
            20,
            1105,
            1,
            46,
            98,
            99,
        ]
    )
    assert pbig.run([7]) == 0 and pbig.output == [999]
    pbig.reset()
    assert pbig.run([8]) == 0 and pbig.output == [1000]
    pbig.reset()
    assert pbig.run([9]) == 0 and pbig.output == [1001]
    # BASE TESTS
    copy_code = [
        109,
        1,
        204,
        -1,
        1001,
        100,
        1,
        100,
        1008,
        100,
        16,
        101,
        1006,
        101,
        0,
        99,
    ]
    copy_program = Program(copy_code)
    assert copy_program.run([]) == 0 and copy_program.output == copy_code
    digit_program = Program([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    assert digit_program.run([]) == 0 and digit_program.output == [1219070632396864]
    large_digit_program = Program([104, 1125899906842624, 99])
    assert large_digit_program.run([]) == 0 and large_digit_program.output == [
        1125899906842624
    ]
