from pathlib import Path
from queue import PriorityQueue
from itertools import product
from typing import List, Tuple, NamedTuple
from functools import cache
from collections import defaultdict


class Puzzle:
    """
    --- Day 23: LAN Party ---
    As The Historians wander around a secure area at Easter Bunny HQ, you come
    across posters for a LAN party scheduled for today! Maybe you can find it;
    you connect to a nearby datalink port and download a map of the local
    network (your puzzle input).

    The network map provides a list of every connection between two computers.
    For example:

    kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn

    Each line of text in the network map represents a single connection; the
    line kh-tc represents a connection between the computer named kh and the
    computer named tc. Connections aren't directional; tc-kh would mean exactly
    the same thing.

    LAN parties typically involve multiplayer games, so maybe you can locate it
    by finding groups of connected computers. Start by looking for sets of three
    computers where each computer in the set is connected to the other two
    computers.

    In this example, there are 12 such sets of three inter-connected computers:

    aq,cg,yn
    aq,vc,wq
    co,de,ka
    co,de,ta
    co,ka,ta
    de,ka,ta
    kh,qp,ub
    qp,td,wh
    tb,vc,wq
    tc,td,wh
    td,wh,yn
    ub,vc,wq

    If the Chief Historian is here, and he's at the LAN party, it would be best
    to know that right away. You're pretty sure his computer's name starts with
    t, so consider only sets of three computers where at least one computer's
    name starts with t. That narrows the list down to 7 sets of three
    inter-connected computers:

    co,de,ta
    co,ka,ta
    de,ka,ta
    qp,td,wh
    tb,vc,wq
    tc,td,wh
    td,wh,yn

    Find all the sets of three inter-connected computers. How many contain at
    least one computer with a name that starts with t?

    Your puzzle answer was 1170.

    --- Part Two ---
    There are still way too many results to go through them all. You'll have to
    find the LAN party another way and go there yourself.

    Since it doesn't seem like any employees are around, you figure they must
    all be at the LAN party. If that's true, the LAN party will be the largest
    set of computers that are all connected to each other. That is, for each
    computer at the LAN party, that computer will have a connection to every
    other computer at the LAN party.

    In the above example, the largest set of computers that are all connected to
    each other is made up of co, de, ka, and ta. Each computer in this set has a
    connection to every other computer in the set:

    ka-co
    ta-co
    de-co
    ta-ka
    de-ta
    ka-de

    The LAN party posters say that the password to get into the LAN party is the
    name of every computer at the LAN party, sorted alphabetically, then joined
    together with commas. (The people running the LAN party are clearly a bunch
    of nerds.) In this example, the password would be co,de,ka,ta.

    What is the password to get into the LAN party?

    Your puzzle answer was bo,dd,eq,ik,lo,lu,ph,ro,rr,rw,uo,wx,yg.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


SAMPLE_NETWORK = [
    tuple(ln.strip().split("-"))
    for ln in """kh-tc
            qp-kh
            de-cg
            ka-co
            yn-aq
            qp-ub
            cg-tb
            vc-aq
            tb-ka
            wh-tc
            yn-cg
            kh-ub
            ta-co
            de-co
            tc-td
            tb-wq
            wh-td
            ta-ka
            td-qp
            aq-cg
            wq-ub
            ub-vc
            de-ta
            wq-aq
            wq-vc
            wh-yn
            ka-de
            kh-ta
            co-tc
            wh-qp
            tb-vc
            td-yn""".split(
        "\n"
    )
]

with open(Path(__file__).parent / "2024_23_input.txt") as fp:
    NETWORK = [tuple(ln.split("-")) for ln in fp.read().split("\n")]


def find_3_clique(connection_list, check_for_t=False):
    nodes = defaultdict(set)
    for a, b in connection_list:
        nodes[a].add(b)
        nodes[b].add(a)
    triples = set()
    for a, b in connection_list:
        for c in nodes[a] & nodes[b]:
            if check_for_t:
                if "t" not in f"{a[0]}{b[0]}{c[0]}":
                    continue
            triples.add(tuple(sorted((a, b, c))))
    return sorted(triples)


def test_find_3_clique():
    assert find_3_clique(SAMPLE_NETWORK) == [
        ("aq", "cg", "yn"),
        ("aq", "vc", "wq"),
        ("co", "de", "ka"),
        ("co", "de", "ta"),
        ("co", "ka", "ta"),
        ("de", "ka", "ta"),
        ("kh", "qp", "ub"),
        ("qp", "td", "wh"),
        ("tb", "vc", "wq"),
        ("tc", "td", "wh"),
        ("td", "wh", "yn"),
        ("ub", "vc", "wq"),
    ]
    assert find_3_clique(SAMPLE_NETWORK, check_for_t=True) == [
        ("co", "de", "ta"),
        ("co", "ka", "ta"),
        ("de", "ka", "ta"),
        ("qp", "td", "wh"),
        ("tb", "vc", "wq"),
        ("tc", "td", "wh"),
        ("td", "wh", "yn"),
    ]


def test_find_my_3_clique():
    assert len(NETWORK) == 3380
    assert NETWORK[0] == ("ht", "nz")
    assert NETWORK[-1] == ("io", "fe")
    assert len(find_3_clique(NETWORK, check_for_t=True)) == 1170
    # First submission of 11011 was not right answer (didn't say to high or low)
    # DOH - forgot to include the check_for_t
    # DOH - also missed that we want "starts with t"
    # finally got right answer of 1170


def find_largest_clique(connection_list):
    nodes = defaultdict(set)
    for a, b in connection_list:
        nodes[a].add(b)
        nodes[b].add(a)

    current_level = connection_list
    while current_level:
        next_level = set()
        for clique in current_level:
            for c in set.intersection(*[nodes[a] for a in clique]):
                new_clique = sorted(clique)
                new_clique.append(c)
                next_level.add(tuple(sorted(new_clique)))
        if next_level:
            current_level = next_level
            continue
        return sorted(current_level)


def test_find_largest_clique():
    assert find_largest_clique(SAMPLE_NETWORK) == [("co", "de", "ka", "ta")]


def test_find_my_largest_clique():
    assert (
        ",".join(find_largest_clique(NETWORK)[0])
        == "bo,dd,eq,ik,lo,lu,ph,ro,rr,rw,uo,wx,yg"
    )
