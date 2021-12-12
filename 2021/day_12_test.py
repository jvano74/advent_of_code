from collections import defaultdict, deque


class Puzzle:
    """
--- Day 12: Passage Pathing ---

With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting
out of this cave anytime soon is by finding a path yourself. Not just a path - the only way to
know if you've found the best path is to find all of them.

Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining
caves (your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end

This is a list of how all of the caves are connected. You start in the cave named start, and
your destination is the cave named end. An entry like b-d means that cave b is connected to
cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
   \\   /
     end

Your goal is to find the number of distinct paths that start at start, end at end,
and don't visit small caves more than once. There are two types of caves: big caves
(written in uppercase, like A) and small caves (written in lowercase, like b). It
would be a waste of time to visit any small cave more than once, but big caves are
large enough that it might be worth visiting them multiple times. So, all paths you
find should visit small caves at most once, and can visit big caves any number
of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end

(Each line in the above list corresponds to a single path; the caves visited by that path are
listed in the order they are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so, cave b would
need to be visited twice (once on the way to cave d and a second time when returning from cave d),
and since cave b is small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc

The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end

Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW

How many paths through this cave system are there that visit small caves at most once?

To begin, get your puzzle input.

--- Part Two ---
After reviewing the available paths, you realize you might have time to visit a single
small cave twice. Specifically, big caves can be visited any number of times, a single
small cave can be visited at most twice, and the remaining small caves can be visited
at most once. However, the caves named start and end can only be visited exactly once
each: once you leave the start cave, you may not return to it, and once you reach the
end cave, the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end

The slightly larger example above now has 103 paths through it,
and the even larger example now has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?

    """


SAMPLE1 = ['start-A', 'start-b', 'A-c', 'A-b', 'b-d', 'A-end', 'b-end']

SAMPLE2 = ['dc-end', 'HN-start', 'start-kj', 'dc-start', 'dc-HN',
           'LN-dc', 'HN-end', 'kj-sa', 'kj-HN', 'kj-dc']

SAMPLE3 = ['fs-end', 'he-DX', 'fs-he', 'start-DX', 'pj-DX', 'end-zg', 'zg-sl',
           'zg-pj', 'pj-he', 'RW-he', 'fs-DX', 'pj-RW', 'zg-RW', 'start-pj',
           'he-WI', 'zg-he', 'pj-fs', 'start-RW']

INPUT = ['EG-bj', 'LN-end', 'bj-LN', 'yv-start', 'iw-ch', 'ch-LN',
         'EG-bn', 'OF-iw', 'LN-yv', 'iw-TQ', 'iw-start', 'TQ-ch',
         'EG-end', 'bj-OF', 'OF-end', 'TQ-start', 'TQ-bj', 'iw-LN',
         'EG-ch', 'yv-iw', 'KW-bj', 'OF-ch', 'bj-ch', 'yv-TQ']


class Maze:
    def __init__(self, connections):
        self.room = defaultdict(set)
        for c in connections:
            a, b = c.split('-')
            self.room[a].add(b)
            self.room[b].add(a)

    def find_paths(self, extra_time=False):
        possible_routes = set()
        frontier = deque()
        frontier.append(('start', extra_time, ['start']))
        while frontier:
            pos, extra_time, path_hx = frontier.popleft()
            for nn in self.room[pos]:
                path_time = extra_time
                if nn == nn.upper():
                    can_visit = True
                elif nn not in path_hx:
                    can_visit = True
                elif path_time and nn != 'start':
                    can_visit = True
                    path_time = False
                else:
                    can_visit = False

                if can_visit:
                    if nn == 'end':
                        possible_routes.add(','.join(path_hx + [nn]))
                    else:
                        frontier.append((nn, path_time, path_hx + [nn]))

        return possible_routes


def test_sample1_maze():
    sample1_maze = Maze(SAMPLE1)
    assert sample1_maze.find_paths() == {
        'start,A,end',  # ok
        'start,A,c,A,end',  # ok
        'start,A,b,A,end',  #
        'start,A,b,A,c,A,end',  #
        'start,A,b,end',  #
        'start,A,c,A,b,A,end',  #
        'start,A,c,A,b,end',  #
        'start,b,end',  # ok
        'start,b,A,end',  # ok
        'start,b,A,c,A,end',  #
    }
    assert len(sample1_maze.find_paths()) == 10
    assert len(sample1_maze.find_paths(True)) == 36


def test_sample2_maze():
    sample2_maze = Maze(SAMPLE2)
    assert len(sample2_maze.find_paths()) == 19
    assert len(sample2_maze.find_paths(True)) == 103


def test_sample3_maze():
    sample3_maze = Maze(SAMPLE3)
    assert len(sample3_maze.find_paths()) == 226
    assert len(sample3_maze.find_paths(True)) == 3509


def test_input_maze():
    my_maze = Maze(INPUT)
    assert len(my_maze.find_paths()) == 4659
    assert len(my_maze.find_paths(True)) == 148962
