from heapq import heappush, heappop
from collections import defaultdict
from typing import NamedTuple


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)


class Puzzle:
    """
--- Day 23: Amphipod ---

A group of amphipods notice your fancy submarine and flag you down. "With such an impressive shell," one amphipod
says, "surely you can help us with a question that has stumped our best scientists."

They go on to explain that a group of timid, stubborn amphipods live in a nearby burrow. Four types of amphipods
live there: Amber (A), Bronze (B), Copper (C), and Desert (D). They live in a burrow that consists of a hallway
and four side rooms. The side rooms are initially full of amphipods, and the hallway is initially empty.

They give you a diagram of the situation (your puzzle input), including locations of each
amphipod (A, B, C, or D, each of which is occupying an otherwise open space), walls (#),
and open space (.).

For example:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

The amphipods would like a method to organize every amphipod into side rooms so that each side room contains
one type of amphipod and the types are sorted A-D going left to right, like this:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########

Amphipods can move up, down, left, or right so long as they are moving into an unoccupied open space. Each
type of amphipod requires a different amount of energy to move one step:
- Amber amphipods require 1 energy per step,
- Bronze amphipods require 10 energy,
- Copper amphipods require 100,
- and Desert ones require 1000.
The amphipods would like you to find a way to organize the amphipods that requires the least total energy.

However, because they are timid and stubborn, the amphipods have some extra rules:

- Amphipods will never stop on the space immediately outside any room. They can move into that space so long
  as they immediately continue moving. (Specifically, this refers to the four open spaces in the hallway that
  are directly above an amphipod starting position.)

- Amphipods will never move from the hallway into a room unless that room is their destination room and that
  room contains no amphipods which do not also have that room as their own destination. If an amphipod's starting
  room is not its destination room, it can stay in that room until it leaves the room. (For example, an Amber
  amphipod will not move from the hallway into the right three rooms, and will only move into the leftmost
  room if that room is empty or if it only contains other Amber amphipods.)

- Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room. (That is,
  once any amphipod starts moving, any other amphipods currently in the hallway are locked in place and will not
  move again until they can move fully into a room.)

In the above example, the amphipods can be organized using a minimum of 12521 energy. One way to do this is
shown below.

Starting configuration:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

One Bronze amphipod moves into the hallway, taking 4 steps and using 40 energy:

#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########

The only Copper amphipod not in its side room moves there, taking 4 steps and using 400 energy:

#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########

A Desert amphipod moves out of the way, taking 3 steps and using 3000 energy, and then the
Bronze amphipod takes its place, taking 3 steps and using 30 energy:

#############
#.....D.....#
###B#.#C#D###
  #A#B#C#A#
  #########

The leftmost Bronze amphipod moves to its room using 40 energy:

#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########

Both amphipods in the rightmost room move into the hallway, using 2003 energy in total:

#############
#.....D.D.A.#
###.#B#C#.###
  #A#B#C#.#
  #########

Both Desert amphipods move into the rightmost room using 7000 energy:

#############
#.........A.#
###.#B#C#D###
  #A#B#C#D#
  #########

Finally, the last Amber amphipod moves into its room, using 8 energy:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########

What is the least energy required to organize the amphipods?

To begin, get your puzzle input.

--- Part Two ---
As you prepare to give the amphipods your solution, you notice that the diagram they handed you was actually
folded up. As you unfold it, you discover an extra part of the diagram.

Between the first and second lines of text that contain amphipod starting positions, insert the following lines:

  #D#C#B#A#
  #D#B#A#C#

So, the above example now becomes:

#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

The amphipods still want to be organized into rooms similar to before:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

In this updated example, the least energy required to organize these amphipods is 44169:

#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#..........D#
###B#C#B#.###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A.........D#
###B#C#B#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A........BD#
###B#C#.#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A......B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#.#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#C#.#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA...B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#D#C#A#
  #########

#############
#AA.D.B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#.#C#A#
  #########

#############
#AA.D...B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#B#C#A#
  #########

#############
#AA.D.....BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#.#.###
  #D#B#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#A#
  #########

#############
#AA.D.....AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#.#
  #########

#############
#AA.......AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #.#B#C#.#
  #D#B#C#D#
  #A#B#C#D#
  #########

#############
#AA.D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #A#B#C#D#
  #########

#############
#A..D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...D.....AD#
###.#B#C#.###
  #A#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.........AD#
###.#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

Using the initial configuration from the full diagram, what is the least energy required to organize the amphipods?
    """


RAW_SAMPLE = '''
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########'''

RAW_INPUT = '''
#############
#...........#
###C#A#B#D###
  #D#C#A#B#
  #########'''

RAW_TARGET = '''
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########'''

RAW_SAMPLE2 = '''
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########'''

RAW_INPUT2 = '''
#############
#...........#
###C#A#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #D#C#A#B#
  #########'''

RAW_TARGET2 = '''
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########'''


class Rooms:
    def __init__(self, raw_input):
        self.map = dict()
        self.energy_cost = {'.': 0,
                            'A': 1,
                            'B': 10,
                            'C': 100,
                            'D': 1000}
        for y, line in enumerate(raw_input.split('\n')[2:]):
            for x, c in enumerate(line):
                self.map[Pt(x, y)] = c

    @staticmethod
    def hash_state(state):
        return frozenset([f'{p.x},{p.y}={c}' for p, c in state.items()])

    def find_possible_moves(self, state, valid_final, valid_hall, locked_spaces):
        moves = []
        delta = [Pt(1, 0), Pt(0, 1), Pt(-1, 0), Pt(0, -1)]
        for p, c in state.items():
            if c == '.':  # non-move
                continue
            if p in locked_spaces:
                continue
            to_check = [(p, 0)]
            potential_move = dict()
            while len(to_check) > 0:
                tp, cost = to_check.pop()
                for d in delta:
                    np = tp + d
                    nc = cost + self.energy_cost[c]
                    if np in state and state[np] == '.' and np not in potential_move:
                        to_check.append((np, nc))
                        potential_move[np] = nc
            for np, cost in potential_move.items():
                if (np in valid_hall and p not in valid_hall) or np in valid_final[c]:
                    new_state = {tp: c if tp == np else '.' if tp == p else tc for tp, tc in state.items()}
                    new_locked_spaces = locked_spaces.copy()
                    if np in valid_final[c]:
                        if np + Pt(0, 1) in valid_final[c] and state[np + Pt(0, 1)] != c:
                            continue
                        new_locked_spaces.add(np)
                    moves.append((f'{c}({cost}):{p.x},{p.y}->{np.x},{np.y}', cost, new_state, new_locked_spaces))
        return moves

    def solve(self, raw_end_state, states_to_watch=None):
        end_state, valid_final, valid_hall = self.parse_end_state(raw_end_state)

        frontier = []
        visited = dict()
        skipped = 0

        start = {p: c for p, c in self.map.items() if c in self.energy_cost}
        locked_spaces = Rooms.check_initial_locks(start, valid_final)
        visited[Rooms.hash_state(start)] = 0
        heappush(frontier, (0, [], start, locked_spaces))

        while frontier:
            energy, hx, state, locked_spaces = heappop(frontier)
            if states_to_watch is not None:
                if state in states_to_watch:
                    print(energy, hx, state)
            if state == end_state:
                return energy
            next_moves = self.find_possible_moves(state, valid_final, valid_hall, locked_spaces)
            for description, delta_energy, new_state, new_locked_spaces in next_moves:
                new_state_hash = Rooms.hash_state(new_state)
                new_energy = energy + delta_energy
                if new_state_hash in visited:
                    old_energy = visited[new_state_hash]
                    if new_energy >= old_energy:  # this should ALWAYS be the case but somehow is not?
                        skipped += 1
                        continue
                visited[new_state_hash] = new_energy
                heappush(frontier, (new_energy, hx + [description], new_state, new_locked_spaces))

    def parse_end_state(self, raw_end_state):
        end_state = {}
        valid_final = defaultdict(set)
        valid_hall = set()
        for y, line in enumerate(raw_end_state.split('\n')[2:]):
            for x, c in enumerate(line):
                if y > 0 and c == '#' and Pt(x, y - 1) in end_state and end_state[Pt(x, y - 1)] == '.':
                    valid_hall.add(Pt(x, y - 1))
                elif c in self.energy_cost:
                    end_state[Pt(x, y)] = c
                    if self.energy_cost[c] > 0:
                        valid_final[c].add(Pt(x, y))
        return end_state, valid_final, valid_hall

    @staticmethod
    def check_initial_locks(start, valid_final):
        locked_spaces = set()
        for c in valid_final:
            for p in valid_final[c]:
                if start[p] == c:
                    if p + Pt(0, 1) not in valid_final[c]:
                        locked_spaces.add(p)
                    elif start[p + Pt(0, 1)] == 'c':
                        locked_spaces.add(p)
        return locked_spaces


def test_sample_find_moves():
    sample = Rooms(RAW_SAMPLE)
    assert sample.solve(RAW_TARGET) == 12521


def test_my_find_moves():
    my_game = Rooms(RAW_INPUT)
    assert my_game.solve(RAW_TARGET) == 15358


def test_sample2_find_moves():
    sample = Rooms(RAW_SAMPLE2)
    assert sample.solve(RAW_TARGET2) == 44169


def test_my2_find_moves():
    my_game = Rooms(RAW_INPUT2)
    assert my_game.solve(RAW_TARGET2) == 51436
