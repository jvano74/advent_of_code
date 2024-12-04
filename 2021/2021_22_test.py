from pathlib import Path
from typing import NamedTuple


class Puzzle:
    """
    --- Day 22: Reactor Reboot ---

    Operating at these extreme ocean depths has overloaded the submarine's reactor; it needs to be rebooted.

    The reactor core is made up of a large 3-dimensional grid made up entirely of cubes, one cube per integer
    3-dimensional coordinate (x,y,z). Each cube can be either on or off; at the start of the reboot process,
    they are all off. (Could it be an old model of a reactor you've seen before?)

    To reboot the reactor, you just need to set all of the cubes to either on or off by following a list of
    reboot steps (your puzzle input). Each step specifies a cuboid (the set of all cubes that have coordinates
    which fall within ranges for x, y, and z) and whether to turn all of the cubes in that cuboid on or off.

    For example, given these reboot steps:

    on x=10..12,y=10..12,z=10..12
    on x=11..13,y=11..13,z=11..13
    off x=9..11,y=9..11,z=9..11
    on x=10..10,y=10..10,z=10..10

    The first step (on x=10..12,y=10..12,z=10..12) turns on a 3x3x3 cuboid consisting of 27 cubes:

    10,10,10
    10,10,11
    10,10,12
    10,11,10
    10,11,11
    10,11,12
    10,12,10
    10,12,11
    10,12,12
    11,10,10
    11,10,11
    11,10,12
    11,11,10
    11,11,11
    11,11,12
    11,12,10
    11,12,11
    11,12,12
    12,10,10
    12,10,11
    12,10,12
    12,11,10
    12,11,11
    12,11,12
    12,12,10
    12,12,11
    12,12,12

    The second step (on x=11..13,y=11..13,z=11..13) turns on a 3x3x3 cuboid that overlaps with the first.
    As a result, only 19 additional cubes turn on; the rest are already on from the previous step:

    11,11,13
    11,12,13
    11,13,11
    11,13,12
    11,13,13
    12,11,13
    12,12,13
    12,13,11
    12,13,12
    12,13,13
    13,11,11
    13,11,12
    13,11,13
    13,12,11
    13,12,12
    13,12,13
    13,13,11
    13,13,12
    13,13,13

    The third step (off x=9..11,y=9..11,z=9..11) turns off a 3x3x3 cuboid that overlaps partially with
    some cubes that are on, ultimately turning off 8 cubes:

    10,10,10
    10,10,11
    10,11,10
    10,11,11
    11,10,10
    11,10,11
    11,11,10
    11,11,11

    The final step (on x=10..10,y=10..10,z=10..10) turns on a single cube, 10,10,10. After this last
    step, 39 cubes are on.

    The initialization procedure only uses cubes that have x, y, and z positions of at least -50 and
    at most 50. For now, ignore cubes outside this region.

    Here is a larger example:

    on x=-20..26,y=-36..17,z=-47..7
    on x=-20..33,y=-21..23,z=-26..28
    on x=-22..28,y=-29..23,z=-38..16
    on x=-46..7,y=-6..46,z=-50..-1
    on x=-49..1,y=-3..46,z=-24..28
    on x=2..47,y=-22..22,z=-23..27
    on x=-27..23,y=-28..26,z=-21..29
    on x=-39..5,y=-6..47,z=-3..44
    on x=-30..21,y=-8..43,z=-13..34
    on x=-22..26,y=-27..20,z=-29..19
    off x=-48..-32,y=26..41,z=-47..-37
    on x=-12..35,y=6..50,z=-50..-2
    off x=-48..-32,y=-32..-16,z=-15..-5
    on x=-18..26,y=-33..15,z=-7..46
    off x=-40..-22,y=-38..-28,z=23..41
    on x=-16..35,y=-41..10,z=-47..6
    off x=-32..-23,y=11..30,z=-14..3
    on x=-49..-5,y=-3..45,z=-29..18
    off x=18..30,y=-20..-8,z=-3..13
    on x=-41..9,y=-7..43,z=-33..15
    on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
    on x=967..23432,y=45373..81175,z=27513..53682

    The last two steps are fully outside the initialization procedure area; all other steps are fully
    within it. After executing these steps in the initialization procedure region, 590784 cubes are on.

    Execute the reboot steps. Afterward, considering only cubes in the region x=-50..50,y=-50..50,z=-50..50,
    how many cubes are on?

    To begin, get your puzzle input.

    --- Part Two ---

    Now that the initialization procedure is complete, you can reboot the reactor.

    Starting with all cubes off, run all of the reboot steps for all cubes in the reactor.

    Consider the following reboot steps:

    on x=-5..47,y=-31..22,z=-19..33
    on x=-44..5,y=-27..21,z=-14..35
    on x=-49..-1,y=-11..42,z=-10..38
    on x=-20..34,y=-40..6,z=-44..1
    off x=26..39,y=40..50,z=-2..11
    on x=-41..5,y=-41..6,z=-36..8
    off x=-43..-33,y=-45..-28,z=7..25
    on x=-33..15,y=-32..19,z=-34..11
    off x=35..47,y=-46..-34,z=-11..5
    on x=-14..36,y=-6..44,z=-16..29
    on x=-57795..-6158,y=29564..72030,z=20435..90618
    on x=36731..105352,y=-21140..28532,z=16094..90401
    on x=30999..107136,y=-53464..15513,z=8553..71215
    on x=13528..83982,y=-99403..-27377,z=-24141..23996
    on x=-72682..-12347,y=18159..111354,z=7391..80950
    on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
    on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
    on x=-52752..22273,y=-49450..9096,z=54442..119054
    on x=-29982..40483,y=-108474..-28371,z=-24328..38471
    on x=-4958..62750,y=40422..118853,z=-7672..65583
    on x=55694..108686,y=-43367..46958,z=-26781..48729
    on x=-98497..-18186,y=-63569..3412,z=1232..88485
    on x=-726..56291,y=-62629..13224,z=18033..85226
    on x=-110886..-34664,y=-81338..-8658,z=8914..63723
    on x=-55829..24974,y=-16897..54165,z=-121762..-28058
    on x=-65152..-11147,y=22489..91432,z=-58782..1780
    on x=-120100..-32970,y=-46592..27473,z=-11695..61039
    on x=-18631..37533,y=-124565..-50804,z=-35667..28308
    on x=-57817..18248,y=49321..117703,z=5745..55881
    on x=14781..98692,y=-1341..70827,z=15753..70151
    on x=-34419..55919,y=-19626..40991,z=39015..114138
    on x=-60785..11593,y=-56135..2999,z=-95368..-26915
    on x=-32178..58085,y=17647..101866,z=-91405..-8878
    on x=-53655..12091,y=50097..105568,z=-75335..-4862
    on x=-111166..-40997,y=-71714..2688,z=5609..50954
    on x=-16602..70118,y=-98693..-44401,z=5197..76897
    on x=16383..101554,y=4615..83635,z=-44907..18747
    off x=-95822..-15171,y=-19987..48940,z=10804..104439
    on x=-89813..-14614,y=16069..88491,z=-3297..45228
    on x=41075..99376,y=-20427..49978,z=-52012..13762
    on x=-21330..50085,y=-17944..62733,z=-112280..-30197
    on x=-16478..35915,y=36008..118594,z=-7885..47086
    off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
    off x=2032..69770,y=-71013..4824,z=7471..94418
    on x=43670..120875,y=-42068..12382,z=-24787..38892
    off x=37514..111226,y=-45862..25743,z=-16714..54663
    off x=25699..97951,y=-30668..59918,z=-15349..69697
    off x=-44271..17935,y=-9516..60759,z=49131..112598
    on x=-61695..-5813,y=40978..94975,z=8655..80240
    off x=-101086..-9439,y=-7088..67543,z=33935..83858
    off x=18020..114017,y=-48931..32606,z=21474..89843
    off x=-77139..10506,y=-89994..-18797,z=-80..59318
    off x=8476..79288,y=-75520..11602,z=-96624..-24783
    on x=-47488..-1262,y=24338..100707,z=16292..72967
    off x=-84341..13987,y=2429..92914,z=-90671..-1318
    off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
    off x=-27365..46395,y=31009..98017,z=15428..76570
    off x=-70369..-16548,y=22648..78696,z=-1892..86821
    on x=-53470..21291,y=-120233..-33476,z=-44150..38147
    off x=-93533..-4276,y=-16170..68771,z=-104985..-24507

    After running the above reboot steps, 2758514936282235 cubes are on.
    (Just for fun, 474140 of those are also in the initialization procedure region.)

    Starting again with all cubes off, execute all reboot steps. Afterward, considering all cubes,
    how many cubes are on?

    """


with open(Path(__file__).parent / "2021_22_input.txt") as fp:
    INPUTS = [line.strip() for line in fp]

SMALL_SAMPLE = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""".split(
    "\n"
)


SAMPLE = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".split(
    "\n"
)

SAMPLE2 = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507""".split(
    "\n"
)


class Pt(NamedTuple):
    x: int
    y: int
    z: int

    def max(self):
        return max(abs(self.x), abs(self.y), abs(self.z))


class Box(NamedTuple):
    min_pt: Pt
    max_pt: Pt

    def size(self):
        return (
            (self.max_pt.x - self.min_pt.x)
            * (self.max_pt.y - self.min_pt.y)
            * (self.max_pt.z - self.min_pt.z)
        )

    def contains_pt(self, pt):
        return (
            self.min_pt.x <= pt.x < self.max_pt.x
            and self.min_pt.y <= pt.y < self.max_pt.y
            and self.min_pt.z <= pt.z < self.max_pt.z
        )

    def overlap(self, other):
        if self.min_pt.x >= other.max_pt.x:
            return False
        if other.min_pt.x >= self.max_pt.x:
            return False
        if self.min_pt.y >= other.max_pt.y:
            return False
        if other.min_pt.y >= self.max_pt.y:
            return False
        if self.min_pt.z >= other.max_pt.z:
            return False
        if other.min_pt.z >= self.max_pt.z:
            return False
        return True

    def union(self, other):
        x_axis = list({self.min_pt.x, self.max_pt.x, other.min_pt.x, other.max_pt.x})
        x_axis.sort()
        y_axis = list({self.min_pt.y, self.max_pt.y, other.min_pt.y, other.max_pt.y})
        y_axis.sort()
        z_axis = list({self.min_pt.z, self.max_pt.z, other.min_pt.z, other.max_pt.z})
        z_axis.sort()

        extra_bits = []
        x_last, y_last, z_last = None, None, None
        for zi, z in enumerate(z_axis):
            if zi == 0:
                z_last = z
                continue
            for yi, y in enumerate(y_axis):
                if yi == 0:
                    y_last = y
                    continue
                for xi, x in enumerate(x_axis):
                    if xi == 0:
                        x_last = x
                        continue
                    min_pt = Pt(x_last, y_last, z_last)
                    max_pt = Pt(x, y, z)
                    if other.contains_pt(min_pt) and not self.contains_pt(min_pt):
                        extra_bits.append(Box(min_pt, max_pt))
                    x_last = x
                y_last = y
            z_last = z
        return extra_bits


def test_box_size():
    assert Box(Pt(0, 3, 5), Pt(2, 4, 8)).size() == 6


def test_box_contains_pt():
    assert Box(Pt(-2, -2, -2), Pt(3, 3, 3)).contains_pt(Pt(0, 0, 0)) is True
    assert Box(Pt(0, 3, 7), Pt(2, 4, 8)).contains_pt(Pt(1, 3, 7)) is True
    assert Box(Pt(0, 3, 7), Pt(2, 4, 8)).contains_pt(Pt(2, 3, 7)) is False
    assert Box(Pt(0, 3, 7), Pt(2, 4, 8)).contains_pt(Pt(-1, 3, 7)) is False


def test_box_overlap():
    assert (
        Box(Pt(-2, -2, -2), Pt(3, 3, 3)).overlap(Box(Pt(-1, -1, -1), Pt(2, 2, 2)))
        is True
    )
    assert Box(Pt(0, 3, 7), Pt(2, 4, 8)).overlap(Box(Pt(1, 3, 7), Pt(4, 4, 8))) is True
    assert Box(Pt(0, 3, 7), Pt(2, 4, 8)).overlap(Box(Pt(1, 3, 3), Pt(4, 4, 4))) is False
    assert Box(Pt(0, 3, 7), Pt(2, 4, 8)).overlap(Box(Pt(2, 3, 3), Pt(4, 4, 4))) is False
    assert (
        Box(Pt(0, 3, 7), Pt(2, 4, 8)).overlap(Box(Pt(-1, -3, -7), Pt(0, 0, 0))) is False
    )


def test_box_union():
    assert Box(Pt(0, 3, 7), Pt(2, 4, 8)).union(Box(Pt(1, 3, 7), Pt(4, 4, 8))) == [
        Box(Pt(2, 3, 7), Pt(4, 4, 8))
    ]
    assert Box(Pt(0, 3, 7), Pt(2, 4, 8)).union(Box(Pt(1, 3, 3), Pt(4, 4, 4))) == [
        Box(Pt(1, 3, 3), Pt(2, 4, 4)),
        Box(Pt(2, 3, 3), Pt(4, 4, 4)),
    ]
    assert (
        Box(Pt(-2, -2, -2), Pt(3, 3, 3)).union(Box(Pt(-1, -1, -1), Pt(2, 2, 2))) == []
    )
    assert Box(Pt(-1, -1, -1), Pt(2, 2, 2)).union(Box(Pt(-2, -2, -2), Pt(3, 3, 3))) == [
        Box(Pt(-2, -2, -2), Pt(-1, -1, -1)),
        Box(Pt(-1, -2, -2), Pt(2, -1, -1)),
        Box(Pt(2, -2, -2), Pt(3, -1, -1)),
        Box(Pt(-2, -1, -2), Pt(-1, 2, -1)),
        Box(Pt(-1, -1, -2), Pt(2, 2, -1)),
        Box(Pt(2, -1, -2), Pt(3, 2, -1)),
        Box(Pt(-2, 2, -2), Pt(-1, 3, -1)),
        Box(Pt(-1, 2, -2), Pt(2, 3, -1)),
        Box(Pt(2, 2, -2), Pt(3, 3, -1)),
        Box(Pt(-2, -2, -1), Pt(-1, -1, 2)),
        Box(Pt(-1, -2, -1), Pt(2, -1, 2)),
        Box(Pt(2, -2, -1), Pt(3, -1, 2)),
        Box(Pt(-2, -1, -1), Pt(-1, 2, 2)),
        Box(Pt(2, -1, -1), Pt(3, 2, 2)),
        Box(Pt(-2, 2, -1), Pt(-1, 3, 2)),
        Box(Pt(-1, 2, -1), Pt(2, 3, 2)),
        Box(Pt(2, 2, -1), Pt(3, 3, 2)),
        Box(Pt(-2, -2, 2), Pt(-1, -1, 3)),
        Box(Pt(-1, -2, 2), Pt(2, -1, 3)),
        Box(Pt(2, -2, 2), Pt(3, -1, 3)),
        Box(Pt(-2, -1, 2), Pt(-1, 2, 3)),
        Box(Pt(-1, -1, 2), Pt(2, 2, 3)),
        Box(Pt(2, -1, 2), Pt(3, 2, 3)),
        Box(Pt(-2, 2, 2), Pt(-1, 3, 3)),
        Box(Pt(-1, 2, 2), Pt(2, 3, 3)),
        Box(Pt(2, 2, 2), Pt(3, 3, 3)),
    ]


class Board:
    def __init__(self, initial_lines, max_range=None):
        self.instructions = []
        self.grid = dict()

        if max_range is not None:
            bounding_box = Box(
                Pt(-max_range, -max_range, -max_range),
                Pt(max_range + 1, max_range + 1, max_range + 1),
            )
        else:
            bounding_box = None

        for line in initial_lines:
            state, region = line.split(" ")

            raw_x, raw_y, raw_z = region.split(",")
            x_range = [int(n) for n in raw_x[2:].split("..")]
            y_range = [int(n) for n in raw_y[2:].split("..")]
            z_range = [int(n) for n in raw_z[2:].split("..")]

            self.instructions.append(
                (
                    state,
                    Box(
                        Pt(x_range[0], y_range[0], z_range[0]),
                        Pt(x_range[1] + 1, y_range[1] + 1, z_range[1] + 1),
                    ),
                )
            )

        for state, next_box in self.instructions:
            if bounding_box is not None and not bounding_box.overlap(next_box):
                continue

            if state == "on":
                boxes_to_add = [next_box]
                while len(boxes_to_add) > 0:
                    inserting_box = boxes_to_add.pop()
                    bits = None
                    for pt, box in self.grid.items():
                        if inserting_box.overlap(box):
                            bits = box.union(inserting_box)
                            boxes_to_add.extend(bits)
                            break
                    if bits is None:
                        self.grid[inserting_box.min_pt] = inserting_box
            elif state == "off":
                box_to_remove = next_box
                next_pass = list(self.grid.items())
                for pt, box in next_pass:
                    if box_to_remove.overlap(box):
                        new_bits = box_to_remove.union(box)
                        del self.grid[pt]
                        for nb in new_bits:
                            self.grid[nb.min_pt] = nb

    def total(self):
        total = 0
        for box in self.grid.values():
            total += box.size()
        return total


def test_board():
    small_board = Board(SMALL_SAMPLE, 50)
    assert small_board.total() == 39
    sample_board = Board(SAMPLE, 50)
    assert sample_board.total() == 590784
    sample2_board = Board(SAMPLE2)
    assert sample2_board.total() == 2758514936282235


def test_game_board():
    game_board = Board(INPUTS, 50)
    assert game_board.total() == 611378


def test_second_part_with_game_board():
    game_board = Board(INPUTS)
    assert game_board.total() == 1214313344725528
