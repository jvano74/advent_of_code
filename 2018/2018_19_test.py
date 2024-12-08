from pathlib import Path
from itertools import count
from collections import defaultdict
import operator


class Puzzle:
    """
    --- Day 19: Go With The Flow ---
    With the Elves well on their way constructing the North Pole base, you turn
    your attention back to understanding the inner workings of programming the
    device.

    You can't help but notice that the device's opcodes don't contain any flow
    control like jump instructions. The device's manual goes on to explain:

    "In programs where flow control is required, the instruction pointer can be
    bound to a register so that it can be
     manipulated directly. This way, setr/seti can function as absolute jumps,
     addr/addi can function as relative jumps, and other opcodes can cause truly
     fascinating effects."

    This mechanism is achieved through a declaration like #ip 1, which would
    modify register 1 so that accesses to it let the program indirectly access
    the instruction pointer itself. To compensate for this kind of binding,
    there are now six registers (numbered 0 through 5); the five not bound to
    the instruction pointer behave as normal. Otherwise, the same rules apply as
    the last time you worked with this device.

    When the instruction pointer is bound to a register, its value is written to
    that register just before each instruction is executed, and the value of
    that register is written back to the instruction pointer immediately after
    each instruction finishes execution. Afterward, move to the next instruction
    by adding one to the instruction pointer, even if the value in the
    instruction pointer was just updated by an instruction. (Because of this,
    instructions must effectively set the instruction pointer to the instruction
    before the one they want executed next.)

    The instruction pointer is 0 during the first instruction, 1 during the
    second, and so on. If the instruction pointer ever causes the device to
    attempt to load an instruction outside the instructions defined in the
    program, the program instead immediately halts. The instruction pointer
    starts at 0.

    It turns out that this new information is already proving useful: the CPU in
    the device is not very powerful, and a background process is occupying most
    of its time. You dump the background process' declarations and instructions
    to a file (your puzzle input), making sure to use the names of the opcodes
    rather than the numbers.

    For example, suppose you have the following program:

    #ip 0
    seti 5 0 1
    seti 6 0 2
    addi 0 1 0
    addr 1 2 3
    setr 1 0 0
    seti 8 0 4
    seti 9 0 5

    When executed, the following instructions are executed. Each line contains
    the value of the instruction pointer at the time the instruction started,
    the values of the six registers before executing the instructions (in square
    brackets), the instruction itself, and the values of the six registers after
    executing the instruction (also in square brackets).

    ip=0 [0, 0, 0, 0, 0, 0] seti 5 0 1 [0, 5, 0, 0, 0, 0]
    ip=1 [1, 5, 0, 0, 0, 0] seti 6 0 2 [1, 5, 6, 0, 0, 0]
    ip=2 [2, 5, 6, 0, 0, 0] addi 0 1 0 [3, 5, 6, 0, 0, 0]
    ip=4 [4, 5, 6, 0, 0, 0] setr 1 0 0 [5, 5, 6, 0, 0, 0]
    ip=6 [6, 5, 6, 0, 0, 0] seti 9 0 5 [6, 5, 6, 0, 0, 9]

    In detail, when running this program, the following events occur:

    The first line (#ip 0) indicates that the instruction pointer should be
    bound to register 0 in this program. This is not an instruction, and so the
    value of the instruction pointer does not change during the processing of
    this line.

    The instruction pointer contains 0, and so the first instruction is executed
    (seti 5 0 1). It updates register 0 to the current instruction pointer value
    (0), sets register 1 to 5, sets the instruction pointer to the value of
    register 0 (which has no effect, as the instruction did not modify register
    0), and then adds one to the instruction pointer.

    The instruction pointer contains 1, and so the second instruction, seti 6 0
    2, is executed. This is very similar to the instruction before it: 6 is
    stored in register 2, and the instruction pointer is left with the value 2.
    The instruction pointer is 2, which points at the instruction addi 0 1 0.
    This is like a relative jump: the value of the instruction pointer, 2, is
    loaded into register 0. Then, addi finds the result of adding the value in
    register 0 and the value 1, storing the result, 3, back in register 0.
    Register 0 is then copied back to the instruction pointer, which will cause
    it to end up 1 larger than it would have otherwise and skip the next
    instruction (addr 1 2 3) entirely. Finally, 1 is added to the instruction
    pointer.

    The instruction pointer is 4, so the instruction setr 1 0 0 is run. This is
    like an absolute jump: it copies the value contained in register 1, 5, into
    register 0, which causes it to end up in the instruction pointer. The
    instruction pointer is then incremented, leaving it at 6.

    The instruction pointer is 6, so the instruction seti 9 0 5 stores 9 into
    register 5. The instruction pointer is incremented, causing it to point
    outside the program, and so the program ends.

    What value is left in register 0 when the background process halts?

    Your puzzle answer was 1568.

    --- Part Two ---
    A new background process immediately spins up in its place. It appears
    identical, but on closer inspection, you notice that this time, register 0
    started with the value 1.

    What value is left in register 0 when this new background process halts?

    Your puzzle answer was 19030032.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


with open(Path(__file__).parent / "2018_19_input.txt") as fp:
    INPUTS = [ln.strip() for ln in fp]
    INPUT_CODE = [
        [c if i == 0 else int(c) for i, c in enumerate(ln.split(" "))]
        for ln in INPUTS
        if ln[0] != "#"
    ]
    IP_REGESTER = 2


def test_input():
    assert INPUTS[0] == "#ip 2"
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


def test_processor():
    sample_code = [
        ["seti", 5, 0, 1],
        ["seti", 6, 0, 2],
        ["addi", 0, 1, 0],
        ["addr", 1, 2, 3],
        ["setr", 1, 0, 0],
        ["seti", 8, 0, 4],
        ["seti", 9, 0, 5],
    ]
    processor = Processor(ep_register=0, code=sample_code)
    processor.step()
    assert processor.registers == [0, 5, 0, 0, 0, 0]
    processor.step()
    assert processor.registers == [1, 5, 6, 0, 0, 0]
    processor.step()
    assert processor.registers == [3, 5, 6, 0, 0, 0]
    processor.step()
    assert processor.registers == [5, 5, 6, 0, 0, 0]
    processor.step()
    assert processor.registers == [6, 5, 6, 0, 0, 9]
    processor.run(code=sample_code)
    assert processor.registers == [6, 5, 6, 0, 0, 9]


def test_puzzle_processor():
    processor = Processor(ep_register=IP_REGESTER)
    processor.run(code=INPUT_CODE)
    assert processor.registers[0] == 1568


def test_puzzle2_processor():
    processor = Processor(ep_register=IP_REGESTER, track_hx=True)
    return_code = processor.run(
        code=INPUT_CODE, registers=[1, 0, 0, 0, 0, 0], max_steps=100_000
    )
    assert processor.registers[1] == 10551292
    # Run without max_steps to try and find register 0 likely
    # will take too long for direct execution...
    # assert processor.registers[0] == 1568
    # so track history to try and figure out what we need...
    first_analysis = (
        [3, 4, 5, 6, 8, 9, 10, 11],
        [
            ((0, 17), 1),
            ((3, 4), 12498),
            ((4, 5), 12498),
            ((5, 6), 12498),
            ((6, 8), 12497),  # NOTE: code skips 7, this is likely the 'end' clause
            ((8, 9), 12497),
            ((9, 10), 12497),
            ((10, 11), 12497),
            ((11, 3), 12497),
            ((25, 27), 1),
            ((35, 1), 1),
        ],
    )
    assert processor.hx_analysis() == first_analysis
    assert return_code == (1, "reached max_steps")
    #
    # Look over lines 3 - 11, below
    #
    HACKED_CODE = INPUT_CODE[:]
    HACKED_CODE[3] = [
        "seti",
        9,
        1,
        2,
    ]  # REMEMBER - jump to 1 before so to get 10 goto 9
    HACKED_CODE[10] = ["divr", 1, 5, 4]
    HACKED_CODE[11] = ["addr", 4, 0, 0]
    return_code = processor.run(
        code=HACKED_CODE, registers=[1, 0, 0, 0, 0, 0], max_steps=100_000
    )
    assert processor.registers[1] == 10551292

    # processor.track_hx = False
    # return_code = processor.run(code=HACKED_CODE, registers=[1, 0, 0, 0, 0, 0])
    hacked_analysis = (
        [2, 3, 10, 11, 12, 13, 14, 15],
        [
            ((0, 17), 1),
            ((2, 3), 12498),
            ((3, 10), 12498),
            ((10, 11), 12498),
            ((11, 12), 12498),
            ((12, 13), 12497),
            ((13, 14), 12497),
            ((14, 15), 12497),
            ((15, 2), 12497),
            ((25, 27), 1),
            ((35, 1), 1),
        ],
    )
    assert processor.hx_analysis() == hacked_analysis
    assert return_code == (1, "reached max_steps")
    assert processor.registers[0] == 105618303
    # NOTE: Just replaced 78106251 with answer so not sure value of above assert
    #       78106251 and 102009186 not right, too high


def manual_algorithm(n):
    total = 0
    for i in range(1, n + 1):
        if n % i == 0:
            total += n // i
    return total


def test_manual_algorithm():  # 78106251
    assert manual_algorithm(10551292) == 19030032


"""
#ip 2
0   addi 2 16 2 
1   seti 1 8 5
2   seti 1 0 3

3   mulr 5 3 4   - reg 4 = [reg 5] * [reg 3]  we want reg 1 = reg 5 * reg 3, we reg 3 += 1 until it is
4   eqrr 4 1 4   - reg 4 = 1 if reg 4 = reg 1 else reg 4 = 0
5   addr 4 2 [2] - ip += reg 4 (if reg 4 = 1 then reg 0 += reg 5
6   addi 2 1 [2] - ip = 8
7   addr 5 0 0   - reg 0 += reg 5
8   addi 3 1 3   - [reg 3] += 1
9   gtrr 3 1 4   - reg 4 = 1 if [reg 3] > reg 1 else reg 4 = 0
10  addr 2 4 [2] - ip += reg 4 (when reg 4 = 1 we escape this loop)  <== hacked reg 4 = reg 1 // reg 5
11  seti 2 1 [2] - ip = 2 (goes to 3)  <== hacked reg 0 += reg 4         ABOVE only if reg 1 % reg 5 == 0

12  addi 5 1 5   - [reg 5] += 1
13  gtrr 5 1 4   - reg 4 = 1 if [reg 5] > reg 1 else reg 4 = 1 else reg 4 = 0
14  addr 4 2 2   - ip += reg 4 
15  seti 1 1 [2] - ip = 1 (goes to 2)

16  mulr 2 2 [2] - ip = reg 2 * reg 2 (which would be out of range 16 * 16 = 256)

17  addi 1 2 1
18  mulr 1 1 1
19  mulr 2 1 1
20  muli 1 11 1
21  addi 4 2 4
22  mulr 4 2 4
23  addi 4 12 4
24  addr 1 4 1
25  addr 2 0 2
26  seti 0 9 [2] - ip = 0
27  setr 2 3 4
28  mulr 4 2 4
29  addr 2 4 4
30  mulr 2 4 4
31  muli 4 14 4
32  mulr 4 2 4
33  addr 1 4 1
34  seti 0 1 0
35  seti 0 4 2  - ip = 3 (top of loop)
"""
