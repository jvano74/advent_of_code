from typing import NamedTuple
import re


class Puzzle:
    """
    --- Day 20: Particle Swarm ---
    Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't
    be able to finish them all in time to render the next frame at this rate.

    It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then
    particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's
    position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

    Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

    Increase the X velocity by the X acceleration.
    Increase the Y velocity by the Y acceleration.
    Increase the Z velocity by the Z acceleration.
    Increase the X position by the X velocity.
    Increase the Y position by the Y velocity.
    Increase the Z position by the Z velocity.

    Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay
    closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation
    is simply the sum of the absolute values of a particle's X, Y, and Z position.

    For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity).
    Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of
    current X positions (marked in parentheses), the following would take place:

    p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
    p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

    p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
    p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

    p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
    p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

    p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
    p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)

    At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run,
    particle 0 will stay closest.

    Which particle will stay closest to position <0,0,0> in the long term?

    --- Part Two ---
    To simplify the problem further, the GPU would like to remove any particles that collide. Particles collide if
    their positions ever exactly match. Because particles are updated simultaneously, more than two particles can
    collide at the same time and place. Once particles collide, they are removed and cannot collide with anything
    else after that tick.

    For example:

    p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
    p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
    p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
    p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

    p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>
    p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
    p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)
    p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

    p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>
    p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
    p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)
    p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

    ------destroyed by collision------
    ------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
    ------destroyed by collision------                      (3)
    p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>

    In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X. On the next
    tick, particle 3 passes through unharmed.

    How many particles are left after all collisions are resolved?
    """
    pass


with open('day_20_input.txt') as fp:
    INPUTS = [line.strip() for line in fp]


class Pt(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y, self.z - other.z)

    def scale(self, factor):
        return Pt(factor * self.x, factor * self.y, factor * self.z)

    def dot(self, other):
        return other.x * self.x + other.y * self.y + other.z * self.z

    def dist(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Ptc(NamedTuple):
    id: int
    p: Pt
    v: Pt
    a: Pt

    def tick(self):
        return Ptc(id=self.id,
                   p=self.p + self.v + self.a,
                   v=self.v + self.a,
                   a=self.a)


def test_pt_operations():
    assert Pt(1, 3, 1) + Pt(2, -1, 0) == Pt(3, 2, 1)
    assert Pt(1, 3, 3) - Pt(2, -1, 1) == Pt(-1, 4, 2)
    assert Pt(1, 3, -2).scale(2) == Pt(2, 6, -4)
    assert Pt(1, 3, 4).dot(Pt(3, -1, 0)) == 0


class Swarm:
    def __init__(self, raw_input):
        self.positions = {}
        self.min_acceleration = None
        # p=<-923,1506,2445>, v=<-131,215,346>, a=<9,-15,-26>
        pv = re.compile(r'p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>')
        particle_count = 0
        collisions = set()
        for spva in raw_input:
            matches = pv.match(spva)
            if matches:
                x, y, z, vx, vy, vz, ax, ay, az = matches.groups()
                ptc = Ptc(id=particle_count,
                          p=Pt(int(x), int(y), int(z)),
                          v=Pt(int(vx), int(vy), int(vz)),
                          a=Pt(int(ax), int(ay), int(az)))
                if self.min_acceleration is None:
                    self.min_acceleration = ptc.a.dist(), particle_count
                else:
                    self.min_acceleration = min(self.min_acceleration, (ptc.a.dist(), particle_count))
                if ptc.p in self.positions:
                    collisions.add(ptc.p)
                else:
                    self.positions[ptc.p] = ptc
                particle_count += 1
        for c in collisions:
            self.positions.pop(c)
        self.particle_count = [particle_count]
        self.particle_count.append(len(self.positions))

    def tick(self):
        next_step = [ptc.tick() for ptc in self.positions.values()]
        self.positions = {}
        collisions = set()
        for ptc in next_step:
            if ptc.p in self.positions:
                collisions.add(ptc.p)
            else:
                self.positions[ptc.p] = ptc
        for c in collisions:
            self.positions.pop(c)
        self.particle_count.append(len(self.positions))

    def run(self, min_collision_free_steps):
        collision_free_steps = 0
        while True:
            lst_count = self.particle_count[-1]
            self.tick()
            if lst_count == self.particle_count[-1]:
                collision_free_steps += 1
            else:
                collision_free_steps = 0
            if collision_free_steps > min_collision_free_steps:
                return lst_count


def test_swarm():
    swarm = Swarm(INPUTS)
    # the closest in the long term will have lowest acceleration regardless of any other items
    assert swarm.min_acceleration == (1, 150)
    assert swarm.run(100) == 657
