class Puzzle:
    """
    --- Day 8: Two-Factor Authentication ---
    You come across a door implementing what you can only assume is an
    implementation of two-factor authentication after a long game of
    requirements telephone.

    To get past the door, you first swipe a keycard (no problem; there was one
    on a nearby desk). Then, it displays a code on a little screen, and you type
    that code on a keypad. Then, presumably, the door unlocks.

    Unfortunately, the screen has been smashed. After a few minutes, you've
    taken everything apart and figured out how it works. Now you just have to
    work out what the screen would have displayed.

    The magnetic strip on the card you swiped encodes a series of instructions
    for the screen; these instructions are your puzzle input. The screen is 50
    pixels wide and 6 pixels tall, all of which start off, and is capable of
    three somewhat peculiar operations:

    - rect AxB turns on all of the pixels in a rectangle at the top-left of the
      screen which is A wide and B tall.

    - rotate row y=A by B shifts all of the pixels in row A (0 is the top row)
      right by B pixels. Pixels that would fall off the right end appear at the
      left end of the row.

    - rotate column x=A by B shifts all of the pixels in column A (0 is the left
      column) down by B pixels. Pixels that would fall off the bottom appear at
      the top of the column.

    For example, here is a simple sequence on a smaller screen:

    rect 3x2 creates a small rectangle in the top-left corner:

    ###....
    ###....
    .......

    rotate column x=1 by 1 rotates the second column down by one pixel:

    #.#....
    ###....
    .#.....

    rotate row y=0 by 4 rotates the top row right by four pixels:

    ....#.#
    ###....
    .#.....

    rotate column x=1 by 1 again rotates the second column down by one pixel,
    causing the bottom pixel to wrap back to the top:

    .#..#.#
    #.#....
    .#.....

    As you can see, this display technology is extremely powerful, and will soon
    dominate the tiny-code-displaying-screen market. That's what the
    advertisement on the back of the display tries to convince you, anyway.

    There seems to be an intermediate check of the voltage used by the display:
    after you swipe your card, if the screen did work, how many pixels should be
    lit?
    """

    pass


class TinyScreen:
    def __init__(self, x_max=50, y_max=6):
        self.x_max = x_max
        self.y_max = y_max
        self.display = [["." for x in range(x_max)] for y in range(y_max)]

    def print(self):
        print("")
        for row in self.display:
            print("".join(row))

    def update(self, instruction):
        bits = instruction.split(" ")
        if bits[0] == "rect":
            rx, ry = bits[1].split("x")
            for y in range(int(ry)):
                for x in range(int(rx)):
                    self.display[y][x] = "#"
        elif bits[0] == "rotate":
            base = int(bits[2][2:])
            dist = int(bits[4])
            if bits[1] == "row":
                shifted = [
                    self.display[base][(x - dist) % self.x_max]
                    for x in range(self.x_max)
                ]
                for x in range(self.x_max):
                    self.display[base][x] = shifted[x]
            if bits[1] == "column":
                shifted = [
                    self.display[(y - dist) % self.y_max][base]
                    for y in range(self.y_max)
                ]
                for y in range(self.y_max):
                    self.display[y][base] = shifted[y]


def test_tinyscreen_update():
    ts = TinyScreen(7, 3)
    print("Created small screen")
    ts.update("rect 3x2")
    ts.print()
    assert ts.display == [list("###...."), list("###...."), list(".......")]
    ts.update("rotate column x=1 by 1")
    ts.print()
    assert ts.display == [list("#.#...."), list("###...."), list(".#.....")]
    ts.update("rotate row y=0 by 4")
    ts.print()
    assert ts.display == [list("....#.#"), list("###...."), list(".#.....")]
    ts.update("rotate column x=1 by 1")
    ts.print()
    assert ts.display == [list(".#..#.#"), list("#.#...."), list(".#.....")]
    assert sum([sum([1 for c in row if c == "#"]) for row in ts.display]) == 6


with open("day_08_input.txt") as f:
    INPUTS = [line.strip() for line in f]


def test_part1():
    ts = TinyScreen()
    for inst in INPUTS:
        ts.update(inst)
    ts.print()
    assert sum([sum([1 for c in row if c == "#"]) for row in ts.display]) == 106
    assert ts.display == [
        list(
            ".##.."
            + "####."
            + "#...."
            + "####."
            + "#...."
            + ".##.."
            + "#...#"
            + "####."
            + ".##.."
            + ".###."
        ),
        list(
            "#..#."
            + "#...."
            + "#...."
            + "#...."
            + "#...."
            + "#..#."
            + "#...#"
            + "#...."
            + "#..#."
            + "#...."
        ),
        list(
            "#...."
            + "###.."
            + "#...."
            + "###.."
            + "#...."
            + "#..#."
            + ".#.#."
            + "###.."
            + "#...."
            + "#...."
        ),
        list(
            "#...."
            + "#...."
            + "#...."
            + "#...."
            + "#...."
            + "#..#."
            + "..#.."
            + "#...."
            + "#...."
            + ".##.."
        ),
        list(
            "#..#."
            + "#...."
            + "#...."
            + "#...."
            + "#...."
            + "#..#."
            + "..#.."
            + "#...."
            + "#..#."
            + "...#."
        ),
        list(
            ".##.."
            + "#...."
            + "####."
            + "####."
            + "####."
            + ".##.."
            + "..#.."
            + "#...."
            + ".##.."
            + "###.."
        ),
    ]
    # that is CFLELOYFCS
