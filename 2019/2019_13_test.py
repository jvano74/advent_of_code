from pathlib import Path
from typing import List, NamedTuple
import pytest


class Puzzle:
    """
    --- Day 13: Care Package ---
    As you ponder the solitude of space and the ever-increasing three-hour roundtrip for messages between you and
    Earth, you notice that the Space Mail Indicator Light is blinking. To help keep you sane, the Elves have sent
    you a care package.

    It's a new game for the ship's arcade cabinet! Unfortunately, the arcade is all the way on the other end of the
    ship. Surely, it won't be hard to build your own - the care package even comes with schematics.

    The arcade cabinet runs Intcode software like the game the Elves sent (your puzzle input). It has a primitive
    screen capable of drawing square tiles on a grid. The software draws tiles to the screen with output
    instructions: every three output instructions specify the x position (distance from the left), y position
    (distance from the top), and tile id. The tile id is interpreted as follows:

    0 is an empty tile. No game object appears in this tile.
    1 is a wall tile. Walls are indestructible barriers.
    2 is a block tile. Blocks can be broken by the ball.
    3 is a horizontal paddle tile. The paddle is indestructible.
    4 is a ball tile. The ball moves diagonally and bounces off objects.

    For example, a sequence of output values like 1,2,3,6,5,4 would draw a horizontal paddle tile (1 tile from the
    left and 2 tiles from the top) and a ball tile (6 tiles from the left and 5 tiles from the top).

    Start the game. How many block tiles are on the screen when the game exits?

    Your puzzle answer was 251.

    --- Part Two ---
    The game didn't run because you didn't put in any quarters. Unfortunately, you did not bring any quarters.
    Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free.

    The arcade cabinet has a joystick that can move left and right. The software reads the position of the
    joystick with input instructions:

    If the joystick is in the neutral position, provide 0.
    If the joystick is tilted to the left, provide -1.
    If the joystick is tilted to the right, provide 1.

    The arcade cabinet also has a segment display capable of showing a single number that represents the player's
    current score. When three output instructions specify X=-1, Y=0, the third output instruction is not a tile;
    the value instead specifies the new score to show in the segment display. For example, a sequence of output
    values like -1,0,12345 would show 12345 as the player's current score.

    Beat the game by breaking all the blocks. What is your score after the last block is broken?

    Your puzzle answer was 12779.
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


with open(Path(__file__).parent / "2019_13_input.txt") as fp:
    raw = fp.read()
SRC = [int(d) for d in raw.split(",")]
PONG = Program(SRC)


FREE_SRC = SRC[:]
FREE_SRC[0] = 2
FREE_PONG = Program(FREE_SRC)


def test_submission1():
    assert PONG.run() == 0
    assert (
        sum([1 if i % 3 == 2 and v == 2 else 0 for i, v in enumerate(PONG.output)])
        == 251
    )


def test_submission2():
    run_result = -1
    while run_result != 0:
        run_result = FREE_PONG.run()
        joystick = 0
        blocks = 0
        while FREE_PONG.output:
            v = FREE_PONG.output.pop()
            y = FREE_PONG.output.pop()
            x = FREE_PONG.output.pop()
            if x == -1 and y == 0:
                score = v
            if v == 2:
                blocks += 1
            if v == 4:
                ball_x = x
            if v == 3:
                paddle_x = x
        if ball_x > paddle_x:
            joystick = 1
        if ball_x < paddle_x:
            joystick = -1
        if ball_x == paddle_x:
            joystick = 0
        print(score, blocks, ball_x, paddle_x)
        if run_result == -1:
            FREE_PONG.input.append(joystick)
    assert score == 12779


def test_program():
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
