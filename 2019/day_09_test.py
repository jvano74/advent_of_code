import pytest
from typing import List


class Puzzle:
    """
    --- Day 9: Sensor Boost ---
    You've just said goodbye to the rebooted rover and left Mars when you receive a faint distress signal coming from
    the asteroid belt. It must be the Ceres monitoring station!

    In order to lock on to the signal, you'll need to boost your sensors. The Elves send up the latest BOOST program
    - Basic Operation Of System Test.

    While BOOST (your puzzle input) is capable of boosting your sensors, for tenuous safety reasons, it refuses to do
    so until the computer it runs on passes some checks to demonstrate it is a complete Intcode computer.

    Your existing Intcode computer is missing one key feature: it needs support for parameters in relative mode.

    Parameters in mode 2, relative mode, behave very similarly to parameters in position mode: the parameter is
    interpreted as a position. Like position mode, parameters in relative mode can be read from or written to.

    The important difference is that relative mode parameters don't count from address 0. Instead, they count from a
    value called the relative base. The relative base starts at 0.

    The address a relative mode parameter refers to is itself plus the current relative base. When the relative base
    is 0, relative mode parameters and position mode parameters with the same value refer to the same address.

    For example, given a relative base of 50, a relative mode parameter of -7 refers to memory address 50 + -7 = 43.

    The relative base is modified with the relative base offset instruction:

    Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases (or decreases,
    if the value is negative) by the value of the parameter.

    For example, if the relative base is 2000, then after the instruction 109,19, the relative base would be 2019.
    If the next instruction were 204,-34, then the value at address 1985 would be output.

    Your Intcode computer will also need a few other capabilities:

    The computer's available memory should be much larger than the initial program. Memory beyond the initial program
    starts with the value 0 and can be read or written like any other memory. (It is invalid to try to access memory
    at a negative address, though.)

    The computer should have support for large numbers. Some instructions near the beginning of the BOOST program
    will verify this capability.

    Here are some example programs that use these features:

    109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and produces a copy of itself as output.
    1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
    104,1125899906842624,99 should output the large number in the middle.
    The BOOST program will ask for a single input; run it in test mode by providing it the value 1. It will perform
    a series of checks on each opcode, output any opcodes (and the associated parameter modes) that seem to be
    functioning incorrectly, and finally output a BOOST keycode.

    Once your Intcode computer is fully functional, the BOOST program should report no malfunctioning opcodes when
    run in test mode; it should only output a single value, the BOOST keycode. What BOOST keycode does it produce?

    Your puzzle answer was 2870072642.

    --- Part Two ---
    You now have a complete Intcode computer.

    Finally, you can lock on to the Ceres distress signal! You just need to boost your sensors using the BOOST program.

    The program runs in sensor boost mode by providing the input instruction the value 2. Once run, it will boost the
    sensors automatically, but it might take a few seconds to complete the operation on slower hardware. In sensor
    boost mode, the program will output a single value: the coordinates of the distress signal.

    Run the BOOST program in sensor boost mode. What are the coordinates of the distress signal?

    Your puzzle answer was 58534.
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


with open('day_09_input.txt') as fp:
    raw = fp.read()
BOOST_SRC = [int(d) for d in raw.split(',')]
BOOST = Program(BOOST_SRC)


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


def test_submission():
    assert BOOST.run([1]) == 0 and BOOST.output == [2870072642]
    BOOST.reset()
    assert BOOST.run([2]) == 0 and BOOST.output == [58534]
