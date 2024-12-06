from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 24: Arithmetic Logic Unit ---

    Magic smoke starts leaking from the submarine's arithmetic logic unit (ALU). Without the ability to perform basic
    arithmetic and logic functions, the submarine can't produce cool patterns with its Christmas lights!

    It also can't navigate. Or run the oxygen system.

    Don't worry, though - you probably have enough oxygen left to give you enough time to build a new ALU.

    The ALU is a four-dimensional processing unit: it has integer variables w, x, y, and z. These variables all start
    with the value 0. The ALU also supports six instructions:

    inp a - Read an input value and write it to variable a.
    add a b - Add the value of a to the value of b, then store the result in variable a.
    mul a b - Multiply the value of a by the value of b, then store the result in variable a.
    div a b - Divide the value of a by the value of b, truncate the result to an integer, then
              store the result in variable a. (Here, "truncate" means to round the value toward zero.)
    mod a b - Divide the value of a by the value of b, then store the remainder in variable a.
              (This is also called the modulo operation.)
    eql a b - If the value of a and b are equal, then store the value 1 in variable a.
              Otherwise, store the value 0 in variable a.

    In all of these instructions, a and b are placeholders; a will always be the variable where the result
    of the operation is stored (one of w, x, y, or z), while b can be either a variable or a number. Numbers
    can be positive or negative, but will always be integers.

    The ALU has no jump instructions; in an ALU program, every instruction is run exactly once in order from
    top to bottom. The program halts after the last instruction has finished executing.

    (Program authors should be especially cautious; attempting to execute div with b=0 or attempting to execute mod
    with a<0 or b<=0 will cause the program to crash and might even damage the ALU. These operations are never intended
    in any serious ALU program.)

    For example, here is an ALU program which takes an input number, negates it, and stores it in x:

    inp x
    mul x -1

    Here is an ALU program which takes two input numbers, then sets z to 1 if the second input number is three times
    larger than the first input number, or sets z to 0 otherwise:

    inp z
    inp x
    mul z 3
    eql z x

    Here is an ALU program which takes a non-negative integer as input, converts it into binary, and stores the
    lowest (1's) bit in z, the second-lowest (2's) bit in y, the third-lowest (4's) bit in x, and the
    fourth-lowest (8's) bit in w:

    inp w
    add z w
    mod z 2
    div w 2
    add y w
    mod y 2
    div w 2
    add x w
    mod x 2
    div w 2
    mod w 2

    Once you have built a replacement ALU, you can install it in the submarine, which will immediately resume what it
    was doing when the ALU failed: validating the submarine's model number. To do this, the ALU will run the MOdel
    Number Automatic Detector program (MONAD, your puzzle input).

    Submarine model numbers are always fourteen-digit numbers consisting only of digits 1 through 9. The digit 0
    cannot appear in a model number.

    When MONAD checks a hypothetical fourteen-digit model number, it uses fourteen separate inp instructions, each
    expecting a single digit of the model number in order of most to least significant. (So, to check the model
    number 13579246899999, you would give 1 to the first inp instruction, 3 to the second inp instruction, 5 to
    the third inp instruction, and so on.) This means that when operating MONAD, each input instruction should
    only ever be given an integer value of at least 1 and at most 9.

    Then, after MONAD has finished running all of its instructions, it will indicate that the model number was
    valid by leaving a 0 in variable z. However, if the model number was invalid, it will leave some other
    non-zero value in z.

    MONAD imposes additional, mysterious restrictions on model numbers, and legend says the last copy of the MONAD
    documentation was eaten by a tanuki. You'll need to figure out what MONAD does some other way.

    To enable as many submarine features as possible, find the largest valid fourteen-digit model number that
    contains no 0 digits. What is the largest model number accepted by MONAD?

    To begin, get your puzzle input.
    """


with open(Path(__file__).parent / "2021_24_input.txt") as fp:
    INPUT = [line.strip() for line in fp]


class Monad:
    def __init__(self, program):
        self.program = program
        self.variables = dict()
        self.input_buffer = []

    def run(self, input_string):
        """
        inp a - read input and write to a
        add a b - add value of a to value of b, store result in variable a
        mul a b - multiply value of a by value of b, store result in variable a
        div a b - divide value of a by the value of b, truncate to integer, store in variable a
        mod a b - divide value of a by the value of b, then store remainder in variable a
        eql a b - if value of a and b are equal, store 1 in variable a, otherwise, store 0 in variable a
        """
        self.input_buffer = [int(d) for d in list(str(input_string))]
        self.variables = {"w": 0, "x": 0, "y": 0, "z": 0}
        for pointer, raw_instruction in enumerate(self.program):
            cmd = raw_instruction[:3]
            var = raw_instruction[4]
            value = raw_instruction.split(" ")[-1]
            if cmd == "inp":
                self.variables[var] = self.input_buffer.pop(0)
            elif cmd == "add":
                if value.isdigit() or value[0] == "-":
                    self.variables[var] += int(value)
                else:
                    self.variables[var] += self.variables[value]
            elif cmd == "mul":
                if value.isdigit() or value[0] == "-":
                    self.variables[var] *= int(value)
                else:
                    self.variables[var] *= self.variables[value]
            elif cmd == "div":
                if value.isdigit() or value[0] == "-":
                    self.variables[var] //= int(value)
                else:
                    self.variables[var] //= self.variables[value]
            elif cmd == "mod":
                if value.isdigit() or value[0] == "-":
                    self.variables[var] %= int(value)
                else:
                    self.variables[var] %= self.variables[value]
            elif cmd == "eql":
                if value.isdigit() or value[0] == "-":
                    self.variables[var] = 1 if self.variables[var] == int(value) else 0
                else:
                    self.variables[var] = (
                        1 if self.variables[var] == self.variables[value] else 0
                    )
        return self.variables["z"]

    def analyze(self, input_string):
        """
        inp a - read input and write to a
        add a b - add value of a to value of b, store result in variable a
        mul a b - multiply value of a by value of b, store result in variable a
        div a b - divide value of a by the value of b, truncate to integer, store in variable a
        mod a b - divide value of a by the value of b, then store remainder in variable a
        eql a b - if value of a and b are equal, store 1 in variable a, otherwise, store 0 in variable a
        """
        self.input_buffer = list(input_string)
        self.variables = {"w": "0", "x": "0", "y": "0", "z": "0"}
        zero_checks = []

        for pointer, raw_instruction in enumerate(self.program):
            cmd = raw_instruction[:3]
            var = raw_instruction[4]
            value = raw_instruction.split(" ")[-1]
            if cmd == "inp":
                self.variables[var] = self.input_buffer.pop(0)
            else:
                left = self.variables[var]
                if value.isdigit() or value[0] == "-":
                    right = value
                else:
                    right = self.variables[value]
                next_value = None
                if cmd == "add":
                    if left == "0":
                        next_value = right
                    elif right == 0:
                        next_value = left
                    else:
                        next_value = f"({left}+{right})"
                elif cmd == "mul":
                    if left == "0" or right == "0":
                        next_value = "0"
                    elif left == "1":
                        next_value = right
                    elif right == "1":
                        next_value = left
                    else:
                        next_value = f"({left}*{right})"
                elif cmd == "div":
                    if left == "0":
                        next_value = "0"
                    elif right == "1":
                        next_value = left
                    else:
                        next_value = f"({left}/{right})"
                elif cmd == "mod":
                    if left == "0" or right == "1":
                        next_value = "0"
                    else:
                        next_value = f"({left}%{right})"
                elif cmd == "eql":
                    if right == "0":
                        zero_checks.append(left)
                        next_value = f"z{len(zero_checks)}"
                        # next_value = '0'  # after running with above z1, z2, z3, etc sub all z = 0 (single digit)
                    elif left == right:
                        next_value = "1"
                    else:
                        next_value = f"({left}=={right})"
                self.variables[var] = next_value

        return self.variables["z"], zero_checks

    def extract_monads(self):
        monads = defaultdict(list)
        local = 0
        max_line = 0
        m_vars = []
        m_settings = []
        for n, line in enumerate(self.program):
            if line == "inp w":
                if n > 0:
                    m_settings.append(m_vars)
                m_vars = []
                local = 0
            else:
                local += 1
                max_line = max(max_line, local)
            monads[local].append(line)
            # extract variables
            if local in [4, 5, 15]:
                m_vars.append(int(line.split(" ")[-1]))
        m_settings.append(m_vars)
        return [
            "| ".join(f"{i: <9}" for i in monads[i]) for i in range(max_line + 1)
        ], m_settings


# def test_run_monad():
#     monad = Monad(INPUT)
#     n = 0
#     result = 1
#     runs_before_heat_death_of_universe = False
#     assert runs_before_heat_death_of_universe
#     while result != 0:
#         n += 1
#         result = monad.run(100_000_000_000_000 - n)
#     assert (100_000_000_000_000 - n) == 99999999999999


def test_analyze_monad():
    monad = Monad(INPUT)
    assert monad.analyze("abcdefghijklmn") != ""  # was too complex
    aligned_commands, m_settings = monad.extract_monads()
    print("\n\n")
    print("\n".join([f"{i:0>2}| {n}" for i, n in enumerate(aligned_commands)]))
    print("\n\n")
    assert m_settings == [
        [1, 11, 14],
        [1, 13, 8],
        [1, 11, 4],
        [1, 10, 10],
        [26, -3, 14],
        [26, -4, 10],
        [1, 12, 4],
        [26, -8, 14],
        [26, -3, 1],
        [26, -12, 6],
        [1, 14, 0],
        [26, -6, 9],
        [1, 11, 13],
        [26, -12, 12],
    ]


"""
| inp w    | x = 0 if w == (z %26) + v2
| mul x 0  |
| add x z  |
| mod x 26 | 
| div z v1 | z //= v1 (1 or 26)
| add x v2 |
| eql x w  | 
| eql x 0  |
| mul y 0  |
| add y 25 |
| mul y x  |
| add y 1  |
| mul z y  | z *= 26 if w != (z %26) + v2 else 1
| mul y 0  |
| add y w  |
| add y v3 |
| mul y x  | y = w + v3 if w != (z %26) + v2 else 0
| add z y  | z += y
"""


def next_z(w, z, v1, v2, v3):
    if w == ((z % 26) + v2):
        return z // v1
    else:
        return (z // v1) * 26 + (w + v3)


def my_function(input_string):
    w = [int(d) for d in list(str(input_string))]
    # m_settings from above
    m_settings = [
        [1, 11, 14],
        [1, 13, 8],
        [1, 11, 4],
        [1, 10, 10],
        [26, -3, 14],
        [26, -4, 10],
        [1, 12, 4],
        [26, -8, 14],
        [26, -3, 1],
        [26, -12, 6],
        [1, 14, 0],
        [26, -6, 9],
        [1, 11, 13],
        [26, -12, 12],
    ]
    z = 0
    for i, (v1, v2, v3) in enumerate(m_settings):
        # z = next_z(w[i], z, v1, v2, v3)  # put function inline to streamline
        if w[i] == ((z % 26) + v2):
            z = z // v1
        else:
            z = (z // v1) * 26 + (w[i] + v3)
    return z


def test_direct_monad():
    monad = Monad(INPUT)
    for test_n in range(90_000_000_000_000, 90_000_000_005_000):
        result_slow = monad.run(test_n)
        result_fast = my_function(test_n)
        assert result_slow == result_fast


# def test_fast_monad():
#     test_n = 100_000_000_000_000
#     runs_before_heat_death_of_universe = False
#     assert runs_before_heat_death_of_universe
#     while True:
#         test_n -= 1
#         if my_function(test_n) == 0:
#             break
#     assert test_n == 99999999999999


def find_zeros_forward(max_depth=None, find_lowest=False):
    # m_settings from above
    m_settings = [
        [1, 11, 14],
        [1, 13, 8],
        [1, 11, 4],
        [1, 10, 10],
        [26, -3, 14],
        [26, -4, 10],
        [1, 12, 4],
        [26, -8, 14],
        [26, -3, 1],
        [26, -12, 6],
        [1, 14, 0],
        [26, -6, 9],
        [1, 11, 13],
        [26, -12, 12],
    ]

    current_z_range = {0: ""}

    for p, (v1, v2, v3) in enumerate(m_settings):
        if max_depth is not None and p > max_depth:
            break
        next_z_range = dict()
        low, high, step = (9, 0, -1) if find_lowest else (1, 10, 1)
        for d in range(low, high, step):
            for z, hx in current_z_range.items():
                if d == ((z % 26) + v2):
                    nz = z // v1
                else:
                    nz = (z // v1) * 26 + (d + v3)
                next_z_range[nz] = f"{hx}{d}"
        current_z_range = next_z_range
    return current_z_range


def pre_image(v1, v2, v3, z_out):
    results = set()
    # d == ((z % 26) + v2)
    if v1 == 1:
        z = z_out
        d = (z % 26) + v2
        if d in range(1, 10):
            results.add((d, z))
    elif v1 == 26:
        z_in = [26 * z_out + i for i in range(0, 26)]
        for z in z_in:
            d = (z % 26) + v2
            if d in range(1, 10):
                results.add((d, z))
    # d != ((z % 26) + v2)
    for d in range(1, 10):
        if (z_out - v3 - d) % 26 == 0:
            if v1 == 1:
                z = (z_out - v3 - d) // 26
                if d != ((z % 26) + v2):
                    results.add((d, z))
            elif v1 == 26:
                z_in = [(z_out - v3 - d) + i for i in range(0, 26)]
                for z in z_in:
                    if d != ((z % 26) + v2):
                        results.add((d, z))
    return results


def find_zeros_rev(max_depth=None):
    # m_settings from above
    m_settings = [
        [1, 11, 14],
        [1, 13, 8],
        [1, 11, 4],
        [1, 10, 10],
        [26, -3, 14],
        [26, -4, 10],
        [1, 12, 4],
        [26, -8, 14],
        [26, -3, 1],
        [26, -12, 6],
        [1, 14, 0],
        [26, -6, 9],
        [1, 11, 13],
        [26, -12, 12],
    ]
    m_settings.reverse()

    current_z_out = defaultdict(str)
    current_z_out[0] = ""

    for p, (v1, v2, v3) in enumerate(m_settings):
        if max_depth is not None and p > max_depth:
            break
        next_z_out = defaultdict(str)
        for z_out, hx in current_z_out.items():
            for d, z in pre_image(v1, v2, v3, z_out):
                next_z_out[z] = max(next_z_out[z], f"{d}{hx}")
        current_z_out = next_z_out
    return current_z_out


def test_find_zeros_part1():
    # part 1
    z_range = find_zeros_forward(13)
    assert z_range[0] == "74929995999389"


def test_find_zeros_part2():
    # part 2
    z_range = find_zeros_forward(13, find_lowest=True)
    assert z_range[0] == "11118151637112"
    # z_outs = find_zeros_rev(5)
