from pathlib import Path
from itertools import count
from collections import defaultdict
import operator


class Puzzle:
    """
    --- Day 21: Chronal Conversion ---
    You should have been watching where you were going, because as you wander the new North Pole base, you trip and
    fall into a very deep hole!

    Just kidding. You're falling through time again.

    If you keep up your current pace, you should have resolved all of the temporal anomalies by the next time the
    device activates. Since you have very little interest in browsing history in 500-year increments for the rest
    of your life, you need to find a way to get back to your present time.

    After a little research, you discover two important facts about the behavior of the device:

    First, you discover that the device is hard-wired to always send you back in time in 500-year increments.
    Changing this is probably not feasible.

    Second, you discover the activation system (your puzzle input) for the time travel module. Currently, it appears
    to run forever without halting.

    If you can cause the activation system to halt at a specific moment, maybe you can make the device send you so
    far back in time that you cause an integer underflow in time itself and wrap around back to your current time!

    The device executes the program as specified in manual section one and manual section two.

    Your goal is to figure out how the program works and cause it to halt. You can only control register 0; every
    other register begins at 0 as usual.

    Because time travel is a dangerous activity, the activation system begins with a few instructions which verify
    that bitwise AND (via bani) does a numeric operation and not an operation as if the inputs were interpreted as
    strings. If the test fails, it enters an infinite loop re-running the test instead of allowing the program to
    execute normally. If the test passes, the program continues, and assumes that all other bitwise operations
    (banr, bori, and borr) also interpret their inputs as numbers. (Clearly, the Elves who wrote this system were
    worried that someone might introduce a bug while trying to emulate this system with a scripting language.)

    What is the lowest non-negative integer value for register 0 that causes the program to halt after executing the
    fewest instructions? (Executing the same instruction multiple times counts as multiple instructions executed.)
    """

    pass


with open(Path(__file__).parent / "2018_21_input.txt") as fp:
    INPUTS = [ln.strip() for ln in fp]
    INPUT_CODE = [
        [c if i == 0 else int(c) for i, c in enumerate(ln.split(" "))]
        for ln in INPUTS[1:]
    ]
    IP_REGESTER = int(INPUTS[0][4])


def test_input():
    assert INPUTS[0] == "#ip 1"
    assert sum(1 for inst in INPUTS if inst[0] == "#") == 1


class Processor:
    op_codes = [
        "addr",
        "addi",
        "mulr",
        "muli",
        "banr",
        "bani",
        "borr",
        "bori",
        "divr",
        "divi",
        "setr",
        "seti",
        "gtir",
        "gtri",
        "gtrr",
        "eqir",
        "eqri",
        "eqrr",
    ]

    binary_operations = {
        "add": operator.add,
        "mul": operator.mul,
        "div": operator.floordiv,
        "ban": operator.and_,
        "bor": operator.or_,
    }

    comparison_operations = {"gt": operator.gt, "eq": operator.eq}

    def __init__(self, code=None, ep_register=None, track_hx=False):
        self.code = code
        self.ep_register = ep_register
        self.track_hx = track_hx

        self.ep = 0
        self.registers = [0, 0, 0, 0, 0, 0]
        self.hx_code_lines = defaultdict(list)
        self.hx_code_line_transitions = defaultdict(lambda: defaultdict(int))
        self.hx_op = []
        self.hx_pre_register = []
        self.hx_post_register = []

    def reset_history(self):
        self.hx_code_lines = defaultdict(list)
        self.hx_code_line_transitions = defaultdict(lambda: defaultdict(int))
        self.hx_op = []
        self.hx_pre_register = []
        self.hx_post_register = []

    def run(self, code=None, registers=None, max_steps=None):
        if code is not None:
            self.code = code
        if registers is None:
            self.registers = [0, 0, 0, 0, 0, 0]
        else:
            self.registers = registers
        if max_steps is None:
            step_range = count(start=1)
        else:
            step_range = range(1, max_steps + 1)

        self.reset_history()

        self.ep = 0
        for step_number in step_range:
            result = self.step(step_number)
            if result != 0:
                return result
        return 1, "reached max_steps"

    def step(self, step_number=None):
        ep = self.ep
        if 0 <= ep < len(self.code):
            if self.ep_register is not None:
                self.registers[self.ep_register] = self.ep
            op = self.code[ep]
            if self.track_hx:
                self.hx_code_lines[ep].append(step_number)
                self.hx_op.append(op[:])
                self.hx_pre_register.append(self.registers[:])
            result = self.operation(op)
            if self.ep_register is not None:
                self.ep = self.registers[self.ep_register]
            self.ep += 1
            if self.track_hx:
                self.hx_post_register.append(self.registers[:])
                self.hx_code_line_transitions[ep][self.ep] += 1
            return result
        return 1, "execution_pointer out of range"

    def operation(self, instruction):
        op = instruction[0]
        op_io = instruction[1:]

        base_inst = op[0:3]
        if base_inst in self.binary_operations:
            return self.binary_operation(
                op[3], op_io, self.binary_operations[base_inst]
            )
        if base_inst == "set":
            return self.assignment(op[3], op_io)

        base_inst = op[0:2]
        if base_inst in self.comparison_operations:
            return self.comparison_operation(
                op[2:], op_io, self.comparison_operations[base_inst]
            )

        return 1

    def binary_operation(self, op, op_io, operation):
        op_io[0] = self.registers[op_io[0]]
        # deal with any input registers
        if op == "r":
            op_io[1] = self.registers[op_io[1]]
        self.registers[op_io[2]] = operation(op_io[0], op_io[1])
        return 0

    def assignment(self, op, op_io):
        # deal with any input registers
        if op == "r":
            op_io[0] = self.registers[op_io[0]]
        self.registers[op_io[2]] = op_io[0]
        return 0

    def comparison_operation(self, op, op_io, operation):
        # deal with any input registers
        if op[0] == "r":
            op_io[0] = self.registers[op_io[0]]
        if op[1] == "r":
            op_io[1] = self.registers[op_io[1]]

        if operation(op_io[0], op_io[1]):
            self.registers[op_io[2]] = 1
        else:
            self.registers[op_io[2]] = 0
        return 0

    def hx_analysis(self, multi_hit_min=2, skip_next_transitions=True):
        multi_hit = sorted(
            line
            for line, when_hit in self.hx_code_lines.items()
            if len(when_hit) >= multi_hit_min
        )
        transitions = {}
        for before, afters in self.hx_code_line_transitions.items():
            for after, state_change_count in afters.items():
                if (
                    before + 1 == after
                    and state_change_count < multi_hit_min
                    and skip_next_transitions
                ):
                    pass
                else:
                    transitions[(before, after)] = state_change_count
        return multi_hit, sorted(transitions.items())


def test_puzzle_processor():
    processor = Processor(ep_register=IP_REGESTER, track_hx=True)
    processor.run(code=INPUT_CODE, registers=[0, 0, 0, 0, 0, 0], max_steps=100_000)
    first_analysis = (
        [
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
        ],
        [
            ((3, 5), 1),
            ((6, 7), 3),
            ((7, 8), 3),
            ((8, 9), 7),
            ((9, 10), 7),
            ((10, 11), 7),
            ((11, 12), 7),
            ((12, 13), 7),
            ((13, 14), 7),
            ((14, 15), 5),
            ((14, 16), 2),
            ((15, 17), 5),
            ((16, 28), 2),
            ((17, 18), 5),
            ((18, 19), 14275),
            ((19, 20), 14275),
            ((20, 21), 14275),
            ((21, 22), 14271),
            ((21, 23), 4),
            ((22, 24), 14270),
            ((23, 26), 4),
            ((24, 25), 14270),
            ((25, 18), 14270),
            ((26, 27), 4),
            ((27, 8), 4),
            ((28, 29), 2),
            ((29, 30), 2),
            ((30, 6), 2),
        ],
    )
    assert processor.hx_analysis() == first_analysis
    # actually used debugger to find first time line 28 was hit and found value of reg_4
    answer_1 = processor.hx_pre_register[1847][4]
    assert answer_1 == 103548


def manual_version(reg_0):
    """
        #ip 1
           0   seti 123 0 4   ------ reg_4 = 123
           1   bani 4 456 4   ------ reg_4 = reg_4 & 456
           2   eqri 4 72 4    ------ reg_4 = 1 if reg_4 == 72 else 0
           3   addr  4 1 [1]  ------ ip += reg_4
           4   seti  0 0 [1]  ------ ip = 0

           5   seti 0 2 4     ------ reg_4 = 0 <==== ARGG!! thought this was setr not seti
                                     count = 0
                                     while count == 0 or reg_4 != reg_0:
                                         count += 1
    |      6   bori 4 65536 3 ======     reg_3 = reg_4 | 65536
    |      7   seti 10552971 1 4 ---     reg_4 = 10552971
                                         while True:
    ||     8   bani 3 255 5   ======         reg_5 = reg_3 & 255
    ||     9   addr 4 5 4     ------         reg_4 += reg_5
    ||     10  bani 4 16777215 4 ---         reg_4 &= 16777215
    ||     11  muli 4 65899 4 ------         reg_4 *= 65899
    ||     12  bani 4 16777215 4 ---         reg_4 &= 16777215
                                             if reg_3 < 256:
                                                break

      --------------------------------------------------------------------
    ||     13  gtir 256 3 5   ------         reg_5 = 1 if reg_3 < 256 else reg_5 = 0  # want reg_3 < 256
    ||     14  addr  5 1 [1]  ------ ip += reg_5 (if reg_5 = 0, 1 goes below, want reg_5 == 1
    ||     15  addi  1 1 [1]  ------ ip += 1 (goes to 17, skipping next)
    ||     16  seti 27 7 [1]  ------ ip = 27 (goes to 28)  <== if reg_0 == reg_4 program will exit
      --------------------------------------------------------------------

    ||     17  seti 0 1 5     ------         reg_5 = 0
                                             while True:
    |||    18  addi 5 1 2     ======             reg_2 = reg_5 + 1
    |||    19  muli 2 256 2   ------             reg_2 *= 256
                                                 if reg_2 > reg_3:
                                                     break
                                                 reg_5 += 1
                                             reg_3 = reg_5

      --------------------------------------------------------------------
    |||    20  gtrr  2 3 2    ------         reg_2 = 1 if reg_2 > reg_3 else reg_2 = 0
    |||    21  addr  2 1 [1]  ------ ip += reg_2 (if reg_2 = 0, 1 goes below, want reg_2 == ? w/ reg_4 == reg_0 or <===
    ||     22  addi  1 1 [1]  ------ ip += 1 (skips next, goes to 24)              reg_2 == ? w/ reg_5 > 0         <===
    |||    23  seti 25 0 [1]  ------ ip = 25 (goes to 26, which set reg_3 = reg_5 and then goes to 8)
      --------------------------------------------------------------------

    |||    24  addi 5 1 5     ------ reg_5 += 1
    |||    25  seti 17 2 [1]  ------ ip = 17 (goes to 18)
    ||     26  setr  5 7  3   ------ reg_3 = reg_5
    ||     27  seti  7 8 [1]  ------ ip = 7 (goes to 8)

    ||     28  eqrr   4 0 5   ------ reg_5 = 1 if reg_4 == reg_0 else reg_5 = 0    <- to exit need reg_0 == reg_4
    ||     29  addr  5 1 [1]  ------ ip += reg_5 (if reg_5 > 0 program will exist)
    ||     30  seti  5 0 [1]  ------ ip = 5 (goes to 6)
    """
    reg_4 = 0  # ARGH, wasted so much time thinking this was reg_0
    loops = 0
    while loops == 0 or reg_4 != reg_0:
        loops += 1  #   111101_11011111_10100100
        reg_3 = reg_4 | 65536  #        1_00000000_00000000
        reg_4 = 10552971  # 10100001_00000110_10001011
        while True:
            reg_4 += reg_3 & 255  #                   11111111
            reg_4 &= 16777215  # 11111111_11111111_11111111
            reg_4 *= 65899  #        1_00000001_01101011
            reg_4 &= 16777215  # 11111111_11111111_11111111
            if reg_3 < 256:  #                 1_00000000
                break
            reg_3 >>= 8
            # reg_5 = 0
            # while True:
            #    reg_2 = reg_5 + 1
            #    reg_2 *= 256          #                 1_00000000
            #    if reg_2 > reg_3:     # effect of this loop is
            #        break             # right shift reg_3 8 bits
            #    reg_5 += 1
            # reg_3 = reg_5
    return loops


def reg_4_values():
    first_seen = {}
    reg_4 = 0
    steps = 0
    while True:
        steps += 1
        reg_3 = reg_4 | 65536
        reg_4 = 10552971
        while True:
            reg_4 += reg_3 & 255
            reg_4 &= 16777215
            reg_4 *= 65899
            reg_4 &= 16777215
            if reg_3 < 256:
                break
            reg_3 >>= 8
        if reg_4 in first_seen:
            return sorted((b, a) for a, b in first_seen.items())
        first_seen[reg_4] = steps


def test_reg_4_values():
    values = reg_4_values()
    assert min(values) == (1, 103548)  # much easier way to get
    assert max(values) == (10610, 14256686)
