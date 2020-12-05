import math
from typing import List, Dict
from collections import defaultdict


test1 = [
'10 ORE => 10 A',
'1 ORE => 1 B',
'7 A, 1 B => 1 C',
'7 A, 1 C => 1 D',
'7 A, 1 D => 1 E',
'7 A, 1 E => 1 FUEL',
]


test2 = [
'9 ORE => 2 A',
'8 ORE => 3 B',
'7 ORE => 5 C',
'3 A, 4 B => 1 AB',
'5 B, 7 C => 1 BC',
'4 C, 1 A => 1 CA',
'2 AB, 3 BC, 4 CA => 1 FUEL'
]


test3 = [
'157 ORE => 5 NZVS',
'165 ORE => 6 DCFZ',
'44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL',
'12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ',
'179 ORE => 7 PSHF',
'177 ORE => 5 HKGWZ',
'7 DCFZ, 7 PSHF => 2 XJWVT',
'165 ORE => 2 GPVTF',
'3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'
]


def parse_formula(eqn: str) -> Dict:
    inputs, output = eqn.split('=>',1)
    raw = {}
    for element in inputs.split(','):
        element = element.strip()
        num, name = element.split(' ')
        raw[name] = int(num)
    output = output.strip()
    num, name = output.split(' ')
    return (name, int(num), raw)


def build_formulary(eqns: List) -> Dict:
    formulary = {}
    for eqn in eqns:
        name, num, raw = parse_formula(eqn)
        if name in formulary:
            print(name,'already in formulary?')
            raise KeyError
        formulary[name] = (num, raw)
    return formulary


def test_parse_formula():
    formulary = build_formulary(test1)
    assert formulary['FUEL'] == (1, {'A': 7, 'E': 1})
    assert formulary['A'] == (10, {'ORE': 10})


def find_base(formulary, desired_fuel = 1, display_output = False):
    to_make = defaultdict(int)
    to_make['FUEL'] = desired_fuel
    leftovers = defaultdict(int)
    ore = 0
    if display_output:
        print('Starting...')
    while len(to_make)>0:
        for element in list(to_make):
            number_needed = to_make[element]
            del to_make[element]
            number, components = formulary[element]
            times = math.ceil((number_needed - leftovers[element])/number)
            leftovers[element] += times * number - number_needed
            if display_output:
                print(f'Making {number * times} of {element} to get {number_needed} using {times} recipiet of',components)
            for to_add in components:
                if to_add == 'ORE':
                    ore += times * components[to_add]
                else:
                    to_make[to_add] += times*components[to_add]
        if display_output:
            print(ore, '\n ', to_make, '\n ', leftovers)
    return ore



def test_find_base():
    print()
    print(test1)
    assert find_base(build_formulary(test1)) == 31
    print(test2)
    assert find_base(build_formulary(test2)) == 165
    print(test3)
    assert find_base(build_formulary(test3)) == 13312


def test_submission():
    print()
    with open('day_14_input.txt') as fp:
        submission = fp.read()
    input_list = submission.split('\n')
    assert find_base(build_formulary(input_list)) == 1590844


def test_submission2():
    print()
    #input_list = test3
    #expected_max = 82892753
    with open('day_14_input.txt') as fp:
        submission = fp.read()
    input_list = submission.split('\n')
    expected_max = 1184209
    MAX_ORE = 1000000000000
    ONE_FULE = find_base(build_formulary(input_list))
    estimated_fule_out = MAX_ORE // ONE_FULE
    print('Starting with formula that takes', ONE_FULE, 'for one to produce', estimated_fule_out, 'FUEL')
    while True:
        needed_ore = find_base(build_formulary(input_list),estimated_fule_out)
        print('GOT', estimated_fule_out, ' FUEL using', needed_ore, 'ORE')
        if needed_ore < MAX_ORE:
            delta = (MAX_ORE - needed_ore)//ONE_FULE
            print('Still have',MAX_ORE - needed_ore,'ORE left which should allow for',delta,'more FUEL')
            if delta == 0:
                print('MAX might be ', estimated_fule_out, 'using', needed_ore, 'ORE')
                delta += 1
            estimated_fule_out += delta
            print('Trying to get', delta, 'more fule...  trying for', estimated_fule_out, 'FUEL')
        elif needed_ore == MAX_ORE:
            print('PERFECT...',estimated_fule_out, 'FUEL')
            break
        else:
            estimated_fule_out -= 1
            print('Needs too much ORE... ', needed_ore, 'maybe...',estimated_fule_out, 'FUEL')
            break
    assert estimated_fule_out == expected_max
