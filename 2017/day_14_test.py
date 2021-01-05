from typing import NamedTuple


class Puzzle:
    """
    --- Day 14: Disk Defragmentation ---
    Suddenly, a scheduled job activates the system's disk defragmenter. Were the situation different, you might sit
    and watch it for a while, but today, you just don't have that kind of time. It's soaking up valuable system
    resources that are needed elsewhere, and so the only option is to help it finish its task as soon as possible.

    The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk,
    the state of the grid is tracked by the bits in a sequence of knot hashes.

    A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128
    bits which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0)
    or used (1).

    The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row.
    For example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of
    flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row,
    flqrgnkx-127.

    The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond
    to 4 bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent
    binary value, high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash
    that begins with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

    Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used
    squares, and . to denote free ones:

    ##.#.#..-->
    .#.#.#.#
    ....#.#.
    #.#.##.#
    .##.#...
    ##..#..#
    .#...#..
    ##.#.##.-->
    |      |
    V      V

    In this example, 8108 squares are used across the entire 128x128 grid.

    Given your actual key string, how many squares are used?

    Your puzzle input is wenycdww.

    --- Part Two ---
    Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all
    adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own
    isolated regions, while several adjacent squares all count as a single region.

    In the example above, the following nine regions are visible, each marked with a distinct digit:

    11.2.3..-->
    .1.2.3.4
    ....5.6.
    7.8.55.9
    .88.5...
    88..5..8
    .8...8..
    88.8.88.-->
    |      |
    V      V

    Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of
    the squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242
    regions are present.

    How many regions are present given your key string?
    """
    pass


INPUT = 'wenycdww'


def scramble(data, length_list, position=0, skip=0):
    tmp = list()
    for length in length_list:
        for i in range(length):
            tmp.append(data[(position + i) % len(data)])
        while len(tmp) > 0:
            data[position % len(data)] = tmp.pop()
            position += 1
        position = position + skip % len(data)
        skip += 1
    return data, position, skip


def encode(string):
    lengths = [ord(c) for c in string]
    lengths.extend([17, 31, 73, 47, 23])
    return lengths


def test_encode():
    assert encode('1,2,3') == [49, 44, 50, 44, 51, 17, 31, 73, 47, 23]


def knot_hash(string, as_binary=False):
    lengths = encode(string)
    data, position, skip = list(range(256)), 0, 0
    for _ in range(64):
        data, position, skip = scramble(data, lengths, position, skip)
    tmp = 0
    result = []
    data.append(0)
    for i, d in enumerate(data):
        if i > 0 and i % 16 == 0:
            if as_binary:
                string = bin(int(hex(256+tmp)[-2:], 16))[2:]
                result.append(string.rjust(8, '0'))
            else:
                result.append(hex(256+tmp)[-2:])
            tmp = 0
        tmp ^= d
    return ''.join(result)


def test_knot_hash():
    assert knot_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272'
    assert knot_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
    assert knot_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
    assert knot_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'
    # new stuff
    assert knot_hash('flqrgnkx-0', as_binary=True)[0:8] == '11010100'
    assert knot_hash('flqrgnkx-1', as_binary=True)[0:8] == '01010101'
    assert knot_hash('flqrgnkx-2', as_binary=True)[0:8] == '00001010'
    assert knot_hash('flqrgnkx-3', as_binary=True)[0:8] == '10101101'
    assert knot_hash('flqrgnkx-4', as_binary=True)[0:8] == '01101000'
    assert knot_hash('flqrgnkx-5', as_binary=True)[0:8] == '11001001'
    assert knot_hash('flqrgnkx-6', as_binary=True)[0:8] == '01000100'
    assert knot_hash('flqrgnkx-7', as_binary=True)[0:8] == '11010110'


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Disk:
    def __init__(self, key_string):
        self.ones = set()
        self.components = {}

        for y in range(128):
            row = knot_hash(f'{key_string}-{y}', as_binary=True)
            for x, c in enumerate(row):
                if c == '1':
                    self.ones.add(Pt(x, y))

    def num_of_components(self):
        component = 0
        pt_as_component = {p: 0 for p in self.ones}
        for p in self.ones:
            if pt_as_component[p] == 0:
                component += 1
                component_boundary = [p]
                while len(component_boundary) > 0:
                    explore_pt = component_boundary.pop()
                    pt_as_component[explore_pt] = component
                    for d in [Pt(-1, 0), Pt(1, 0), Pt(0, 1), Pt(0, -1)]:
                        new_p = explore_pt + d
                        if new_p in pt_as_component and pt_as_component[new_p] == 0:
                            component_boundary.append(new_p)
        self.components = pt_as_component
        return component


def test_calculate_grid():
    # sample_disk = Disk('flqrgnkx')
    # assert len(sample_disk) == 8108
    puzzle_disk = Disk(INPUT)
    assert len(puzzle_disk.ones) == 8226
    assert puzzle_disk.num_of_components() == 1128
