import math
from pathlib import Path
from typing import List, NamedTuple


class Puzzle:
    """
    --- Day 8: Playground ---
    Equipped with a new understanding of teleporter maintenance, you confidently
    step onto the repaired teleporter pad.

    You rematerialize on an unfamiliar teleporter pad and find yourself in a
    vast underground space which contains a giant playground!

    Across the playground, a group of Elves are working on setting up an
    ambitious Christmas decoration project. Through careful rigging, they have
    suspended a large number of small electrical junction boxes.

    Their plan is to connect the junction boxes with long strings of lights.
    Most of the junction boxes don't provide electricity; however, when two
    junction boxes are connected by a string of lights, electricity can pass
    between those two junction boxes.

    The Elves are trying to figure out which junction boxes to connect so that
    electricity can reach every junction box. They even have a list of all of
    the junction boxes' positions in 3D space (your puzzle input).

    For example:

    162,817,812
    57,618,57
    906,360,560
    592,479,940
    352,342,300
    466,668,158
    542,29,236
    431,825,988
    739,650,466
    52,470,668
    216,146,977
    819,987,18
    117,168,530
    805,96,715
    346,949,466
    970,615,88
    941,993,340
    862,61,35
    984,92,344
    425,690,689

    This list describes the position of 20 junction boxes, one per line. Each
    position is given as X,Y,Z coordinates. So, the first junction box in the
    list is at X=162, Y=817, Z=812.

    To save on string lights, the Elves would like to focus on connecting pairs
    of junction boxes that are as close together as possible according to
    straight-line distance. In this example, the two junction boxes which are
    closest together are 162,817,812 and 425,690,689.

    By connecting these two junction boxes together, because electricity can
    flow between them, they become part of the same circuit. After connecting
    them, there is a single circuit which contains two junction boxes, and the
    remaining 18 junction boxes remain in their own individual circuits.

    Now, the two junction boxes which are closest together but aren't already
    directly connected are 162,817,812 and 431,825,988. After connecting them,
    since 162,817,812 is already connected to another junction box, there is now
    a single circuit which contains three junction boxes and an additional 17
    circuits which contain one junction box each.

    The next two junction boxes to connect are 906,360,560 and 805,96,715. After
    connecting them, there is a circuit containing 3 junction boxes, a circuit
    containing 2 junction boxes, and 15 circuits which contain one junction box
    each.

    The next two junction boxes are 431,825,988 and 425,690,689. Because these
    two junction boxes were already in the same circuit, nothing happens!

    This process continues for a while, and the Elves are concerned that they
    don't have enough extension cables for all these circuits. They would like
    to know how big the circuits will be.

    After making the ten shortest connections, there are 11 circuits: one
    circuit which contains 5 junction boxes, one circuit which contains 4
    junction boxes, two circuits which contain 2 junction boxes each, and seven
    circuits which each contain a single junction box. Multiplying together the
    sizes of the three largest circuits (5, 4, and one of the circuits of size
    2) produces 40.

    Your list contains many junction boxes; connect together the 1000 pairs of
    junction boxes which are closest together. Afterward, what do you get if you
    multiply together the sizes of the three largest circuits?

    Your puzzle answer was 112230.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The Elves were right; they definitely don't have enough extension cables.
    You'll need to keep connecting junction boxes together until they're all in
    one large circuit.

    Continuing the above example, the first connection which causes all of the
    junction boxes to form a single circuit is between the junction boxes at
    216,146,977 and 117,168,530. The Elves need to know how far those junction
    boxes are from the wall so they can pick the right extension cable;
    multiplying the X coordinates of those two junction boxes (216 and 117)
    produces 25272.

    Continue connecting the closest unconnected pairs of junction boxes together
    until they're all in the same circuit. What do you get if you multiply
    together the X coordinates of the last two junction boxes you need to
    connect?

    Your puzzle answer was 2573952864.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open(Path(__file__).parent / "2025_08_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")
    RAW_INPUT.pop()

SAMPLE = [
    "162,817,812",
    "57,618,57",
    "906,360,560",
    "592,479,940",
    "352,342,300",
    "466,668,158",
    "542,29,236",
    "431,825,988",
    "739,650,466",
    "52,470,668",
    "216,146,977",
    "819,987,18",
    "117,168,530",
    "805,96,715",
    "346,949,466",
    "970,615,88",
    "941,993,340",
    "862,61,35",
    "984,92,344",
    "425,690,689",
]


class Pt(NamedTuple):
    x: int
    y: int
    z: int

    @classmethod
    def raw(cls, raw):
        x, y, z = raw.split(",")
        return cls(int(x), int(y), int(z))

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y, self.z - other.z)

    def dist(self, other):
        return math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


class Playground:

    def __init__(self, raw_points: List[str]):
        points = []
        for raw_pt in raw_points:
            points.append(Pt.raw(raw_pt))
        self.total_points = len(points)
        distances = []
        while points:
            a = points.pop()
            for b in points:
                distances.append((a.dist(b), a, b))
        self.distances = sorted(distances)

    def connect(self, max_connections=10, connect_all=False):
        connections = 0
        circuits = [
            {}
        ]  # Useful to have a null 0 circuit to simplify position logic of found circuits
        for _, a, b in self.distances:
            found_a = None
            found_b = None
            for position, circuit in enumerate(circuits):
                if a in circuit:
                    found_a = position
                if b in circuit:
                    found_b = position

            if not found_a and not found_b:
                connections += 1
                circuits.append({a, b})
            elif found_a and not found_b:
                connections += 1
                circuits[found_a].add(b)
            elif found_b and not found_a:
                connections += 1
                circuits[found_b].add(a)
            elif found_a and found_b and found_a == found_b:
                # would save more extension cords to pass here, but we will still count the connection
                connections += 1
            elif found_a and found_b and found_a != found_b:
                connections += 1
                circuits[found_a] |= circuits[found_b]
                circuits.pop(found_b)
            else:
                pass

            if connect_all and len(circuits[1]) == self.total_points:
                return a.x * b.x
            if not connect_all and connections >= max_connections:
                return sorted(((len(c), c) for c in circuits), reverse=True)


def test_playground():
    sample_playground = Playground(SAMPLE)
    components = sample_playground.connect()
    # we may have circuits so the following count doesn't line up...
    # assert sum(len - 1 for len, _ in components if len != 0) == 10
    assert math.prod(len for len, _ in components[0:3]) == 40
    assert sample_playground.connect(connect_all=True) == 25272

    my_playground = Playground(RAW_INPUT)
    my_components = my_playground.connect(max_connections=1000)
    # we may have circuits so the following count doesn't line up...
    # assert sum(len - 1 for len, _ in my_components if len != 0) == 1000
    # first guess 2016 was too low but 112230 is correct
    assert math.prod(len for len, _ in my_components[0:3]) == 112230
    assert my_playground.connect(connect_all=True) == 2573952864
