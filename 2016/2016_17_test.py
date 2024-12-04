import hashlib
import re
from typing import NamedTuple
from queue import PriorityQueue


class Puzzle:
    """
    --- Day 17: Two Steps Forward ---
    You're trying to access a secure vault protected by a 4x4 grid of small rooms connected by doors. You start in
    the top-left room (marked S), and you can access the vault (marked V) once you reach the bottom-right room:

    #########
    #S| | | #
    #-#-#-#-#
    # | | | #
    #-#-#-#-#
    # | | | #
    #-#-#-#-#
    # | | |
    ####### V

    Fixed walls are marked with #, and doors are marked with - or |.

    The doors in your current room are either open or closed (and locked) based on the hexadecimal MD5 hash of
    a passcode (your puzzle input) followed by a sequence of uppercase characters representing the path you have
    taken so far (U for up, D for down, L for left, and R for right).

    Only the first four characters of the hash are used; they represent, respectively, the doors up, down, left,
    and right from your current position. Any b, c, d, e, or f means that the corresponding door is open; any
    other character (any number or a) means that the corresponding door is closed and locked.

    To access the vault, all you need to do is reach the bottom-right room; reaching this room opens the vault
    and all doors in the maze.

    For example, suppose the passcode is hijkl. Initially, you have taken no steps, and so your path is empty:
    you simply find the MD5 hash of hijkl alone. The first four characters of this hash are ced9, which indicate
    that up is open (c), down is open (e), left is open (d), and right is closed and locked (9). Because you start
    in the top-left corner, there are no "up" or "left" doors to be open, so your only choice is down.

    Next, having gone only one step (down, or D), you find the hash of hijklD. This produces f2bc, which indicates
    that you can go back up, left (but that's a wall), or right. Going right means hashing hijklDR to get 5745
    - all doors closed and locked. However, going up instead is worthwhile: even though it returns you to the
    room you started in, your path would then be DU, opening a different set of doors.

    After going DU (and then hashing hijklDU to get 528e), only the right door is open; after going DUR, all
    doors lock. (Fortunately, your actual passcode is not hijkl).

    Passcodes actually used by Easter Bunny Vault Security do allow access to the vault if you know the right
    path. For example:

    If your passcode were ihgpwlah, the shortest path would be DDRRRD.
    With kglvqrro, the shortest path would be DDUDRLRRUDRD.
    With ulqzkmiv, the shortest would be DRURDRUDDLLDLUURRDULRLDUUDDDRR.
    Given your vault's passcode, what is the shortest path (the actual path, not just the length) to reach the vault?

    Your puzzle input is gdjjyniy.

    --- Part Two ---
    You're curious how robust this security solution really is, and so you decide to find longer and longer paths
    which still provide access to the vault. You remember that paths always end the first time they reach the
    bottom-right room (that is, they can never pass through it, only end in it).

    For example:

    If your passcode were ihgpwlah, the longest path would take 370 steps.
    With kglvqrro, the longest path would be 492 steps long.
    With ulqzkmiv, the longest path would be 830 steps long.
    What is the length of the longest path that reaches the vault?
    """
    pass


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def up(self):
        return Pt(self.x, self.y - 1)

    def down(self):
        return Pt(self.x, self.y + 1)

    def left(self):
        return Pt(self.x - 1, self.y)

    def right(self):
        return Pt(self.x + 1, self.y)


class Maze:
    def __init__(self, passcode, longest=False):
        self.passcode = passcode
        self.max = Pt(3, 3)
        self.longest = longest

    def open_doors(self, pt, path_str):
        doors = set()
        # path_str = ''.join(path)
        hv = hashlib.md5(f'{self.passcode}{path_str}'.encode('utf-8')).hexdigest()
        if re.match(r'[b-f]', hv[0]) and 0 < pt.y:
            doors.add(('U', pt.up()))
        if re.match(r'[b-f]', hv[1]) and pt.y < self.max.y:
            doors.add(('D', pt.down()))
        if re.match(r'[b-f]', hv[2]) and 0 < pt.x:
            doors.add(('L', pt.left()))
        if re.match(r'[b-f]', hv[3]) and pt.x < self.max.x:
            doors.add(('R', pt.right()))
        return doors

    def find_path(self, start, end, max_distance=None):
        boundary = PriorityQueue()
        history = set()
        long_paths = set()

        boundary.put((0, start, ''))
        history.add('')

        while not boundary.empty():  # ARG! another bug in syntax for stopping condition tripped me up.
            distance, pt, path = boundary.get()
            if max_distance is not None and distance > max_distance:
                break
            if pt == end:
                if not self.longest:
                    return path
                long_paths.add(distance)
            else:
                doors = self.open_doors(pt, path)
                for direction, new_pt in doors:
                    new_path = f'{path}{direction}'
                    # if new_path not in history:  # don't need to track history as everything in here shorter
                    boundary.put((distance + 1, new_pt, new_path))
        return max(long_paths)


def test_sample_maze():
    sample_maze = Maze('hijkl')
    assert sample_maze.open_doors(Pt(0, 0), '') == {('D', Pt(0, 1))}
    sample_maze = Maze('ihgpwlah')
    assert sample_maze.find_path(Pt(0, 0), Pt(3, 3)) == 'DDRRRD'
    sample_maze = Maze('kglvqrro')
    assert sample_maze.find_path(Pt(0, 0), Pt(3, 3)) == 'DDUDRLRRUDRD'
    sample_maze = Maze('ulqzkmiv')
    assert sample_maze.find_path(Pt(0, 0), Pt(3, 3)) == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'


def test_puzzle_maze():
    puzzle_maze = Maze('gdjjyniy')
    assert puzzle_maze.find_path(Pt(0, 0), Pt(3, 3)) == 'DUDDRLRRRD'


def test_sample_maze2():
    sample_maze = Maze('ihgpwlah', longest=True)
    assert sample_maze.find_path(Pt(0, 0), Pt(3, 3)) == 370
    sample_maze = Maze('kglvqrro', longest=True)
    assert sample_maze.find_path(Pt(0, 0), Pt(3, 3)) == 492
    sample_maze = Maze('ulqzkmiv', longest=True)
    assert sample_maze.find_path(Pt(0, 0), Pt(3, 3)) == 830


def test_puzzle_maze2():
    puzzle_maze = Maze('gdjjyniy', longest=True)
    assert puzzle_maze.find_path(Pt(0, 0), Pt(3, 3)) == 578
