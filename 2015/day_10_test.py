def look_say(look):
    """
    --- Day 10: Elves Look, Elves Say ---
    Today, the Elves are playing a game called look-and-say. They take turns making sequences by reading aloud the
    previous sequence and using that reading as the next sequence. For example, 211 is read as "one two, two ones",
    which becomes 1221 (1 2, 2 1s).

    Look-and-say sequences are generated iteratively, using the previous value as input for the next step.
    For each step, take the previous value, and replace each run of digits (like 111) with the number of digits (3)
    followed by the digit itself (1).

    For example:

    1 becomes 11 (1 copy of digit 1).
    11 becomes 21 (2 copies of digit 1).
    21 becomes 1211 (one 2 followed by one 1).
    1211 becomes 111221 (one 1, one 2, and two 1s).
    111221 becomes 312211 (three 1s, two 2s, and one 1).
    Starting with the digits in your puzzle input, apply this process 40 times. What is the length of the result?

    Your puzzle answer was 492982.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    Neat, right? You might also enjoy hearing John Conway talking about this sequence
    (that's Conway of Conway's Game of Life fame).

    Now, starting again with the digits in your puzzle input, apply this process 50 times.
    What is the length of the new result?

    Your puzzle input is still 1321131112.
    """

    look = str(look)
    last = look[0]
    count = 1
    say = ''
    for c in look[1:]:
        if c == last:
            count += 1
        else:
            say += str(count) + last
            last = c
            count = 1
    say += str(count) + last
    return say

def repeat(n,loops=40):
    for i in range(loops):
        n = look_say(n)
    return len(str(n))

def test_look_say():
    assert look_say('1') == '11'
    assert look_say('11') == '21'
    assert look_say('21') == '1211'
    assert look_say('1211') == '111221'
    assert repeat('1',4) == 6
    assert repeat('1321131112') == 492982
    assert repeat('1321131112',50) == 6989950
