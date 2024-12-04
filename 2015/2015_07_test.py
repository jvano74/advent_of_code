from pathlib import Path
import numpy as np
import re
from collections import defaultdict
import pytest


class Puzzle:
    """
    --- Day 7: Some Assembly Required ---
    This year, Santa brought little Bobby Tables a set of wires and bitwise logic
    gates! Unfortunately, little Bobby is a little under the recommended age range,
    and he needs help assembling the circuit.

    Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal
    (a number from 0 to 65535). A signal is provided to each wire by a gate, another
    wire, or some specific value. Each wire can only get a signal from one source, but
    can provide its signal to multiple destinations. A gate provides no signal until
    all of its inputs have a signal.

    The included instructions booklet describes how to connect the parts together:
        x AND y -> z means to connect wires x and y to an AND gate, and then connect
        its output to wire z.

    For example:

    123 -> x means that the signal 123 is provided to wire x.

    x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.

    p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then
    provided to wire q.

    NOT e -> f means that the bitwise complement of the value from wire e is
    provided to wire f.

    Other possible gates include OR (bitwise OR) and RSHIFT (right-shift).

    If, for some reason, you'd like to emulate the circuit instead, almost
    all programming languages (for example, C, JavaScript, or Python) provide
    operators for these gates.

    For example, here is a simple circuit:

    123 -> x
    456 -> y
    x AND y -> d
    x OR y -> e
    x LSHIFT 2 -> f
    y RSHIFT 2 -> g
    NOT x -> h
    NOT y -> i

    After it is run, these are the signals on the wires:

    d: 72
    e: 507
    f: 492
    g: 114
    h: 65412
    i: 65079
    x: 123
    y: 456

    In little Bobby's kit's instructions booklet (provided as your puzzle input),
    what signal is ultimately provided to wire a?
    """

    pass


class Signal:
    def __init__(self, data):
        self.data = data

    def output(self):
        return np.ushort(self.data)


class Wire:
    def __init__(self, line_in=None):
        self.line_in = line_in
        if line_in is None:
            self.data = None
        else:
            self.data = line_in.output()

    def output(self):
        if self.data is not None:
            return self.data
        if self.line_in is None:
            return None
        self.data = self.line_in.output()
        if self.data is None:
            return None
        return np.ushort(self.data)


class Gate:
    def __init__(self, operation=None, line1_in=None, line2_in=None):
        self.operation = operation
        self.line1_in = line1_in
        self.line2_in = line2_in
        self.data = None

    def output(self):
        if self.data is not None:
            return self.data
        if self.line1_in is None:
            return None
        line1 = self.line1_in.output()
        if line1 is None:
            return None
        if self.operation == "NOT":
            self.data = np.ushort(~line1)
            return self.data
        if self.line2_in is None:
            return None
        if self.operation == "RSHIFT":
            self.data = np.ushort(line1 >> self.line2_in)
            return self.data
        if self.operation == "LSHIFT":
            self.data = np.ushort(line1 << self.line2_in)
            return self.data
        line2 = self.line2_in.output()
        if line2 is None:
            return None
        if self.operation == "AND":
            self.data = np.ushort(line1 & line2)
            return self.data
        if self.operation == "OR":
            self.data = np.ushort(line1 | line2)
            return self.data
        return None


class Kit:
    wires = defaultdict(Wire)

    def wire_in(self, instruction):
        parse = re.match(r"(?P<inputs>.*) -> (?P<out_wire>[a-z]+)", instruction)
        if not parse:
            raise NotImplementedError(f"Instruction {instruction} not implemented")

        out_wire_label = parse.group("out_wire")
        out_wire = self.wires[out_wire_label]
        if out_wire.line_in is not None:
            raise KeyError(f"Wire {out_wire} already connected in kit")

        parse = re.match(r"((?P<in_wire>[a-z]+)|(?P<in_signal>\d+)) ->", instruction)
        if parse and parse.group("in_signal"):
            value = int(parse.group("in_signal"))
            self.add_signal_to_wire(out_wire, value)
            return
        if parse and parse.group("in_wire"):
            out_wire.line_in = self.wires[parse.group("in_wire")]
            return

        parse = re.match(r"NOT (?P<in_wire>[a-z]+) ->", instruction)
        if parse:
            self.add_not_gate(out_wire, self.wires[parse.group("in_wire")])
            return

        parse = re.match(
            r"(?P<in_wire>[a-z]+) (?P<direction>[RL])SHIFT (?P<bits>\d+) ->",
            instruction,
        )
        if parse:
            self.add_shift_gate(
                out_wire,
                self.wires[parse.group("in_wire")],
                parse.group("direction"),
                int(parse.group("bits")),
            )
            return

        parse = re.match(
            r"((?P<in1_wire>[a-z]+)|(?P<in1_signal>\d+)) (?P<gate>AND|OR) "
            r"((?P<in2_wire>[a-z]+)|(?P<in2_signal>\d+)) ->",
            instruction,
        )
        if parse:
            self.add_gate(
                out_wire,
                parse.group("gate"),
                (
                    self.wires[parse.group("in1_wire")]
                    if parse.group("in1_wire")
                    else Signal(int(parse.group("in1_signal")))
                ),
                (
                    self.wires[parse.group("in2_wire")]
                    if parse.group("in2_wire")
                    else Signal(int(parse.group("in2_signal")))
                ),
            )
            return

        raise NotImplementedError(f"Instruction {instruction} not implemented")

    @staticmethod
    def add_signal_to_wire(out_wire, data):
        out_wire.line_in = Signal(data)

    @staticmethod
    def add_not_gate(out_wire, in_wire):
        out_wire.line_in = Wire(Gate("NOT", in_wire))

    @staticmethod
    def add_shift_gate(out_wire, in_wire, direction, bits):
        out_wire.line_in = Wire(Gate(f"{direction}SHIFT", in_wire, bits))

    @staticmethod
    def add_gate(out_wire, gate, in1_wire, in2_wire):
        out_wire.line_in = Wire(Gate(gate, in1_wire, in2_wire))

    def execute_directions(self):
        with open(Path(__file__).parent / "2015_07_input.txt", "r") as fp:
            line = fp.readline()
            while line:
                self.wire_in(line)
                line = fp.readline()


def test_signal():
    s1 = Signal(123)
    s2 = Signal(333)
    assert s1.output() == 123
    assert s2.output() == 333


def test_wire():
    s1 = Signal(342)
    w1 = Wire()
    assert w1.output() is None
    w1.line_in = s1
    assert w1.output() == 342
    w2 = Wire(s1)
    assert w2.output() == 342


def test_gates():
    s1 = Signal(12)
    g1 = Gate("NOT", s1)
    assert g1.output() == 65523
    g2 = Gate("LSHIFT", s1, 3)
    assert g2.output() == 96
    g3 = Gate("RSHIFT", g2, 3)
    assert g3.output() == 12


def test_kit():
    kit_1 = Kit()
    kit_1.wire_in("123 -> a")
    assert kit_1.wires["a"].output() == 123
    kit_1.wire_in("NOT a -> b")
    assert kit_1.wires["b"].output() == 65412
    with pytest.raises(NotImplementedError):
        kit_1.wire_in("NOT 123 -> c")
    kit_1.wire_in("a LSHIFT 3 -> c")
    assert kit_1.wires["c"].output() == 984
    kit_1.wire_in("c RSHIFT 3 -> d")
    assert kit_1.wires["d"].output() == 123


def test_kit2():
    kit_2 = Kit()
    kit_2.wire_in("123 -> x")
    kit_2.wire_in("456 -> y")
    kit_2.wire_in("x AND y -> d")
    kit_2.wire_in("x OR y -> e")
    kit_2.wire_in("x LSHIFT 2 -> f")
    kit_2.wire_in("y RSHIFT 2 -> g")
    kit_2.wire_in("NOT x -> h")
    kit_2.wire_in("NOT y -> i")
    assert kit_2.wires["d"].output() == 72
    assert kit_2.wires["e"].output() == 507
    assert kit_2.wires["f"].output() == 492
    assert kit_2.wires["g"].output() == 114
    assert kit_2.wires["h"].output() == 65412
    assert kit_2.wires["i"].output() == 65079
    assert kit_2.wires["x"].output() == 123
    assert kit_2.wires["y"].output() == 456


def test_submission():
    kit_sub = Kit()
    kit_sub.execute_directions()
    assert kit_sub.wires["a"].output() == 3176
    # assert kit_sub.wires['a'].output() == 14710
