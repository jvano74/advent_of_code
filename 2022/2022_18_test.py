from pathlib import Path
from heapq import heappush, heappop
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

    def __neg__(self):
        return Pt(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y, self.z - other.z)

    def pt_min(self, other):
        return Pt(min(self.x, other.x), min(self.y, other.y), min(self.z, other.z))

    def pt_max(self, other):
        return Pt(max(self.x, other.x), max(self.y, other.y), max(self.z, other.z))


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


with open(Path(__file__).parent / "2022_18_input.txt") as fp:
    MY_INPUT = [parse_point(line) for line in fp]


DIRECTIONS = {
    Pt(0, 0, 1),  # top
    Pt(0, 0, -1),  # bottom
    Pt(-1, 0, 0),  # left
    Pt(1, 0, 0),  # right
    Pt(0, 1, 0),  # front
    Pt(0, -1, 0),  # back
}


class Face(NamedTuple):
    pt: Pt
    face: Pt


def faces(pt, neighbors):
    count = 0
    for dir in DIRECTIONS:
        if pt + dir in neighbors:
            count += 1
    return count


class Blob:
    def __init__(self, bits) -> None:
        self.pt_min = Pt(0, 0, 0)
        self.pt_max = Pt(0, 0, 0)
        self.bits = set()
        for pt in bits:
            self.pt_min = self.pt_min.pt_min(pt)
            self.pt_max = self.pt_max.pt_max(pt)
            self.bits.add(pt)
        self.boundry_layer = set()
        self.surfaces = set()
        for pt in self.bits:
            for dir in DIRECTIONS:
                new_pt = pt + dir
                if new_pt not in self.bits:
                    self.boundry_layer.add(new_pt)
                    self.surfaces.add((pt, dir))
        # thicken boundry layer
        for _ in range(5):
            for pt in set(self.boundry_layer):
                for dir in DIRECTIONS:
                    new_pt = pt + dir
                    if new_pt not in self.bits and new_pt not in self.boundry_layer:
                        self.boundry_layer.add(new_pt)

    def total_boundry_volume(self):
        return len(self.boundry_layer)

    def total_surface_area(self):
        return len(self.surfaces)

    def find_boundry(self):
        free_boundry = sorted(list(self.boundry_layer), reverse=True)
        found_boundry = dict()
        while free_boundry:
            start_pt = free_boundry.pop()

            current_boundry = {start_pt}
            exploring = []
            heappush(exploring, start_pt)
            while exploring:
                current_pt = heappop(exploring)
                for delta in DIRECTIONS:
                    next_pt = current_pt + delta
                    if next_pt in free_boundry:
                        free_boundry.remove(next_pt)
                        current_boundry.add(next_pt)
                        heappush(exploring, next_pt)
            found_boundry[start_pt] = current_boundry
        return found_boundry

    def find_surfaces_on_layer(self, boundry_layer):
        count = 0
        for pt, face in self.surfaces:
            if pt + face in boundry_layer:
                count += 1
        return count

    def find_surfaces(self):
        free_surfaces = set(self.surfaces)
        found_surfaces = dict()
        while free_surfaces:
            start_pt, start_face = free_surfaces.pop()
            current_surface = {
                (start_pt, start_face),
            }
            exploring = []
            heappush(exploring, (start_pt, start_face))
            while exploring:
                current_pt, current_face = heappop(exploring)
                dir_to_check = DIRECTIONS - {current_face, -current_face}
                for next_face in dir_to_check:
                    next_pt = current_pt + next_face  # around current face
                    next_pt_above = next_pt + current_face  # above current cube
                    if (next_pt_above, -next_face) in free_surfaces:
                        free_surfaces.remove((next_pt_above, -next_face))
                        current_surface.add((next_pt_above, -next_face))
                        heappush(exploring, (next_pt_above, -next_face))
                    elif (next_pt, current_face) in free_surfaces:
                        free_surfaces.remove((next_pt, current_face))
                        current_surface.add((next_pt, current_face))
                        heappush(exploring, (next_pt, current_face))
                    elif (current_pt, next_face) in free_surfaces:
                        free_surfaces.remove((current_pt, next_face))
                        current_surface.add((current_pt, next_face))
                        heappush(exploring, (current_pt, next_face))
            found_surfaces[start_pt] = current_surface
        return found_surfaces


def test_sample():
    assert len(DIRECTIONS) == 6
    sample = Blob(SAMPLE)
    assert sample.total_boundry_volume() == 845  # for just 1 layer only 35
    assert sample.total_surface_area() == 64
    surfaces = sample.find_boundry()
    assert {pt: len(s) for pt, s in surfaces.items()} == {
        Pt(x=-5, y=2, z=2): 844,
        Pt(x=2, y=2, z=5): 1,
    }
    assert sample.find_surfaces_on_layer(surfaces[Pt(x=-5, y=2, z=2)]) == 58


def test_my_blob():
    my_blob = Blob(MY_INPUT)
    assert my_blob.total_surface_area() == 4302
    surfaces = my_blob.find_boundry()
    assert {pt: len(s) for pt, s in surfaces.items() if len(s) > 2000} == {
        Pt(x=-6, y=9, z=9): 9813,
    }
    assert my_blob.find_surfaces_on_layer(surfaces[Pt(x=-6, y=9, z=9)]) == 2492
