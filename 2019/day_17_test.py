import pytest
from typing import List, NamedTuple
from collections import deque, defaultdict


class Point(NamedTuple):
    x: int
    y: int


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
        return ''.join([chr(c) for c in self.output])

with open('day_17_input.txt') as fp:
    raw = fp.read()
SRC = [int(d) for d in raw.split(',')]
ASCII = Program(SRC)

SRC2 = SRC[:]
SRC2[0] = 2
ASCII2 = Program(SRC2)


class Image:
    DELTAS = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]
    RIGHT = {Point(0, 1): Point(1, 0), Point(1, 0): Point(0, -1), Point(0, -1): Point(-1, 0), Point(-1, 0): Point(0, 1)}
    LEFT = {Point(0, 1): Point(-1, 0), Point(1, 0): Point(0, 1), Point(0, -1): Point(1, 0), Point(-1, 0): Point(0, -1)}

    def __init__(self, raw):
        self.scaffold = set()
        self.intersection = set()
        for y, scan_row in enumerate(raw.split('\n')):
            for x, c in enumerate(scan_row):
                if c == "#":
                    self.scaffold.add(Point(x, -y))
        self.find_intersections()

    def find_intersections(self):
        for pt in self.scaffold:
            if {Point(pt.x + d.x, pt.y + d.y) for d in self.DELTAS}.issubset(self.scaffold):
                self.intersection.add(pt)

    def alignment_sum(self):
        return -sum([pt.x * pt.y for pt in self.intersection])

    def find_path(self, loc: Point, dir) -> str:
        path = []
        distance = 0
        while True:
            left_dir = self.LEFT[dir]
            right_dir = self.RIGHT[dir]
            while Point(loc.x + dir.x, loc.y + dir.y) in self.scaffold:
                loc = Point(loc.x + dir.x, loc.y + dir.y)
                distance += 1
            if distance > 0:
                path.append(str(distance))
                distance = 0
            if Point(loc.x + left_dir.x, loc.y + left_dir.y) in self.scaffold:
                dir = left_dir
                loc = Point(loc.x + left_dir.x, loc.y + left_dir.y)
                path.append('L')
                distance = 1
            elif Point(loc.x + right_dir.x, loc.y + right_dir.y) in self.scaffold:
                dir = right_dir
                loc = Point(loc.x + right_dir.x, loc.y + right_dir.y)
                path.append('R')
                distance = 1
            else:
                return ','.join(path)


def test_submission():
    ASCII.run()
    monitor = ASCII.print_output()
    image = Image(monitor)

    print()
    print('Output:')
    print(monitor)
    assert image.alignment_sum() == 8520
    assert image.find_path(Point(0, -16), Point(0, 1)) == \
        'R,6,L,8,R,8,' \
        'R,6,L,8,R,8,' \
        'R,4,R,6,R,6,R,4,R,4,' \
        'L,8,R,6,L,10,L,10,' \
        'R,4,R,6,R,6,R,4,R,4,' \
        'L,8,R,6,L,10,L,10,' \
        'R,4,R,6,R,6,R,4,R,4,' \
        'L,8,R,6,L,10,L,10,' \
        'R,6,L,8,R,8,' \
        'L,8,R,6,L,10,L,10'
    # so sequence to program for bot is
    # Main A,A,B,C,B,C,B,C,A,C
    # A 'R,6,L,8,R,8,'
    # B 'R,4,R,6,R,6,R,4,R,4,'
    # C 'L,8,R,6,L,10,L,10'

def test_submission2():
    BOTMOVES = ['A,A,B,C,B,C,B,C,A,C.',
                'R,6,L,8,R,8.',
                'R,4,R,6,R,6,R,4,R,4.',
                'L,8,R,6,L,10,L,10.',
                'n.']
    ASCII_BOTMOVES = [10 if c == '.' else ord(c) for ins in BOTMOVES for c in ins]
    ASCII2.run(ASCII_BOTMOVES)
    assert ASCII2.input == []

    print(''.join([chr(c) if c < 255 else str(c) for c in ASCII2.output]))

    for c in ASCII2.output:
        if c > 255:
            assert c == 926819


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
    copy_code = [109, 1, 204, -1,1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    copy_program = Program(copy_code)
    assert copy_program.run([]) == 0 and copy_program.output == copy_code
    digit_program = Program([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    assert digit_program.run([]) == 0 and digit_program.output == [1219070632396864]
    large_digit_program = Program([104, 1125899906842624, 99])
    assert large_digit_program.run([]) == 0 and large_digit_program.output == [1125899906842624]
