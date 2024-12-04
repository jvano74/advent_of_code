from pathlib import Path


class Puzzle:
    """
    --- Day 23: Opening the Turing Lock ---
    Little Jane Marie just got her very first computer for Christmas from some unknown benefactor. It comes with
    instructions and an example program, but the computer itself seems to be malfunctioning. She's curious what
    the program does, and would like you to help her run it.

    The manual explains that the computer supports two registers and six instructions (truly, it goes on to remind
    the reader, a state-of-the-art technology). The registers are named a and b, can hold any non-negative integer,
    and begin with a value of 0. The instructions are as follows:

    - hlf r sets register r to half its current value, then continues with the next instruction.
    - tpl r sets register r to triple its current value, then continues with the next instruction.
    - inc r increments register r, adding 1 to it, then continues with the next instruction.
    - jmp offset is a jump; it continues with the instruction offset away relative to itself.
    - jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
    - jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).

    All three jump instructions work with an offset relative to that instruction. The offset is always written with
    a prefix + or - to indicate the direction of the jump (forward or backward, respectively). For example, jmp +1
    would simply continue with the next instruction, while jmp +0 would continuously jump back to itself forever.

    The program exits when it tries to run an instruction beyond the ones defined.

    For example, this program sets a to 2, because the jio instruction causes it to skip the tpl instruction:

    inc a
    jio a, +2
    tpl a
    inc a

    What is the value in register b when the program in your puzzle input is finished executing?
    """

    pass


with open(Path(__file__).parent / "2015_23_input.txt") as fp:
    INPUT = [line.strip() for line in fp]


class Computer:
    def __init__(self, program):
        self.a = 0
        self.b = 0
        self.pointer = 0
        self.program = program

    def perform_instruction(self, i_line):
        if i_line[:3] == "hlf":
            if i_line[4] == "a" and self.a % 2 == 0:
                self.a //= 2
            elif i_line[4] == "b" and self.b % 2 == 0:
                self.b //= 2
            else:
                raise Exception(f"Invalid operation {i_line}")
            self.pointer += 1
        elif i_line[:3] == "tpl":
            if i_line[4] == "a":
                self.a *= 3
            elif i_line[4] == "b":
                self.b *= 3
            else:
                raise Exception(f"Invalid operation {i_line}")
            self.pointer += 1
        elif i_line[:3] == "inc":
            if i_line[4] == "a":
                self.a += 1
            elif i_line[4] == "b":
                self.b += 1
            else:
                raise Exception(f"Invalid operation {i_line}")
            self.pointer += 1
        elif i_line[:3] == "jmp":
            self.pointer += int(i_line[4:])
        elif i_line[:3] == "jie":
            if i_line[4:7] == "a, ":
                if self.a % 2 == 0:
                    self.pointer += int(i_line[7:])
                else:
                    # raise Exception(f'Undefined operation {i_line}')
                    self.pointer += 1
            elif i_line[4:7] == "b, ":
                if self.b % 2 == 0:
                    self.pointer += int(i_line[7:])
                else:
                    # raise Exception(f'Undefined operation {i_line}')
                    self.pointer += 1
            else:
                raise Exception(f"Invalid operation {i_line}")
        elif i_line[:3] == "jio":
            if i_line[4:7] == "a, ":
                if self.a == 1:
                    self.pointer += int(i_line[7:])
                else:
                    # raise Exception(f'Undefined operation {i_line}')
                    self.pointer += 1
            elif i_line[4:7] == "b, ":
                if self.b == 1:
                    self.pointer += int(i_line[7:])
                else:
                    # raise Exception(f'Undefined operation {i_line}')
                    self.pointer += 1
            else:
                raise Exception(f"Invalid operation {i_line}")
        else:
            raise Exception("Unknown operation")

    def run(self):
        while 0 <= self.pointer < len(self.program):
            self.perform_instruction(self.program[self.pointer])


def test_program():
    computer = Computer(INPUT)
    computer.run()
    assert computer.b == 255


def test_program2():
    computer = Computer(INPUT)
    computer.a = 1
    computer.run()
    assert computer.b == 334
