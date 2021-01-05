from typing import NamedTuple


class Puzzle:
    r"""
    --- Day 13: Mine Cart Madness ---
    A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on. The Elves
    are very busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with.

    Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, the Elves seem to
    be making this up as they go along. They haven't even figured out how to avoid collisions yet.

    You map out the tracks (your puzzle input) and see where you can help.

    Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). Curves connect exactly two
    perpendicular pieces of track; for example, this is a closed loop:

    /----\
    |    |
    |    |
    \----/
    Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left,
    turning right, or continuing straight. Here are two loops connected by two intersections:

    /-----\
    |     |
    |  /--+--\
    |  |  |  |
    \--+--/  |
       |     |
       \-----/
    Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On your
    initial map, the track under each cart is a straight path matching the direction the cart is facing.)

    Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes
    straight the second time, turns right the third time, and then repeats those directions starting again with left
    the fourth time, straight the fifth time, and so on. This process is independent of the particular intersection at
    which the cart has arrived - that is, the cart has no per-intersection memory.

    Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their
    current location: carts on the top row move first (acting from left to right), then carts on the second row move
    (again from left to right), then carts on the third row, and so on. Once each cart has moved one step, the process
    repeats; each of these loops is called a tick.

    For example, suppose there are two carts on a straight track:

    |  |  |  |  |
    v  |  |  |  |
    |  v  v  |  |
    |  |  |  v  X
    |  |  ^  ^  |
    ^  ^  |  |  |
    |  |  |  |  |

    First, the top cart moves. It is facing down (v), so it moves down one square. Second, the bottom cart moves.
    It is facing up (^), so it moves up one square. Because all carts have moved, the first tick ends. Then, the
    process repeats, starting with the first cart. The first cart moves down, then the second cart moves up - right
    into the first cart, colliding with it! (The location of the crash is marked with an X.) This ends the second
    and last tick.

    Here is a longer example:

    /->-\
    |   |  /----\
    | /-+--+-\  |
    | | |  | v  |
    \-+-/  \-+--/
      \------/

    /-->\
    |   |  /----\
    | /-+--+-\  |
    | | |  | |  |
    \-+-/  \->--/
      \------/

    /---v
    |   |  /----\
    | /-+--+-\  |
    | | |  | |  |
    \-+-/  \-+>-/
      \------/

    /---\
    |   v  /----\
    | /-+--+-\  |
    | | |  | |  |
    \-+-/  \-+->/
      \------/

    /---\
    |   |  /----\
    | /->--+-\  |
    | | |  | |  |
    \-+-/  \-+--^
      \------/

    /---\
    |   |  /----\
    | /-+>-+-\  |
    | | |  | |  ^
    \-+-/  \-+--/
      \------/

    /---\
    |   |  /----\
    | /-+->+-\  ^
    | | |  | |  |
    \-+-/  \-+--/
      \------/

    /---\
    |   |  /----<
    | /-+-->-\  |
    | | |  | |  |
    \-+-/  \-+--/
      \------/

    /---\
    |   |  /---<\
    | /-+--+>\  |
    | | |  | |  |
    \-+-/  \-+--/
      \------/

    /---\
    |   |  /--<-\
    | /-+--+-v  |
    | | |  | |  |
    \-+-/  \-+--/
      \------/

    /---\
    |   |  /-<--\
    | /-+--+-\  |
    | | |  | v  |
    \-+-/  \-+--/
      \------/

    /---\
    |   |  /<---\
    | /-+--+-\  |
    | | |  | |  |
    \-+-/  \-<--/
      \------/

    /---\
    |   |  v----\
    | /-+--+-\  |
    | | |  | |  |
    \-+-/  \<+--/
      \------/

    /---\
    |   |  /----\
    | /-+--v-\  |
    | | |  | |  |
    \-+-/  ^-+--/
      \------/

    /---\
    |   |  /----\
    | /-+--+-\  |
    | | |  X |  |
    \-+-/  \-+--/
      \------/

    After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd
    like to know the location of the first crash. Locations are given in X,Y coordinates, where the furthest left
    column is X=0 and the furthest top row is Y=0:

               111
     0123456789012
    0/---\
    1|   |  /----\
    2| /-+--+-\  |
    3| | |  X |  |
    4\-+-/  \-+--/
    5  \------/

    In this example, the location of the first crash is 7,3.

    --- Part Two ---

    There isn't much you can do to prevent crashes in this ridiculous system. However, by predicting the crashes, the
    Elves know where to be in advance and instantly remove the two crashing carts the moment any crash occurs.

    They can proceed like this for a while, but eventually, they're going to run out of carts. It could be useful to
    figure out where the last cart that hasn't crashed will end up.
    
    For example:
    
    />-<\
    |   |
    | /<+-\
    | | | v
    \>+</ |
      |   ^
      \<->/
    
    /---\
    |   |
    | v-+-\
    | | | |
    \-+-/ |
      |   |
      ^---^
    
    /---\
    |   |
    | /-+-\
    | v | |
    \-+-/ |
      ^   ^
      \---/
    
    /---\
    |   |
    | /-+-\
    | | | |
    \-+-/ ^
      |   |
      \---/
    After four very expensive crashes, a tick ends with only one cart remaining; its final location is 6,4.
    
    What is the location of the last cart at the end of the first tick where it is the only cart left?
    """
    pass


SAMPLE = ['/->-\\',
          '|   |  /----\\',
          '| /-+--+-\\  |',
          '| | |  | v  |',
          '\\-+-/  \\-+--/',
          '  \\------/']


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)


class Track:

    train_delta = {
        'v|': ('v', Pt(0, 1)),
        '^|': ('^', Pt(0, -1)),
        '>-': ('>', Pt(1, 0)),
        '<-': ('<', Pt(-1, 0)),

        'v/': ('<', Pt(-1, 0)),
        '^/': ('>', Pt(1, 0)),
        '>/': ('^', Pt(0, -1)),
        '</': ('v', Pt(0, 1)),

        'v\\': ('>', Pt(1, 0)),
        '^\\': ('<', Pt(-1, 0)),
        '>\\': ('v', Pt(0, 1)),
        '<\\': ('^', Pt(0, -1)),

        'vl': ('>', Pt(1, 0)),
        'vs': ('v', Pt(0, 1)),
        'vr': ('<', Pt(-1, 0)),

        '^l': ('<', Pt(-1, 0)),
        '^s': ('^', Pt(0, -1)),
        '^r': ('>', Pt(1, 0)),

        '>l': ('^', Pt(0, -1)),
        '>s': ('>', Pt(1, 0)),
        '>r': ('v', Pt(0, 1)),

        '<l': ('v', Pt(0, 1)),
        '<s': ('<', Pt(-1, 0)),
        '<r': ('^', Pt(0, -1)),

        'l': 's',
        's': 'r',
        'r': 'l',
    }

    def __init__(self, raw_lines):
        self.trains = {}
        self.track = {}
        self.x_max = 0
        self.y_max = 0
        self.time = 0
        self.train_time = 0

        for y, raw_line in enumerate(raw_lines):
            self.y_max = max(y, self.y_max)
            self.x_max = max(len(raw_line), self.x_max)
            for x, c in enumerate(raw_line):
                pt = Pt(x, y)
                if c in {'+', '|', '/', '-', '\\'}:
                    self.track[pt] = c
                elif c in {'^', 'v'}:
                    self.trains[pt] = (c, 'l')
                    self.track[pt] = '|'
                elif c in {'<', '>'}:
                    self.trains[pt] = (c, 'l')
                    self.track[pt] = '-'

    def print_track(self, show_trains=True, x_min=0, y_min=0, x_max=None, y_max=None):
        if y_max is None:
            y_max = self.y_max
        if x_max is None:
            x_max = self.x_max
        result = []
        for y in range(y_min, y_max + 1):
            line = [f'{y}'.rjust(3, '0')]
            for x in range(x_min, x_max + 1):
                pt = Pt(x, y)
                c = self.track[pt] if pt in self.track else ' '
                if show_trains and pt in self.trains:
                    c = self.trains[pt][0]
                line.append(c)
            result.append(''.join(line))
        return result

    def train_tick(self, train, loc):
        train_dir, train_mem = train
        if loc in self.track:
            track = self.track[loc]
        else:
            track = '?'
        train_track = f'{train_dir}{track}' if track != '+' else f'{train_dir}{train_mem}'
        if train_track not in self.train_delta:
            raise Exception(f'No delta for {train_track} at {loc}')
        new_train_dir, delta = self.train_delta[train_track]
        new_loc = loc + delta
        if track == '+':
            train_mem = self.train_delta[train_mem]
        return (new_train_dir, train_mem), new_loc

    def tick(self, remove_crashes=False):
        self.time += 1
        self.train_time = 0
        for train_loc in sorted(pt for pt in self.trains):
            if train_loc not in self.trains:
                pass  # crashed train
            else:
                train = self.trains.pop(train_loc)
                self.train_time += 1
                new_train, new_train_loc = self.train_tick(train, train_loc)
                if new_train_loc not in self.trains:
                    self.trains[new_train_loc] = new_train
                elif remove_crashes:
                    self.trains.pop(new_train_loc)  # remove collision
                    if len(self.trains) == 1:
                        return self.trains
                else:
                    return new_train_loc  # collision
        return None


def test_sample_track():
    track = Track(SAMPLE)
    result = track.tick()
    # print()
    while result is None:
        result = track.tick()
        # print('\n'.join(track.print_track()))
    assert result == Pt(7, 3)


with open('day_13_input.txt') as fp:
    INPUT = [line for line in fp]


def test_puzzle_track():
    track = Track(INPUT)
    # print()
    # print('\n'.join(track.print_track()))
    result = None
    while result is None:
        result = track.tick()
        # print()
        # print(f'{track.time}.{track.train_time}')
        # print('\n'.join(track.print_track()))
    assert result == Pt(108, 60)


def test_puzzle2_track():
    track = Track(INPUT)
    result = None
    while result is None:
        result = track.tick(remove_crashes=True)
    assert result == {Pt(x=92, y=42): ('<', 'l')}
