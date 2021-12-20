from typing import NamedTuple
from collections import defaultdict


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def max(self, other):
        return Pt(max(self.x, other.x), max(self.y, other.y))


class Puzzle:
    """

--- Day 20: Trench Map ---

With the scanners fully deployed, you turn their attention to mapping the floor of the ocean trench.

When you get back the image from the scanners, it seems to just be random noise. Perhaps you can combine
an image enhancement algorithm and the input image (your puzzle input) to clean it up a little.

For example:

..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###

The first section is the image enhancement algorithm. It is normally given on a single line, but it has been wrapped
to multiple lines in this example for legibility. The second section is the input image, a two-dimensional grid of
light pixels (#) and dark pixels (.).

The image enhancement algorithm describes how to enhance an image by simultaneously converting all pixels in the
input image into an output image. Each pixel of the output image is determined by looking at a 3x3 square of pixels
centered on the corresponding input image pixel. So, to determine the value of the pixel at (5,10) in the output
image, nine pixels from the input image need to be considered: (4,9), (4,10), (4,11), (5,9), (5,10), (5,11), (6,9),
(6,10), and (6,11). These nine input pixels are combined into a single binary number that is used as an index in
the image enhancement algorithm string.

For example, to determine the output pixel that corresponds to the very middle pixel of the input image, the nine
pixels marked by [...] would need to be considered:

# . . # .
#[. . .].
#[# . .]#
.[. # .].
. . # # #

Starting from the top-left and reading across each row, these pixels are ..., then #.., then .#.; combining these
forms ...#...#.. By turning dark pixels (.) into 0 and light pixels (#) into 1, the binary number 000100010 can
be formed, which is 34 in decimal.

The image enhancement algorithm string is exactly 512 characters long, enough to match every possible 9-bit binary
number. The first few characters of the string (numbered starting from zero) are as follows:

0         10        20        30  34    40        50        60        70
|         |         |         |   |     |         |         |         |
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##

In the middle of this first group of characters, the character at index 34 can be found: #. So, the output pixel in
the center of the output image should be #, a light pixel.

This process can then be repeated to calculate every pixel of the output image.

Through advances in imaging technology, the images being operated on here are infinite in size. Every pixel of the
infinite output image needs to be calculated exactly based on the relevant pixels of the input image. The small
input image you have is only a small region of the actual infinite input image; the rest of the input image consists
of dark pixels (.). For the purposes of the example, to save on space, only a portion of the infinite-sized input
and output images will be shown.

The starting input image, therefore, looks something like this, with more dark pixels (.) extending forever in
every direction not shown here:

...............
...............
...............
...............
...............
.....#..#......
.....#.........
.....##..#.....
.......#.......
.......###.....
...............
...............
...............
...............
...............

By applying the image enhancement algorithm to every pixel simultaneously, the following output image can be obtained:

...............
...............
...............
...............
.....##.##.....
....#..#.#.....
....##.#..#....
....####..#....
.....#..##.....
......##..#....
.......#.#.....
...............
...............
...............
...............

Through further advances in imaging technology, the above output image can also be used as an input image! This
allows it to be enhanced a second time:

...............
...............
...............
..........#....
....#..#.#.....
...#.#...###...
...#...##.#....
...#.....#.#...
....#.#####....
.....#.#####...
......##.##....
.......###.....
...............
...............
...............

Truly incredible - now the small details are really starting to come through. After enhancing the original input
image twice, 35 pixels are lit.

Start with the original input image and apply the image enhancement algorithm twice, being careful to account for
the infinite size of the images. How many pixels are lit in the resulting image?

To begin, get your puzzle input.

    """


RAW_SAMPLE = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##''' \
             + '''#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###''' \
             + '''.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.''' \
             + '''.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....''' \
             + '''.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..''' \
             + '''...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....''' \
             + '''..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
'''

with open('day_20_input.txt') as fp:
    RAW_INPUT = fp.read()


class Image:
    def __init__(self, raw_string):
        self.default_value = 0
        self.grid = defaultdict(lambda: 0)
        self.min_pt = Pt(0, 0)
        self.max_pt = Pt(0, 0)
        self.enhance, raw_grid = raw_string.split('\n\n')
        for y, line in enumerate(raw_grid.split('\n')):
            for x, c in enumerate(line):
                pt = Pt(x, y)
                if c == '#':
                    self.grid[pt] = 1
                    self.max_pt = self.max_pt.max(pt)

    def enhance_code(self, pt):
        check = [Pt(-1, -1), Pt(0, -1), Pt(1, -1), Pt(-1, 0), Pt(0, 0), Pt(1, 0), Pt(-1, 1), Pt(0, 1), Pt(1, 1)]
        codes = [str(self.grid[pt + d]) for d in check]
        value = int(''.join(codes), 2)
        return 1 if self.enhance[value] == '#' else 0

    def enhance_image(self):
        if self.default_value == 0 and self.enhance[0] == '#':
            self.default_value = 1
            next_grid = defaultdict(lambda: 1)
        else:
            self.default_value = 0
            next_grid = defaultdict(lambda: 0)
        self.min_pt += Pt(-2, -2)
        self.max_pt += Pt(2, 2)
        result = []
        for y in range(self.min_pt.y, self.max_pt.y + 1):
            line = []
            for x in range(self.min_pt.x, self.max_pt.x + 1):
                pt = Pt(x, y)
                c = self.enhance_code(pt)
                line.append('#' if c == 1 else '.')
                next_grid[pt] = c
            result.append(''.join(line))
        self.grid = next_grid
        return '\n'.join(result)


def test_image():
    sample = Image(RAW_SAMPLE)
    print('\nFIRST ENHANCE\n')
    print(sample.enhance_image())
    print('\nSECOND ENHANCE\n')
    print(sample.enhance_image())
    print('\n\n')
    assert sum(sample.grid.values()) == 35
    for _ in range(50-2):
        sample.enhance_image()
    assert sum(sample.grid.values()) == 3351


def test_my_image():
    my_image = Image(RAW_INPUT)
    print('\nFIRST ENHANCE\n')
    print(my_image.enhance_image())
    print('\nSECOND ENHANCE\n')
    print(my_image.enhance_image())
    print('\n\n')
    assert sum(my_image.grid.values()) == 5203
    for _ in range(50-2):
        my_image.enhance_image()
    assert sum(my_image.grid.values()) == 18806
