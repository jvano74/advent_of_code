from pathlib import Path


class Puzzle:
    """
    --- Day 25: Full of Hot Air ---
    As the expedition finally reaches the extraction point, several large hot
    air balloons drift down to meet you. Crews quickly start unloading the
    equipment the balloons brought: many hot air balloon kits, some fuel tanks,
    and a fuel heating machine.

    The fuel heating machine is a new addition to the process. When this
    mountain was a volcano, the ambient temperature was more reasonable; now,
    it's so cold that the fuel won't work at all without being warmed up first.

    The Elves, seemingly in an attempt to make the new machine feel welcome,
    have already attached a pair of googly eyes and started calling it "Bob".

    To heat the fuel, Bob needs to know the total amount of fuel that will be
    processed ahead of time so it can correctly calibrate heat output and flow
    rate. This amount is simply the sum of the fuel requirements of all of the
    hot air balloons, and those fuel requirements are even listed clearly on the
    side of each hot air balloon's burner.

    You assume the Elves will have no trouble adding up some numbers and are
    about to go back to figuring out which balloon is yours when you get a tap
    on the shoulder. Apparently, the fuel requirements use numbers written in a
    format the Elves don't recognize; predictably, they'd like your help
    deciphering them.

    You make a list of all of the fuel requirements (your puzzle input), but you
    don't recognize the number format either. For example:

    1=-0-2
    12111
    2=0=
    21
    2=01
    111
    20012
    112
    1=-1=
    1-12
    12
    1=
    122

    Fortunately, Bob is labeled with a support phone number. Not to be deterred,
    you call and ask for help.

    "That's right, just supply the fuel amount to the-- oh, for more than one
    burner? No problem, you just need to add together our Special
    Numeral-Analogue Fuel Units. Patent pending! They're way better than normal
    numbers for--"

    You mention that it's quite cold up here and ask if they can skip ahead.

    "Okay, our Special Numeral-Analogue Fuel Units - SNAFU for short - are sort
    of like normal numbers. You know how starting on the right, normal numbers
    have a ones place, a tens place, a hundreds place, and so on, where the
    digit in each place tells you how many of that value you have?"

    "SNAFU works the same way, except it uses powers of five instead of ten.
    Starting from the right, you have a ones place, a fives place, a
    twenty-fives place, a one-hundred-and-twenty-fives place, and so on. It's
    that easy!"

    You ask why some of the digits look like - or = instead of "digits".

    "You know, I never did ask the engineers why they did that. Instead of using
    digits four through zero, the digits are 2, 1, 0, minus (written -), and
    double-minus (written =). Minus is worth -1, and double-minus is worth -2."

    "So, because ten (in normal numbers) is two fives and no ones, in SNAFU it
    is written 20. Since eight (in normal numbers) is two fives minus two ones,
    it is written 2=."

    "You can do it the other direction, too. Say you have the SNAFU number
    2=-01. That's 2 in the 625s place, = (double-minus) in the 125s place, -
    (minus) in the 25s place, 0 in the 5s place, and 1 in the 1s place. (2 times
    625) plus (-2 times 125) plus (-1 times 25) plus (0 times 5) plus (1 times
    1). That's 1250 plus -250 plus -25 plus 0 plus 1. 976!"

    "I see here that you're connected via our premium uplink service, so I'll
    transmit our handy SNAFU brochure to you now. Did you need anything else?"

    You ask if the fuel will even work in these temperatures.

    "Wait, it's how cold? There's no way the fuel - or any fuel - would work in
    those conditions! There are only a few places in the-- where did you say you
    are again?"

    Just then, you notice one of the Elves pour a few drops from a
    snowflake-shaped container into one of the fuel tanks, thank the support
    representative for their time, and disconnect the call.

    The SNAFU brochure contains a few more examples of decimal ("normal")
    numbers and their SNAFU counterparts:

    Decimal          SNAFU
            1              1
            2              2
            3             1=
            4             1-
            5             10
            6             11
            7             12
            8             2=
            9             2-
        10             20
        15            1=0
        20            1-0
        2022         1=11-2
        12345        1-0---0
    314159265  1121-1110-1=0

    Based on this process, the SNAFU numbers in the example above can be
    converted to decimal numbers as follows:

    SNAFU  Decimal
    1=-0-2     1747
    12111      906
    2=0=      198
        21       11
    2=01      201
    111       31
    20012     1257
    112       32
    1=-1=      353
    1-12      107
        12        7
        1=        3
    122       37

    In decimal, the sum of these numbers is 4890.

    As you go to input this number on Bob's console, you discover that some
    buttons you expected are missing. Instead, you are met with buttons labeled
    =, -, 0, 1, and 2. Bob needs the input value expressed as a SNAFU number,
    not in decimal.

    Reversing the process, you can determine that for the decimal number 4890,
    the SNAFU number you need to supply to Bob's console is 2=-1=0.

    The Elves are starting to get cold. What SNAFU number do you supply to Bob's
    console?

    Your puzzle answer was 2-==10--=-0101==1201.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The hot air balloons quickly carry you to the North Pole. As soon as you
    land, most of the expedition is escorted directly to a small building
    attached to the reindeer stables.

    The head smoothie chef has just finished warming up the industrial-grade
    smoothie blender as you arrive. It will take 50 stars to fill the blender.
    The expedition Elves turn their attention to you, and you begin emptying the
    fruit from your pack onto the table.

    As you do, a very young Elf - one you recognize from the expedition team -
    approaches the table and holds up a single star fruit he found. The head
    smoothie chef places it in the blender.

    Only 49 stars to go.

    You have enough stars to Start The Blender.

    You make a smoothie with all fifty stars and deliver it to the reindeer! The
    sleigh is already warmed up by the time they finish eating.

    Congratulations! You've finished every puzzle in Advent of Code 2022! I hope
    you had as much fun solving them as I had making them for you. I'd love to
    hear about your adventure; you can get in touch with me via contact info on
    my website or through Twitter.

    If you'd like to see more things like this in the future, please consider
    supporting Advent of Code and sharing it with others.

    To hear about future projects, you can follow me on Twitter.

    I've highlighted the easter eggs in each puzzle, just in case you missed
    any. Hover your mouse over them, and the easter egg will appear.

    You can [Share] this moment with your friends, or [Go Check on Your
    Calendar].

    """


TEST_MATRIX = {
    "1=-0-2": 1747,
    "12111": 906,
    "2=0=": 198,
    "21": 11,
    "2=01": 201,
    "111": 31,
    "20012": 1257,
    "112": 32,
    "1=-1=": 353,
    "1-12": 107,
    "12": 7,
    "1=": 3,
    "122": 37,
}


SAMPLE = TEST_MATRIX.keys()


with open(Path(__file__).parent / "2022_25_input.txt") as fp:
    MY_INPUT = [line.strip() for line in fp]


def snafu_to_decimal(raw: str) -> int:
    total = 0
    pow = 1
    for digit in reversed(raw):
        match digit:
            case "=":
                total += -2 * pow
            case "-":
                total += -1 * pow
            case "0":
                total += 0 * pow
            case "1":
                total += 1 * pow
            case "2":
                total += 2 * pow
            case _:
                raise Exception("Invalid digit")
        pow *= 5
    return total


def decimal_to_snafu(decimal: int) -> str:
    if decimal < 0:
        raise NotImplementedError

    remainders = []
    while decimal > 0:
        remainder = decimal % 5
        match remainder:
            case 4:
                remainders.append("-")
                decimal = (decimal // 5) + 1
                pass
            case 3:
                remainders.append("=")
                decimal = (decimal // 5) + 1
                pass
            case _:
                remainders.append(f"{remainder}")
                decimal = decimal // 5
    return "".join(reversed(remainders))


def test_snafu_to_decimal():
    for snafu, decimal in TEST_MATRIX.items():
        assert snafu_to_decimal(snafu) == decimal


def test_decimal_to_snafu():
    for snafu, decimal in TEST_MATRIX.items():
        assert decimal_to_snafu(decimal) == snafu


def test_sample():
    snafu_sum = sum(snafu_to_decimal(d) for d in SAMPLE)
    assert decimal_to_snafu(snafu_sum) == "2=-1=0"


def test_my_input():
    snafu_sum = sum(snafu_to_decimal(d) for d in MY_INPUT)
    assert decimal_to_snafu(snafu_sum) == "2-==10--=-0101==1201"
