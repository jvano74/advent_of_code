from collections import defaultdict
import re

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
    """


with open('day_19_input.txt') as fp:
    raw = fp.read()
    reactions, STARTING = raw.split('\n\n')
    SUBMISSION = reactions.split('\n')


def build_formulary(formulary_text):
    formulary = defaultdict(list)
    for line in formulary_text:
        orig, _, new = line.split(' ')
        formulary[orig].append(new)
    return formulary


def build_unformulary(formulary_text):
    formulary = defaultdict(list)
    for line in formulary_text:
        orig, _, new = line.split(' ')
        formulary[new].append(orig)
    return formulary


def new_elements_from_initial(initial, formulary):
    options = set()
    for pos in range(len(initial)):
        if pos > 1 and initial[pos-1:pos+1] in formulary:
            for replacement_element in formulary[initial[pos - 1:pos + 1]]:
                options.add(initial[:pos-1]+replacement_element+initial[pos+1:])
        elif initial[pos:pos+1] in formulary:
            for replacement_element in formulary[initial[pos:pos + 1]]:
                options.add(initial[:pos]+replacement_element+initial[pos+1:])
    return options


def reduced_elements_from_initial(element, unformulary):
    options = set()
    for key, values in unformulary.items():
        if re.search(key, element):
            for value in values:
                options.add(re.sub(key, value, element, 1))
    return options


def defabricate(target, unformulary):
    current = set()
    current.add(target)
    generation = 0
    while len(current) > 0 :
        if 'e' in current:
            return generation
        next_generation = set()
        for element in current:
            if not re.search('e', element):
                next_generation = next_generation.union(reduced_elements_from_initial(element, unformulary))
        current = next_generation
        generation += 1
        print(f'gen={generation} len={len(current)}')
    raise ValueError(f'Unable to synthesize {target}')


def test_calibration():
    formulary = build_formulary(['H => HO', 'H => OH', 'O => HH'])
    assert dict(formulary) == {'H': ['HO', 'OH'], 'O': ['HH']}
    assert new_elements_from_initial('HOH', formulary) == {'HHHH', 'HOHO', 'OHOH', 'HOOH'}


def test_degenerate():
    unformulary = build_unformulary(['e => H', 'e => O', 'H => HO', 'H => OH', 'O => HH'])
    assert defabricate('HOHOHO', unformulary) == 6


def test_submission():
    formulary = build_formulary(SUBMISSION)
    assert len(new_elements_from_initial(STARTING, formulary)) == 576


def test_submission2():
    unformulary = build_formulary(SUBMISSION)
    assert defabricate(STARTING, unformulary) == 6
