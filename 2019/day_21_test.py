import pytest
from typing import List


class Puzzle:
    """
    --- Day 21: Springdroid Adventure ---
    You lift off from Pluto and start flying in the direction of Santa.

    While experimenting further with the tractor beam, you accidentally pull an asteroid directly into your ship! It
    deals significant damage to your hull and causes your ship to begin tumbling violently.

    You can send a droid out to investigate, but the tumbling is causing enough artificial gravity that one wrong step
    could send the droid through a hole in the hull and flying out into space.

    The clear choice for this mission is a droid that can jump over the holes in the hull - a springdroid.

    You can use an Intcode program (your puzzle input) running on an ASCII-capable computer to program the springdroid.
    However, springdroids don't run Intcode; instead, they run a simplified assembly language called springscript.

    While a springdroid is certainly capable of navigating the artificial gravity and giant holes, it has one downside:
    it can only remember at most 15 springscript instructions.

    The springdroid will move forward automatically, constantly thinking about whether to jump. The springscript
    program defines the logic for this decision.

    Springscript programs only use Boolean values, not numbers or strings. Two registers are available: T, the
    temporary value register, and J, the jump register. If the jump register is true at the end of the springscript
    program, the springdroid will try to jump. Both of these registers start with the value false.

    Springdroids have a sensor that can detect whether there is ground at various distances in the direction it is
    facing; these values are provided in read-only registers. Your springdroid can detect ground at four distances:
    one tile away (A), two tiles away (B), three tiles away (C), and four tiles away (D). If there is ground at the
    given distance, the register will be true; if there is a hole, the register will be false.

    There are only three instructions available in springscript:

    AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to false.
    OR X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y to false.
    NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.

    In all three instructions, the second argument (Y) needs to be a writable register (either T or J). The first
    argument (X) can be any register (including A, B, C, or D).

    For example, the one-instruction program NOT A J means "if the tile immediately in front of me is not ground, jump".

    Or, here is a program that jumps if a three-tile-wide hole (with ground on the other side of the hole) is detected:

    NOT A J
    NOT B T
    AND T J
    NOT C T
    AND T J
    AND D J

    The Intcode program expects ASCII inputs and outputs. It will begin by displaying a prompt; then, input the desired
    instructions one per line. End each line with a newline (ASCII code 10). When you have finished entering your
    program, provide the command WALK followed by a newline to instruct the springdroid to begin surveying the hull.

    If the springdroid falls into space, an ASCII rendering of the last moments of its life will be produced. In these,
    @ is the springdroid, # is hull, and . is empty space. For example, suppose you program the springdroid like this:

    NOT D J
    WALK

    This one-instruction program sets J to true if and only if there is no ground four tiles away. In other words,
    it attempts to jump into any hole it finds:

    .................
    .................
    @................
    #####.###########

    .................
    .................
    .@...............
    #####.###########

    .................
    ..@..............
    .................
    #####.###########

    ...@.............
    .................
    .................
    #####.###########

    .................
    ....@............
    .................
    #####.###########

    .................
    .................
    .....@...........
    #####.###########

    .................
    .................
    .................
    #####@###########

    However, if the springdroid successfully makes it across, it will use an output instruction to indicate the amount
    of damage to the hull as a single giant integer outside the normal ASCII range.

    Program the springdroid with logic that allows it to survey the hull without falling into space. What amount of
    hull damage does it report?

    Your puzzle answer was 19348840.

    --- Part Two ---
    There are many areas the springdroid can't reach. You flip through the manual and discover a way to increase its
    sensor range.

    Instead of ending your springcode program with WALK, use RUN. Doing this will enable extended sensor mode,
    capable of sensing ground up to nine tiles away. This data is available in five new read-only registers:

    Register E indicates whether there is ground five tiles away.
    Register F indicates whether there is ground six tiles away.
    Register G indicates whether there is ground seven tiles away.
    Register H indicates whether there is ground eight tiles away.
    Register I indicates whether there is ground nine tiles away.
    All other functions remain the same.

    Successfully survey the rest of the hull by ending your program with RUN. What amount of hull damage does the
    springdroid now report?

    Your puzzle answer was 1141857182.
    """
    pass


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
            raise SyntaxError(f'Unknown optcode {op_code}\nOpt Hx:\n{self.opt_hx}')

    def read_memory(self, pos):
        if len(self.memory) - 1 < pos:
            self.memory.extend([0]*(pos + 1 - len(self.memory)))
        return self.memory[pos]

    def write_memory(self, pos, mode, val):
        if mode == 2:
            pos += self.relative_base
        if len(self.memory) - 1 < pos:
            self.memory.extend([0]*(pos + 1 - len(self.memory)))
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
            raise SyntaxError(f'Unknown op_code {op_code}')
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
            raise SyntaxError(f'Unknown op_code {op_code}')
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
            raise SyntaxError(f'Unknown op_code {op_code}')
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

    def print_output(self):
        return ''.join([chr(c) if c < 256 else str(c) for c in self.output])


with open('day_21_input.txt') as fp:
    raw = fp.read()
SRC = [int(d) for d in raw.split(',')]
DROID = Program(SRC)

# LOGIC (NOT A or NOT B or NOT C) and D
SS = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""

# LOGIC (NOT A or NOT B or NOT C) and ( D and (E or H) )
SS2 = """OR E T
OR H T
AND D T
NOT A J
NOT J J
AND B J
AND C J
NOT J J
AND T J
RUN
"""


def test_submission():
    _ = DROID.run()
    print()
    print('PROGRAM INITIAL OUTPUT:')
    print(DROID.print_output())
    DROID.input = [ord(c) for c in SS]
    result = DROID.run()
    print('PROGRAM OUTPUT AFTER PROGRAMMED:')
    print(DROID.print_output())
    assert result == 0


def test_submission2():
    _ = DROID.run()
    print()
    print('PROGRAM INITIAL OUTPUT:')
    print(DROID.print_output())
    DROID.input = [ord(c) for c in SS2]
    result = DROID.run()
    print('PROGRAM OUTPUT AFTER PROGRAMMED:')
    print(DROID.print_output())
    assert result == 0


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
    pbig = Program([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                    1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                    999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])
    assert pbig.run([7]) == 0 and pbig.output == [999]
    pbig.reset()
    assert pbig.run([8]) == 0 and pbig.output == [1000]
    pbig.reset()
    assert pbig.run([9]) == 0 and pbig.output == [1001]
    # BASE TESTS
    copy_code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    copy_program = Program(copy_code)
    assert copy_program.run([]) == 0 and copy_program.output == copy_code
    digit_program = Program([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    assert digit_program.run([]) == 0 and digit_program.output == [1219070632396864]
    large_digit_program = Program([104, 1125899906842624, 99])
    assert large_digit_program.run([]) == 0 and large_digit_program.output == [1125899906842624]
