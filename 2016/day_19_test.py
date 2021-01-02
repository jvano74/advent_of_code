from collections import deque

class Puzzle:
    """
    --- Day 19: An Elephant Named Joseph ---
    The Elves contact you over a highly secure emergency channel. Back at the North Pole, the Elves are busy
    misunderstanding White Elephant parties.

    Each Elf brings a present. They all sit in a circle, numbered starting with position 1. Then, starting with
    the first Elf, they take turns stealing all the presents from the Elf to their left. An Elf with no presents
    is removed from the circle and does not take turns.

    For example, with five Elves (numbered 1 to 5):

      1
    5   2
     4 3

    Elf 1 takes Elf 2's present.
    Elf 2 has no presents and is skipped.
    Elf 3 takes Elf 4's present.
    Elf 4 has no presents and is also skipped.
    Elf 5 takes Elf 1's two presents.
    Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
    Elf 3 takes Elf 5's three presents.
    So, with five Elves, the Elf that sits starting in position 3 gets all the presents.

    With the number of Elves given in your puzzle input, which Elf gets all the presents?

    Your puzzle input is 3001330.

    --- Part Two ---
    Realizing the folly of their present-exchange rules, the Elves agree to instead steal presents from the Elf
    directly across the circle. If two Elves are across the circle, the one on the left (from the perspective of
    the stealer) is stolen from. The other rules remain unchanged: Elves with no presents are removed from the
    circle entirely, and the other elves move in slightly to keep the circle evenly spaced.

    For example, with five Elves (again numbered 1 to 5):

    The Elves sit in a circle; Elf 1 goes first:
      1
    5   2
     4 3

    Elves 3 and 4 are across the circle; Elf 3's present is stolen, being the one to the left. Elf 3 leaves the
    circle, and the rest of the Elves move in:

      1           1
    5   2  -->  5   2
     4 -          4

    Elf 2 steals from the Elf directly across the circle, Elf 5:
      1         1
    -   2  -->     2
      4         4

    Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:
     -          2
        2  -->
     4          4

    Finally, Elf 2 steals from Elf 4:
     2
        -->  2
     -

    So, with five Elves, the Elf that sits starting in position 2 gets all the presents.

    With the number of Elves given in your puzzle input, which Elf now gets all the presents?
    """
    pass


def winner(size):
    players = deque(1 + i for i in range(size))
    remaining_players = len(players)
    while remaining_players > 1:
        players.rotate(-1)
        players.popleft()
        remaining_players -= 1
    return players.popleft()


def winner_fast(size):
    next_player = [0 if i == 0 else i + 1 if i + 1 <= size else 1 for i in range(size+1)]
    prev_player = [0 if i == 0 else size if i == 1 else i - 1 for i in range(size+1)]
    current_player = 1
    target_player = next_player[current_player]
    while size > 1:
        # remove target_player
        next_player[prev_player[target_player]] = next_player[target_player]
        prev_player[next_player[target_player]] = prev_player[target_player]
        next_player[target_player] = 0
        prev_player[target_player] = 0
        size -= 1
        # next_player
        current_player = next_player[current_player]
        target_player = next_player[current_player]
    return current_player


def test_winner():
    # assert winner(5) == 3
    assert winner_fast(5) == 3
    # assert winner(3_001_330) == 1_808_357
    assert winner_fast(3_001_330) == 1_808_357


def winner2(size):
    players = deque(1 + i for i in range(size))
    remaining_players = len(players)
    while remaining_players > 1:
        other_players = remaining_players-1
        picked_player = other_players//2 + other_players % 2
        players.rotate(-picked_player)
        players.popleft()
        players.rotate(picked_player-1)
        remaining_players -= 1
    return players.popleft()


def winner2_fast(size):
    next_player = [0 if i == 0 else i + 1 if i + 1 <= size else 1 for i in range(size+1)]
    prev_player = [0 if i == 0 else size if i == 1 else i - 1 for i in range(size+1)]
    current_player = 1
    target_player = current_player + (size - 1) // 2 + ((size - 1) % 2)
    while size > 1:
        next_target = next_player[target_player]
        if size % 2 == 1:
            next_target = next_player[next_target]
        next_player[prev_player[target_player]] = next_player[target_player]
        prev_player[next_player[target_player]] = prev_player[target_player]
        next_player[target_player] = 0
        prev_player[target_player] = 0
        size -= 1
        # next_player
        current_player = next_player[current_player]
        target_player = next_target
    return current_player

def test_winner2():
    print()
    assert winner2(5) == 2
    assert winner2_fast(5) == 2
    assert winner2_fast(6) == 3
    # assert winner2(3_001_330) == 1_407_007  # this was not the fastest but I let it run and finally got 1407007
    assert winner2_fast(3_001_330) == 1_407_007  # faster linked list approach
