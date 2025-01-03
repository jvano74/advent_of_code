from pathlib import Path


class Puzzle:
    """
    --- Day 7: Internet Protocol Version 7 ---
    While snooping around the local network of EBHQ, you compile a list of IP
    addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to
    figure out which IPs support TLS (transport-layer snooping).

    An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or
    ABBA. An ABBA is any four-character sequence which consists of a pair of two
    different characters followed by the reverse of that pair, such as xyyx or
    abba. However, the IP also must not have an ABBA within any hypernet
    sequences, which are contained by square brackets.

    For example:

    abba[mnop]qrst supports TLS (abba outside square brackets).

    abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even
    though xyyx is outside square brackets).

    aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior
    characters must be different).

    ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even
    though it's within a larger string).

    How many IPs in your puzzle input support TLS?

    Your puzzle answer was 118.

    --- Part Two ---
    You would also like to know which IPs support SSL (super-secret listening).

    An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in
    the supernet sequences (outside any square bracketed sections), and a
    corresponding Byte Allocation Block, or BAB, anywhere in the hypernet
    sequences. An ABA is any three-character sequence which consists of the same
    character twice with a different character between them, such as xyx or aba.
    A corresponding BAB is the same characters but in reversed positions: yxy
    and bab, respectively.

    For example:

    aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab
    within square brackets).

    xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).

    aaa[kek]eke supports SSL (eke in supernet with corresponding kek in
    hypernet; the aaa sequence is not related, because the interior character
    must be different).

    zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a
    corresponding bzb, even though zaz and zbz overlap).

    How many IPs in your puzzle input support SSL?

    How many IPs in your puzzle input support SSL?

    Your puzzle answer was 260.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """

    pass


SAMPLE = ["abba[mnop]qrst", "abcd[bddb]xyyx", "aaaa[qwer]tyui", "ioxxoj[asdfgh]zxcvbn"]
SAMPLE_RESULTS = [True, False, False, True]

SAMPLE2 = ["aba[bab]xyz", "xyx[xyx]xyx", "aaa[kek]eke", "zazbz[bzb]cdb"]
SAMPLE2_RESULTS = [True, False, True, True]

with open(Path(__file__).parent / "2016_07_input.txt") as f:
    INPUTS = [line.strip() for line in f]


def supports_tls(ip):
    hyernet = False
    supports_tls = False
    for i, c in enumerate(ip[:-3]):
        if c == "[":
            hyernet = True
        elif c == "]":
            hyernet = False
        elif ip[i] == ip[i + 3] != ip[i + 1] == ip[i + 2]:
            if hyernet:
                return False
            supports_tls = True
    return supports_tls


def test_supports_tls():
    assert [supports_tls(s) for s in SAMPLE] == SAMPLE_RESULTS
    assert sum([supports_tls(s) for s in INPUTS]) == 118


def supports_ssl(ip):
    hyernet = False
    possible_aba = {}
    possible_bab = {}
    for i, a in enumerate(ip[:-2]):
        b = ip[i + 1]
        c = ip[i + 2]
        if a == "[":
            hyernet = True
        elif a == "]":
            hyernet = False
        elif b != "[" and b != "]" and a == c != b:
            if hyernet:
                possible_bab[ip[i : i + 3]] = i
            else:
                possible_aba[ip[i : i + 3]] = i
    for aba in possible_aba:
        bab = "".join([aba[1], aba[0], aba[1]])
        if bab in possible_bab:
            return True
    return False


def test_supports_ssl():
    print("Closer looks")
    assert [supports_ssl(s) for s in SAMPLE2] == SAMPLE2_RESULTS
    assert sum([supports_ssl(s) for s in INPUTS]) == 260
    # first guess of 378 was too high
