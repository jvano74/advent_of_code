from pathlib import Path
from typing import List
from collections import defaultdict
import pytest


class Puzzle:
    """
    --- Day 23: Category Six ---
    The droids have finished repairing as much of the ship as they can. Their report indicates that this was a
    Category 6 disaster - not because it was that bad, but because it destroyed the stockpile of Category 6 network
    cables as well as most of the ship's network infrastructure.

    You'll need to rebuild the network from scratch.

    The computers on the network are standard Intcode computers that communicate by sending packets to each other.
    There are 50 of them in total, each running a copy of the same Network Interface Controller (NIC) software (your
    puzzle input). The computers have network addresses 0 through 49; when each computer boots up, it will request
    its network address via a single input instruction. Be sure to give each computer a unique network address.

    Once a computer has received its network address, it will begin doing work and communicating over the network by
    sending and receiving packets. All packets contain two values named X and Y. Packets sent to a computer are
    queued by the recipient and read in the order they are received.

    To send a packet to another computer, the NIC will use three output instructions that provide the destination
    address of the packet followed by its X and Y values. For example, three output instructions that provide the
    values 10, 20, 30 would send a packet with X=20 and Y=30 to the computer with address 10.

    To receive a packet from another computer, the NIC will use an input instruction. If the incoming packet queue is
    empty, provide -1. Otherwise, provide the X value of the next packet; the computer will then use a second input
    instruction to receive the Y value for the same packet. Once both values of the packet are read in this way, the
    packet is removed from the queue.

    Note that these input and output instructions never block. Specifically, output instructions do not wait for the
    sent packet to be received - the computer might send multiple packets before receiving any. Similarly, input
    instructions do not wait for a packet to arrive - if no packet is waiting, input instructions should receive -1.

    Boot up all 50 computers and attach them to your network. What is the Y value of the first packet sent to
    address 255?

    Your puzzle answer was 16660.

    --- Part Two ---
    Packets sent to address 255 are handled by a device called a NAT (Not Always Transmitting). The NAT is responsible
    for managing power consumption of the network by blocking certain packets and watching for idle periods in the
    computers.

    If a packet would be sent to address 255, the NAT receives it instead. The NAT remembers only the last packet it
    receives; that is, the data in each packet it receives overwrites the NAT's packet memory with the new packet's
    X and Y values.

    The NAT also monitors all computers on the network. If all computers have empty incoming packet queues and are
    continuously trying to receive packets without sending packets, the network is considered idle.

    Once the network is idle, the NAT sends only the last packet it received to address 0; this will cause the
    computers on the network to resume activity. In this way, the NAT can throttle power consumption of the network
    when the ship needs power in other areas.

    Monitor packets released to the computer at address 0 by the NAT. What is the first Y value delivered by the NAT
    to the computer at address 0 twice in a row?

    Your puzzle answer was 11504.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """

    pass


HALT = 99
ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUAL = 8
BASE = 9


class Program:
    def __init__(self, program):
        self.head = 0
        self.relative_base = 0
        self.disk = list(program)
        self.memory = list(program)
        self.input = []
        self.output = []
        self.opt_hx = []

    def reset(self):
        self.head = 0
        self.relative_base = 0
        self.memory = list(self.disk)
        self.input = []
        self.output = []
        self.opt_hx = []

    def process(self, op_code, modes):
        if op_code in [INPUT, OUTPUT, BASE]:
            self.process_one_parameter_operation(modes, op_code)
        elif op_code in [JUMP_IF_TRUE, JUMP_IF_FALSE]:
            self.process_two_parameter_operation(modes, op_code)
        elif op_code in [ADD, MULTIPLY, LESS_THAN, EQUAL]:
            self.process_three_parameter_operation(modes, op_code)
        else:
            raise SyntaxError(f"Unknown optcode {op_code}\nOpt Hx:\n{self.opt_hx}")

    def read_memory(self, pos):
        if len(self.memory) - 1 < pos:
            self.memory.extend([0] * (pos + 1 - len(self.memory)))
        return self.memory[pos]

    def write_memory(self, pos, mode, val):
        if mode == 2:
            pos += self.relative_base
        if len(self.memory) - 1 < pos:
            self.memory.extend([0] * (pos + 1 - len(self.memory)))
        self.memory[pos] = val

    def get_val(self, offset=1, mode=0):
        val = self.read_memory(self.head + offset)
        if mode == 0:
            return self.read_memory(val)
        if mode == 2:
            return self.read_memory(self.relative_base + val)
        return val

    def process_one_parameter_operation(self, modes, op_code):
        if op_code == INPUT:
            if len(self.input) == 0:
                return
            mem_loc = self.memory[self.head + 1]
            self.write_memory(mem_loc, modes % 10, self.input.pop(0))
        elif op_code == OUTPUT:
            self.output.append(self.get_val(1, modes % 10))
        elif op_code == BASE:
            self.relative_base += self.get_val(1, modes % 10)
        else:
            raise SyntaxError(f"Unknown op_code {op_code}")
        self.head += 2

    def process_two_parameter_operation(self, modes, op_code):
        reg_a = self.get_val(1, modes % 10)
        modes //= 10
        reg_b = self.get_val(2, modes % 10)
        if op_code == JUMP_IF_TRUE:
            if reg_a:
                self.head = reg_b
                return
        elif op_code == JUMP_IF_FALSE:
            if not reg_a:
                self.head = reg_b
                return
        else:
            raise SyntaxError(f"Unknown op_code {op_code}")
        self.head += 3

    def process_three_parameter_operation(self, modes, op_code):
        reg_a = self.get_val(1, modes % 10)
        modes //= 10
        reg_b = self.get_val(2, modes % 10)
        modes //= 10
        mem_loc = self.memory[self.head + 3]
        if op_code == ADD:
            self.write_memory(mem_loc, modes % 10, reg_a + reg_b)
        elif op_code == MULTIPLY:
            self.write_memory(mem_loc, modes % 10, reg_a * reg_b)
        elif op_code == LESS_THAN:
            self.write_memory(mem_loc, modes % 10, 1 if reg_a < reg_b else 0)
        elif op_code == EQUAL:
            self.write_memory(mem_loc, modes % 10, 1 if reg_a == reg_b else 0)
        else:
            raise SyntaxError(f"Unknown op_code {op_code}")
        self.head += 4

    def run(self, std_in: List[int] = None) -> int:
        if std_in is not None:
            self.input = std_in
        while True:
            op_code = self.memory[self.head] % 100
            modes = self.memory[self.head] // 100
            if op_code == HALT:
                return 0
            if op_code == INPUT and len(self.input) == 0:
                return -1
            self.process(op_code, modes)

    def print_output(self):
        return "".join([chr(c) if c < 256 else str(c) for c in self.output])


class Network:
    def __init__(self, number_of_nodes: int):
        with open(Path(__file__).parent / "2019_23_input.txt") as fp:
            raw = fp.read()
        src = [int(d) for d in raw.split(",")]
        self.nodes = {}
        self.status = {}
        self.wan = defaultdict(list)
        self.nat_x = None
        self.nat_y = None
        self.previous_nat_y = None
        for address in range(number_of_nodes):
            new_node = Program(src)
            new_node.input.append(address)
            self.nodes[address] = new_node

    def tick(self, use_nat: bool = False):
        # first move outputs to inputs
        idle = True
        for address, node in self.nodes.items():
            while len(node.output) > 0:
                idle = False
                dest_address = node.output.pop(0)
                dest_x = node.output.pop(0)
                dest_y = node.output.pop(0)
                if dest_address in self.nodes:
                    self.nodes[dest_address].input.append(dest_x)
                    self.nodes[dest_address].input.append(dest_y)
                elif use_nat and dest_address == 255:
                    self.nat_x = dest_x
                    self.nat_y = dest_y
                else:
                    self.wan[dest_address].append(dest_x)
                    self.wan[dest_address].append(dest_y)
        for address, node in self.nodes.items():
            if len(node.input) == 0:
                node.input.append(-1)
            else:
                idle = False
        if use_nat and idle and self.nat_x is not None:
            if self.nat_y == self.previous_nat_y:
                return self.nat_y
            self.previous_nat_y = self.nat_y
            self.nodes[0].input[0] = self.nat_x
            self.nodes[0].input.append(self.nat_y)
        for address, node in self.nodes.items():
            status = node.run()
            self.status[address] = (status, len(node.input), len(node.output))


def test_submission():
    net = Network(50)
    while len(net.wan) == 0:
        net.tick()
    assert net.wan[255][1] == 16660


def test_submission2():
    net = Network(50)
    nat_dup = None
    while nat_dup is None:
        nat_dup = net.tick(True)
    assert nat_dup == 11504


def test_program():
    error_program = Program([555])
    with pytest.raises(SyntaxError):
        error_program.run([])
    p1 = Program([1, 0, 0, 0, 99])
    assert p1.run([]) == 0 and p1.memory == [2, 0, 0, 0, 99]
    p2 = Program([2, 3, 0, 3, 99])
    assert p2.run([]) == 0 and p2.memory == [2, 3, 0, 6, 99]
    p3 = Program([2, 4, 4, 5, 99, 0])
    assert p3.run([]) == 0 and p3.memory == [2, 4, 4, 5, 99, 9801]
    p4 = Program([1, 1, 1, 4, 99, 5, 6, 0, 99])
    assert p4.run([]) == 0 and p4.memory == [30, 1, 1, 4, 2, 5, 6, 0, 99]
    # IO TESTS
    io = Program([3, 0, 4, 0, 99])
    assert io.run([12]) == 0 and io.output == [12] and io.memory == [12, 0, 4, 0, 99]
    # COMPARE TESTS
    p5 = Program([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
    assert p5.run([8]) == 0 and p5.output == [1]
    p5.reset()
    assert p5.run([7]) == 0 and p5.output == [0]
    p6 = Program([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
    assert p6.run([7]) == 0 and p6.output == [1]
    p6.reset()
    assert p6.run([8]) == 0 and p6.output == [0]
    p7 = Program([3, 3, 1108, -1, 8, 3, 4, 3, 99])
    assert p7.run([8]) == 0 and p7.output == [1]
    p8 = Program([3, 3, 1107, -1, 8, 3, 4, 3, 99])
    assert p8.run([7]) == 0 and p8.output == [1]
    p8.reset()
    assert p8.run([8]) == 0 and p8.output == [0]
    # JUMP TESTS
    pjump1 = Program([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9])
    assert pjump1.run([0]) == 0 and pjump1.output == [0]
    pjump1.reset()
    assert pjump1.run([4]) == 0 and pjump1.output == [1]
    pjump2 = Program([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
    assert pjump2.run([0]) == 0 and pjump2.output == [0]
    pjump2.reset()
    assert pjump2.run([7]) == 0 and pjump2.output == [1]
    pbig = Program(
        [
            3,
            21,
            1008,
            21,
            8,
            20,
            1005,
            20,
            22,
            107,
            8,
            21,
            20,
            1006,
            20,
            31,
            1106,
            0,
            36,
            98,
            0,
            0,
            1002,
            21,
            125,
            20,
            4,
            20,
            1105,
            1,
            46,
            104,
            999,
            1105,
            1,
            46,
            1101,
            1000,
            1,
            20,
            4,
            20,
            1105,
            1,
            46,
            98,
            99,
        ]
    )
    assert pbig.run([7]) == 0 and pbig.output == [999]
    pbig.reset()
    assert pbig.run([8]) == 0 and pbig.output == [1000]
    pbig.reset()
    assert pbig.run([9]) == 0 and pbig.output == [1001]
    # BASE TESTS
    copy_code = [
        109,
        1,
        204,
        -1,
        1001,
        100,
        1,
        100,
        1008,
        100,
        16,
        101,
        1006,
        101,
        0,
        99,
    ]
    copy_program = Program(copy_code)
    assert copy_program.run([]) == 0 and copy_program.output == copy_code
    digit_program = Program([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    assert digit_program.run([]) == 0 and digit_program.output == [1219070632396864]
    large_digit_program = Program([104, 1125899906842624, 99])
    assert large_digit_program.run([]) == 0 and large_digit_program.output == [
        1125899906842624
    ]
