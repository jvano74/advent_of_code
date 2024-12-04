from pathlib import Path
from collections import Counter


class Puzzle:
    """
    --- Day 14: Extended Polymerization ---
    The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has
    polymerization equipment that would produce suitable materials to reinforce the submarine, and the nearby
    volcanically-active caves should even have the necessary input elements in sufficient quantities.

    The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers
    a polymer template and a list of pair insertion rules (your puzzle input). You just need to work out what
    polymer would result after repeating the pair insertion process a few times.

    For example:

    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C

    The first line is the polymer template - this is the starting point of the process.

    The following section defines the pair insertion rules. A rule like AB -> C means that when
    elements A and B are immediately adjacent, element C should be inserted between them. These
    insertions all happen simultaneously.

    So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

    - The first pair (NN) matches the rule NN -> C, so element C is inserted between the
      first N and the second N.

    - The second pair (NC) matches the rule NC -> B, so element B is inserted between
      the N and the C.

    - The third pair (CB) matches the rule CB -> H, so element H is inserted between
      the C and the B.

    Note that these pairs overlap: the second element of one pair is the first element of the
    next pair. Also, because all pairs are considered simultaneously, inserted elements are not
    considered to be part of a pair until the next step.

    After the first step of this process, the polymer becomes NCNBCHB.

    Here are the results of a few steps using the above rules:

    Template:     NNCB
    After step 1: NCNBCHB
    After step 2: NBCCNBBBCBHCB
    After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
    After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

    This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073.
    After step 10, B occurs 1749 times, C occurs 298 times, H occurs 191 times, and N occurs 865 times;
    taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least
    common element (H, 161) produces 1749 - 161 = 1588.

    Apply 10 steps of pair insertion to the polymer template and find the most and least common elements
    in the result. What do you get if you take the quantity of the most common element and subtract the
    quantity of the least common element?

    To begin, get your puzzle input.

    --- Part Two ---
    The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more
    steps of the pair insertion process; a total of 40 steps should do it.

    In the above example, the most common element is B (occurring 2192039569602 times) and the least common
    element is H (occurring 3849876073 times); subtracting these produces 2188189693529.

    Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in
    the result. What do you get if you take the quantity of the most common element and subtract the quantity
    of the least common element?

    """


RAW_SAMPLE = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

with open(Path(__file__).parent / "2021_14_input.txt") as fp:
    RAW_INPUT = fp.read()


class Polymerization:
    def __init__(self, replacements):
        self.insertions = dict()
        for r in replacements:
            base, insert = r.split(" -> ")
            self.insertions[base] = insert

    def run(self, initial_compound, steps):
        result = initial_compound
        for _ in range(steps):
            result = self.step(result)
        return result

    def step(self, initial_compound):
        result = []
        for pos, left in enumerate(initial_compound):
            if pos + 1 == len(initial_compound):
                result.append(left)
                return "".join(result)
            result.append(left)
            right = initial_compound[pos + 1]
            if f"{left}{right}" in self.insertions:
                result.append(self.insertions[f"{left}{right}"])

    def fast_steps(self, initial_compound, steps):
        fast_map = Counter()
        for pos, left in enumerate(initial_compound):
            if pos + 1 == len(initial_compound):
                fast_map[f"{left}*"] += 1
            else:
                right = initial_compound[pos + 1]
                fast_map[f"{left}{right}"] += 1
        for _ in range(steps):
            next_step = Counter()
            for n in fast_map:
                if n not in self.insertions:
                    next_step[n] += fast_map[n]
                else:
                    new = self.insertions[n]
                    left, right = n
                    next_step[f"{left}{new}"] += fast_map[n]
                    next_step[f"{new}{right}"] += fast_map[n]
            fast_map = next_step
        data = Counter()
        for n in fast_map:
            left, _ = n
            data[left] += fast_map[n]
        frequency = data.most_common()
        return frequency[0][1] - frequency[-1][1]

    @staticmethod
    def analyze(compound):
        data = Counter(compound)
        frequency = data.most_common()
        return frequency[0][1] - frequency[-1][1]


def test_polymerization():
    base, raw_replacements = RAW_SAMPLE.split("\n\n")
    replacements = [rl.strip() for rl in raw_replacements.split("\n")]
    sample_polymerization = Polymerization(replacements)
    assert sample_polymerization.step("NNCB") == "NCNBCHB"
    assert sample_polymerization.run("NNCB", 2) == "NBCCNBBBCBHCB"
    assert sample_polymerization.run("NNCB", 3) == "NBBBCNCCNBBNBNBBCHBHHBCHB"
    assert (
        sample_polymerization.run("NNCB", 4)
        == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    )
    assert Polymerization.analyze(sample_polymerization.run(base, 10)) == 1588
    assert sample_polymerization.fast_steps(base, 40) == 2188189693529


def test_real_polymerization():
    base, raw_replacements = RAW_INPUT.split("\n\n")
    replacements = [rl.strip() for rl in raw_replacements.split("\n")]
    sample_polymerization = Polymerization(replacements)
    assert Polymerization.analyze(sample_polymerization.run(base, 10)) == 3259
    assert sample_polymerization.fast_steps(base, 40) == 3259
