import cmath
from numbers import Number
from fractions import Fraction
from operator import add, sub, mul, truediv

OP = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,  # Fraction or truediv or ifloordiv
}


class Puzzle:
    """
    --- Day 21: Monkey Math ---
    The monkeys are back! You're worried they're going to try to steal your
    stuff again, but it seems like they're just holding their ground and making
    various monkey noises at you.

    Eventually, one of the elephants realizes you don't speak monkey and comes
    over to interpret. As it turns out, they overheard you talking about trying
    to find the grove; they can show you a shortcut if you answer their riddle.

    Each monkey is given a job: either to yell a specific number or to yell the
    result of a math operation. All of the number-yelling monkeys know their
    number from the start; however, the math operation monkeys need to wait for
    two other monkeys to yell a number, and those two other monkeys might also
    be waiting on other monkeys.

    Your job is to work out the number the monkey named root will yell before
    the monkeys figure it out themselves.

    For example:

    root: pppw + sjmn
    dbpl: 5
    cczh: sllz + lgvd
    zczc: 2
    ptdq: humn - dvpt
    dvpt: 3
    lfqf: 4
    humn: 5
    ljgn: 2
    sjmn: drzm * dbpl
    sllz: 4
    pppw: cczh / lfqf
    lgvd: ljgn * ptdq
    drzm: hmdt - zczc
    hmdt: 32

    Each line contains the name of a monkey, a colon, and then the job of that
    monkey:

    A lone number means the monkey's job is simply to yell that number.

    A job like aaaa + bbbb means the monkey waits for monkeys aaaa and bbbb to
    yell each of their numbers; the monkey then yells the sum of those two
    numbers.

    aaaa - bbbb means the monkey yells aaaa's number minus bbbb's number.

    Job aaaa * bbbb will yell aaaa's number multiplied by bbbb's number.

    Job aaaa / bbbb will yell aaaa's number divided by bbbb's number.

    So, in the above example, monkey drzm has to wait for monkeys hmdt and zczc
    to yell their numbers. Fortunately, both hmdt and zczc have jobs that
    involve simply yelling a single number, so they do this immediately: 32 and
    2. Monkey drzm can then yell its number by finding 32 minus 2: 30.

    Then, monkey sjmn has one of its numbers (30, from monkey drzm), and already
    has its other number, 5, from dbpl. This allows it to yell its own number by
    finding 30 multiplied by 5: 150.

    This process continues until root yells a number: 152.

    However, your actual situation involves considerably more monkeys. What
    number will the monkey named root yell?

    Your puzzle answer was 155708040358220.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    Due to some kind of monkey-elephant-human mistranslation, you seem to have
    misunderstood a few key details about the riddle.

    First, you got the wrong job for the monkey named root; specifically, you
    got the wrong math operation. The correct operation for monkey root should
    be =, which means that it still listens for two numbers (from the same two
    monkeys as before), but now checks that the two numbers match.

    Second, you got the wrong monkey for the job starting with humn:. It isn't a
    monkey - it's you. Actually, you got the job wrong, too: you need to figure
    out what number you need to yell so that root's equality check passes. (The
    number that appears after humn: in your input is now irrelevant.)

    In the above example, the number you need to yell to pass root's equality
    test is 301. (This causes root to get the same number, 150, from both of its
    monkeys.)

    What number do you yell to pass root's equality test?
    """


SAMPLE = {
    "root": "pppw + sjmn",
    "dbpl": "5",
    "cczh": "sllz + lgvd",
    "zczc": "2",
    "ptdq": "humn - dvpt",
    "dvpt": "3",
    "lfqf": "4",
    "humn": "5",
    "ljgn": "2",
    "sjmn": "drzm * dbpl",
    "sllz": "4",
    "pppw": "cczh / lfqf",
    "lgvd": "ljgn * ptdq",
    "drzm": "hmdt - zczc",
    "hmdt": "32",
}


with open("day_21_input.txt") as fp:
    MY_INPUT = {}
    for ln in fp:
        key, value = ln.strip().split(": ")
        MY_INPUT[key] = value


class MonkeyMath:
    def __init__(self, values, fix_root=False) -> None:
        known = {}
        for key, value in values.items():
            if value.count(" ") == 0:
                known[key] = int(value)

        if fix_root:
            # known["humn"] = (0, 1)
            known["humn"] = 0 + 1j
            self.left, _, self.right = values["root"].split(" ")
            calc_next = [{self.left, self.right}]
        else:
            calc_next = [{"root"}]
        while calc_next:
            boundry = calc_next[-1]
            next_layer = set()
            for node in boundry:
                if node in known:
                    continue
                x_key, op, y_key = values[node].split(" ")
                if x_key in known and y_key in known:
                    x = known[x_key]
                    y = known[y_key]
                    if isinstance(x, Number) and isinstance(y, Number):
                        known[node] = OP[op](x, y)
                        continue
                    # if y is number
                    if (
                        isinstance(x, tuple)
                        and isinstance(y, Number)
                        and op in {"+", "-"}
                    ):
                        known[node] = (OP[op](x[0], y), x[1])
                        continue
                    if (
                        isinstance(x, tuple)
                        and isinstance(y, Number)
                        and op in {"*", "/"}
                    ):
                        known[node] = (OP[op](x[0], y), OP[op](x[1], y))
                        continue
                    # if x is number
                    if (
                        isinstance(x, Number)
                        and isinstance(y, tuple)
                        and op in {"+", "-"}
                    ):
                        known[node] = (OP[op](x, y[0]), y[1])
                        continue
                    if isinstance(x, Number) and isinstance(y, tuple) and op == "*":
                        known[node] = (x * y[0], x * y[1])
                        continue
                    known[node] = f"({x}{op}{y})"
                    continue
                if x_key not in known:
                    next_layer.add(x_key)
                if y_key not in known:
                    next_layer.add(y_key)
            if next_layer:
                calc_next.append(next_layer)
            else:
                calc_next.pop()
        self.values = values
        self.known = known


def test_sample():
    sample = MonkeyMath(SAMPLE)
    assert sample.known["root"] == 152
    sample = MonkeyMath(SAMPLE, fix_root=True)
    assert sample.known[sample.left] == (-0.5 + 0.5j)  
    # ((4+(2*((0, 1)-3)))/4) = (-0.5, 0.5)
    assert sample.known[sample.right] == 150
    assert (150 + 0.5) / 0.5 == 301


def test_my_input():
    my_input = MonkeyMath(MY_INPUT)
    assert my_input.known["root"] == 155708040358220.0
    my_input = MonkeyMath(MY_INPUT, fix_root=True)
    assert my_input.known[my_input.left] == (107542057559298.95-17.765806210250652j)
    # (Fraction(95819973285335362, 891), Fraction(47488, 2673))
    assert my_input.known[my_input.right] == 48165982835110
    assert (
        Fraction(48165982835110 * 891 * 2673 - 95819973285335362 * 2673, 47488)
        == -2977859937970467
    ) # -2977859937970467 is not right answer
