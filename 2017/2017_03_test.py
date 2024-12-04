import math
from collections import defaultdict


class Puzzle:
    """
    --- Day 3: Spiral Memory ---
    You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

    Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up
    while spiraling outward. For example, the first few squares are allocated like this:

    17  16  15  14  13
    18   5   4   3  12
    19   6   1   2  11
    20   7   8   9  10
    21  22  23---> ...

    While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1
    (the location of the only access port for this memory system) by programs that can only move up, down, left,
    or right. They always take the shortest path: the Manhattan Distance between the location of the data and
    square 1.

    For example:

    Data from square 1 is carried 0 steps, since it's at the access port.
    Data from square 12 is carried 3 steps, such as: down, left, left.
    Data from square 23 is carried only 2 steps: up twice.
    Data from square 1024 must be carried 31 steps.

    How many steps are required to carry the data from the square identified in your puzzle input all the way
    to the access port?

    Your puzzle input is 277678.

    --- Part Two ---
    As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1.
    Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares,
    including diagonals.

    So, the first few squares' values are chosen as follows:

    Square 1 starts with the value 1.
    Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
    Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
    Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
    Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.

    Once a square is written, its value does not change.
    Therefore, the first few squares would receive the following values:

    147  142  133  122   59
    304    5    4    2   57
    330   10    1    1   54
    351   11   23   25   26
    362  747  806--->   ...

    What is the first value written that is larger than your puzzle input?
    """
    pass


INPUTS = 277678

def spiral_number(x, y):
    ring = max([abs(x), abs(y)])
    if ring == 0:
        return 1
    min_val = (2*ring-1) ** 2
    max_val = (2*ring+1) ** 2
    if x == ring:
        if y == -ring:
            return max_val
        else:
            return min_val + y + ring
    if y == ring:
        return min_val - x + 3*ring
    if x == -ring:
        return min_val - y + 5*ring
    if y == -ring:
        return min_val + x + 7*ring
    return -1


def test_spiral_numer():
    """
    17 (-2, 2) 16 (-1, 2) 15 (0, 2) 14 (1, 2) 13 (2, 2)
    18 (-2, 1)  5 (-1, 1)  4 (0, 1)  3 (1, 1) 12 (2, 1)
    19 (-2, 0)  6 (-1, 0)  1 (0, 0)  2 (1, 0) 11 (2, 0)
    20 (-2,-1)  7 (-1,-1)  8 (0,-1)  9 (1,-1) 10 (2,-1)
    21 (-2,-2) 22 (-1,-2) 23 (0,-2) 24 (1,-2) 25 (2,-2)
    """
    assert spiral_number(0,0) == 1
    assert spiral_number(1,0) == 2
    assert spiral_number(1,1) == 3
    assert spiral_number(0,1) == 4
    assert spiral_number(-1,1) == 5
    assert spiral_number(-1,0) == 6
    assert spiral_number(-1,-1) == 7
    assert spiral_number(0,-1) == 8
    assert spiral_number(1, -1) == 9
    assert spiral_number(2, 0) == 11
    assert spiral_number(0, 2) == 15
    assert spiral_number(-2, 0) == 19
    assert spiral_number(0, -2) == 23
    assert spiral_number(2, -2) == 25


def number_to_spiral(num):
    ring = math.ceil((math.sqrt(num) - 1) / 2)
    if ring == 0:
        return 0, 0
    leg_length = 2*ring
    left_over = num - (2 * ring - 1) ** 2
    leg = (left_over - 1) // leg_length
    extra = (left_over - 1) % leg_length
    # print(f'num {num} in ring {ring} with left_over {left_over} on leg {leg} with extra {extra}')
    if leg == 0:
        return ring, extra - ring + 1
    if leg == 1:
        return ring - extra - 1, ring
    if leg == 2:
        return - ring, ring - extra - 1
    if leg == 3:
        return extra - ring + 1, - ring
    return 0, 0

def test_number_to_spiral():
    """
    17 (-2, 2) 16 (-1, 2) 15 (0, 2) 14 (1, 2) 13 (2, 2)
    18 (-2, 1)  5 (-1, 1)  4 (0, 1)  3 (1, 1) 12 (2, 1)
    19 (-2, 0)  6 (-1, 0)  1 (0, 0)  2 (1, 0) 11 (2, 0)
    20 (-2,-1)  7 (-1,-1)  8 (0,-1)  9 (1,-1) 10 (2,-1)
    21 (-2,-2) 22 (-1,-2) 23 (0,-2) 24 (1,-2) 25 (2,-2)
    """
    #print('\n\nClearing out print buffer\n\n')
    #for n in range(100):
    #    x = number_to_spiral(n)
    assert number_to_spiral(1) == (0, 0)
    assert number_to_spiral(2) == (1, 0)
    assert number_to_spiral(3) == (1, 1)
    assert number_to_spiral(4) == (0, 1)
    assert number_to_spiral(5) == (-1, 1)
    assert number_to_spiral(6) == (-1, 0)
    assert number_to_spiral(7) == (-1, -1)
    assert number_to_spiral(8) == (0, -1)
    assert number_to_spiral(9) == (1, -1)
    assert number_to_spiral(10) == (2, -1)
    assert number_to_spiral(14) == (1, 2)
    assert sum(abs(d) for d in number_to_spiral(INPUTS)) == 475


class Puzzle2:
    """
    --- Part Two ---
    As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1.
    Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares,
    including diagonals.

    So, the first few squares' values are chosen as follows:

    Square 1 starts with the value 1.
    Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
    Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
    Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
    Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.

    Once a square is written, its value does not change.
    Therefore, the first few squares would receive the following values:

    147  142  133  122   59
    304    5    4    2   57
    330   10    1    1   54
    351   11   23   25   26
    362  747  806--->   ...

    What is the first value written that is larger than your puzzle input?
    """
    pass


def fill(n,max):
    mem = defaultdict(int)
    mem[(0,0)] = 1
    for pos in range(n):
        x,y = number_to_spiral(pos)
        val = 0
        for dx in [-1, 0 ,1 ]:
            for dy in [-1, 0, 1]:
                val += mem[(x+dx,y+dy)]
        mem[(x,y)] = val
        if val > max:
            return val
    return mem


def test_fill():
    assert fill(100000,INPUTS) == 279138