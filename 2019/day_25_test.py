#import pytest
from typing import List, NamedTuple
#from collections import deque, defaultdict
import pytest


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

    def type(self, command):
        self.input.extend([ord(c) for c in command])
        self.input.append(10)

    def clear_output(self):
        self.output = []

    def print_output(self, clear=True):
        out = ''.join([chr(c) if c < 256 else str(c) for c in self.output])
        if clear:
            self.clear_output()
        return out



with open('day_25_input.txt') as fp:
    raw = fp.read()
SRC = [int(d) for d in raw.split(',')]


class Mission:
    def __init__(self, source, allow_reset=True):
        self.command_history = []
        self.program = Program(source)
        self.allow_reset = allow_reset

    def reset(self):
        self.command_history = []
        self.program.reset()

    def undo(self):
        if len(self.command_history) == 0:
            return -1, 'Nothing to undo'
        self.command_history.pop()
        self.program.reset()
        for command in self.command_history:
            self.program.type(command)

    def run_command(self, command=''):
        while len(command) == 0:
            command = input(f'{len(self.command_history)}>')
        if command == 'history':
            return -1, f'Command history: {self.command_history}'

        if command == 'reset' and len(self.command_history) > 0:
            self.reset()
        elif command == 'undo' and len(self.command_history) > 0:
            self.undo()
        elif command[0] == '>':
            commands = command[1:].split('>')
            for command in commands:
                self.command_history.append(command)
                self.program.type(command)
        else:
            self.command_history.append(command)
            self.program.type(command)
        status = self.program.run()
        out = self.program.print_output()
        return status, out

    def run(self):
        status, out = -1, ''
        while status == -1:
            print(out)
            status, out = self.run_command()
            if status == 0:
                print('GAME OVER MAN!')
                print(self.command_history)
                if not self.allow_reset:
                    return out
                command = input('(r)eset or (u)ndo>')
                if command == 'u':
                    status, out = self.undo()
                elif command == 'r':
                    status, out = self.reset()
                else:
                    return out


MAP_AND_NOTES = """
    Map:
    
       CW-SE-PF       
       |              
       HC             
       |              
       EN             
       |              
       AR-ST SL-PS-HW 
       |     |  |     
       HO----ST KT    
       |     |  |     
    GW-SB    |  OB    
       |     |        
       NA    |        
             |        
    CO-WD----HB       

    Items: 
    - astronaut ice cream
    - antenna
    - hologram
    - space heater

    Code:
    25166400
"""

def test_submission():
    mission = Mission(SRC, False)
    commands = '>north>west>take antenna' + \
               '>south>take hologram' + \
               '>west>take astronaut ice cream>east' + \
               '>north>north>north>north>take space heater' + \
               '>north>east'
    final_command = 'east'
    status, out = mission.run_command(commands)
    print(out)
    assert status == -1
    status, out = mission.run_command(final_command)
    print(out)
    final_screen = ['== Pressure-Sensitive Floor ==',
                    'Analyzing...',
                    'Doors here lead:',
                    '- west',
                    'A loud, robotic voice says "Analysis complete! You may proceed." and you ',
                    'enter the cockpit.',
                    'Santa notices your small droid, looks puzzled for a moment, realizes what ',
                    'has happened, and radios your ship directly.',
                    '"Oh, hello! You should be able to get in by typing 25166400 on the keypad at ',
                    'the main airlock."']
    assert status == 0
    assert ''.join(out.split('\n')) == ''.join(final_screen)


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

if __name__ == '__main__':
    Mission(SRC).run()