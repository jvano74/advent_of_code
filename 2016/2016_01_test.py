from pathlib import Path
import pytest


class Problem:
    """
    --- Day 1: No Time for a Taxicab ---
    Santa's sleigh uses a very high-precision clock to guide its movements, and
    the clock's oscillator is regulated by stars. Unfortunately, the stars have
    been stolen... by the Easter Bunny. To save Christmas, Santa needs you to
    retrieve all fifty stars by December 25th.

    Collect stars by solving puzzles. Two puzzles will be made available on each
    day in the Advent calendar; the second puzzle is unlocked when you complete
    the first. Each puzzle grants one star. Good luck!

    You're airdropped near Easter Bunny Headquarters in a city somewhere.
    "Near", unfortunately, is as close as you can get - the instructions on the
    Easter Bunny Recruiting Document the Elves intercepted start here, and
    nobody had time to work them out further.

    The Document indicates that you should start at the given coordinates (where
    you just landed) and face North. Then, follow the provided sequence: either
    turn left (L) or right (R) 90 degrees, then walk forward the given number of
    blocks, ending at a new intersection.

    There's no time to follow such ridiculous instructions on foot, though, so
    you take a moment and work out the destination. Given that you can only walk
    on the street grid of the city, how far is the shortest path to the
    destination?

    For example:

    Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks
    away. R2, R2, R2 leaves you 2 blocks due South of your starting position,
    which is 2 blocks away. R5, L5, R5, R3 leaves you 12 blocks away.

    How many blocks away is Easter Bunny HQ?

    --- Part Two ---
    Then, you notice the instructions continue on the back of the Recruiting
    Document. Easter Bunny HQ is actually at the first location you visit twice.

    For example, if your instructions are R8, R4, R4, R8, the first location you
    visit twice is 4 blocks away, due East.

    How many blocks away is the first location you visit twice?
    """

    pass


with open(Path(__file__).parent / "2016_01_input.txt") as f:
    for line in f:
        INPUTS = line.strip().split(", ")


def navigate(directions, check_overlap=False):
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    orientation = 0
    x, y = (0, 0)
    walked = {(x, y)}
    for step in directions:
        if step[0] == "L":
            orientation -= 1
        elif step[0] == "R":
            orientation += 1
        dx, dy = deltas[orientation % 4]
        if check_overlap:
            for _ in range(int(step[1:])):
                x += dx
                y += dy
                if (x, y) in walked:
                    return abs(x) + abs(y)
                walked.add((x, y))
        else:
            x += dx * int(step[1:])
            y += dy * int(step[1:])
    if check_overlap:
        raise Exception("Lost", "Path never crossed")
    return abs(x) + abs(y)


def test_inputs():
    assert navigate(["R2", "L3"]) == 5
    assert navigate(["R2", "R2", "R2"]) == 2
    assert navigate(["R5", "L5", "R5", "R3"]) == 12
    assert navigate(INPUTS) == 298

    with pytest.raises(Exception):
        assert navigate(["R2", "L3"], True)
    assert navigate(["R8", "R4", "R4", "R8"], True) == 4
    assert navigate(INPUTS, True) == 158
