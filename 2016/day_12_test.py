from collections import defaultdict
import re


class Puzzle:
    """
     --- Day 12: Leonardo's Monorail ---
    You finally reach the top floor of this building: a garden with a slanted glass ceiling. Looks like there are no
    more stars to be had.

    While sitting on a nearby bench amidst some tiger lilies, you manage to decrypt some of the files you extracted
    from the servers downstairs.

    According to these documents, Easter Bunny HQ isn't just this building - it's a collection of buildings in the
    nearby area. They're all connected by a local monorail, and there's another building not far from here!
    Unfortunately, being night, the monorail is currently not operating.

    You remotely connect to the monorail control systems and discover that the boot sequence expects a password.
    The password-checking logic (your puzzle input) is easy to extract, but the code it uses is strange: it's
    assembunny code designed for the new computer you just assembled. You'll have to execute the code and get
    the password.

    The assembunny code you've extracted operates on four registers (a, b, c, and d) that start at 0 and can hold
    any integer. However, it seems to make use of only a few instructions:

    cpy x y copies x (either an integer or the value of a register) into register y.
    inc x increases the value of register x by one.
    dec x decreases the value of register x by one.
    jnz x y jumps to an instruction y away (positive means forward; negative means backward),
            but only if x is not zero.

    The jnz instruction moves relative to itself: an offset of -1 would continue at the previous instruction,
    while an offset of 2 would skip over the next instruction.

    For example:

    cpy 41 a
    inc a
    inc a
    dec a
    jnz a 2
    dec a

    The above code would set register a to 41, increase its value by 2, decrease its value by 1, and then skip the
    last dec a (because a is not zero, so the jnz a 2 skips it), leaving register a at 42. When you move past the
    last instruction, the program halts.

    After executing the assembunny code in your puzzle input, what value is left in register a?

    --- Part Two ---
    As you head down the fire escape to the monorail, you notice it didn't start; register c needs to be initialized
    to the position of the ignition key.

    If you instead initialize register c to be 1, what value is now left in register a?
    """
    pass


INPUT = ['cpy 1 a',
         'cpy 1 b',
         'cpy 26 d',
         'jnz c 2',
         'jnz 1 5',
         'cpy 7 c',
         'inc d',
         'dec c',
         'jnz c -2',
         'cpy a c',
         'inc a',
         'dec b',
         'jnz b -2',
         'cpy c b',
         'dec d',
         'jnz d -6',
         'cpy 18 c',
         'cpy 11 d',
         'inc a',
         'dec d',
         'jnz d -2',
         'dec c',
         'jnz c -5']


class Processor:

    def __init__(self, program):
        self.program = program
        self.execution = 0
        self.registers = defaultdict(int)

    def step(self):
        if 0 <= self.execution < len(self.program):
            cmd, argv = self.program[self.execution].split(' ', 1)
            argv = argv.split(' ')
            values = [int(v) if re.match(r'^-?\d+$', v) else self.registers[v] for v in argv]

            if cmd == 'jnz':
                if values[0] != 0:
                    self.execution += values[1]
                else:
                    self.execution += 1
                return 0

            self.execution += 1
            if cmd == 'cpy':
                self.registers[argv[1]] = values[0]
            elif cmd == 'inc':
                self.registers[argv[0]] += 1
            elif cmd == 'dec':
                self.registers[argv[0]] -= 1
            return 0
        return 1

    def run(self):
        while self.step() == 0:
            pass
        return self.registers['a']


def test_processor():
    sample_processor = Processor(['cpy 41 a', 'inc a', 'inc a', 'dec a', 'jnz a 2', 'dec a'])
    assert sample_processor.run() == 42


def test_puzzle_processor():
    puzzle_processor = Processor(INPUT)
    result = puzzle_processor.run()
    assert result == 318009


def test_puzzle2_processor():
    puzzle_processor = Processor(INPUT)
    puzzle_processor.registers['c'] = 1
    result = puzzle_processor.run()
    assert result == 9227663
