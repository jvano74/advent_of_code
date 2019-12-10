import pytest
from typing import List
from itertools import permutations


HALT = 99
ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUAL = 8


class Program:
    def __init__(self, program):
        self.head = 0
        self.disk = list(program)
        self.memory = list(program)
        self.input = []
        self.output = []
        self.opt_hx = []

    def reset(self):
        self.head = 0
        self.memory = list(self.disk)
        self.input = []
        self.output = []
        self.opt_hx = []

    def process(self,optcode,modes):
        if optcode in [INPUT, OUTPUT]:
            self.process_one_parameter_operation(modes, optcode)
        elif optcode in [JUMP_IF_TRUE, JUMP_IF_FALSE]:
            self.process_two_parameter_operation(modes, optcode)
        elif optcode in [ADD, MULTIPLY, LESS_THAN, EQUAL] :
            self.process_three_parameter_operation(modes, optcode)
        else:
            raise SyntaxError(f'Unknown optcode {optcode}\nOpt Hx:\n{self.opt_hx}')

    def process_one_parameter_operation(self, modes, optcode):
        aa = self.memory[self.head + 1]
        a = aa if modes % 10 else self.memory[aa]
        modes //= 10
        if optcode == INPUT:
            if len(self.input) == 0:
                return
            self.memory[aa] = self.input.pop(0)
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
        if optcode == JUMP_IF_TRUE:
            if a:
                self.head = b
                return
        elif optcode == JUMP_IF_FALSE:
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
        elif optcode == LESS_THAN:
            self.memory[ac] = 1 if a < b else 0
        elif optcode == EQUAL:
            self.memory[ac] = 1 if a == b else 0
        else:
            raise SyntaxError(f'Unknown optcode {optcode}')
        self.head += 4

    def run(self, input: List[int] = None) -> int:
        if input is not None:
            self.input = input
        while True:
            optcode = self.memory[self.head] % 100
            modes = self.memory[self.head] // 100
            if optcode == HALT:
                return 0
            if optcode == INPUT and len(self.input) == 0:
                return -1
            self.process(optcode, modes)


with open('input_day_07.txt') as fp:
    raw = fp.read()
ACS = [int(d) for d in raw.split(',')]
ACP = Program(ACS)


def thruster_output(procgram_code: str, phases: List, signal_in: int = 0) -> int:
    ACPs = []
    input = []
    for p in phases:
        tP = Program(procgram_code)
        input.append(p)
        tP.input = input
        input = tP.output
        ACPs.append(tP)

    while True:
        exit_codes = 0
        ACPs[0].input.append(signal_in)
        for tP in ACPs:
            exit_codes += tP.run()
        signal_in = ACPs[-1].output.pop(0)
        if exit_codes == 0:
            return signal_in


def test_thruster_output():
    test_phases = list(permutations(range(5)))
    assert max([thruster_output(ACS, pl) for pl in test_phases]) == 14902


def test_feed_back():
    # one pass
    assert thruster_output([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
                           [4,3,2,1,0]) == 43210
    assert thruster_output([3,23,3,24,1002,24,10,24,1002,23,-1,23,
                            101,5,23,23,1,24,23,23,4,23,99,0,0],
                           [0,1,2,3,4]) == 54321
    assert thruster_output([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                            1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0],
                           [1,0,4,3,2]) == 65210
    # feed back
    assert thruster_output([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                            27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],
                           [9,8,7,6,5]) == 139629729


def test_feed_back_thruster_output():
    test_phases = list(permutations(range(5,10)))
    assert max([thruster_output(ACS, pl) for pl in test_phases]) == 6489132


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
    io = Program([3,0,4,0,99])
    assert io.run([12]) == 0 and io.output == [12] and io.memory == [12,0,4,0,99]
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
