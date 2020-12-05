class Puzzle:
    """
     --- Day 3: Squares With Three Sides ---
     Now that you can think clearly, you move deeper into the labyrinth of hallways and office furniture that makes
     up this part of Easter Bunny HQ. This must be a graphic design department; the walls are covered in
     specifications for triangles.

     Or are they?

     The design document gives the side lengths of each triangle it describes, but... 5 10 25? Some of these
     aren't triangles. You can't help but mark the impossible ones.

     In a valid triangle, the sum of any two sides must be larger than the remaining side. For example,
     the "triangle" given above is impossible, because 5 + 10 is not larger than 25.

     In your puzzle input, how many of the listed triangles are possible?

     -- Part Two ---
     Now that you've helpfully marked up their design documents, it occurs to you that triangles are specified
     in groups of three vertically. Each set of three numbers in a column specifies a triangle. Rows are unrelated.

     For example, given the following specification, numbers with the same hundreds digit would be part
     of the same triangle:

     101 301 501
     102 302 502
     103 303 503
     201 401 601
     202 402 602
     203 403 603

     In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?
    """
    pass


with open('day_03_input.txt') as f:
    INPUTS = [[int(s) for s in line.strip().split()] for line in f]

SAMPLE = [5, 10, 25]

SAMPLE2 = [
    [101, 301, 501],
    [102, 302, 502],
    [103, 303, 503],
    [201, 401, 601],
    [202, 402, 602],
    [203, 403, 603]]

SAMPLE2_TRANSFORMED = [
    [101, 102, 103],
    [301, 302, 303],
    [501, 502, 503],
    [201, 202, 203],
    [401, 402, 403],
    [601, 602, 603]]


def valid_triangle(sides):
    ordered = sorted(sides)
    return ordered[0] + ordered[1] > ordered[2]


def transform(original_list):
    new_list = []
    for pos in range(0,len(original_list),3):
        a = original_list[pos + 0]
        b = original_list[pos + 1]
        c = original_list[pos + 2]
        new_list.append([a[0], b[0], c[0]])
        new_list.append([a[1], b[1], c[1]])
        new_list.append([a[2], b[2], c[2]])
    return new_list


def test_transform():
    assert transform((SAMPLE2)) == SAMPLE2_TRANSFORMED


def test_valid_triangle():
    assert valid_triangle([3, 4, 5])
    assert not valid_triangle(SAMPLE)
    assert sum([valid_triangle(t) for t in INPUTS]) == 1050
    assert sum([valid_triangle(t) for t in transform(INPUTS)]) == 1921 # initial guess was 1589 which was
                                                                  # wrong because of sort of INPUTS from part 1




