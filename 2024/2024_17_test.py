from itertools import product


class Puzzle:
    """
    --- Day 17: Chronospatial Computer ---
    The Historians push the button on their strange device, but this time, you
    all just feel like you're falling.

    "Situation critical", the device announces in a familiar voice.
    "Bootstrapping process failed. Initializing debugger...."

    The small handheld device suddenly unfolds into an entire computer! The
    Historians look around nervously before one of them tosses it to you.

    This seems to be a 3-bit computer: its program is a list of 3-bit numbers (0
    through 7), like 0,1,2,3. The computer also has three registers named A, B,
    and C, but these registers aren't limited to 3 bits and can instead hold any
    integer.

    The computer knows eight instructions, each identified by a 3-bit number
    (called the instruction's opcode). Each instruction also reads the 3-bit
    number after it as an input; this is called its operand.

    A number called the instruction pointer identifies the position in the
    program from which the next opcode will be read; it starts at 0, pointing at
    the first 3-bit number in the program. Except for jump instructions, the
    instruction pointer increases by 2 after each instruction is processed (to
    move past the instruction's opcode and its operand). If the computer tries
    to read an opcode past the end of the program, it instead halts.

    So, the program 0,1,2,3 would run the instruction whose opcode is 0 and pass
    it the operand 1, then run the instruction having opcode 2 and pass it the
    operand 3, then halt.

    There are two types of operands; each instruction specifies the type of its
    operand. The value of a literal operand is the operand itself. For example,
    the value of the literal operand 7 is the number 7. The value of a combo
    operand can be found as follows:

    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs.

    The eight instructions are as follows:

    The adv instruction (opcode 0) performs division. The numerator is the value
    in the A register. The denominator is found by raising 2 to the power of the
    instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2);
    an operand of 5 would divide A by 2^B.) The result of the division operation
    is truncated to an integer and then written to the A register.

    The bxl instruction (opcode 1) calculates the bitwise XOR of register B and
    the instruction's literal operand, then stores the result in register B.

    The bst instruction (opcode 2) calculates the value of its combo operand
    modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to
    the B register.

    The jnz instruction (opcode 3) does nothing if the A register is 0. However,
    if the A register is not zero, it jumps by setting the instruction pointer
    to the value of its literal operand; if this instruction jumps, the
    instruction pointer is not increased by 2 after this instruction.

    The bxc instruction (opcode 4) calculates the bitwise XOR of register B and
    register C, then stores the result in register B. (For legacy reasons, this
    instruction reads an operand but ignores it.)

    The out instruction (opcode 5) calculates the value of its combo operand
    modulo 8, then outputs that value. (If a program outputs multiple values,
    they are separated by commas.)

    The bdv instruction (opcode 6) works exactly like the adv instruction except
    that the result is stored in the B register. (The numerator is still read
    from the A register.)

    The cdv instruction (opcode 7) works exactly like the adv instruction except
    that the result is stored in the C register. (The numerator is still read
    from the A register.)

    Here are some examples of instruction operation:

    If register C contains 9, the program 2,6 would set register B to 1.
    If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    If register A contains 2024, the program 0,1,5,4,3,0 would output
    4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    If register B contains 29, the program 1,7 would set register B to 26.
    If register B contains 2024 and register C contains 43690, the program 4,0
    would set register B to 44354.

    The Historians' strange device has finished initializing its debugger and is
    displaying some information about the program it is trying to run (your
    puzzle input). For example:

    Register A: 729
    Register B: 0
    Register C: 0

    Program: 0,1,5,4,3,0

    Your first task is to determine what the program is trying to output. To do
    this, initialize the registers to the given values, then run the given
    program, collecting any output produced by out instructions. (Always join
    the values produced by out instructions with commas.) After the above
    program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.

    Using the information provided by the debugger, initialize the registers to
    the given values, then run the program. Once it halts, what do you get if
    you use commas to join the values it output into a single string?

    Your puzzle answer was 4,1,5,3,1,5,3,5,7.

    --- Part Two ---
    Digging deeper in the device's manual, you discover the problem: this
    program is supposed to output another copy of the program! Unfortunately,
    the value in register A seems to have been corrupted. You'll need to find a
    new value to which you can initialize register A so that the program's
    output instructions produce an exact copy of the program itself.

    For example:

    Register A: 2024
    Register B: 0
    Register C: 0

    Program: 0,3,5,4,3,0

    This program outputs a copy of itself if register A is instead initialized
    to 117440. (The original initial value of register A, 2024, is ignored.)

    What is the lowest positive initial value for register A that causes the
    program to output a copy of itself?

    """


SAMPLE_REGISTERS = {
    "A": 729,
    "B": 0,
    "C": 0,
}
SAMPLE_PROGRAM = [0, 1, 5, 4, 3, 0]


MY_REGISTERS = {
    "A": 56256477,
    "B": 0,
    "C": 0,
}
MY_PROGRAM = [2, 4, 1, 1, 7, 5, 1, 5, 0, 3, 4, 3, 5, 5, 3, 0]


class ThreeBitProcessor:
    def __init__(self, register, program):
        self.register = register
        self.program = program
        self.instruction_pointer = 0
        self.output = []

    def combo_operand(self, operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return self.register["A"]
        if operand == 5:
            return self.register["B"]
        if operand == 6:
            return self.register["C"]
        raise Exception(f"invalid {operand=}")

    def cycle(self):
        optcode = self.program[self.instruction_pointer]
        operand = self.program[self.instruction_pointer + 1]
        jump = 2
        match optcode:
            case 0:  # adv
                self.register["A"] //= 2 ** self.combo_operand(operand)
            case 1:  # bxl
                self.register["B"] ^= operand
            case 2:  # bst
                self.register["B"] = self.combo_operand(operand) % 8
            case 3:  # jnz
                if self.register["A"] != 0:
                    self.instruction_pointer = operand
                    jump = 0
            case 4:  # bxc
                self.register["B"] ^= self.register["C"]
            case 5:  # out
                self.output.append(self.combo_operand(operand) % 8)
            case 6:  # bdv
                self.register["B"] = self.register["A"] // 2 ** self.combo_operand(
                    operand
                )
            case 7:  # cdv
                self.register["C"] = self.register["A"] // 2 ** self.combo_operand(
                    operand
                )
        self.instruction_pointer += jump
        return 1

    def run(self):
        while self.instruction_pointer < len(self.program):
            self.cycle()
        return self.output


def test_part_1():
    test_processor = ThreeBitProcessor({"A": 0, "B": 0, "C": 9}, [2, 6])
    assert test_processor.run() == []
    assert test_processor.register["B"] == 1

    test_processor = ThreeBitProcessor({"A": 10, "B": 0, "C": 0}, [5, 0, 5, 1, 5, 4])
    assert test_processor.run() == [0, 1, 2]

    test_processor = ThreeBitProcessor({"A": 2024, "B": 0, "C": 0}, [0, 1, 5, 4, 3, 0])
    assert test_processor.run() == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert test_processor.register["A"] == 0

    test_processor = ThreeBitProcessor({"A": 0, "B": 29, "C": 0}, [1, 7])
    assert test_processor.run() == []
    assert test_processor.register["B"] == 26

    test_processor = ThreeBitProcessor({"A": 0, "B": 2024, "C": 43690}, [4, 0])
    assert test_processor.run() == []
    assert test_processor.register["B"] == 44354

    sample_processor = ThreeBitProcessor(SAMPLE_REGISTERS, SAMPLE_PROGRAM)
    assert sample_processor.run() == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]

    my_processor = ThreeBitProcessor(MY_REGISTERS, MY_PROGRAM)
    answer = ",".join(str(digit) for digit in my_processor.run())
    assert answer == "4,1,5,3,1,5,3,5,7"
    # initial answer "3,0,2,4,6,7,6,0,4" was incorrect as I forgot to correct exponent from ^ to **


MY_BREAKDOWN = """

X:  2, 4 = A mod 8 > B         abc
    1, 1 = B xor 1 > B         abC
    7, 5 = A // 2 ** B > C     ---
    1, 5 = B xor 5 > B         Abc
    0, 3 = A // 2 ** 3 > A
    4, 3 = B xor C > B
    5, 5 = B mod 8 > output = (A mod 8 xor 4) xor (A // 2 ** (A mod 8 xor 1)
    3, 0 = if A != 0 goto X 

    the jump logic in this isn't too bad so should be able to reverse the logic

    program:   2,  4,  1,  1,  7,  5,  1,  5,  0,  3,  4,  3,  5,  5,  3,  0
    as bits: 010,100,001,001,111,101,001,101,000,011,100,011,101,101,011,000

    rev bit: 000,011,101,101,011,100,011,000,101,001,101,111,001,001,100,010

    rev bit: 000,011,101,101,011,100,011,000,101,001,101,111,001,001,100,010
                                                                         ^__ = 110 ^ 010 = 100
                                                                     100 __^ = 011
                                                                     ^__ = 000 ^ 100 = 100
                                                              10 001 __^ = 101
                                                                 ^__ = 101 ^ 001 = 100
                                                                 __^ = 0??
    masks:                                                       101 100 100
    masks:                                                    11 011 000 000
    masks:                                                    11 011 000 000
    
"""


def experiment_part_2():
    valid = []
    b0s = {"101"}
    b1s = {format(n, "03b") for n in [7]}
    b2s = {format(n, "03b") for n in [6, 2]}
    b3s = {format(n, "03b") for n in [7]}
    b4s = {format(n, "03b") for n in [6]}
    b5s = {format(n, "03b") for n in [2, 4]}
    b6s = {format(n, "03b") for n in [3, 4]}
    b7s = {format(n, "03b") for n in [3, 6, 7]}
    b8s = {format(n, "03b") for n in [0, 2, 5, 6, 7]}
    b9s = {format(n, "03b") for n in [3, 6]}
    b10s = {format(n, "03b") for n in [0, 1, 2, 4]}
    b11s = {format(n, "03b") for n in [2, 3]}
    b12s = {format(n, "03b") for n in [2]}
    b13s = {format(n, "03b") for n in [3]}
    b14s = {format(n, "03b") for n in [5]}
    b15s = {format(n, "03b") for n in [4]}

    for b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15 in product(
        b0s,
        b1s,
        b2s,
        b3s,
        b4s,
        b5s,
        b6s,
        b7s,
        b8s,
        b9s,
        b10s,
        b11s,
        b12s,
        b13s,
        b14s,
        b15s,
    ):
        b_str = (
            f"{b15}{b14}{b13}{b12}{b11}{b10}{b9}{b8}{b7}{b6}{b5}{b4}{b3}{b2}{b1}{b0}"
        )
        fixed_registers = {
            "A": int(b_str, 2),
            "B": 0,
            "C": 0,
        }
        my_processor = ThreeBitProcessor(
            fixed_registers,
            MY_PROGRAM,
        )
        if my_processor.run()[:16] == MY_PROGRAM[:16]:
            valid.append(int(b_str, 2))
            # print(f"{b_str}={int(b_str,2)}")
    # 100,101,011,010,011,001,110,010,111,011,010,110,111,110,111,101=164542125273021
    # 100,101,011,010,011,100,110,010,111,011,010,110,111,110,111,101=164545346498493
    # 100,101,011,010,011,001,110,010,111,011,010,110,111,010,111,101=164542125272765
    # 100,101,011,010,011,100,110,010,111,011,010,110,111,010,111,101=164545346498237

    # min(164542125273021, 164545346498493, 164542125272765, 164545346498237) = 164542125272765
    return min(valid)


def test_part_2():
    recursive_seed = 117440
    recursive_program = [0, 3, 5, 4, 3, 0]
    sample_processor = ThreeBitProcessor(
        {"A": recursive_seed, "B": 0, "C": 0}, recursive_program
    )
    assert sample_processor.run() == recursive_program
    assert recursive_seed == 117440

    recursive_seed = 164542125272765
    assert experiment_part_2() == recursive_seed
    my_processor = ThreeBitProcessor({"A": recursive_seed, "B": 0, "C": 0}, MY_PROGRAM)
    assert my_processor.run() == MY_PROGRAM
    assert recursive_seed == 164542125272765
