from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 6: Signals and Noise ---
    Something is jamming your communications with Santa. Fortunately, your
    signal is only partially jammed, and protocol in situations like this is to
    switch to a simple repetition code to get the message through.

    In this model, the same message is sent repeatedly. You've recorded the
    repeating message signal (your puzzle input), but the data seems quite
    corrupted - almost too badly to recover. Almost.

    All you need to do is figure out which character is most frequent for each
    position. For example, suppose you had recorded the following messages:

    eedadn
    drvtee
    eandsr
    raavrd
    atevrs
    tsrnev
    sdttsa
    rasrtv
    nssdts
    ntnada
    svetve
    tesnvt
    vntsnd
    vrdear
    dvrsen
    enarar

    The most common character in the first column is e; in the second, a; in the
    third, s, and so on. Combining these characters returns the error-corrected
    message, easter.

    Given the recording in your puzzle input, what is the error-corrected
    version of the message being sent?

    --- Part Two ---

    Of course, that would be the message - if you hadn't agreed to use a
    modified repetition code instead.

    In this modified code, the sender instead transmits what looks like random
    data, but for each character, the character they actually want to send is
    slightly less likely than the others. Even after signal-jamming noise, you
    can look at the letter distributions in each column and choose the least
    common letter to reconstruct the original message.

    In the above example, the least common character in the first column is a;
    in the second, d, and so on. Repeating this process for the remaining
    characters produces the original message, advent.

    Given the recording in your puzzle input and this new decoding methodology,
    what is the original message that Santa is trying to send?
    """

    pass


with open(Path(__file__).parent / "2016_06_input.txt") as f:
    INPUTS = [line.strip() for line in f]

SAMPLES = [
    "eedadn",
    "drvtee",
    "eandsr",
    "raavrd",
    "atevrs",
    "tsrnev",
    "sdttsa",
    "rasrtv",
    "nssdts",
    "ntnada",
    "svetve",
    "tesnvt",
    "vntsnd",
    "vrdear",
    "dvrsen",
    "enarar",
]


def list_to_frequency_list(msgs):
    result = [defaultdict(int) for _ in msgs[0]]
    for msg in msgs:
        for i, c in enumerate(msg):
            result[i][c] += 1
    # return ''.join(
    # [sorted(freq_dict.items(), key=lambda x, v: -v)[0] for freq_dict in result]
    # )
    return "".join(
        [sorted(freq_dict.items(), key=lambda kv: -kv[1])[0][0] for freq_dict in result]
    )


def list_to_frequency_list2(msgs):
    result = [defaultdict(int) for _ in msgs[0]]
    for msg in msgs:
        for i, c in enumerate(msg):
            result[i][c] += 1
    # return ''.join(
    # [sorted(freq_dict.items(), key=lambda x, v: -v)[0] for freq_dict in result]
    # )
    return "".join(
        [sorted(freq_dict.items(), key=lambda kv: kv[1])[0][0] for freq_dict in result]
    )


def test_list_to_frequency_list():
    assert list_to_frequency_list(SAMPLES) == "easter"
    assert list_to_frequency_list(INPUTS) == "zcreqgiv"


def test_list_to_frequency_list2():
    assert list_to_frequency_list2(SAMPLES) == "advent"
    assert list_to_frequency_list2(INPUTS) == "pljvorrk"
