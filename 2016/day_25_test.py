from collections import defaultdict
import re


class Puzzle:
    """
    --- Day 25: Clock Signal ---
    You open the door and find yourself on the roof. The city sprawls away from you for miles and miles.

    There's not much time now - it's already Christmas, but you're nowhere near the North Pole, much too far to
    deliver these stars to the sleigh in time.

    However, maybe the huge antenna up here can offer a solution. After all, the sleigh doesn't need the stars,
    exactly; it needs the timing data they provide, and you happen to have a massive signal generator right here.

    You connect the stars you have to your prototype computer, connect that to the antenna, and begin the transmission.

    Nothing happens.

    You call the service number printed on the side of the antenna and quickly explain the situation. "I'm not sure
    what kind of equipment you have connected over there," he says, "but you need a clock signal." You try to explain
    that this is a signal for a clock.

    "No, no, a clock signal - timing information so the antenna computer knows how to read the data you're sending it.
    An endless, alternating pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.

    You ask if the antenna can handle a clock signal at the frequency you would need to use for the data from the
    stars. "There's no way it can! The only antenna we've installed capable of that is on top of a top-secret Easter
    Bunny installation, and you're definitely not-" You hang up the phone.

    You've extracted the antenna's clock signal generation assembunny code (your puzzle input); it looks mostly
    compatible with code you worked on just recently.

    This antenna code, being a signal generator, uses one extra instruction:

    - out x transmits x (either an integer or the value of a register) as the next value for the clock signal.

    The code takes a value (via register a) that describes the signal to generate, but you're not sure how it's used.
    You'll have to find the input to produce the right signal through experimentation.

    What is the lowest positive integer that can be used to initialize register a and cause the code to output a
    clock signal of 0, 1, 0, 1... repeating forever?

    --- Part Two ---
    The antenna is ready. Now, all you need is the fifty stars required to generate the signal for the sleigh,
    but you don't have enough.

    You look toward the sky in desperation... suddenly noticing that a lone star has been installed at the top of
    the antenna! Only 49 more to go.

    You don't have enough stars to transmit the signal, though. You need 4 more.
    """
    pass


INPUT = ['cpy a d', 'cpy 15 c', 'cpy 170 b', 'inc d', 'dec b', 'jnz b -2', 'dec c', 'jnz c -5', 'cpy d a',
         'jnz 0 0', 'cpy a b', 'cpy 0 a', 'cpy 2 c', 'jnz b 2', 'jnz 1 6', 'dec b', 'dec c', 'jnz c -4',
         'inc a', 'jnz 1 -7', 'cpy 2 b', 'jnz c 2', 'jnz 1 4', 'dec b', 'dec c', 'jnz 1 -4', 'jnz 0 0',
         'out b', 'jnz a -19', 'jnz 1 -21']


class Processor:

    def __init__(self, program):
        self.program = program
        self.execution = 0
        self.registers = defaultdict(int)
        self.clock_signal = 1
        self.signal_hx = []

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
            elif cmd == 'out':
                if self.clock_signal == 1 and values[0] != 0:
                    return -1
                elif self.clock_signal == 0 and values[0] != 1:
                    return -1
                else:
                    self.clock_signal = values[0]  # ARG!@#$% bug with == rather than = broke search
                    #                                I ended up solving by hand - once fixed also found answer
                    if (self.execution, self.clock_signal, self.registers) in self.signal_hx:
                        return 11
                    self.signal_hx.append((self.execution, self.clock_signal, self.registers.copy()))
            return 0
        return 1

    def run(self):
        ret_code = 0
        while ret_code == 0:
            ret_code = self.step()
        return ret_code, self.registers['a']

    def rerun(self, reg_a=0):
        self.execution = 0
        self.registers = defaultdict(int)
        self.registers['a'] = reg_a
        self.clock_signal = 1
        self.signal_hx = []
        return self.run()


def test_processor():
    sample_processor = Processor(['cpy 41 a', 'inc a', 'inc a', 'dec a', 'jnz a 2', 'dec a'])
    assert sample_processor.run() == (1, 42)


def test_puzzle_processor():
    puzzle_processor = Processor(INPUT)
    # a = 180
    a = 0
    res_val = 0
    while res_val != 11:
        res_val, res_a = puzzle_processor.rerun(a)
        if res_val != 11:
            a += 1
    assert a == 180
    assert res_val == 11


"""
Reviewing code by hand

0    'cpy a d', 
1    'cpy 15 c', 
2    'cpy 170 b', <--- a
3    'inc d',     <- b
4    'dec b', 
5    'jnz b -2',  <- up to   d += b (170) c (15) times (so a gets 170*15)
6    'dec c', 
7    'jnz c -5',  <--- up to a 

[[ we can start on 8 with a as set, b=0, c=0 and d = a + 170*15 ]]
  
8    'cpy d a',   <====== v
9    'jnz 0 0',   <====== y  (either keep a or refresh with d)
10   'cpy a b', 
11   'cpy 0 a', 

12   'cpy 2 c',     <===== d
13   'jnz b 2', --> down to n  <=== h
14   'jnz 1 6', -----> down to z
15   'dec b',   --< n 
16   'dec c', 
17   'jnz c -4', <=== up to h
18   'inc a',  [[ a will be around d//2 when b hits 0 ]]
19   'jnz 1 -7', <===== up to d

20   'cpy 2 b', -----< z [ note c always comes in 2
21   'jnz c 2', --> down to w <=== w2
22   'jnz 1 4', ----> down to x
23   'dec b',   --< w
24   'dec c', 
25   'jnz 1 -4', <=== w2

26   'jnz 0 0', ----< x
27   'out b',     <<< TRANSMIT b 
28   'jnz a -19', <====== up tp y
29   'jnz 1 -21'  <====== up tp v

guessed 1546 (too high) which would make d at start = 2^12

it looks like this is getting the binary rep of d = a + 170*15

.. so if I take the desired output of binary 10101010 with enough digits to go above 170*15... 

looks like that works...
"""


def test_by_hand():
    assert 0b101010101010 - 170 * 15 == 180
