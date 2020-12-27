class Puzzle:
    """
    --- Day 11: Chronal Charge ---
    You watch the Elves and their sleigh fade into the distance as they head toward the North Pole.

    Actually, you're the one fading. The falling sensation returns.

    The low fuel warning light is illuminated on your wrist-mounted device. Tapping it once causes it to project a
    hologram of the situation: a 300x300 grid of fuel cells and their current power levels, some negative. You're
    not sure what negative power means in the context of time travel, but it can't be good.

    Each fuel cell has a coordinate ranging from 1 to 300 in both the X (horizontal) and Y (vertical) direction.
    In X,Y notation, the top-left cell is 1,1, and the top-right cell is 300,1.

    The interface lets you select any 3x3 square of fuel cells. To increase your chances of getting to your
    destination, you decide to choose the 3x3 square with the largest total power.

    The power level in a given fuel cell can be found through the following process:

    - Find the fuel cell's rack ID, which is its X coordinate plus 10.
    - Begin with a power level of the rack ID times the Y coordinate.
    - Increase the power level by the value of the grid serial number (your puzzle input).
    - Set the power level to itself multiplied by the rack ID.
    - Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    - Subtract 5 from the power level.

    For example, to find the power level of the fuel cell at 3,5 in a grid with serial number 8:

    - The rack ID is 3 + 10 = 13.
    - The power level starts at 13 * 5 = 65.
    - Adding the serial number produces 65 + 8 = 73.
    - Multiplying by the rack ID produces 73 * 13 = 949.
    - The hundreds digit of 949 is 9.
    - Subtracting 5 produces 9 - 5 = 4.

    So, the power level of this fuel cell is 4.

    Here are some more example power levels:

    Fuel cell at  122,79, grid serial number 57: power level -5.
    Fuel cell at 217,196, grid serial number 39: power level  0.
    Fuel cell at 101,153, grid serial number 71: power level  4.

    Your goal is to find the 3x3 square which has the largest total power. The square must be entirely within the
    300x300 grid. Identify this square using the X,Y coordinate of its top-left fuel cell. For example:

    For grid serial number 18, the largest total 3x3 square has a top-left corner of 33,45 (with a total power of 29);
    these fuel cells appear in the middle of this 5x5 region:

    -2  -4   4   4   4
    -4   4   4   4  -5
     4   3   3   4  -4
     1   1   2   4  -3
    -1   0   2  -5  -2

    For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a total power of 30);
    they are in the middle of this region:

    -3   4   2   2   2
    -4   4   3   3   4
    -5   3   3   4  -4
     4   3   3   4  -3
     3   3   3  -5  -1

    What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?

    Your puzzle input is 9005.

    --- Part Two ---
    You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3.
    Sizes from 1x1 to 300x300 are supported.

    Realizing this, you now must find the square of any size with the largest total power. Identify this square
    by including its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner
    of 3,5 is identified as 3,5,9.

    For example:

    For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner
    of 90,269, so its identifier is 90,269,16.

    For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner
    of 232,251, so its identifier is 232,251,12.

    What is the X,Y,size identifier of the square with the largest total power?
    """
    pass


def calculate_power(x, y, base):
    """
    - Find the fuel cell's rack ID, which is its X coordinate plus 10.
    - Begin with a power level of the rack ID times the Y coordinate.
    - Increase the power level by the value of the grid serial number (your puzzle input).
    - Set the power level to itself multiplied by the rack ID.
    - Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    - Subtract 5 from the power level.

    ( yx^2//100 + xy//5 + y + x(base//100) + base//10 ) % 10 - 5

    """
    rack_id = x + 10
    power = (y * rack_id + base) * rack_id
    return (power // 100) % 10 - 5


def test_calculate_power():
    assert calculate_power(3, 5, 8) == 4


class PowerGrid:
    def __init__(self, base):
        self.power = {}
        self.sub_totals = {}
        for y in range(1, 301):
            for x in range(1, 301):
                self.power[(x, y)] = calculate_power(x, y, base)
                self.sub_totals[(x, y, 1)] = self.power[(x, y)]

    def display_power(self, start=(1,1), size=300):
        display = []
        for y in range(start[1], start[1]+size):
            line = []
            for x in range(start[0], start[0]+size):
                line.append(self.power[(x, y)])
            display.append(' '.join(['{:2d}'.format(d) for d in line]))
        return display

    def compute_sub_totals(self, grid_range=None):
        if grid_range is None:
            grid_range = range(1, 4)
        for gs in grid_range:
            if gs == 0 or gs == 1:
                continue
            for y in range(1, 302 - gs):
                for x in range(1, 302 - gs):
                    if gs % 2 == 0 and (x, y, gs // 2) in self.sub_totals:
                        sub_total = self.sub_totals[(x, y, gs // 2)] + \
                                    self.sub_totals[(x + gs // 2, y, gs // 2)] + \
                                    self.sub_totals[(x, y + gs // 2, gs // 2)] + \
                                    self.sub_totals[(x + gs // 2, y + gs // 2, gs // 2)]
                        self.sub_totals[(x, y, gs)] = sub_total
                    elif (x, y, gs - 1) in self.sub_totals:
                        delta = sum(self.power[(x + dx, y + gs - 1)] for dx in range(gs - 1)) + \
                                sum(self.power[(x + gs - 1, y + dy)] for dy in range(gs))
                        self.sub_totals[(x, y, gs)] = self.sub_totals[(x, y, gs - 1)] + delta
                    else:
                        sub_total = sum(self.power[(x + dx, y + dy)]
                                        for dx in range(gs) for dy in range(gs))
                        self.sub_totals[(x, y, gs)] = sub_total

    def get_max(self):
        return max((v, k) for k, v in self.sub_totals.items())


def test_sample_powergrid():
    sample = PowerGrid(18)
    sample.compute_sub_totals()
    print()
    print('\n'.join(sample.display_power((32, 44), 5)))
    assert sample.get_max() == (29, (33, 45, 3))


def test_sample2_powergrid():
    sample = PowerGrid(42)
    print()
    print('\n'.join(sample.display_power((20, 60), 5)))
    sample.compute_sub_totals()
    assert sample.get_max() == (30, (21, 61, 3))


def test_powergrid():
    sample = PowerGrid(9005)
    sample.compute_sub_totals()
    print()
    print('\n'.join(sample.display_power((20, 32), 5)))
    assert sample.get_max() == (31, (20, 32, 3))
    # answer is 20,32

def test_sample_pt2_powergrid():
    sample = PowerGrid(18)
    sample.compute_sub_totals(range(2, 301))
    assert sample.get_max() == (113, (90, 269, 16))


def test_sample2_pt2_powergrid():
    sample = PowerGrid(42)
    sample.compute_sub_totals(range(2, 301))
    assert sample.get_max() == (119, (232, 251, 12))


def test_pt2_powergrid():
    sample = PowerGrid(9005)
    sample.compute_sub_totals(range(2, 301))
    print()
    print('\n'.join(sample.display_power((20, 32), 5)))
    assert sample.get_max() == (148, (235, 287, 13))
    # answer was 235,287,13
    # took a bit on run time to get...
