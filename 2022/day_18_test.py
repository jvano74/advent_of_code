from typing import NamedTuple


class Puzzle:
    """
    --- Day 18: Boiling Boulders ---

    You and the elephants finally reach fresh air. You've emerged near the base
    of a large volcano that seems to be actively erupting! Fortunately, the lava
    seems to be flowing away from you and toward the ocean.

    Bits of lava are still being ejected toward you, so you're sheltering in the
    cavern exit a little longer. Outside the cave, you can see the lava landing
    in a pond and hear it loudly hissing as it solidifies.

    Depending on the specific compounds in the lava and speed at which it cools,
    it might be forming obsidian! The cooling rate should be based on the
    surface area of the lava droplets, so you take a quick scan of a droplet as
    it flies past you (your puzzle input).

    Because of how quickly the lava is moving, the scan isn't very good; its
    resolution is quite low and, as a result, it approximates the shape of the
    lava droplet with 1x1x1 cubes on a 3D grid, each given as its x,y,z
    position.

    To approximate the surface area, count the number of sides of each cube that
    are not immediately connected to another cube. So, if your scan were only
    two adjacent cubes like 1,1,1 and 2,1,1, each cube would have a single side
    covered and five sides exposed, a total surface area of 10 sides.

    Here's a larger example:

    2,2,2
    1,2,2
    3,2,2
    2,1,2
    2,3,2
    2,2,1
    2,2,3
    2,2,4
    2,2,6
    1,2,5
    3,2,5
    2,1,5
    2,3,5

    In the above example, after counting up all the sides that aren't connected
    to another cube, the total surface area is 64.

    What is the surface area of your scanned lava droplet?

    Your puzzle answer was 4302.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---

    Something seems off about your calculation. The cooling rate depends on
    exterior surface area, but your calculation also included the surface area
    of air pockets trapped in the lava droplet.

    Instead, consider only cube sides that could be reached by the water and
    steam as the lava droplet tumbles into the pond. The steam will expand to
    reach as much as possible, completely displacing any air on the outside of
    the lava droplet but never expanding diagonally.

    In the larger example above, exactly one cube of air is trapped within the
    lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is
    58.

    What is the exterior surface area of your scanned lava droplet?
    """


class Pt(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y, self.z - other.z)

    def pt_min(self, other):
        return Pt(min(self.x, other.x), min(self.y, other.y), min(self.z, other.z))

    def pt_max(self, other):
        return Pt(max(self.x, other.x), max(self.y, other.y), max(self.z, other.z))

    def top(self):
        return Pt(self.x, self.y, self.z + 1)

    def bottom(self):
        return Pt(self.x, self.y, self.z - 1)

    def left(self):
        return Pt(self.x - 1, self.y, self.z)

    def right(self):
        return Pt(self.x + 1, self.y, self.z)

    def front(self):
        return Pt(self.x, self.y + 1, self.z)

    def back(self):
        return Pt(self.x, self.y - 1, self.z)

    def faces(self, neighbors):
        return len(
            {
                self.top(),
                self.bottom(),
                self.left(),
                self.right(),
                self.front(),
                self.back(),
            }
            - neighbors
        )


def parse_point(line):
    x, y, z = (int(c) for c in line.split(","))
    return Pt(x, y, z)


SAMPLE = [
    Pt(2, 2, 2),
    Pt(1, 2, 2),
    Pt(3, 2, 2),
    Pt(2, 1, 2),
    Pt(2, 3, 2),
    Pt(2, 2, 1),
    Pt(2, 2, 3),
    Pt(2, 2, 4),
    Pt(2, 2, 6),
    Pt(1, 2, 5),
    Pt(3, 2, 5),
    Pt(2, 1, 5),
    Pt(2, 3, 5),
]

with open("day_18_input.txt") as fp:
    MY_INPUT = [parse_point(line) for line in fp]


class Blob:
    def __init__(self, bits) -> None:
        self.pt_min = Pt(0, 0, 0)
        self.pt_max = Pt(0, 0, 0)
        self.bits = set()
        for pt in bits:
            self.pt_min = self.pt_min.pt_min(pt)
            self.pt_max = self.pt_max.pt_max(pt)
            self.bits.add(pt)


def test_pt():
    assert sum(pt.faces(set(SAMPLE)) for pt in SAMPLE) == 64
    assert sum(pt.faces(set(MY_INPUT)) for pt in MY_INPUT) == 4302
