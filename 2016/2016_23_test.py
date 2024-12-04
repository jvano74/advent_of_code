from collections import defaultdict
import re


class Puzzle:
    """
    --- Day 23: Safe Cracking ---
    This is one of the top floors of the nicest tower in EBHQ. The Easter Bunny's private office is here, complete with
    a safe hidden behind a painting, and who wouldn't hide a star in a safe behind a painting?

    The safe has a digital screen and keypad for code entry. A sticky note attached to the safe has a password hint on
    it: "eggs". The painting is of a large rabbit coloring some eggs. You see 7.

    When you go to type the code, though, nothing appears on the display; instead, the keypad comes apart in your
    hands, apparently having been smashed. Behind it is some kind of socket - one that matches a connector in your
    prototype computer! You pull apart the smashed keypad and extract the logic circuit, plug it into your computer,
    and plug your computer into the safe.

    Now, you just need to figure out what output the keypad would have sent to the safe. You extract the assembunny
    code from the logic chip (your puzzle input).

    The code looks like it uses almost the same architecture and instruction set that the monorail computer used! You
    should be able to use the same assembunny interpreter for this as you did there, but with one new instruction:

    tgl x toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative
    means backward):

    - For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
    - For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
    - The arguments of a toggled instruction are not affected.
    - If an attempt is made to toggle an instruction outside the program, nothing happens.
    - If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that
      instruction, skip it instead.
    - If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting
      instruction is not executed until the next time it is reached.

    For example, given this program:

    cpy 2 a
    tgl a
    tgl a
    tgl a
    cpy 1 a
    dec a
    dec a
    cpy 2 a initializes register a to 2.

    The first tgl a toggles an instruction a (2) away from it, which changes the third tgl a into inc a.
    The second tgl a also modifies an instruction 2 away from it, which changes the cpy 1 a into jnz 1 a.
    The fourth line, which is now inc a, increments a to 3.
    Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions ahead, skipping the dec a instructions.

    In this example, the final value in register a is 3.

    The rest of the electronics seem to place the keypad entry (the number of eggs, 7) in register a, run the code,
    and then send the value left in register a to the safe.

    What value should be sent to the safe?

    --- Part Two ---
    The safe doesn't open, but it does make several angry noises to express its frustration.

    You're quite sure your logic is working correctly, so the only other thing is... you check the painting again. As
    it turns out, colored eggs are still eggs. Now you count 12.

    As you run the program with this new input, the prototype computer begins to overheat. You wonder what's taking
    so long, and whether the lack of any instruction more powerful than "add one" has anything to do with it. Don't
    bunnies usually multiply?

    Anyway, what value should actually be sent to the safe?
    """
    pass


INPUT = ['cpy a b', 'dec b', 'cpy a d', 'cpy 0 a', 'cpy b c', 'inc a', 'dec c', 'jnz c -2', 'dec d', 'jnz d -5',
         'dec b', 'cpy b c', 'cpy c d', 'dec d', 'inc c', 'jnz d -2', 'tgl c', 'cpy -16 c', 'jnz 1 c',
         'cpy 73 c', 'jnz 82 d', 'inc a', 'inc d', 'jnz d -2', 'inc c', 'jnz c -5']


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

            if cmd == 'tgl':
                tgl_loc = self.execution + values[0]
                if 0 <= tgl_loc < len(self.program):
                    tgl_cmd, tgl_argv = self.program[tgl_loc].split(' ', 1)
                    if len(tgl_argv) == 1:
                        if tgl_cmd == 'inc':
                            tgl_cmd = 'dec'
                        else:
                            tgl_cmd = 'inc'
                    else:
                        if tgl_cmd == 'jnz':
                            tgl_cmd = 'cpy'
                        else:
                            tgl_cmd = 'jnz'
                    self.program[tgl_loc] = f'{tgl_cmd} {tgl_argv}'
                self.execution += 1
                return 0

            self.execution += 1
            if cmd == 'cpy':
                if type(argv[1]) != int:
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
    sample_processor = Processor(['cpy 2 a', 'tgl a', 'tgl a', 'tgl a', 'cpy 1 a', 'dec a', 'dec a'])
    assert sample_processor.run() == 3


def test_puzzle_processor():
    puzzle_processor = Processor(INPUT)
    puzzle_processor.registers['a'] = 7
    result = puzzle_processor.run()
    assert result == 11026


def xtest_puzzle_processor2():
    # run time too long, manually reviewed code to determine calculation
    puzzle_processor = Processor(INPUT)
    puzzle_processor.registers['a'] = 12
    result = puzzle_processor.run()
    assert result == 11026


"""
Based on text hint just looking at code...

0 'cpy a b',  
1 'dec b', 
2 'cpy a d',  a goes to d  <======= when c is -16
3 'cpy 0 a',  clears a

4 'cpy b c',  <==== puts b in c
5 'inc a',    <==
6 'dec c', 
7 'jnz c -2', <== adds c to a 
8 'dec d', 
9 'jnz d -5', <==== repeats d times 

net effect of above is a gets b * d with c and d = 0 at end
a * (a - 1) -> a = 12*11 = 132

10 'dec b',  a-2
11 'cpy b c', 
12 'cpy c d', 
13 'dec d',    <======
14 'inc c', 
15 'jnz d -2', <====== c + d = (a-2) + (a-2) -> c = 2(a-2) = 20 (vs 10)
16 'tgl c', 
17 'cpy -16 c', 
18 'jnz 1 c', << now cpy 1 to c <========== to c
19 'cpy 73 c', 
20 'jnz 82 d', << now cpy 82 d <==X
21 'inc a',    <=A
22 'inc d',  << now dec d
23 'jnz d -2', <=A  add d to a c times (e.g. add 73 * 82 to a)
24 'inc c', << now dec c 
25 'jnz c -5' <==X

Looks like this takes a * (a-1) * (a-2) * ... * 2 * 1 (e.g. factorial) and adds 73* 82
"""


def test_by_hand1():
    ans = 1
    for a in range(1, 8):
        ans *= a
    ans += 73 * 82
    assert ans == 11026


def test_by_hand2():
    ans = 1
    for a in range(1, 13):
        ans *= a
    ans += 73 * 82
    assert ans == 479007586
