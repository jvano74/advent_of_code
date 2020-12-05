import pytest
from typing import List, NamedTuple
from collections import deque, defaultdict


class Point(NamedTuple):
    x: int
    y: int


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


class Robot:
    COMMANDS = {1:0, 2:2, 3:3, 4:1}
    CW_COMMAND = {1:4, 2:3, 3:1, 4:2}
    CC_COMMAND = {1:3, 2:4, 3:2, 4:1}
    INVERSE = {1:2, 2:1, 3:4, 4:3}
    DIRECTION = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]
    DIRECTION_TO_CMD = {Point(0, 1):1, Point(1, 0):4, Point(0, -1):2, Point(-1, 0):3}
    UNKNOWN = 0
    OPEN = 1
    GOAL = 2
    WALL = 9

    def path_to_commands(self, path):
        commands = []
        start = path.pop()
        while path:
            end = path.pop()
            delta = Point(end.x - start.x, end.y - start.y)
            commands.append(self.DIRECTION_TO_CMD[delta])
            start = end
        return commands

    def neighbors(self, loc, nbh_type=None):
        neighbors = set()
        if nbh_type is None:
            nbh_type = self.OPEN
        for delta in self.DIRECTION:
            new_loc = Point(loc.x + delta.x, loc.y + delta.y)
            if self.grid[new_loc] == nbh_type:
                neighbors.add(new_loc)
        return neighbors

    def __init__(self, program):
        self.program = program
        self.loc = Point(0, 0)
        self.min = Point(0, 0)
        self.max = Point(0, 0)
        self.goal = None
        self.grid = defaultdict(int)
        self.grid[self.loc] = self.OPEN
        self.boundary = self.neighbors(self.loc, self.UNKNOWN)

    def shortest_path(self, start: Point, end: Point) -> List:
        frontier = deque()
        visited = set()

        frontier.append((start, [start]))
        visited.add(start)

        while frontier:
            pos, path_hx = frontier.popleft()
            for nn in self.neighbors(pos):
                if nn not in visited:
                    if nn == end:
                        path_hx.append(nn)
                        return path_hx
                    new_hx = list(path_hx)
                    new_hx.append(nn)
                    frontier.append((nn, new_hx))
                    visited.add(nn)
        raise LookupError(f'Not {end} not part of {start}')

    def explore(self, everything=None):
        while self.boundary:
            next_unknown = self.boundary.pop()
            path = self.shortest_path(next_unknown, self.loc)
            cmds = self.path_to_commands(path)
            for c in cmds:
                result = self.move(c)
                if result == 0 and not everything:
                    return 0
        if everything:
            return 0
        return -1

    def move(self, command):
        self.program.input.append(command)
        run_result = self.program.run()
        delta = self.DIRECTION[self.COMMANDS[command]]
        new_loc = Point(self.loc.x + delta.x, self.loc.y + delta.y)
        self.min = Point(min(self.min.x, new_loc.x), min(self.min.y, new_loc.y))
        self.max = Point(max(self.max.x, new_loc.x), max(self.max.y, new_loc.y))
        status = self.program.output.pop()
        if run_result != -1:
            raise RuntimeError('Unexpected program exit')
        if status == 0:
            self.grid[new_loc] = self.WALL
            if new_loc in self.boundary:
                self.boundary.remove(new_loc)
            return -1
        elif status == 1:
            self.loc = new_loc
            self.grid[new_loc] = self.OPEN
            if new_loc in self.boundary:
                self.boundary.remove(new_loc)
            new_boundary = self.neighbors(self.loc, self.UNKNOWN)
            self.boundary = self.boundary.union(new_boundary)
            return 1
        elif status == 2:
            self.loc = new_loc
            self.grid[new_loc] = self.OPEN
            self.goal = new_loc
            if new_loc in self.boundary:
                self.boundary.remove(new_loc)
            self.boundary.union(self.neighbors(self.loc, self.UNKNOWN))
            return 0

    def draw(self):
        for x in range(self.min.x, self.max.x + 1):
            print(x % 10 if x > 0 else -x % 10, end='')
        print()
        for y in range(self.max.y, self.min.y-1, -1):
            for x in range(self.min.x, self.max.x + 1):
                if self.goal == Point(x, y):
                    print('X', end='')
                elif Point(x, y) == self.loc:
                    print('@', end='')
                elif x == 0 and y == 0:
                    print('0', end='')
                elif self.grid[Point(x, y)] == self.OPEN:
                    print('.', end='')
                elif self.grid[Point(x, y)] == self.WALL:
                    print('#', end='')
                elif Point(x, y) in self.boundary:
                    print('?', end='')
                else:
                    print(' ', end='')
            print(':',y)
        for x in range(self.min.x, self.max.x + 1):
            print(x % 10 if x > 0 else -x % 10, end='')
        print()
        print()

    def flood(self):
        count = 0
        o2 = set(self.goal)
        next_o2 = self.neighbors(self.goal)
        boundary = set(next_o2)
        while boundary:
            count += 1
            o2 = o2.union(next_o2)
            next_o2 = set()
            for pt in boundary:
                next_o2 = next_o2.union(self.neighbors(pt)) - o2
            boundary = set(next_o2)
        return count


with open('day_15_input.txt') as fp:
    raw = fp.read()
SRC = [int(d) for d in raw.split(',')]
REPAIR = Program(SRC)


def test_submission():
    robot = Robot(REPAIR)
    if robot.explore() == 0:
        print(robot.goal)
        assert len(robot.shortest_path(Point(0,0), robot.goal)) - 1 == 296
    robot.explore(True)
    robot.draw()
    assert robot.flood() == 302
    assert True


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
    copy_code = [109, 1, 204, -1,1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    copy_program = Program(copy_code)
    assert copy_program.run([]) == 0 and copy_program.output == copy_code
    digit_program = Program([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    assert digit_program.run([]) == 0 and digit_program.output == [1219070632396864]
    large_digit_program = Program([104, 1125899906842624, 99])
    assert large_digit_program.run([]) == 0 and large_digit_program.output == [1125899906842624]
