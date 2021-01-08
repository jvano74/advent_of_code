from collections import defaultdict
import re
import sympy


class Puzzle:
    """
    --- Day 23: Coprocessor Conflagration ---
    You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental
    coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause
    serious issues for the rest of the computer, so you head in and see what you can do.

    The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality
    seems very similar, but some of the instructions are different:

    - set X Y sets register X to the value of Y.
    - sub X Y decreases register X by the value of Y.
    - mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    - jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips
      the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

    Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

    The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing
    any meaningful work.

    If you run the program (your puzzle input), how many times is the mul instruction invoked?

    --- Part Two ---
    Now, it's time to fix the problem.

    The debug mode switch is wired directly to register a. You flip the switch, which makes register a now start at 1
    when the program is executed.

    Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose a very
    efficient implementation. You'll need to optimize the program if it has any hope of completing before Santa
    needs that printer working.

    The coprocessor's ultimate goal is to determine the final value left in register h once the program completes.
    Technically, if it had that... it wouldn't even need to run the program.

    After setting register a to 1, if the program were to run to completion, what value would be left in register h?
    """
    pass


INPUT = ['set b 84', 'set c b', 'jnz a 2', 'jnz 1 5', 'mul b 100', 'sub b -100000', 'set c b', 'sub c -17000',
         'set f 1', 'set d 2', 'set e 2', 'set g d', 'mul g e', 'sub g b', 'jnz g 2', 'set f 0', 'sub e -1',
         'set g e', 'sub g b', 'jnz g -8', 'sub d -1', 'set g d', 'sub g b', 'jnz g -13', 'jnz f 2', 'sub h -1',
         'set g b', 'sub g c', 'jnz g 2', 'jnz 1 3', 'sub b -17', 'jnz 1 -23']


class Micro:
    def __init__(self, code, std_in=None, std_out=None, rcv_as_recover=True):
        self.rcv_as_recover = rcv_as_recover
        if std_in is None:
            std_in = []
        if std_out is None:
            std_out = []
        self.code = code
        self.registers = defaultdict(int)
        self.execution = 0
        self.line_in = std_in
        self.next_read = 0
        self.line_out = std_out
        self.paused = False
        self.hx = defaultdict(int)

    def get_value(self, in_val):
        """
        Get the value of the input character, either from input string if numeric or value from register if letter
        """
        if re.match(r'-?\d+', in_val):
            return int(in_val)
        return self.registers[in_val]

    def can_read(self):
        return self.next_read < len(self.line_in)

    def ready_to_resume(self):
        if self.paused and self.can_read():
            return True
        return False

    def tick(self):
        """
        - set X Y sets register X to the value of Y.
        - sub X Y decreases register X by the value of Y.
        - mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
        - jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips
          the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

        return/exit codes:
        0, msg - continue
        1, msg - halting
        2, msg - out of range
        """
        if not (0 <= self.execution < len(self.code)):
            return 2, 'out of range'
        instruction = self.code[self.execution].split(' ')

        # jump instruction
        if instruction[0] == 'jnz':
            if self.get_value(instruction[1]) != 0:
                self.execution += self.get_value(instruction[2])
            else:
                self.execution += 1
            return 0, 'jnz'

        # for nom jump point to next execution
        self.execution += 1

        # register instructions
        if instruction[0] == 'set':
            self.registers[instruction[1]] = self.get_value(instruction[2])
            return 0, 'set'
        if instruction[0] == 'sub':
            self.registers[instruction[1]] -= self.get_value(instruction[2])
            return 0, 'sub'
        if instruction[0] == 'mul':
            self.registers[instruction[1]] *= self.get_value(instruction[2])
            return 0, 'mul'

    def run(self):
        self.paused = False
        self.hx = defaultdict(int)
        while True:
            exit_code = self.tick()
            if exit_code[0] != 0:
                return exit_code
            self.hx[exit_code[1]] += 1


def test_micro2():
    micro = Micro(INPUT)
    assert micro.run() == (2, 'out of range')
    assert micro.hx['mul'] == 6724
    assert micro.registers['h'] == 1


def manual_review(a=0):
    """
    set a 1 (new)
    set b 84
    set c b
    jnz a 2 <-- down to m
    jnz 1 5 <---- down to n [test mode b=84, c=84]
    mul b 100 <-- m b = 8400
    sub b -100_000   b = 18400
    set c b          c = 18400
    sub c -17000  [live mode b=108_400, c=125_400]

    set [[f]] 1 <---- n <====== t (each jump back b += 17, c remains fixed)
    set d 2
        set e 2 <---------- q               e starts at 2
            set g d <-------- p             g = d  (d = 2 until g=0 loop ends then d = 3, then 4 etc...
            mul g e
            sub g b                         g = g*e - b
              jnz g 2 <------ down to o     if g = 0 skip h count
              set [[f]] 0
            sub e -1 <------ o [e += 1]
            set g e
            sub g b
            jnz g -8 <-------- up to p

        sub d -1
        set g d
        sub g b
        jnz g -13 <---------- up q
      jnz [[f]] 2 <== down to r
      sub [[[h]]] -1                        (h only appears here, is basic counter)
      set g b <== r
    sub g c                                 g = g - c (note c is fixed)
      jnz g 2 <==== down to s
      jnz 1 3 <-- END (g = 0)
    sub b -17 <==== s
    jnz 1 -23 <====== up to t
    """
    h = 0
    b, c = (84, 84) if a == 0 else (108_400, 125_400)
    for b in range(b, c+1, 17):
        # this is counting primes
        # for d in range(2, b):
        #    for e in range(2, b):
        #        if d * e == b:
        #            f = 0
        # if f == 0:
        #    h += 1
        if not sympy.isprime(b):
            h += 1
    return h


def test_manual_review():
    assert manual_review(0) == 1
    assert manual_review(1) == 903
