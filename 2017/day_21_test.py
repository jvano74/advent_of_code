from typing import NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 21: Fractal Art ---
    You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the
    detail of an image through a set of rules.

    The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.).
    The program always begins with this pattern:

    .#.
    ..#
    ###
    Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.

    Then, the program repeats the following process:

    If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square into
    a 3x3 square by following the corresponding enhancement rule.

    Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3 square
    into a 4x4 square by following the corresponding enhancement rule.

    Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.

    The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules.
    The artist explains that sometimes, one must rotate or flip the input pattern to find a match.
    (Never rotate or flip the output pattern, though.)

    Each pattern is written concisely: rows are listed as single units, ordered top-down, and separated by slashes.
    For example, the following rules correspond to the adjacent patterns:

    ../.#  =  ..
              .#

                    .#.
    .#./..#/###  =  ..#
                    ###

                            #..#
    #..#/..../#..#/.##.  =  ....
                            #..#
                            .##.

    When searching for a rule to use, rotate and flip the pattern as necessary. For example, all of the following
    patterns match the same rule:

    .#.   .#.   #..   ###
    ..#   #..   #.#   ..#
    ###   ###   ##.   .#.

    Suppose the book contained the following two rules:

    ../.# => ##./#../...
    .#./..#/### => #..#/..../..../#..#

    As before, the program begins with this pattern:

    .#.
    ..#
    ###

    The size of the grid (3) is not divisible by 2, but it is divisible by 3. It divides evenly into a single square;
    the square matches the second rule, which produces:

    #..#
    ....
    ....
    #..#

    The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used. It divides evenly into
    four squares:

    #.|.#
    ..|..
    --+--
    ..|..
    #.|.#

    Each of these squares matches the same rule (../.# => ##./#../...), three of which require some flipping and
    rotation to line up with the rule. The output for the rule is the same in all four cases:

    ##.|##.
    #..|#..
    ...|...
    ---+---
    ##.|##.
    #..|#..
    ...|...
    Finally, the squares are joined into a new grid:

    ##.##.
    #..#..
    ......
    ##.##.
    #..#..
    ......
    Thus, after 2 iterations, the grid contains 12 pixels that are on.

    How many pixels stay on after 5 iterations?

    --- Part Two ---
    How many pixels stay on after 18 iterations?
    """
    pass


SAMPLE = ['../.# => ##./#../...',
          '.#./..#/### => #..#/..../..../#..#']

with open('day_21_input.txt') as fp:
    INPUTS = [line.strip() for line in fp]


class Pt(NamedTuple):
    x: int
    y: int


def split_grid(input_grid, block_size, size):
    result = defaultdict(set)
    # Need to create empty sets for grid (some can be empty)
    for i_y in range(size // block_size):
        for i_x in range(size // block_size):
            result[Pt(i_x, i_y)] = set()
    for pt in input_grid:
        index_pt = Pt(pt.x // block_size, pt.y // block_size)
        result[index_pt].add(Pt(pt.x % block_size, pt.y % block_size))
    return result


def merge_grid(input_blocks, block_size):
    result = set()
    for index_pt, block in input_blocks.items():
        for pt in block:
            result.add(Pt(block_size * index_pt.x + pt.x,
                          block_size * index_pt.y + pt.y))
    return result


def flip_and_rotate(pattern, size, flips, cw_rotates):
    result = set()
    for pt in pattern:
        if flips == 1:
            new_pt = Pt(size - 1 - pt.x, pt.y)
        else:
            new_pt = Pt(pt.x, pt.y)
        for _ in range(cw_rotates):
            new_pt = Pt(new_pt.y, size - 1 - new_pt.x)
        result.add(new_pt)
    return frozenset(result)


def test_flip_and_rotate():
    test_pattern = {Pt(0, 0), Pt(1, 2)}
    assert flip_and_rotate(test_pattern, 0, 0, 0) == frozenset(test_pattern)
    assert set(flip_and_rotate(test_pattern, 4, 1, 0)) == {Pt(3, 0), Pt(2, 2)}


class FractalArt:
    # STARTING IMAGE
    #    .#.  Pt(1, 0)
    #    ..#  Pt(2, 1)
    #    ###  Pt(0, 2) Pt(1, 2) Pt(2, 2)
    STARTING_IMAGE = {Pt(1, 0), Pt(2, 1), Pt(0, 2), Pt(1, 2), Pt(2, 2)}

    def __init__(self, raw_rules, starting_size=3, starting_image=None, maintain_orientation=True):
        self.rules = FractalArt.build_additional_rules(raw_rules, maintain_orientation)
        if starting_image is None:
            self.image = FractalArt.STARTING_IMAGE.copy()
            self.size = 3
        else:
            self.image = starting_image
            self.size = starting_size
        self.grid_ids = {}
        self.grid_size_in = 3
        self.grid_in = {}
        self.grid_size_out = 2
        self.grid_out = {}
        self.generation = 0

    @staticmethod
    def build_additional_rules(raw_input, maintain_orientation=True):
        rules = {}
        for r_id, line in enumerate(raw_input):
            raw_input_grid, raw_output_grid = line.split(' => ')
            in_size, in_grid = FractalArt.parse_raw_grid(raw_input_grid)
            out_size, out_grid = FractalArt.parse_raw_grid(raw_output_grid)
            rotations = FractalArt.get_rotations(in_size, in_grid, out_size, out_grid, maintain_orientation)
            for rot in rotations:
                r_input_grid, r_output_grid = rotations[rot]
                rules[(in_size, r_input_grid)] = (r_output_grid, f'{r_id}{rot}')
        return rules

    @staticmethod
    def parse_raw_grid(raw_input):
        input_rows = raw_input.split('/')
        size = len(input_rows)
        grid = set()
        for y, row in enumerate(input_rows):
            for x, c in enumerate(row):
                if c == '#':
                    grid.add(Pt(x, y))
        return size, frozenset(grid)

    @staticmethod
    def get_rotations(size_a, pattern_a, size_b, pattern_b, maintain_orientation=True):
        results = {}
        for f, r in [(flips, cw_rotations) for flips in range(2) for cw_rotations in range(4)]:
            new_pattern_a = flip_and_rotate(pattern_a, size_a, f, r)
            if maintain_orientation:
                new_pattern_b = flip_and_rotate(pattern_b, size_b, f, r)
            else:
                new_pattern_b = pattern_b
            results[(f, r)] = (new_pattern_a, new_pattern_b)
        return results

    def print_image(self, indent=3):
        result = []
        for y in range(0, self.size):
            line = [''.rjust(indent, ' ')]
            for x in range(0, self.size):
                if Pt(x, y) in self.image:
                    line.append('#')
                else:
                    line.append('.')
            result.append(''.join(line))
        print('\n'.join(result))

    def print_grids(self, size, grid, indent=6):
        result = []
        block_size = size // sum(1 for pt in grid if pt.y == 0)
        for y in range(0, size):
            index_y = y // block_size
            if y % block_size == 0:
                line = ['+'.rjust(indent + 1, ' ')]
                extra = []
                for index_x in (pt.x for pt in grid if pt.y == 0):
                    pt = Pt(index_x, index_y)
                    extra.append(f' {self.grid_ids[pt]},')
                    line.append(''.ljust(block_size, '-'))
                    line.append('+')
                line.extend(extra)
                result.append(''.join(line))
            line = [''.rjust(indent, ' ')]
            for x in range(0, size):
                if x % block_size == 0:
                    line.append('|')
                pt = Pt(x // block_size, index_y)
                if Pt(x % block_size, y % block_size) in grid[pt]:
                    line.append('#')
                else:
                    line.append('.')
            result.append(''.join(line))
        print('\n'.join(result))

    @staticmethod
    def block_size(in_size, out_size=False):
        if out_size:
            return 3 if in_size % 2 == 0 else 4
        return 2 if in_size % 2 == 0 else 3

    @staticmethod
    def next_size(in_size):
        return 3 * in_size // 2 if in_size % 2 == 0 else 4 * in_size // 3

    def step(self):
        self.generation += 1
        self.grid_size_in = self.size

        block_size_in = FractalArt.block_size(self.size)
        block_size_out = FractalArt.block_size(self.size, out_size=True)

        self.grid_in = split_grid(self.image, block_size_in, self.size)

        self.grid_out = {}
        self.grid_ids = {}
        self.size = FractalArt.next_size(self.size)
        self.grid_size_out = self.size

        for index_pt, block in self.grid_in.items():
            self.grid_out[index_pt], self.grid_ids[index_pt] = self.rules[(block_size_in, frozenset(block))]
        self.image = merge_grid(self.grid_out, block_size_out)

    def do_art(self, steps, print_steps=False, print_partial=False):
        if print_steps:
            print()
            print(f'gen {self.generation} size {self.size}')
            self.print_image()
        for _ in range(steps):
            self.step()
            if print_steps:
                print()
                print(f'gen {self.generation} size {self.size}')
                if print_partial:
                    self.print_grids(self.grid_size_in, self.grid_in)
                    print()
                    self.print_grids(self.grid_size_out, self.grid_out)
                    print()
                self.print_image()
        return len(self.image)


def test_build_rules():
    rules = FractalArt.build_additional_rules(SAMPLE)
    assert len(rules) == 12
    puzzle_rules = FractalArt.build_additional_rules(INPUTS)
    assert len(puzzle_rules) == 528


def test_sample_art():
    fractal_art = FractalArt(SAMPLE, maintain_orientation=False)
    result = fractal_art.do_art(2, print_steps=True, print_partial=True)
    assert result == 12


def test_puzzle_art():
    fractal_art = FractalArt(INPUTS, maintain_orientation=False)
    result = fractal_art.do_art(5, print_steps=False, print_partial=False)
    # 226, 347, 58, 41, 65 and 52 are not right :|
    # finally, right answer was 123...
    assert result == 123
    # part 2
    fractal_art = FractalArt(INPUTS, maintain_orientation=False)
    result = fractal_art.do_art(18)
    assert result == 1984683
