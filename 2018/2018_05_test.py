from pathlib import Path


class Puzzle:
    """
    --- Day 5: Alchemical Reduction ---
    You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress,
    but are still struggling with the suit's size reduction capabilities.

    While the very latest in 1518 alchemical technology might have solved their problem eventually, you can
    do better. You scan the chemical composition of the suit's material and discover that it is formed by
    extremely long polymers (one of which is available as your puzzle input).

    The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent
    units of the same type and opposite polarity are destroyed. Units' types are represented by letters;
    units' polarity is represented by capitalization. For instance, r and R are units with the same type
    but opposite polarity, whereas r and s are entirely different types and do not react.

    For example:

    In aA, a and A react, leaving nothing behind.

    In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.

    In abAB, no two adjacent units are of the same type, and so nothing happens.

    In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.

    Now, consider a larger example, dabAcCaCBAcCcaDA:

    dabAcCaCBAcCcaDA  The first 'cC' is removed.
    dabAaCBAcCcaDA    This creates 'Aa', which is removed.
    dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
    dabCBAcaDA        No further actions can be taken.

    After all possible reactions, the resulting polymer contains 10 units.

    How many units remain after fully reacting the polymer you scanned? (Note: in this puzzle and others,
    the input is large; if you copy/paste your input, make sure you get the whole thing.)

    --- Part Two ---
    Time to improve the polymer.

    One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should.
    Your goal is to figure out which unit type is causing the most problems, remove all instances of it
    (regardless of polarity), fully react the remaining polymer, and measure its length.

    For example, again using the polymer dabAcCaCBAcCcaDA from above:

    Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
    Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
    Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
    Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.
    In this example, removing all C/c units was best, producing the answer 4.

    What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully
    reacting the result?
    """

    pass


SAMPLE = "dabAcCaCBAcCcaDA"

with open(Path(__file__).parent / "2018_05_input.txt") as fp:
    INPUT = fp.read().strip()


def react(a, b):
    if a == b:
        return False
    if a.upper() == b:
        return True
    if a == b.upper():
        return True
    return False


def reduce(orig):
    new_string = []
    reduced = False
    for element in orig:
        if len(new_string) > 0 and react(new_string[-1], element):
            new_string = new_string[:-1]
            reduced = True
        else:
            new_string.append(element)
    if reduced:
        return reduce(new_string)
    return new_string


def test_reduce():
    assert "".join(reduce(SAMPLE)) == "dabCBAcaDA"
    assert len(reduce(INPUT)) == 10598


def modify(orig):
    removal_units = set([a.upper() for a in orig])
    test_cases = {
        a: orig.replace(a.upper(), "").replace(a.lower(), "") for a in removal_units
    }
    print(f"test cases = {len(test_cases)}")
    results = {case: reduce(data) for case, data in test_cases.items()}
    return min([len(data) for (r, data) in results.items()])


def test_modify():
    assert modify(SAMPLE) == 4
    assert modify(INPUT) == 5312
