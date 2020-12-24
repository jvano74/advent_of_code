import pytest
from typing import List, NamedTuple


class Puzzle:
    """
    --- Day 19: Tractor Beam ---
    Unsure of the state of Santa's ship, you borrowed the tractor beam technology from Triton. Time to test it out.

    When you're safely away from anything else, you activate the tractor beam, but nothing happens. It's hard to tell
    whether it's working if there's nothing to use it on. Fortunately, your ship's drone system can be configured to
    deploy a drone to specific coordinates and then check whether it's being pulled. There's even an Intcode program
    (your puzzle input) that gives you access to the drone system.

    The program uses two input instructions to request the X and Y position to which the drone should be deployed.
    Negative numbers are invalid and will confuse the drone; all numbers should be zero or positive.

    Then, the program will output whether the drone is stationary (0) or being pulled by something (1). For example,
    the coordinate X=0, Y=0 is directly in front of the tractor beam emitter, so the drone control program will always
    report 1 at that location.

    To better understand the tractor beam, it is important to get a good picture of the beam itself. For example,
    suppose you scan the 10x10 grid of points closest to the emitter:

           X
      0->      9
     0#.........
     |.#........
     v..##......
      ...###....
      ....###...
    Y .....####.
      ......####
      ......####
      .......###
     9........##

    In this example, the number of points affected by the tractor beam in the 10x10 area closest to the emitter is 27.

    However, you'll need to scan a larger area to understand the shape of the beam. How many points are affected by
    the tractor beam in the 50x50 area closest to the emitter? (For each of X and Y, this will be 0 through 49.)

    Your puzzle answer was 110.

    --- Part Two ---
    You aren't sure how large Santa's ship is. You aren't even sure if you'll need to use this thing on Santa's ship,
    but it doesn't hurt to be prepared. You figure Santa's ship might fit in a 100x100 square.

    The beam gets wider as it travels away from the emitter; you'll need to be a minimum distance away to fit a
    square of that size into the beam fully. (Don't rotate the square; it should be aligned to the same axes as
    the drone grid.)

    For example, suppose you have the following tractor beam readings:

    #.......................................
    .#......................................
    ..##....................................
    ...###..................................
    ....###.................................
    .....####...............................
    ......#####.............................
    ......######............................
    .......#######..........................
    ........########........................
    .........#########......................
    ..........#########.....................
    ...........##########...................
    ...........############.................
    ............############................
    .............#############..............
    ..............##############............
    ...............###############..........
    ................###############.........
    ................#################.......
    .................########OOOOOOOOOO.....
    ..................#######OOOOOOOOOO#....
    ...................######OOOOOOOOOO###..
    ....................#####OOOOOOOOOO#####
    .....................####OOOOOOOOOO#####
    .....................####OOOOOOOOOO#####
    ......................###OOOOOOOOOO#####
    .......................##OOOOOOOOOO#####
    ........................#OOOOOOOOOO#####
    .........................OOOOOOOOOO#####
    ..........................##############
    ..........................##############
    ...........................#############
    ............................############
    .............................###########

    In this example, the 10x10 square closest to the emitter that fits entirely within the tractor beam has been
    marked O. Within it, the point closest to the emitter (the only highlighted O) is at X=25, Y=20.

    Find the 100x100 square closest to the emitter that fits entirely within the tractor beam; within that square,
    find the point closest to the emitter. What value do you get if you take that point's X coordinate, multiply it
    by 10000, then add the point's Y coordinate? (In the example above, this would be 250020.)

    Your puzzle answer was 17302065.
    """
    pass


class Point(NamedTuple):
    x: int
    y: int


class BoxRange(NamedTuple):
    ul: Point
    lr: Point


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
            raise SyntaxError(f'Unknown optcode {op_code}\nOpt Hx:\n{self.opt_hx}')

    def read_memory(self, pos):
        if len(self.memory) - 1 < pos:
            self.memory.extend([0]*(pos + 1 - len(self.memory)))
        return self.memory[pos]

    def write_memory(self, pos, mode, val):
        if mode == 2:
            pos += self.relative_base
        if len(self.memory) - 1 < pos:
            self.memory.extend([0]*(pos + 1 - len(self.memory)))
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
            raise SyntaxError(f'Unknown op_code {op_code}')
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
            raise SyntaxError(f'Unknown op_code {op_code}')
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
            raise SyntaxError(f'Unknown op_code {op_code}')
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


with open('day_19_input.txt') as fp:
    raw = fp.read()
SRC = [int(d) for d in raw.split(',')]
DRONE = Program(SRC)


class Image:
    DELTAS = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]

    def __init__(self, program):
        self.program = program
        self.beam = set()

    def is_point_in_beam(self, x, y):
        self.program.reset()
        run_result = self.program.run([x, y])
        if run_result != 0:
            raise ChildProcessError
        return True if self.program.output.pop() == 1 else False

    def scan_range(self, p1: Point, p4: Point):
        for y in range(p1.y, p4.y + 1):
            seen_beam = False
            if y < 10:
                x_max = 3 * y + 1
            else:
                x_max = p4.x + 1
            x_start = p1.x
            for x in range(x_start, x_max):
                if self.is_point_in_beam(x, y):
                    if not seen_beam:
                        x_start = x
                    seen_beam = True
                    self.beam.add(Point(x, y))
                elif seen_beam:
                    break

    def does_region_fit_in_beam(self, box: BoxRange):
        p1 = box.ul
        p4 = box.lr
        if self.is_point_in_beam(p1.x, p1.y) and self.is_point_in_beam(p4.x, p1.y) and \
           self.is_point_in_beam(p1.x, p4.y) and self.is_point_in_beam(p4.x, p4.y):
            return True
        return False

    def sum_in_range(self, p1: Point, p4: Point):
        ramge_sum = 0
        for x in range(p1.x, p4.x + 1):
            for y in range(p1.y, p4.y + 1):
                if Point(x, y) in self.beam:
                    ramge_sum += 1
        return ramge_sum

    def print_region(self, p1: Point, p4: Point, box: BoxRange = None):
        print(f'UL={p1} LR={p4} box={box}')
        if box is None:
            box_x = range(0, 0)
            box_y = range(0, 0)
        else:
            box_x = range(box.ul.x, box.lr.x + 1)
            box_y = range(box.ul.y, box.lr.y + 1)
        for y in range(p1.y, p4.y + 1):
            for x in range(p1.x, p4.x + 1):
                if Point(x, y) in self.beam:
                    if x in box_x and y in box_y:
                        print('o', end='')
                    else:
                        print('#', end='')
                else:
                    if x in box_x and y in box_y:
                        print('x', end='')
                    else:
                        print('.', end='')
            print(y)


def make_box(ll: Point, length: int, height: int):
    return BoxRange(Point(ll.x, ll.y - height), Point(ll.x + length, ll.y))


def search_for_box(lower: Point, size: int):
    image = Image(DRONE)

    santa_ll = lower
    santa_box = make_box(santa_ll, size - 1, size - 1)

    while not image.does_region_fit_in_beam(santa_box):
        # move down and over
        y = santa_ll.y + 1
        x = santa_ll.x
        while not image.is_point_in_beam(x, y):
            x += 1
        santa_ll = Point(x, y)
        santa_box = make_box(santa_ll, size - 1, size - 1)

    santa_ll_range = make_box(Point(santa_ll.x - 15, santa_ll.y + 15), 30, 30)
    santa_ur = Point(santa_ll.x + size, santa_ll.y - size)
    santa_ur_range = make_box(Point(santa_ur.x - 15, santa_ur.y + 15), 30, 30)

    image.scan_range(santa_ll_range.ul, santa_ll_range.lr)
    image.print_region(santa_ll_range.ul, santa_ll_range.lr, santa_box)

    image.scan_range(santa_ur_range.ul, santa_ur_range.lr)
    image.print_region(santa_ur_range.ul, santa_ur_range.lr, santa_box)

    print(santa_box)
    return santa_box.ul.x * 10000 + santa_box.ul.y


def test_submission():
    image = Image(DRONE)
    image.scan_range(Point(0, 0), Point(49, 49))
    image.print_region(Point(0, 0), Point(49, 49))
    assert image.sum_in_range(Point(0, 0), Point(49, 49)) == 110


def test_box_stuff():
    image = Image(DRONE)
    image.scan_range(Point(220, 280), Point(300, 300))

    smaller_box = make_box(Point(300 - 60, 299), 13, 13)
    image.print_region(Point(220, 280), Point(300, 300), smaller_box)
    assert image.does_region_fit_in_beam(smaller_box)

    big_box = make_box(Point(300 - 60, 299), 13, 14)
    image.print_region(Point(220, 280), Point(300, 300), big_box)
    assert image.does_region_fit_in_beam(big_box) is False


def test_submission2():
    assert search_for_box(Point(0, 10), 100) == 17302065


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
    pbig = Program([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                    1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                    999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])
    assert pbig.run([7]) == 0 and pbig.output == [999]
    pbig.reset()
    assert pbig.run([8]) == 0 and pbig.output == [1000]
    pbig.reset()
    assert pbig.run([9]) == 0 and pbig.output == [1001]
    # BASE TESTS
    copy_code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    copy_program = Program(copy_code)
    assert copy_program.run([]) == 0 and copy_program.output == copy_code
    digit_program = Program([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    assert digit_program.run([]) == 0 and digit_program.output == [1219070632396864]
    large_digit_program = Program([104, 1125899906842624, 99])
    assert large_digit_program.run([]) == 0 and large_digit_program.output == [1125899906842624]
