from pathlib import Path
from typing import List
from itertools import permutations
import pytest


class Puzzle:
    """
    --- Day 7: Amplification Circuit ---
    Based on the navigational maps, you're going to need to send more power to your ship's thrusters to reach Santa in
    time. To do this, you'll need to configure a series of amplifiers already installed on the ship.

    There are five amplifiers connected in series; each one receives an input signal and produces an output signal.
    They are connected such that the first amplifier's output leads to the second amplifier's input, the second
    amplifier's output leads to the third amplifier's input, and so on. The first amplifier's input value is 0, and
    the last amplifier's output leads to your ship's thrusters.

        O-------O  O-------O  O-------O  O-------O  O-------O
    0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
        O-------O  O-------O  O-------O  O-------O  O-------O

    The Elves have sent you some Amplifier Controller Software (your puzzle input), a program that should run on your
    existing Intcode computer. Each amplifier will need to run a copy of the program.

    When a copy of the program starts running on an amplifier, it will first use an input instruction to ask the
    amplifier for its current phase setting (an integer from 0 to 4). Each phase setting is used exactly once, but
    the Elves can't remember which amplifier needs which phase setting.

    The program will then call another input instruction to get the amplifier's input signal, compute the correct
    output signal, and supply it back to the amplifier with an output instruction. (If the amplifier has not yet
    received an input signal, it waits until one arrives.)

    Your job is to find the largest output signal that can be sent to the thrusters by trying every possible
    combination of phase settings on the amplifiers. Make sure that memory is not shared or reused between copies
    of the program.

    For example, suppose you want to try the phase setting sequence 3,1,2,4,0, which would mean setting amplifier A
    to phase setting 3, amplifier B to setting 1, C to 2, D to 4, and E to 0. Then, you could determine the output
    signal that gets sent from amplifier E to the thrusters with the following steps:

    Start the copy of the amplifier controller software that will run on amplifier A. At its first input instruction,
    provide it the amplifier's phase setting, 3. At its second input instruction, provide it the input signal, 0. After
    some calculations, it will use an output instruction to indicate the amplifier's output signal.

    Start the software for amplifier B. Provide it the phase setting (1) and then whatever output signal was produced
    from amplifier A. It will then produce a new output signal destined for amplifier C.

    Start the software for amplifier C, provide the phase setting (2) and the value from amplifier B, then collect
    its output signal.

    Run amplifier D's software, provide the phase setting (4) and input value, and collect its output signal.

    Run amplifier E's software, provide the phase setting (0) and input value, and collect its output signal.

    The final output signal from amplifier E would be sent to the thrusters. However, this phase setting sequence may
    not have been the best one; another sequence might have sent a higher signal to the thrusters.

    Here are some example programs:

    Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

    3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
    Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

    3,23,3,24,1002,24,10,24,1002,23,-1,23,
    101,5,23,23,1,24,23,23,4,23,99,0,0
    Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

    3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
    1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0

    Try every combination of phase settings on the amplifiers. What is the highest signal that can be sent to
    the thrusters?

    Your puzzle answer was 14902.

    --- Part Two ---
    It's no good - in this configuration, the amplifiers can't generate a large enough output signal to produce the
    thrust you'll need. The Elves quickly talk you through rewiring the amplifiers into a feedback loop:

          O-------O  O-------O  O-------O  O-------O  O-------O
    0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
       |  O-------O  O-------O  O-------O  O-------O  O-------O |
       |                                                        |
       '--------------------------------------------------------+
                                                                |
                                                                v
                                                         (to thrusters)

    Most of the amplifiers are connected as they were before; amplifier A's output is connected to amplifier B's
    input, and so on. However, the output from amplifier E is now connected into amplifier A's input. This creates
    the feedback loop: the signal will be sent through the amplifiers many times.

    In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9, again each
    used exactly once. These settings will cause the Amplifier Controller Software to repeatedly take input and
    produce output many times before halting. Provide each amplifier its phase setting at its first input instruction;
    all further input/output instructions are for signals.

    Don't restart the Amplifier Controller Software on any amplifier during this process. Each one should continue
    receiving and sending signals until it halts.

    All signals sent or received in this process will be between pairs of amplifiers except the very first signal
    and the very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once.

    Eventually, the software on the amplifiers will halt after they have processed the final loop. When this happens,
    the last output signal from amplifier E is sent to the thrusters. Your job is to find the largest output signal
    that can be sent to the thrusters using the new phase settings and feedback loop arrangement.

    Here are some example programs:

    Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

    3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
    Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

    3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
    Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that
    can be sent to the thrusters?

    Your puzzle answer was 6489132.
    """

    pass


HALT = 99
ADD = 1
MULTIPLY = 2
INPUT = 3
LN_OUTPUT = 4
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

    def process(self, optcode, modes):
        if optcode in [INPUT, LN_OUTPUT]:
            self.process_one_parameter_operation(modes, optcode)
        elif optcode in [JUMP_IF_TRUE, JUMP_IF_FALSE]:
            self.process_two_parameter_operation(modes, optcode)
        elif optcode in [ADD, MULTIPLY, LESS_THAN, EQUAL]:
            self.process_three_parameter_operation(modes, optcode)
        else:
            raise SyntaxError(f"Unknown optcode {optcode}\nOpt Hx:\n{self.opt_hx}")

    def process_one_parameter_operation(self, modes, op_code):
        aa = self.memory[self.head + 1]
        a = aa if modes % 10 else self.memory[aa]
        modes //= 10
        if op_code == INPUT:
            if len(self.input) == 0:
                return
            self.memory[aa] = self.input.pop(0)
        elif op_code == LN_OUTPUT:
            self.output.append(a)
        else:
            raise SyntaxError(f"Unknown optcode {op_code}")
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
            raise SyntaxError(f"Unknown optcode {optcode}")
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
            raise SyntaxError(f"Unknown optcode {optcode}")
        self.head += 4

    def run(self, ln_input: List[int] = None) -> int:
        if ln_input is not None:
            self.input = ln_input
        while True:
            optcode = self.memory[self.head] % 100
            modes = self.memory[self.head] // 100
            if optcode == HALT:
                return 0
            if optcode == INPUT and len(self.input) == 0:
                return -1
            self.process(optcode, modes)


with open(Path(__file__).parent / "2019_07_input.txt") as fp:
    raw = fp.read()
ACS = [int(d) for d in raw.split(",")]
ACP = Program(ACS)


def thruster_output(program_code: list, phases, signal_in: int = 0) -> list:
    ac_ps = []
    thrust_input = []
    for p in phases:
        t_p = Program(program_code)
        thrust_input.append(p)
        t_p.input = thrust_input
        thrust_input = t_p.output
        ac_ps.append(t_p)

    while True:
        exit_codes = 0
        ac_ps[0].input.append(signal_in)
        for t_p in ac_ps:
            exit_codes += t_p.run()
        signal_in = ac_ps[-1].output.pop(0)
        if exit_codes == 0:
            return signal_in


def test_thruster_output():
    test_phases = list(permutations(range(5)))
    assert max([thruster_output(ACS, pl) for pl in test_phases]) == 14902


def test_feed_back():
    # one pass
    assert (
        thruster_output(
            [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
            [4, 3, 2, 1, 0],
        )
        == 43210
    )
    assert (
        thruster_output(
            [
                3,
                23,
                3,
                24,
                1002,
                24,
                10,
                24,
                1002,
                23,
                -1,
                23,
                101,
                5,
                23,
                23,
                1,
                24,
                23,
                23,
                4,
                23,
                99,
                0,
                0,
            ],
            [0, 1, 2, 3, 4],
        )
        == 54321
    )
    assert (
        thruster_output(
            [
                3,
                31,
                3,
                32,
                1002,
                32,
                10,
                32,
                1001,
                31,
                -2,
                31,
                1007,
                31,
                0,
                33,
                1002,
                33,
                7,
                33,
                1,
                33,
                31,
                31,
                1,
                32,
                31,
                31,
                4,
                31,
                99,
                0,
                0,
                0,
            ],
            [1, 0, 4, 3, 2],
        )
        == 65210
    )
    # feed back
    assert (
        thruster_output(
            [
                3,
                26,
                1001,
                26,
                -4,
                26,
                3,
                27,
                1002,
                27,
                2,
                27,
                1,
                27,
                26,
                27,
                4,
                27,
                1001,
                28,
                -1,
                28,
                1005,
                28,
                6,
                99,
                0,
                0,
                5,
            ],
            [9, 8, 7, 6, 5],
        )
        == 139629729
    )


def test_feed_back_thruster_output():
    test_phases = list(permutations(range(5, 10)))
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
