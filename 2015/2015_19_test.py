from pathlib import Path
from collections import defaultdict
import re
import ast


class Solution:
    """
    --- Day 19: Medicine for Rudolph ---
    Rudolph the Red-Nosed Reindeer is sick! His nose isn't shining very brightly, and he needs medicine.

    Red-Nosed Reindeer biology isn't similar to regular reindeer biology; Rudolph is going to need
    custom-made medicine. Unfortunately, Red-Nosed Reindeer chemistry isn't similar to regular
    reindeer chemistry, either.

    The North Pole is equipped with a Red-Nosed Reindeer nuclear fusion/fission plant, capable of
    constructing any Red-Nosed Reindeer molecule you need. It works by starting with some input
    molecule and then doing a series of replacements, one per step, until it has the right molecule.

    However, the machine has to be calibrated before it can be used. Calibration involves determining
    the number of molecules that can be generated in one step from a given starting point.

    For example, imagine a simpler machine that supports only the following replacements:

    H => HO
    H => OH
    O => HH

    Given the replacements above and starting with HOH, the following molecules could be generated:

    HOOH (via H => HO on the first H).
    HOHO (via H => HO on the second H).
    OHOH (via H => OH on the first H).
    HOOH (via H => OH on the second H).
    HHHH (via O => HH).

    So, in the example above, there are 4 distinct molecules (not five, because HOOH appears twice)
    after one replacement from HOH. Santa's favorite molecule, HOHOHO, can become 7 distinct molecules
    (over nine replacements: six from H, and three from O).

    The machine replaces without regard for the surrounding characters. For example, given the string
    H2O, the transition H => OO would result in OO2O.

    Your puzzle input describes all of the possible replacements and, at the bottom, the medicine molecule
    for which you need to calibrate the machine. How many distinct molecules can be created after all the
    different ways you can do one replacement on the medicine molecule?

    --- Part Two ---
    Now that the machine is calibrated, you're ready to begin molecule fabrication.

    Molecule fabrication always begins with just a single electron, e, and applying replacements one at a time,
    just like the ones during calibration.

    For example, suppose you have the following replacements:

    e => H
    e => O
    H => HO
    H => OH
    O => HH
    If you'd like to make HOH, you start with e, and then make the following replacements:

    e => O to get O
    O => HH to get HH
    H => OH (on the second H) to get HOH
    So, you could make HOH after 3 steps. Santa's favorite molecule, HOHOHO, can be made in 6 steps.

    How long will it take to make the medicine? Given the available replacements and the medicine molecule in
    your puzzle input, what is the fewest number of steps to go from e to the medicine molecule?
    """


with open(Path(__file__).parent / "2015_19_input.txt") as fp:
    raw = fp.read()
    reactions, STARTING = raw.split("\n\n")
    SUBMISSION = reactions.split("\n")


def build_formulary(formulary_text):
    formulary = defaultdict(list)
    for line in formulary_text:
        orig, _, new = line.split(" ")
        formulary[orig].append(new)
    return formulary


def test_calibration():
    formulary = build_formulary(["H => HO", "H => OH", "O => HH"])
    assert formulary.items() == ({"H": ["HO", "OH"], "O": ["HH"]}).items()


def new_elements_from_initial(initial, formulary):
    options = set()
    for pos in range(len(initial)):
        if pos > 1 and initial[pos - 1 : pos + 1] in formulary:
            for replacement_element in formulary[initial[pos - 1 : pos + 1]]:
                options.add(
                    initial[: pos - 1] + replacement_element + initial[pos + 1 :]
                )
        elif initial[pos : pos + 1] in formulary:
            for replacement_element in formulary[initial[pos : pos + 1]]:
                options.add(initial[:pos] + replacement_element + initial[pos + 1 :])
    return options


def test_new_elements_from_initial():
    formulary = build_formulary(["H => HO", "H => OH", "O => HH"])
    assert new_elements_from_initial("HOH", formulary) == {
        "HHHH",
        "HOHO",
        "OHOH",
        "HOOH",
    }


def test_submission1():
    formulary = build_formulary(SUBMISSION)
    assert len(new_elements_from_initial(STARTING, formulary)) == 576


"""
--- Part Two ---
Now that the machine is calibrated, you're ready to begin molecule fabrication.

Molecule fabrication always begins with just a single electron, e, and applying replacements one at a time, 
just like the ones during calibration.

For example, suppose you have the following replacements:

e => H
e => O
H => HO
H => OH
O => HH
If you'd like to make HOH, you start with e, and then make the following replacements:

e => O to get O
O => HH to get HH
H => OH (on the second H) to get HOH
So, you could make HOH after 3 steps. Santa's favorite molecule, HOHOHO, can be made in 6 steps.

How long will it take to make the medicine? Given the available replacements and the medicine molecule in 
your puzzle input, what is the fewest number of steps to go from e to the medicine molecule?
"""


def build_unformulary(formulary_text):
    formulary = defaultdict(list)
    for line in formulary_text:
        orig, _, new = line.split(" ")
        formulary[new].append(orig)
    return formulary


def reduced_elements_from_initial(element, unformulary):
    options = set()
    for key, values in unformulary.items():
        if re.search(key, element):
            for value in values:
                options.add(re.sub(key, value, element, 1))
    return options


def deconstruct(target, unformulary):
    current = [(0, target)]
    while len(current) > 0:
        current = sorted(current)
        generation, element = current.pop()
        if element == "e":
            return generation
        if element.count("e") == 0:
            for parent_element in reduced_elements_from_initial(element, unformulary):
                current.append((generation + 1, parent_element))
    raise ValueError(f"Unable to synthesize {target}")


def test_deconstruct():
    unformulary = build_unformulary(
        ["e => H", "e => O", "H => HO", "H => OH", "O => HH"]
    )
    assert deconstruct("HOHOHO", unformulary) == 6


def test_slow_submission2():
    # For the longest time I though this was too slow
    # Refactored to perform depth first rather than breath first and ran in reasonable time
    unformulary = build_unformulary(SUBMISSION)
    assert deconstruct(STARTING, unformulary) == 207


"""
Observation:

In the formulary we only see Rn and Ar as outputs (and later also determined same for Y!) 

This should allow us to break up how we try to deconstruct the final output.  

First let's grab all formulary elements with Rn and Ar:

Those with format A ( B ):

    H =>  C   Rn   Al    Ar
    
    Al => Th  Rn   F     Ar
    B =>  Ti  Rn   F     Ar
    Ca => P   Rn   F     Ar
    H =>  O   Rn   F     Ar
    N =>  C   Rn   F     Ar
    O =>  N   Rn   F     Ar
    P =>  Si  Rn   F     Ar
    
    Ca => Si  Rn   Mg    Ar
    H =>  N   Rn   Mg    Ar
    O =>  C   Rn   Mg    Ar

Those with format A ( X [Y] Z ):

    Ca => Si  Rn   F [Y] F   Ar
    H =>  N   Rn   F [Y] F   Ar
    O =>  C   Rn   F [Y] F   Ar
    
    H =>  C   Rn   F [Y] Mg  Ar
    H =>  C   Rn   Mg [Y] F  Ar

One with format A ( X [Y] X [Y] X ):

    H =>  C   Rn   F [Y] F [Y] F Ar


--------
Another interesting thing is all the F elements

F => CaF
F => PMg
F => SiAl

"""


def build_interesting_unformulary(formulary_text):
    normal_formulary = {}
    rn_formulary = {}
    for line in formulary_text:
        orig, _, new = line.split(" ")
        if new.count("Rn") == 0:
            if new in normal_formulary:
                raise Exception(f"Compound {new} already in normal formulary")
            normal_formulary[new] = orig
        else:
            pre, post = new.split("Rn")
            if post[-2:] != "Ar":
                raise Exception(f"Compound {new} missing Ar end")
            middle = tuple(post[:-2].split("Y"))
            num_of_y = len(middle)
            if num_of_y not in rn_formulary:
                rn_formulary[num_of_y] = {}
            if middle not in rn_formulary[num_of_y]:
                rn_formulary[num_of_y][middle] = [pre]
            rn_formulary[num_of_y][middle].append(orig)
    return normal_formulary, rn_formulary


def split_by_RnY(molecule):
    """
    [['ORnPBPMg'],
     ['CaCaCaSiThCaCaSiThCaCaPBSiRnF'],
     ['RnF'],
     ['CaCaSiThCaCaSiThCaCaCaCaCaCaSiRnF', 'F'],
     ['SiRnMg'],
     ['CaSiRnPTiTiBF', 'PBF'],
     ['SiRnCaSiRnTiRnF'],
     ['SiAl'],
     ['PTiBPTiRnCaSiAl'],
     ['CaPTiTiBPMg', 'F'],
     ['PTiRnF'],
     ['SiRnCaCaF'],
     ['RnCaF'],
     ['CaSiRnSiRnMg'],
     ['F', 'CaSiRnMg'],
     ['CaCaSiThPRnF'],
     ['PBCaSiRnMg'],
     ['CaCaSiThCaSiRnTiMg'],
     ['F'],
     ['SiThSiThCaCaSiRnMg'],
     ['CaCaSiRnF'],
     ['TiBPTiRnCaSiAl'],
     ['CaPTiRnF'],
     ['PBPBCaCaSiThCaPBSiThPRnF'],
     ['SiThCaSiThCaSiThCaPTiBSiRnF', 'F'],
     ['CaCaPRnF'],
     ['PBCaCaPBSiRnTiRnF'],
     ['CaPRnF'],
     ['SiRnCaCaCaSiThCaRnCaF'],
     ['', 'CaSiRnF'],
     ['BCaCaCaSiThF'],
     ['PBF'],
     ['CaSiRnF'],
     ['RnCaCaCaF'],
     ['SiRnF'],
     ['TiRnPMg'],
     ['F']]
    """
    return [bit.split("Y") for bit in molecule.split("Ar")]


def enhance_string(molecule):
    enhance = f"['{molecule}']"
    enhance = enhance.replace("Ar", "Ar'],'")
    enhance = enhance.replace("Rn", "',['Rn")
    # enhance = enhance.replace('T',"',['T'],'")
    # return json.loads(enhance)
    # return enhance
    return ast.literal_eval(enhance)


class RnAr:
    def __init__(self, head, inner):
        self.head = head
        self.inner_len = len(inner)
        self.inner = parse_enhanced_string(inner)

    def display(self, offset):
        print(f"{offset}{self.head} len={self.inner_len}")
        for inner in self.inner:
            if type(inner) == RnAr:
                inner.display(f"{offset}    ")
            else:
                print(f"{offset}    {inner}")


def parse_enhanced_string(eh):
    head = []
    for ele in eh:
        if type(ele) == list:
            head[-1] = RnAr(head[-1], ele)
        elif type(ele) == str:
            head.append(RnAr(ele, ""))
    return head


def test_submission2():
    # Too slow
    # unformulary = build_unformulary(SUBMISSION)
    # assert defabricate(STARTING, unformulary) == 6
    nof, rnf = build_interesting_unformulary(SUBMISSION)
    working_bits = split_by_RnY(STARTING)
    eh = enhance_string(STARTING)
    eh2 = parse_enhanced_string(eh)
    print()
    print(nof)
    print(rnf)
    print()
    print(working_bits)
    print()
    for x in eh2:
        x.display("")
    assert False
