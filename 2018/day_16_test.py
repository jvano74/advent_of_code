import re
import operator


class Puzzle:
    """
    --- Day 16: Chronal Classification ---
    As you see the Elves defend their hot chocolate successfully, you go back to falling through time. This is going
    to become a problem.

    If you're ever going to return to your own time, you need to understand how this device on your wrist works. You
    have a little while before you reach your next destination, and with a bit of trial and error, you manage to pull
    up a programming manual on the device's tiny screen.

    According to the manual, the device has four registers (numbered 0 through 3) that can be manipulated by
    instructions containing one of 16 opcodes. The registers start with the value 0.

    Every instruction consists of four values: an opcode, two inputs (named A and B), and an output (named C),
    in that order. The opcode specifies the behavior of the instruction and how the inputs are interpreted.
    The output, C, is always treated as a register.

    In the opcode descriptions below, if something says "value A", it means to take the number given as A literally.
    (This is also called an "immediate" value.) If something says "register A", it means to use the number given
    as A to read from (or write to) the register with that number. So, if the opcode addi adds register A and
    value B, storing the result in register C, and the instruction addi 0 7 3 is encountered, it would add 7 to the
    value contained by register 0 and store the sum in register 3, never modifying registers 0, 1, or 2 in the process.

    Many opcodes are similar except for how they interpret their arguments.
    The opcodes fall into seven general categories:

    Addition:

    addr (add register) stores into register C the result of adding register A and register B.
    addi (add immediate) stores into register C the result of adding register A and value B.

    Multiplication:

    mulr (multiply register) stores into register C the result of multiplying register A and register B.
    muli (multiply immediate) stores into register C the result of multiplying register A and value B.

    Bitwise AND:

    banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.

    Bitwise OR:

    borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.

    Assignment:

    setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    seti (set immediate) stores value A into register C. (Input B is ignored.)

    Greater-than testing:

    gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B.
         Otherwise, register C is set to 0.
    gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B.
         Otherwise, register C is set to 0.
    gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B.
         Otherwise, register C is set to 0.

    Equality testing:

    eqir (equal immediate/register) sets register C to 1 if value A is equal to register B.
         Otherwise, register C is set to 0.
    eqri (equal register/immediate) sets register C to 1 if register A is equal to value B.
         Otherwise, register C is set to 0.
    eqrr (equal register/register) sets register C to 1 if register A is equal to register B.
         Otherwise, register C is set to 0.

    Unfortunately, while the manual gives the name of each opcode, it doesn't seem to indicate the number. However,
    you can monitor the CPU to see the contents of the registers before and after instructions are executed to try
    to work them out. Each opcode has a number from 0 through 15, but the manual doesn't say which is which.
    For example, suppose you capture the following sample:

    Before: [3, 2, 1, 1]
    9 2 1 2
    After:  [3, 2, 2, 1]

    This sample shows the effect of the instruction 9 2 1 2 on the registers. Before the instruction is executed,
    register 0 has value 3, register 1 has value 2, and registers 2 and 3 have value 1. After the instruction is
    executed, register 2's value becomes 2.

    The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2, B=1, and C=2. Opcode 9 could be
    any of the 16 opcodes listed above, but only three of them behave in a way that would cause the result shown
    in the sample:

    Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1 (which has a value of 2) produces 2,
                            which matches the value stored in the output register, register 2.
    Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1 produces 2,
                            which matches the value stored in the output register, register 2.
    Opcode 9 could be seti: value 2 matches the value stored in the output register,
                            register 2; the number given for B is irrelevant.

    None of the other opcodes produce the result captured in the sample. Because of this, the sample above behaves
    like three opcodes.

    You collect many of these samples (the first section of your puzzle input). The manual also includes a small test
    program (the second section of your puzzle input) - you can ignore it for now.

    Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?
    """
    pass


with open('day_16_input.txt') as fp:
    part_1_raw, part_2_raw = fp.read().split('\n\n\n\n')
    INPUT_PART_1 = [[ln.strip() for ln in ex.split('\n')] for ex in part_1_raw.split('\n\n')]
    INPUT_PART_2 = [ln.strip() for ln in part_2_raw.split('\n')]


def test_input():
    assert INPUT_PART_1[0] == ['Before: [0, 2, 0, 2]', '6 0 1 1', 'After:  [0, 1, 0, 2]']
    assert INPUT_PART_1[-1] == ['Before: [1, 2, 2, 1]', '9 3 1 3', 'After:  [1, 2, 2, 1]']
    assert len(INPUT_PART_1) == 811
    assert INPUT_PART_2[0] == '2 0 1 1'
    assert INPUT_PART_2[-1] == '12 2 0 0'


class Processor:
    def __init__(self, code):
        self.registers = [0, 0, 0, 0]
        self.code = code

    def operation(self, op):
        if op[0][0:3] == 'add':
            # return self.addition(op)
            return self.binary_operation(op, operator.add)
        if op[0][0:3] == 'mul':
            # return self.multiplication(op)
            return self.binary_operation(op, operator.mul)
        if op[0][0:3] == 'ban':
            # return self.bitwise_and(op)
            return self.binary_operation(op, operator.and_)
        if op[0][0:3] == 'bor':
            # return self.bitwise_or(op)
            return self.binary_operation(op, operator.or_)
        if op[0][0:3] == 'set':
            return self.assignment(op)
        if op[0][0:2] == 'gt':
            # return self.greater_than(op)
            return self.comparison_operation(op, operator.gt)
        if op[0][0:2] == 'eq':
            # return self.equality(op)
            return self.comparison_operation(op, operator.eq)
        return 1

    def binary_operation(self, op, operation):
        op[1] = self.registers[0]
        # deal with any input registers
        if op[0][3] == 'r':
            op[2] = self.registers[1]

        self.registers[op[3]] = operation(op[1], op[2])
        return 0

    def addition(self, op):
        """
        addr (add register)
        addi (add immediate)
        """
        if op[0][0:3] != 'add':
            return 1

        op[1] = self.registers[0]
        # deal with any input registers
        if op[0][3] == 'r':
            op[2] = self.registers[1]

        self.registers[op[3]] = op[1] + op[2]
        return 0

    def multiplication(self, op):
        """
        mulr (multiply register)
        muli (multiply immediate)
        """
        if op[0][0:3] != 'mul':
            return 1

        op[1] = self.registers[0]
        # deal with any input registers
        if op[0][3] == 'r':
            op[2] = self.registers[1]

        self.registers[op[3]] = op[1] * op[2]
        return 0

    def bitwise_and(self, op):
        """
        banr (bitwise AND register)
        bani (bitwise AND immediate)
        """
        if op[0][0:3] != 'ban':
            return 1

        op[1] = self.registers[0]
        # deal with any input registers
        if op[0][3] == 'r':
            op[2] = self.registers[1]

        self.registers[op[3]] = op[1] & op[2]
        return 0

    def bitwise_or(self, op):
        """
        borr (bitwise OR register)
        bori (bitwise OR immediate)
        """
        if op[0][0:3] != 'bor':
            return 1

        op[1] = self.registers[0]
        # deal with any input registers
        if op[0][3] == 'r':
            op[2] = self.registers[1]

        self.registers[op[3]] = op[1] | op[2]
        return 0

    def assignment(self, op):
        """
        setr (set register)
        seti (set immediate)
        """
        if op[0][0:3] != 'set':
            return 1

        # deal with any input registers
        if op[0][3] == 'r':
            op[1] = self.registers[0]

        self.registers[op[3]] = op[1]
        return 0

    def comparison_operation(self, op, operation):
        # deal with any input registers
        if op[0][2] == 'r':
            op[1] = self.registers[0]
        if op[0][3] == 'r':
            op[2] = self.registers[1]

        if operation(op[1], op[2]):
            self.registers[op[3]] = 1
        else:
            self.registers[op[3]] = 0
        return 0

    def greater_than(self, op):
        """
        gtir (greater-than immediate/register)
        gtri (greater-than register/immediate)
        gtrr (greater-than register/register)
        """
        if op[0][0:2] != 'gt':
            return 1

        # deal with any input registers
        if op[0][2] == 'r':
            op[1] = self.registers[0]
        if op[0][3] == 'r':
            op[2] = self.registers[1]

        if op[1] > op[2]:
            self.registers[op[3]] = 1
        else:
            self.registers[op[3]] = 0
        return 0

    def equality(self, op):
        """
        eqir (equal immediate/register)
        eqri (equal register/immediate)
        eqrr (equal register/register)
        """
        if op[0][0:2] != 'eq':
            return 1

        # deal with any input registers
        if op[0][2] == 'r':
            op[1] = self.registers[0]
        if op[0][3] == 'r':
            op[2] = self.registers[1]

        if op[1] == op[2]:
            self.registers[op[3]] = 1
        else:
            self.registers[op[3]] = 0
        return 0

    def check_observation(self, observation):
        """
        Observation format:
        ['Before: [3, 2, 1, 1]', '9 2 1 2', 'After:  [3, 2, 2, 1]']
        """
        raw_before, raw_operation, raw_after = observation
        before = [int(i) for i in re.findall(r'(\d+)', raw_before)]
        operation = [int(i) for i in re.findall(r'(\d+)', raw_operation)]
        after = [int(i) for i in re.findall(r'(\d+)', raw_after)]

        possible_match = 0
        for op_code in ['addr', 'addi',
                        'mulr', 'muli',
                        'banr', 'bani',
                        'borr', 'bori',
                        'setr', 'seti',
                        'gtir', 'gtri', 'gtrr',
                        'eqir', 'eqri', 'eqrr']:
            operation[0] = op_code
            self.registers = before[:]
            result = self.operation(operation)
            if result != 0:
                raise Exception('Unexpected operation')
            if self.registers == after:
                possible_match += 1
        return possible_match


def test_obsercations():
    processor = Processor([])
    more_than_2 = [1 for obs in INPUT_PART_1 if processor.check_observation(obs) > 2]
    assert len(more_than_2) == 427  # 427 not right and 382, 192 and 170 too low
