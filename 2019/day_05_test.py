import pytest
from typing import List
from enum import Enum


HALT = 99
ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JIFTRUE = 5
JIFFALSE = 6
LESSTHAN = 7
EQUAL = 8


class Program:


    def __init__(self, program):
        self.head = 0
        self.disk = list(program)
        self.memory = list(program)
        self.input = []
        self.output = []

    def reset(self):
        self.head = 0
        self.memory = list(self.disk)
        self.input = []
        self.output = []

    def process(self):
        optcode = self.memory[self.head] % 100
        modes = self.memory[self.head] // 100
        if optcode in [INPUT, OUTPUT]:
            self.process_one_parameter_operation(modes, optcode)
        elif optcode in [JIFTRUE, JIFFALSE]:
            self.process_two_parameter_operation(modes, optcode)
        elif optcode in [ADD, MULTIPLY, LESSTHAN, EQUAL] :
            self.process_three_parameter_operation(modes, optcode)
        else:
            raise SyntaxError(f'Unknown optcode {optcode}')

    def process_one_parameter_operation(self, modes, optcode):
        aa = self.memory[self.head + 1]
        a = aa if modes % 10 else self.memory[aa]
        modes //= 10
        if optcode == INPUT:
            self.memory[aa] = self.input.pop()
        elif optcode == OUTPUT:
            self.output.append(a)
        else:
            raise SyntaxError(f'Unknown optcode {optcode}')
        self.head += 2

    def process_two_parameter_operation(self, modes, optcode):
        aa = self.memory[self.head + 1]
        a = aa if modes % 10 else self.memory[aa]
        modes //= 10
        ab = self.memory[self.head + 2]
        b = ab if modes % 10 else self.memory[ab]
        modes //= 10
        if optcode == JIFTRUE:
            if a:
                self.head = b
                return
        elif optcode == JIFFALSE:
            if not a:
                self.head = b
                return
        else:
            raise SyntaxError(f'Unknown optcode {optcode}')
        self.head += 3

    def process_three_parameter_operation(self, modes, optcode):
        aa = self.memory[self.head + 1]
        a = aa if modes % 10 else self.memory[aa]
        modes //= 10

        ab = self.memory[self.head + 2]
        b = ab if modes % 10 else self.memory[ab]
        modes //= 10

        ac = self.memory[self.head + 3]
        if optcode == ADD:
            self.memory[ac] = a + b
        elif optcode == MULTIPLY:
            self.memory[ac] = a * b
        elif optcode == LESSTHAN:
            self.memory[ac] = 1 if a < b else 0
        elif optcode == EQUAL:
            self.memory[ac] = 1 if a == b else 0
        else:
            raise SyntaxError(f'Unknown optcode {optcode}')
        self.head += 4


    def run(self, input: List[int]) -> List[int]:
        self.input = input
        while self.memory[self.head] != HALT:
            self.process()
        return self.output


def test_program():
    error_program = Program([555])
    with pytest.raises(SyntaxError):
        error_program.run([])
    p1 = Program([1, 0, 0, 0, 99])
    assert p1.run([]) == [] and p1.memory == [2, 0, 0, 0, 99]
    p2 = Program([2, 3, 0, 3, 99])
    assert p2.run([]) == [] and p2.memory == [2, 3, 0, 6, 99]
    p3 = Program([2, 4, 4, 5, 99, 0])
    assert p3.run([]) == [] and p3.memory == [2, 4, 4, 5, 99, 9801]
    p4 = Program([1, 1, 1, 4, 99, 5, 6, 0, 99])
    assert p4.run([]) == [] and p4.memory == [30, 1, 1, 4, 2, 5, 6, 0, 99]
    # IO TESTS
    io = Program([3,0,4,0,99])
    assert io.run([12]) == [12] and io.memory == [12,0,4,0,99]
    # COMPARE TESTS
    p5 = Program([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
    assert p5.run([8]) == [1]
    p5.reset()
    assert p5.run([7]) == [0]
    p6 = Program([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
    assert p6.run([7]) == [1]
    p6.reset()
    assert p6.run([8]) == [0]
    p7 = Program([3, 3, 1108, -1, 8, 3, 4, 3, 99])
    assert p7.run([8]) == [1]
    p8 = Program([3, 3, 1107, -1, 8, 3, 4, 3, 99])
    assert p8.run([7]) == [1]
    p8.reset()
    assert p8.run([8]) == [0]
    # JUMP TESTS
    pjump1 = Program([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9])
    assert pjump1.run([0]) == [0]
    pjump1.reset()
    assert pjump1.run([4]) == [1]
    pjump2 = Program([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
    assert pjump2.run([0]) == [0]
    pjump2.reset()
    assert pjump2.run([7]) == [1]
    pbig = Program([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                    1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                    999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])
    assert pbig.run([7]) == [999]
    pbig.reset()
    assert pbig.run([8]) == [1000]
    pbig.reset()
    assert pbig.run([9]) == [1001]


def test_run_diagnosis():
    with open('day_05_input.txt') as fp:
        raw = fp.read()
    RAW_DIAG_PROG = [int(d) for d in raw.split(',')]
    diag_prog = Program(RAW_DIAG_PROG)
    assert diag_prog.run([1]) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 7566643]
    diag_prog.reset()
    assert diag_prog.run([5]) == [9265694]
