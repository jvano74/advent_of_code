class Puzzle:
    """
    --- Day 16: Permutation Promenade ---
    You come upon a very unusual sight; a group of programs here appear to be dancing.

    There are sixteen programs in total, named a through p. They start by standing in a line:
    a stands in position 0, b stands in position 1, and so on until p, which stands in position 15.

    The programs' dance consists of a sequence of dance moves:

    - Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise.
      (For example, s3 on abcde produces cdeab).
    - Exchange, written xA/B, makes the programs at positions A and B swap places.
    - Partner, written pA/B, makes the programs named A and B swap places.

    For example, with only five programs standing in a line (abcde), they could do the following dance:

    s1, a spin of size 1: eabcd.
    x3/4, swapping the last two programs: eabdc.
    pe/b, swapping programs e and b: baedc.
    After finishing their dance, the programs end up in order baedc.

    You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs
    standing after their dance?

    --- Part Two ---
    Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

    Keeping the positions they ended up in from their previous dance, the programs perform it again and again:
    including the first dance, a total of one billion (1000000000) times.

    In the example above, their second dance would begin with the order baedc, and use the same dance moves:

    s1, a spin of size 1: cbaed.
    x3/4, swapping the last two programs: cbade.
    pe/b, swapping programs e and b: ceadb.

    In what order are the programs standing after their billion dances?
    """
    pass


with open('day_16_input.txt') as fp:
    INPUTS = fp.read().strip().split(',')


def test_inputs():
    programs = set()
    numbers = set()
    for ins in INPUTS:
        if ins[0] == 's':
            numbers.add(ins[1:])
        if ins[0] == 'x':
            a, b = ins[1:].split('/')
            numbers.add(a)
            numbers.add(b)
        elif ins[0] == 'p':
            a, b = ins[1:].split('/')
            programs.add(a)
            programs.add(b)
    assert programs == {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'}
    assert numbers == {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'}


def shuffle(moves, initial, split=False):
    prog = [c for c in initial]
    prog2 = [c for c in initial]
    for m in moves:
        if m[0] == 's':
            d = int(m[1:])
            end = prog[-d:]
            end.extend(prog[:-d])
            prog = end
        if m[0] == 'x':
            a, b = (int(c) for c in m[1:].split('/'))
            prog[a], prog[b] = prog[b], prog[a]
        elif m[0] == 'p':
            a, b = m[1:].split('/')
            if split:
                a_loc = prog2.index(a)
                b_loc = prog2.index(b)
                prog2[a_loc], prog2[b_loc] = prog2[b_loc], prog2[a_loc]
            else:
                a_loc = prog.index(a)
                b_loc = prog.index(b)
                prog[a_loc], prog[b_loc] = prog[b_loc], prog[a_loc]
    return ''.join(prog), ''.join(prog2)


def test_shuffle():
    assert shuffle(['s1'], 'abcde') == 'eabcd'
    assert shuffle(['s1', 'x3/4'], 'abcde') == 'eabdc'
    assert shuffle(['s1', 'x3/4', 'pe/b'], 'abcde') == 'baedc'


def get_cycles(initial, final):
    f = {x: final[i] for i, x in enumerate(initial)}
    cycles = []
    while len(initial) > 0:
        start = initial[0]
        initial = initial.replace(start, '')
        cycle = [start]
        x = f[start]
        initial = initial.replace(x, '')
        while x != start:
            cycle.append(x)
            x = f[x]
            initial = initial.replace(x, '')
        cycles.append(cycle)
    return cycles


def apply_perms(initial, cycles, power):
    perm = {}
    for cycle in cycles:
        cycle_length = len(cycle)
        perm.update({v: cycle[(i + power) % cycle_length] for i, v in enumerate(cycle)})
    return ''.join(perm[c] for c in initial)


def test_puzzle_shuffle():
    assert shuffle(INPUTS, 'abcdefghijklmnop') == ('cknmidebghlajpfo', 'abcdefghijklmnop')
    # for second part raise this to 1_000_000_000
    # let's figure out permutations to simplify this
    # a c n p o f d m j h b k l   g e i
    # c n p o f d m j h b k l a   e i g
    # 13                          3
    p_13 = ['a', 'c', 'n', 'p', 'o', 'f', 'd', 'm', 'j', 'h', 'b', 'k', 'l']
    p_3 = ['e', 'i', 'g']
    assert get_cycles('abcdefghijklmnop', 'cknmidebghlajpfo') == [p_13, p_3]
    # assert 1_000_000_000 % 13 == 12
    # assert 1_000_000_000 % 3 == 1
    # perm = {v: p_3[(i + 1_000_000_000) % 3] for i, v in enumerate(p_3)}
    # perm.update({v: p_13[(i + 1_000_000_000) % 13] for i, v in enumerate(p_13)})
    # assert ''.join(perm[c] for c in 'abcdefghijklmnop') == 'lhafioejgmbkdcpn'
    assert apply_perms('abcdefghijklmnop', [p_13, p_3], 1) == 'cknmidebghlajpfo'
    assert apply_perms('abcdefghijklmnop', [p_13, p_3], 1_000_000_000) == 'lhafioejgmbkdcpn'
    # why is 'lhafioejgmbkdcpn' not right? ...
    #
    #
    # Finally figured it out, need to separate the letter specific swapping from position swaps
    assert shuffle(INPUTS, 'abcdefghijklmnop', split=True) == ('nbdfcpoejgamhilk', 'lkinbmhjpgofaced')
    # positional permutations
    perms_position = get_cycles('abcdefghijklmnop', 'nbdfcpoejgamhilk')
    assert perms_position == [['a', 'n', 'i', 'j', 'g', 'o', 'l', 'm', 'h', 'e', 'c', 'd', 'f', 'p', 'k'],
                              ['b']]
    # letter shift permutations
    perms_labels = get_cycles('abcdefghijklmnop', 'lkinbmhjpgofaced')
    assert perms_labels == [['a', 'l', 'f', 'm'],
                            ['b', 'k', 'o', 'e'],
                            ['c', 'i', 'p', 'd', 'n'],
                            ['g', 'h', 'j']]
    assert apply_perms(apply_perms('abcdefghijklmnop', perms_position, 1),
                       perms_labels, 1) == 'cknmidebghlajpfo'
    assert apply_perms(apply_perms('abcdefghijklmnop', perms_position, 1_000_000_000),
                       perms_labels, 1_000_000_000) == 'cbolhmkgfpenidaj'
