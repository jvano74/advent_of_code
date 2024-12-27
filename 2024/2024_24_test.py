from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 24: Crossed Wires ---
    You and The Historians arrive at the edge of a large grove somewhere in the
    jungle. After the last incident, the Elves installed a small device that
    monitors the fruit. While The Historians search the grove, one of them asks
    if you can take a look at the monitoring device; apparently, it's been
    malfunctioning recently.

    The device seems to be trying to produce a number through some boolean logic
    gates. Each gate has two inputs and one output. The gates all operate on
    values that are either true (1) or false (0).

    - AND gates output 1 if both inputs are 1; if either input is 0, these gates
      output 0.
    - OR gates output 1 if one or both inputs is 1; if both inputs are 0, these
      gates output 0.
    - XOR gates output 1 if the inputs are different; if the inputs are the
      same, these gates output 0.

    Gates wait until both inputs are received before producing output; wires can
    carry 0, 1 or no value at all. There are no loops; once a gate has
    determined its output, the output will not change until the whole system is
    reset. Each wire is connected to at most one gate output, but can be
    connected to many gate inputs.

    Rather than risk getting shocked while tinkering with the live system, you
    write down all of the gate connections and initial wire values (your puzzle
    input) so you can consider them in relative safety. For example:

    x00: 1
    x01: 1
    x02: 1
    y00: 0
    y01: 1
    y02: 0

    x00 AND y00 -> z00
    x01 XOR y01 -> z01
    x02 OR y02 -> z02

    Because gates wait for input, some wires need to start with a value (as
    inputs to the entire system). The first section specifies these values. For
    example, x00: 1 means that the wire named x00 starts with the value 1 (as if
    a gate is already outputting that value onto that wire).

    The second section lists all of the gates and the wires connected to them.
    For example, x00 AND y00 -> z00 describes an instance of an AND gate which
    has wires x00 and y00 connected to its inputs and which will write its
    output to wire z00.

    In this example, simulating these gates eventually causes 0 to appear on
    wire z00, 0 to appear on wire z01, and 1 to appear on wire z02.

    Ultimately, the system is trying to produce a number by combining the bits
    on all wires starting with z. z00 is the least significant bit, then z01,
    then z02, and so on.

    In this example, the three output bits form the binary number 100 which is
    equal to the decimal number 4.

    Here's a larger example:

    x00: 1
    x01: 0
    x02: 1
    x03: 1
    x04: 0
    y00: 1
    y01: 1
    y02: 1
    y03: 1
    y04: 1

    ntg XOR fgs -> mjb
    y02 OR x01 -> tnw
    kwq OR kpj -> z05
    x00 OR x03 -> fst
    tgd XOR rvg -> z01
    vdt OR tnw -> bfw
    bfw AND frj -> z10
    ffh OR nrd -> bqk
    y00 AND y03 -> djm
    y03 OR y00 -> psh
    bqk OR frj -> z08
    tnw OR fst -> frj
    gnj AND tgd -> z11
    bfw XOR mjb -> z00
    x03 OR x00 -> vdt
    gnj AND wpb -> z02
    x04 AND y00 -> kjc
    djm OR pbm -> qhw
    nrd AND vdt -> hwm
    kjc AND fst -> rvg
    y04 OR y02 -> fgs
    y01 AND x02 -> pbm
    ntg OR kjc -> kwq
    psh XOR fgs -> tgd
    qhw XOR tgd -> z09
    pbm OR djm -> kpj
    x03 XOR y03 -> ffh
    x00 XOR y04 -> ntg
    bfw OR bqk -> z06
    nrd XOR fgs -> wpb
    frj XOR qhw -> z04
    bqk OR frj -> z07
    y03 OR x01 -> nrd
    hwm AND bqk -> z03
    tgd XOR rvg -> z12
    tnw OR pbm -> gnj

    After waiting for values on all wires starting with z, the wires in this
    system have the following values:

    bfw: 1
    bqk: 1
    djm: 1
    ffh: 0
    fgs: 1
    frj: 1
    fst: 1
    gnj: 1
    hwm: 1
    kjc: 0
    kpj: 1
    kwq: 0
    mjb: 1
    nrd: 1
    ntg: 0
    pbm: 1
    psh: 1
    qhw: 1
    rvg: 0
    tgd: 0
    tnw: 1
    vdt: 1
    wpb: 0
    z00: 0
    z01: 0
    z02: 0
    z03: 1
    z04: 0
    z05: 1
    z06: 1
    z07: 1
    z08: 1
    z09: 1
    z10: 1
    z11: 0
    z12: 0

    Combining the bits from all wires starting with z produces the binary number
    0011111101000. Converting this number to decimal produces 2024.

    Simulate the system of gates and wires. What decimal number does it output
    on the wires starting with z?

    Your puzzle answer was 55920211035878.

    --- Part Two ---
    After inspecting the monitoring device more closely, you determine that the
    system you're simulating is trying to add two binary numbers.

    Specifically, it is treating the bits on wires starting with x as one binary
    number, treating the bits on wires starting with y as a second binary
    number, and then attempting to add those two numbers together. The output of
    this operation is produced as a binary number on the wires starting with z.
    (In all three cases, wire 00 is the least significant bit, then 01, then 02,
    and so on.)

    The initial values for the wires in your puzzle input represent just one
    instance of a pair of numbers that sum to the wrong value. Ultimately, any
    two binary numbers provided as input should be handled correctly. That is,
    for any combination of bits on wires starting with x and wires starting with
    y, the sum of the two numbers those bits represent should be produced as a
    binary number on the wires starting with z.

    For example, if you have an addition system with four x wires, four y wires,
    and five z wires, you should be able to supply any four-bit number on the x
    wires, any four-bit number on the y numbers, and eventually find the sum of
    those two numbers as a five-bit number on the z wires. One of the many ways
    you could provide numbers to such a system would be to pass 11 on the x
    wires (1011 in binary) and 13 on the y wires (1101 in binary):

    x00: 1
    x01: 1
    x02: 0
    x03: 1
    y00: 1
    y01: 0
    y02: 1
    y03: 1

    If the system were working correctly, then after all gates are finished
    processing, you should find 24 (11+13) on the z wires as the five-bit binary
    number 11000:

    z00: 0
    z01: 0
    z02: 0
    z03: 1
    z04: 1

    Unfortunately, your actual system needs to add numbers with many more bits
    and therefore has many more wires.

    Based on forensic analysis of scuff marks and scratches on the device, you
    can tell that there are exactly four pairs of gates whose output wires have
    been swapped. (A gate can only be in at most one such pair; no gate's output
    was swapped multiple times.)

    For example, the system below is supposed to find the bitwise AND of the
    six-bit number on x00 through x05 and the six-bit number on y00 through y05
    and then write the result as a six-bit number on z00 through z05:

    x00: 0
    x01: 1
    x02: 0
    x03: 1
    x04: 0
    x05: 1
    y00: 0
    y01: 0
    y02: 1
    y03: 1
    y04: 0
    y05: 1

    x00 AND y00 -> z05
    x01 AND y01 -> z02
    x02 AND y02 -> z01
    x03 AND y03 -> z03
    x04 AND y04 -> z04
    x05 AND y05 -> z00

    However, in this example, two pairs of gates have had their output wires
    swapped, causing the system to produce wrong answers. The first pair of
    gates with swapped outputs is x00 AND y00 -> z05 and x05 AND y05 -> z00; the
    second pair of gates is x01 AND y01 -> z02 and x02 AND y02 -> z01.
    Correcting these two swaps results in this system that works as intended for
    any set of initial values on wires that start with x or y:

    x00 AND y00 -> z00
    x01 AND y01 -> z01
    x02 AND y02 -> z02
    x03 AND y03 -> z03
    x04 AND y04 -> z04
    x05 AND y05 -> z05

    In this example, two pairs of gates have outputs that are involved in a
    swap. By sorting their output wires' names and joining them with commas, the
    list of wires involved in swaps is z00,z01,z02,z05.

    Of course, your actual system is much more complex than this, and the gates
    that need their outputs swapped could be anywhere, not just attached to a
    wire starting with z. If you were to determine that you need to swap output
    wires aaa with eee, ooo with z99, bbb with ccc, and aoc with z24, your
    answer would be aaa,aoc,bbb,ccc,eee,ooo,z24,z99.

    Your system of gates and wires has four pairs of gates which need their
    output wires swapped - eight wires in total. Determine which four pairs of
    gates need their outputs swapped so that your system correctly performs
    addition; what do you get if you sort the names of the eight wires involved
    in a swap and then join those names with commas?

    Your puzzle answer was btb,cmv,mwp,rdg,rmj,z17,z23,z30.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


LARGE_SAMPLE = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""[
    1:-1
]

SMALL_SAMPLE = """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""[
    1:-1
]

SWAP_SAMPLE = """
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
"""[
    1:-1
]


with open(Path(__file__).parent / "2024_24_input.txt") as fp:
    RAW_INPUT = fp.read()


class FruitMonitor:
    def __init__(self, raw_input):
        raw_input_wires, raw_gates = raw_input.split("\n\n")
        self.input_wires = {
            label: int(value)
            for label, value in [
                raw_ln.split(": ") for raw_ln in raw_input_wires.split("\n")
            ]
        }

        self.logic = {}
        self.first_layer = defaultdict(dict)
        self.errors = defaultdict(lambda: defaultdict(dict))
        self.swaps = set()

        for raw_ln in raw_gates.split("\n"):
            label, out_wire = raw_ln.split(" -> ")
            a, gate, b = label.split(" ")
            self.logic[out_wire] = gate, a, b
            if {a[0], b[0]} == {"x", "y"}:
                if a[1:] != b[1:]:
                    self.errors["CROSSED-INPUTS"][out_wire][gate] = (a, b)
                else:
                    self.first_layer[gate][int(a[1:])] = out_wire

    def find_output(self):
        yet_to_calculate = set(self.logic.keys())
        wires = self.input_wires.copy()
        while yet_to_calculate:
            to_remove = set()
            for out_wire in yet_to_calculate:
                (gate, a, b) = self.logic[out_wire]
                if a in wires and b in wires:
                    if gate == "AND":
                        wires[out_wire] = wires[a] & wires[b]
                    elif gate == "OR":
                        wires[out_wire] = wires[a] | wires[b]
                    elif gate == "XOR":
                        wires[out_wire] = wires[a] ^ wires[b]
                    else:
                        raise Exception(f"Invalid operator {gate=}")
                    to_remove.add(out_wire)
            yet_to_calculate -= to_remove

        return sum(
            value * (2 ** int(wire[1:]))
            for wire, value in wires.items()
            if wire[0] == "z"
        )

    def pp(self, wire, depth=0):
        if wire[0] in "xy":
            return "  " * depth + wire
        op, x, y = self.logic[wire]
        return (
            "  " * depth
            + op
            + f" ({wire})\n"
            + self.pp(x, depth + 1)
            + "\n"
            + self.pp(y, depth + 1)
        )

    def verify_recarry(self, wire, bit):
        if (
            bit in self.first_layer["RECARRY"]
            and wire == self.first_layer["RECARRY"][bit]
        ):
            return True, None
        if bit in self.errors["RECARRY"] and wire in self.errors["RECARRY"][bit]:
            return False, self.errors["RECARRY"][bit][wire]

        print(f"verify_recarry {wire=} {bit=}")
        op, x, y = self.logic[wire]
        and_bit = self.first_layer["AND"][bit]
        if op != "AND":
            self.errors["RECARRY"][bit][wire] = f"{wire=} op not AND swap {and_bit=}"
            return False, self.errors["RECARRY"][bit][wire]
        xor_bit = self.first_layer["XOR"][bit]
        if x == xor_bit:
            y_carry, y_swap = self.verify_carry(y, bit)
            if y_carry:
                self.first_layer["RECARRY"][bit] = wire
                return True, None
            self.errors["RECARRY"][bit][
                wire
            ] = f"{wire=} not recarry - {y} not carry {y_swap=}"
            return False, self.errors["RECARRY"][bit][wire]
        if y == xor_bit:
            x_carry, x_swap = self.verify_carry(x, bit)
            if x_carry:
                self.first_layer["RECARRY"][bit] = wire
                return True, None
            self.errors["RECARRY"][bit][
                wire
            ] = f"{wire=} not recarry - {x} not carry {x_swap=}"
            return False, self.errors["RECARRY"][bit][wire]
        y_carry, y_swap = self.verify_carry(y, bit)
        if y_carry:
            self.errors["RECARRY"][bit][wire] = f"{wire=} not recarry - {y} not carry"
            return False, f"swap {x=} and {xor_bit=}"
        x_carry, x_swap = self.verify_carry(x, bit)
        if x_carry:
            self.errors["RECARRY"][bit][wire] = f"swap {y=} and {xor_bit=}"
            return False, self.errors["RECARRY"][bit][wire]
        self.errors["RECARRY"][bit][
            wire
        ] = f"Unsure of what to swap {x_swap=}, {y_swap=}"
        return False, self.errors["RECARRY"][bit][wire]

    def verify_carry(self, wire, bit):
        if bit in self.first_layer["CARRY"] and wire == self.first_layer["CARRY"][bit]:
            return True, None
        if bit in self.errors["CARRY"] and wire in self.errors["CARRY"][bit]:
            return False, self.errors["CARRY"][bit][wire]
        print(f"verify_carry {wire=} {bit=}")
        and_bit = self.first_layer["AND"][bit - 1]
        if wire not in self.logic:
            swap = set()
            if bit == 1:
                swap.add(and_bit)
            else:
                for test_wire, (test_op, a, b) in self.logic.items():
                    if test_op != "OR":
                        continue
                    if and_bit not in {a, b}:
                        continue
                    swap.add(test_wire)
            self.errors["CARRY"][bit][wire] = f"{wire} not carry try {swap}"
            return False, self.errors["CARRY"][bit][wire]
        op, x, y = self.logic[wire]
        if bit == 1:
            if op != "AND":
                self.errors["CARRY"][bit][wire] = f"{bit=} and {wire=} op not AND"
                return False, self.errors["CARRY"][bit][wire]
            if {x, y} != {f"x00", "y00"}:
                self.errors["CARRY"][bit][wire] = f"{bit=} and {x}, {y} != x00, y00"
                return False, self.errors["CARRY"][bit][wire]
            self.first_layer["CARRY"][bit] = wire
            return True, None
        # or_bit = self.first_layer["OR"][bit]
        if op != "OR":
            self.errors["CARRY"][bit][wire] = f"{wire=} op not AND swap ???"
            return False, self.errors["CARRY"][bit][wire]
        if x == and_bit:
            y_recarry, y_swap = self.verify_recarry(y, bit - 1)
            if y_recarry:
                self.first_layer["CARRY"][bit] = wire
                return True, None
            return False, y_swap
        if y == and_bit:
            x_recarry, x_swap = self.verify_recarry(x, bit - 1)
            if x_recarry:
                self.first_layer["CARRY"][bit] = wire
                return True, None
            self.errors["CARRY"][bit][wire] = x_swap
            return False, self.errors["CARRY"][bit][wire]
        y_recarry, y_swap = self.verify_recarry(y, bit - 1)
        if y_recarry:
            self.errors["CARRY"][bit][
                wire
            ] = f"checking {wire=} is carry {y=} is valid recarry but {x=} not {and_bit=}"
            return False, self.errors["CARRY"][bit][wire]
        x_recarry, x_swap = self.verify_recarry(x, bit - 1)
        if x_recarry:
            self.errors["CARRY"][bit][wire] = f"swap {y=} and {and_bit=}"
            return False, self.errors["CARRY"][bit][wire]
        self.errors["CARRY"][bit][
            wire
        ] = f"Unsure of swap for {wire=} {bit=} carry {x=}, {y=}"
        return False, self.errors["CARRY"][bit][wire]

    def verify_z(self, wire, bit):
        print(f"verify_z {wire=} {bit=}")
        op, x, y = self.logic[wire]
        if bit == 0:
            if op == "XOR" and {x, y} == {"x00", "y00"}:
                return True, None
            return False, f"{op} {x}, {y} != XOR x00, y00"
        xor_bit = self.first_layer["XOR"][bit]
        if op != "XOR":
            swap = set()
            # carry_bit = self.first_layer["CARRY"]
            for test_wire, (test_op, a, b) in self.logic.items():
                if test_op != "XOR":
                    continue
                if xor_bit not in {a, b}:
                    continue
                swap.add(test_wire)
            return (
                False,
                f"{wire=} not XOR, {swap=}?",
            )
        xor_bit = self.first_layer["XOR"][bit]
        if x == xor_bit:
            return self.verify_carry(y, bit)
        if y == xor_bit:
            return self.verify_carry(x, bit)
        x_carry, x_swap = self.verify_carry(x, bit)
        if x_carry:
            return False, f"swap {y=} and {xor_bit=}"
        y_carry, y_swap = self.verify_carry(y, bit)
        if y_carry:
            return False, f"swap {x=} and {xor_bit=}"
        return False, f"Unsure of what to swap {x_swap=} {y_swap=}"

    def verify(self):
        bit = 0
        while bit < 45:
            z_valid, swaps = self.verify_z(f"z{bit:02}", bit)
            if z_valid:
                bit += 1
                continue
            print(f"failed verify_z on z{bit:02}, {swaps}")
            return False
        return True

    def swap(self, a, b):
        self.swaps.add(a)
        self.swaps.add(b)
        self.logic[a], self.logic[b] = self.logic[b], self.logic[a]
        for gate in self.first_layer.keys():
            for bit in self.first_layer[gate].keys():
                if self.first_layer[gate][bit] in {a, b}:
                    current = self.first_layer[gate][bit]
                    self.first_layer[gate][bit] = a if current == b else b


def test_fruit_monitor():
    sample = FruitMonitor(SMALL_SAMPLE)
    out_value = sample.find_output()
    assert out_value == 4

    sample2 = FruitMonitor(LARGE_SAMPLE)
    out_value = sample2.find_output()
    assert out_value == 2024


def test_my_fruit_monitor():
    my_monitor = FruitMonitor(RAW_INPUT)
    out_value = my_monitor.find_output()
    assert out_value == 55920211035878


def test_my_order_output():
    mon = FruitMonitor(RAW_INPUT)
    # swaps
    # z17
    mon.swap("z17", "cmv")
    # z23
    mon.swap("z23", "rmj")
    # print(mon.pp("z23"))
    # z30
    mon.swap("z30", "rdg")
    # print(mon.pp("z30"))
    # z38
    mon.swap("mwp", "btb")
    # print(mon.pp("z31"))

    assert mon.verify()
    assert ",".join(sorted(mon.swaps)) == "btb,cmv,mwp,rdg,rmj,z17,z23,z30"
