from typing import NamedTuple
from tqdm import tqdm


class Puzzle:
    """
    --- Day 15: Beacon Exclusion Zone ---

    You feel the ground rumble again as the distress signal leads you to a large
    network of subterranean tunnels. You don't have time to search them all, but
    you don't need to: your pack contains a set of deployable sensors that you
    imagine were originally built to locate lost Elves.

    The sensors aren't very powerful, but that's okay; your handheld device
    indicates that you're close enough to the source of the distress signal to
    use them. You pull the emergency sensor system out of your pack, hit the big
    button on top, and the sensors zoom off down the tunnels.

    Once a sensor finds a spot it thinks will give it a good reading, it
    attaches itself to a hard surface and begins monitoring for the nearest
    signal source beacon. Sensors and beacons always exist at integer
    coordinates. Each sensor knows its own position and can determine the
    position of a beacon precisely; however, sensors can only lock on to the one
    beacon closest to the sensor as measured by the Manhattan distance. (There
    is never a tie where two beacons are the same distance to a sensor.)

    It doesn't take long for the sensors to report back their positions and
    closest beacons (your puzzle input). For example:

    Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    Sensor at x=9, y=16: closest beacon is at x=10, y=16
    Sensor at x=13, y=2: closest beacon is at x=15, y=3
    Sensor at x=12, y=14: closest beacon is at x=10, y=16
    Sensor at x=10, y=20: closest beacon is at x=10, y=16
    Sensor at x=14, y=17: closest beacon is at x=10, y=16
    Sensor at x=8, y=7: closest beacon is at x=2, y=10
    Sensor at x=2, y=0: closest beacon is at x=2, y=10
    Sensor at x=0, y=11: closest beacon is at x=2, y=10
    Sensor at x=20, y=14: closest beacon is at x=25, y=17
    Sensor at x=17, y=20: closest beacon is at x=21, y=22
    Sensor at x=16, y=7: closest beacon is at x=15, y=3
    Sensor at x=14, y=3: closest beacon is at x=15, y=3
    Sensor at x=20, y=1: closest beacon is at x=15, y=3

    So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For
    the sensor at 9,16, the closest beacon to it is at 10,16.

    Drawing sensors as S and beacons as B, the above arrangement of sensors and
    beacons looks like this:

                1    1    2    2
        0    5    0    5    0    5
    0 ....S.......................
    1 ......................S.....
    2 ...............S............
    3 ................SB..........
    4 ............................
    5 ............................
    6 ............................
    7 ..........S.......S.........
    8 ............................
    9 ............................
    10 ....B.......................
    11 ..S.........................
    12 ............................
    13 ............................
    14 ..............S.......S.....
    15 B...........................
    16 ...........SB...............
    17 ................S..........B
    18 ....S.......................
    19 ............................
    20 ............S......S........
    21 ............................
    22 .......................B....

    This isn't necessarily a comprehensive map of all beacons in the area,
    though. Because each sensor only identifies its closest beacon, if a sensor
    detects a beacon, you know there are no other beacons that close or closer
    to that sensor. There could still be beacons that just happen to not be the
    closest beacon to any sensor. Consider the sensor at 8,7:

                1    1    2    2
        0    5    0    5    0    5
    -2 ..........#.................
    -1 .........###................
    0 ....S...#####...............
    1 .......#######........S.....
    2 ......#########S............
    3 .....###########SB..........
    4 ....#############...........
    5 ...###############..........
    6 ..#################.........
    7 .#########S#######S#........
    8 ..#################.........
    9 ...###############..........
    10 ....B############...........
    11 ..S..###########............
    12 ......#########.............
    13 .......#######..............
    14 ........#####.S.......S.....
    15 B........###................
    16 ..........#SB...............
    17 ................S..........B
    18 ....S.......................
    19 ............................
    20 ............S......S........
    21 ............................
    22 .......................B....

    This sensor's closest beacon is at 2,10, and so you know there are no
    beacons that close or closer (in any positions marked #).

    None of the detected beacons seem to be producing the distress signal, so
    you'll need to work out where the distress beacon is by working out where it
    isn't. For now, keep things simple by counting the positions where a beacon
    cannot possibly be along just a single row.

    So, suppose you have an arrangement of beacons and sensors like in the
    example above and, just in the row where y=10, you'd like to count the
    number of positions a beacon cannot possibly exist. The coverage from all
    sensors near that row looks like this:

                    1    1    2    2
        0    5    0    5    0    5
    9 ...#########################...
    10 ..####B######################..
    11 .###S#############.###########.

    In this example, in the row where y=10, there are 26 positions where a
    beacon cannot be present.

    Consult the report from the sensors you just deployed. In the row where
    y=2000000, how many positions cannot contain a beacon?

    --- Part Two ---
    Your handheld device indicates that the distress signal is coming from a
    beacon nearby. The distress beacon is not detected by any sensor, but the
    distress beacon must have x and y coordinates each no lower than 0 and no
    larger than 4000000.

    To isolate the distress beacon's signal, you need to determine its tuning
    frequency, which can be found by multiplying its x coordinate by 4000000 and
    then adding its y coordinate.

    In the example above, the search space is smaller: instead, the x and y
    coordinates can each be at most 20. With this reduced search area, there is
    only a single position that could have a beacon: x=14, y=11. The tuning
    frequency for this distress beacon is 56000011.

    Find the only possible position for the distress beacon. What is its tuning
    frequency?

    """


SAMPLE = [
    "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
    "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
    "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
    "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
    "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
    "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
    "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
    "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
    "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
    "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
    "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
    "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
    "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
    "Sensor at x=20, y=1: closest beacon is at x=15, y=3",
]


with open("day_15_input.txt") as fp:
    MY_INPUT = [line.strip() for line in fp]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class C(NamedTuple):
    x: int
    y: int
    r: int

    def intersection(self, other):
        points = set()
        center_dist = Pt(self.x, self.y).dist(Pt(other.x, other.y))
        if center_dist > self.r + other.r:
            return points
        if center_dist < abs(other.r - self.r):
            return points
        if self.r < other.r:
            small, big = self, other
        else:
            big, small = self, other
        big_center = Pt(x=big.x, y=big.y)
        for y in range(small.y - small.r, small.y + small.r + 1):
            dx = small.r - abs(y - small.y)
            for pt in [Pt(small.x - dx, y), Pt(small.x + dx, y)]:
                if big_center.dist(pt) == big.r:
                    points.add(pt)
        return points

    def edge(self):
        pt_on_edge = set()
        for y in range(self.y - self.r, self.y + self.r + 1):
            dx = self.r - abs(y - self.y)
            pt_on_edge.add(Pt(self.x - dx, y))
            pt_on_edge.add(Pt(self.x + dx, y))
        return pt_on_edge

    def inner(self):
        pt_in_circle = set()
        for y in range(self.y - self.r, self.y + self.r + 1):
            dx = self.r - abs(y - self.y)
            for x in range(self.x - dx, self.x + 1 + dx):
                pt_in_circle.add(Pt(x, y))
        return pt_in_circle


class SensorGrid:
    def __init__(self, readings, fast=False) -> None:
        self.sensors_with_beacons = dict()
        self.sensors_ranges = dict()
        self.beacons = set()
        self.not_beacon = set()
        for reading in readings:
            # sample reading
            # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
            sx, sy, bx, by = [
                int(eq.split("=")[1])
                for eq in reading.replace(",", "").replace(":", "").split(" ")
                if eq.count("=")
            ]
            sensor_pt = Pt(x=sx, y=sy)
            nearest_beacon = Pt(x=bx, y=by)
            self.sensors_with_beacons[sensor_pt] = nearest_beacon
            self.sensors_ranges[sensor_pt] = sensor_pt.dist(nearest_beacon)
            self.beacons.add(nearest_beacon)
            if not fast:
                clear_range = sensor_pt.dist(nearest_beacon)
                sensor = C(x=sensor_pt.x, y=sensor_pt.y, r=clear_range)
                self.not_beacon = self.not_beacon.union(sensor.inner())

    def is_not_beacon(self, pt, primary_sensor):
        if (
            primary_sensor is not None
            and pt.dist(primary_sensor) <= self.sensors_ranges[primary_sensor]
        ):
            return True, primary_sensor
        for sensor_pt, r in self.sensors_ranges.items():
            if sensor_pt.dist(pt) <= r:
                return True, sensor_pt
        return False, None

    def check_row(self, y, x_min=None, x_max=None, stop_at_possible=False):
        if x_min is None or x_max is None:
            max_radius = max(self.sensors_ranges.values())
        if x_min is None:
            x_min = min(pt.x for pt in self.sensors_ranges) - max_radius - 1
        if x_max is None:
            x_max = max(pt.x for pt in self.sensors_ranges) + max_radius + 1
        clear_pts = 0
        primary_sensor = None
        for x in range(x_min, x_max + 1):
            test_pt = Pt(x, y)
            if test_pt in self.beacons:
                continue
            is_not_beacon, primary_sensor = self.is_not_beacon(test_pt, primary_sensor)
            if is_not_beacon:
                clear_pts += 1
            if stop_at_possible and not is_not_beacon:
                return test_pt
        if stop_at_possible:
            return None
        return clear_pts

    def check_grid(self, x_min=0, x_max=20, y_min=0, y_max=20):
        for y in tqdm(range(y_min, y_max + 1)):
            found = self.check_row(y, x_min=x_min, x_max=x_max, stop_at_possible=True)
            if found is not None:
                return found

    def check_set(self, test_set, x_min=0, x_max=20, y_min=0, y_max=20):
        for pt in tqdm(test_set):
            if x_min <= pt.x <= x_max and y_min <= pt.y <= y_max:
                inside = False
                for sensor_pt, r in self.sensors_ranges.items():
                    if sensor_pt.dist(pt) <= r:
                        inside = True
                        break
                if inside is False:
                    return pt

    def check_boundry(self, x_min=0, x_max=20, y_min=0, y_max=20):
        boundry = set()
        for sensor_pt, r in tqdm(self.sensors_ranges.items()):
            sensor = C(x=sensor_pt.x, y=sensor_pt.y, r=r + 1)
            boundry = boundry.union(sensor.edge())
        return self.check_set(boundry, x_min, x_max, y_min, y_max)

    def check_intersections(self, x_min=0, x_max=20, y_min=0, y_max=20):
        boundry = set()
        for sensor_pt1, r1 in tqdm(self.sensors_ranges.items()):
            for sensor_pt2, r2 in tqdm(self.sensors_ranges.items()):
                if sensor_pt1 == sensor_pt2:
                    continue
                sensor1 = C(x=sensor_pt1.x, y=sensor_pt1.y, r=r1 + 1)
                sensor2 = C(x=sensor_pt2.x, y=sensor_pt2.y, r=r2 + 1)
                boundry = boundry.union(sensor1.intersection(sensor2))
        return self.check_set(boundry, x_min, x_max, y_min, y_max)


def test_sensorgrid():
    assert C(x=0, y=0, r=0).inner() == {Pt(x=0, y=0)}
    assert C(x=0, y=0, r=1).inner() == {
        Pt(x=0, y=-1),
        Pt(x=-1, y=0),
        Pt(x=0, y=0),
        Pt(x=1, y=0),
        Pt(x=0, y=1),
    }
    assert C(x=0, y=0, r=1).edge() == {
        Pt(x=0, y=-1),
        Pt(x=-1, y=0),
        Pt(x=1, y=0),
        Pt(x=0, y=1),
    }
    assert len(C(x=0, y=0, r=2).inner()) == 13
    assert len(C(x=0, y=0, r=2).edge()) == 8
    sample = SensorGrid(SAMPLE)
    assert (
        sum(1 for pt in sample.not_beacon if pt.y == 10 and pt not in sample.beacons)
        == 26
    )
    # try again with a faster algorithm
    sample = SensorGrid(SAMPLE, fast=True)
    assert sample.check_row(y=10) == 26
    assert sample.check_grid() == Pt(14, 11)
    assert sample.check_boundry() == Pt(14, 11)
    assert sample.check_intersections() == Pt(14, 11)
    assert 4000000 * Pt(14, 11).x + Pt(14, 11).y == 56000011

    # full input requires faster algorithm - run rather pytest
    # my_input = SensorGrid(MY_INPUT, fast=True)
    # note x_min=108_898, x_max=3_955_070, max_r=1_997_803
    # assert my_input.check_row(y=2_000_000) == 5_525_847
    # assert my_input.check_grid(x_max=4_000_000, y_max=4_000_000) == Pt(x=0, y=0)
    # assert my_input.check_boundry(x_max=4_000_000, y_max=4_000_000) == Pt(x=0, y=0)
    # assert my_input.check_intersections() == Pt(14, 11)
    assert (
        4000000 * Pt(x=3335216, y=3187704).x + Pt(x=3335216, y=3187704).y
        == 13340867187704
    )


if __name__ == "__main__":
    my_input = SensorGrid(MY_INPUT, fast=True)
    result = my_input.check_intersections(x_max=4_000_000, y_max=4_000_000)
    print(f"result = {result}")  # result = Pt(x=3335216, y=3187704)
