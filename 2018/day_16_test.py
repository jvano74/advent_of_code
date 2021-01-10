import re
import operator
from collections import defaultdict
from typing import NamedTuple


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

    --- Part Two ---
    Using the samples you collected, work out the number of each opcode and execute the test program
    (the second section of your puzzle input).

    What value is contained in register 0 after executing the test program?
    """
    pass


with open('day_16_input.txt') as fp:
    part_1_raw, part_2_raw = fp.read().split('\n\n\n\n')
    INPUT_PART_1 = [[ln.strip() for ln in ex.split('\n')] for ex in part_1_raw.split('\n\n')]
    INPUT_PART_2 = [[int(d) for d in ln.strip().split(' ')] for ln in part_2_raw.split('\n')]


def test_input():
    assert INPUT_PART_1[0] == ['Before: [0, 2, 0, 2]', '6 0 1 1', 'After:  [0, 1, 0, 2]']
    assert INPUT_PART_1[-1] == ['Before: [1, 2, 2, 1]', '9 3 1 3', 'After:  [1, 2, 2, 1]']
    assert len(INPUT_PART_1) == 811
    assert INPUT_PART_2[0] == [2, 0, 1, 1]
    assert INPUT_PART_2[-1] == [12, 2, 0, 0]


class Observation(NamedTuple):
    operation: list
    register_before: list
    register_after: list

    @staticmethod
    def raw(raw_observation):
        """
        Observation format:
        ['Before: [3, 2, 1, 1]', '9 2 1 2', 'After:  [3, 2, 2, 1]']
        """
        raw_before, raw_operation, raw_after = raw_observation
        before = [int(i) for i in re.findall(r'(\d+)', raw_before)]
        operation = [int(i) for i in re.findall(r'(\d+)', raw_operation)]
        after = [int(i) for i in re.findall(r'(\d+)', raw_after)]
        return Observation(operation, before, after)


class Processor:
    op_codes = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
                'setr', 'seti',
                'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

    binary_operations = {'add': operator.add, 'mul': operator.mul,
                         'ban': operator.and_, 'bor': operator.or_}

    comparison_operations = {'gt': operator.gt,
                             'eq': operator.eq}

    def __init__(self, code):
        self.code = code
        self.execution_pointer = 0
        self.registers = [0, 0, 0, 0]
        self.op_code_id_to_code = {}

    def step(self):
        if 0 <= self.execution_pointer < len(self.code):
            op = self.code[self.execution_pointer]
            result = self.operation(op)
            self.execution_pointer += 1
            return result
        return 1, 'execution_pointer out of range'

    def run(self, code):
        self.code = code
        self.execution_pointer = 0
        self.registers = [0, 0, 0, 0]
        while True:
            result = self.step()
            if result != 0:
                return result

    def operation(self, instruction):
        op = instruction[0]
        if op in self.op_code_id_to_code:
            op = self.op_code_id_to_code[op]
        op_io = instruction[1:]

        base_inst = op[0:3]
        if base_inst in self.binary_operations:
            return self.binary_operation(op[3], op_io, self.binary_operations[base_inst])
        if base_inst == 'set':
            return self.assignment(op[3], op_io)

        base_inst = op[0:2]
        if base_inst in self.comparison_operations:
            return self.comparison_operation(op[2:], op_io, self.comparison_operations[base_inst])

        return 1

    def binary_operation(self, op, op_io, operation):
        op_io[0] = self.registers[op_io[0]]
        # deal with any input registers
        if op == 'r':
            op_io[1] = self.registers[op_io[1]]
        self.registers[op_io[2]] = operation(op_io[0], op_io[1])
        return 0

    def assignment(self, op, op_io):
        # deal with any input registers
        if op == 'r':
            op_io[0] = self.registers[op_io[0]]
        self.registers[op_io[2]] = op_io[0]
        return 0

    def comparison_operation(self, op, op_io, operation):
        # deal with any input registers
        if op[0] == 'r':
            op_io[0] = self.registers[op_io[0]]
        if op[1] == 'r':
            op_io[1] = self.registers[op_io[1]]

        if operation(op_io[0], op_io[1]):
            self.registers[op_io[2]] = 1
        else:
            self.registers[op_io[2]] = 0
        return 0

    def check_observation(self, obs: Observation):
        matching_op_codes = set()
        unknown_ops = set(self.op_codes) - set(self.op_code_id_to_code.values())
        for op_code in unknown_ops:
            obs.operation[0] = op_code
            self.registers = obs.register_before[:]
            result = self.operation(obs.operation)
            if result != 0:
                raise Exception('Unexpected operation')
            if self.registers == obs.register_after:
                matching_op_codes.add(op_code)
        return matching_op_codes

    def decompile(self, raw_observations):
        unresolved_observations = defaultdict(list)
        for raw_observation in raw_observations:
            observation = Observation.raw(raw_observation)
            unresolved_observations[observation.operation[0]].append(observation)

        pass_number = 0
        possible_id_to_codes = {}
        while len(unresolved_observations) > 0:
            pass_number += 1
            now_resolved_code_ids = set()
            for op_code_id, observations in unresolved_observations.items():
                for observation in observations:
                    matching_op_codes = self.check_observation(observation)
                    if op_code_id in possible_id_to_codes:
                        matching_op_codes = possible_id_to_codes[op_code_id].intersection(matching_op_codes)

                    if len(matching_op_codes) == 1:
                        op_code = matching_op_codes.pop()
                        self.op_code_id_to_code[op_code_id] = op_code
                        now_resolved_code_ids.add(op_code_id)
                        break  # op_code_id done, no need to review further observations
                    else:
                        possible_id_to_codes[op_code_id] = matching_op_codes  # update
            for code_id in now_resolved_code_ids:
                unresolved_observations.pop(code_id)

        return pass_number


SAMPLE_OBSERVATION = Observation(operation=[9, 2, 1, 2],
                                 register_before=[3, 2, 1, 1],
                                 register_after=[3, 2, 2, 1])


def test_observations():
    processor = Processor(INPUT_PART_2)
    assert processor.check_observation(SAMPLE_OBSERVATION) == {'addi', 'mulr', 'seti'}

    more_than_2 = [1 for obs in INPUT_PART_1 if len(processor.check_observation(Observation.raw(obs))) > 2]
    assert sum(more_than_2) == 560
    decompile_passes = processor.decompile(INPUT_PART_1)
    assert decompile_passes == 5
    processor.run(INPUT_PART_2)
    assert processor.registers[0] == 622
