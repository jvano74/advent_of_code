class Puzzle:
    """
    --- Day 21: Scrambled Letters and Hash ---
    The computer system you're breaking into uses a weird scrambling function to store its passwords. It shouldn't be
    much trouble to create your own scrambled password so you can add it to the system; you just have to implement the
    scrambler.

    The scrambling function is a series of operations (the exact list is provided in your puzzle input). Starting with
    the password to be scrambled, apply each operation in succession to the string. The individual operations behave
    as follows:

    - swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
    - swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear
      in the string).
    - rotate left/right X steps means that the whole string should be rotated; for example, one right rotation
      would turn abcd into dabc.
    - rotate based on position of letter X means that the whole string should be rotated to the right based on the
      index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index
      is determined, rotate the string to the right one time, plus a number of times equal to that index, plus
      one additional time if the index was at least 4.
    - reverse positions X through Y means that the span of letters at indexes X through Y (including the letters
      at X and Y) should be reversed in order.
    - move position X to position Y means that the letter which is at index X should be removed from the string,
      then inserted such that it ends up at index Y.

    For example, suppose you start with abcde and perform the following operations:

    - swap position 4 with position 0 swaps the first and last letters, producing the input for the
      next step, ebcda.
    - swap letter d with letter b swaps the positions of d and b: edcba.
    - reverse positions 0 through 4 causes the entire string to be reversed, producing abcde.
    - rotate left 1 step shifts all letters left one position, causing the first letter to wrap to the end of
      the string: bcdea.
    - move position 1 to position 4 removes the letter at position 1 (c), then inserts it at position 4
      (the end of the string): bdeac.
    - move position 3 to position 0 removes the letter at position 3 (a), then inserts it at position 0
      (the front of the string): abdec.
    - rotate based on position of letter b finds the index of letter b (1), then rotates the string right once
      plus a number of times equal to that index (2): ecabd.
    - rotate based on position of letter d finds the index of letter d (4), then rotates the string right once,
      plus a number of times equal to that index, plus an additional time because the index was at least 4, for
      a total of 6 right rotations: decab.

    After these steps, the resulting scrambled password is decab.

    Now, you just need to generate a new scrambled password and you can access the system. Given the list of
    scrambling operations in your puzzle input, what is the result of scrambling abcdefgh?

    --- Part Two ---
    You scrambled the password correctly, but you discover that you can't actually modify the password file on the
    system. You'll need to un-scramble one of the existing passwords by reversing the scrambling process.

    What is the un-scrambled version of the scrambled password fbgdceah?
    """
    pass


with open('day_21_input.txt') as fp:
    INPUTS = [line.strip() for line in fp]


def scramble(input_string, instruction_list, un_scramble=False):
    str_array = [c for c in input_string]
    if un_scramble:
        instruction_list = [i for i in reversed(instruction_list)]
    for instruction in instruction_list:
        ins_parsed = instruction.split(' ')
        ins = f'{ins_parsed[0]} {ins_parsed[1]}'
        if un_scramble and ins == 'rotate left':
            ins = 'rotate right'
        elif un_scramble and ins == 'rotate right':
            ins = 'rotate left'
        if ins == 'swap position':
            x = int(ins_parsed[2])
            y = int(ins_parsed[5])
            str_array[x], str_array[y] = str_array[y], str_array[x]
        elif ins == 'swap letter':
            x = str_array.index(ins_parsed[2])
            y = str_array.index(ins_parsed[5])
            str_array[x], str_array[y] = str_array[y], str_array[x]
        elif ins == 'rotate left':
            x = int(ins_parsed[2])
            to_end = str_array[0:x]
            str_array = str_array[x:]
            str_array.extend(to_end)
        elif ins == 'rotate right':
            x = len(str_array) - int(ins_parsed[2])
            to_end = str_array[0:x]
            str_array = str_array[x:]
            str_array.extend(to_end)
        elif ins == 'reverse positions':
            x = int(ins_parsed[2])
            y = int(ins_parsed[4])
            rev_array = str_array[x:y+1]
            for i in range(y - x + 1):
                str_array[y - i] = rev_array[i]
        elif ins == 'move position':
            x = int(ins_parsed[2])
            y = int(ins_parsed[5])
            if un_scramble:
                x, y = y, x
            char_moved = str_array.pop(x)
            str_array.insert(y, char_moved)
        elif ins == 'rotate based':
            if un_scramble:
                rot_index = str_array.index(ins_parsed[6])
                # going for brute force here with length 8
                un_rot = {1: 1, 3: 2, 5: 3, 7: 4, 2: -2, 4: -1, 6: 0, 0: 1}
                x = un_rot[rot_index]
                if x < 0:
                    x += 8
                to_end = str_array[0:x]
                str_array = str_array[x:]
                str_array.extend(to_end)
            else:
                right_rotation = str_array.index(ins_parsed[6])
                if right_rotation >= 4:
                    right_rotation += 2
                else:
                    right_rotation += 1
                x = len(str_array) - right_rotation
                to_end = str_array[0:x]
                str_array = str_array[x:]
                str_array.extend(to_end)
    return ''.join(str_array)


def test_example_scramble():
    assert scramble('abcde', ['swap position 4 with position 0']) == 'ebcda'
    assert scramble('ebcda', ['swap letter d with letter b']) == 'edcba'
    assert scramble('edcba', ['reverse positions 0 through 4']) == 'abcde'
    assert scramble('abcde', ['rotate left 1 step']) == 'bcdea'
    # not in example but check rotate right
    assert scramble('abcde', ['rotate right 2 step']) == 'deabc'
    # resuming example
    assert scramble('bcdea', ['move position 1 to position 4']) == 'bdeac'
    assert scramble('bdeac', ['move position 3 to position 0']) == 'abdec'
    assert scramble('abdec', ['rotate based on position of letter b']) == 'ecabd'
    assert scramble('ecabd', ['rotate based on position of letter d']) == 'decab'


def helper_rotate_test(char, unscrambled, scrambled):
    scrambled_observed = scramble(unscrambled, [f'rotate based on position of letter {char}'])
    assert scrambled_observed == scrambled
    unscrambled_observed = scramble(scrambled, [f'rotate based on position of letter {char}'], un_scramble=True)
    assert unscrambled_observed == unscrambled


def test_unrotate():
    helper_rotate_test('a', 'abcdefgh', 'habcdefg')
    helper_rotate_test('b', 'abcdefgh', 'ghabcdef')
    helper_rotate_test('c', 'abcdefgh', 'fghabcde')
    helper_rotate_test('d', 'abcdefgh', 'efghabcd')
    helper_rotate_test('e', 'abcdefgh', 'cdefghab')
    helper_rotate_test('f', 'abcdefgh', 'bcdefgha')
    helper_rotate_test('g', 'abcdefgh', 'abcdefgh')
    helper_rotate_test('h', 'abcdefgh', 'habcdefg')


def test_example_un_scramble():
    assert scramble('ebcda', ['swap position 4 with position 0'], un_scramble=True) == 'abcde'
    assert scramble('edcba', ['swap letter d with letter b'], un_scramble=True) == 'ebcda'
    assert scramble('abcde', ['reverse positions 0 through 4'], un_scramble=True) == 'edcba'
    assert scramble('bcdea', ['rotate left 1 step'], un_scramble=True) == 'abcde'
    # not in example but check rotate right
    assert scramble('deabc', ['rotate right 2 step'], un_scramble=True) == 'abcde'
    # resuming example
    assert scramble('bdeac', ['move position 1 to position 4'], un_scramble=True) == 'bcdea'
    assert scramble('abdec', ['move position 3 to position 0'], un_scramble=True) == 'bdeac'
    assert scramble('ecabd', ['rotate based on position of letter b'], un_scramble=True) == 'abdec'
    assert scramble('decab', ['rotate based on position of letter d'], un_scramble=True) == 'ecabd'


def test_puzzle_scramble():
    assert scramble('abcdefgh', INPUTS) == 'agcebfdh'


def test_puzzle_un_scramble():
    assert scramble('fbgdceah', INPUTS, un_scramble=True) == 'afhdbegc'
    # check
    assert scramble('afhdbegc', INPUTS) == 'fbgdceah'

