def deal_into(deck):
    return deck[::-1]


def cut(param, deck):
    return deck[param:] + deck[:param]


def increment(param, deck):
    pos = 0
    new_order = [''] * len(deck)
    for d in deck:
        new_order[pos] = d
        pos += param
        pos %= len(deck)
    return new_order


def shuffle(lines, deck, position):
    for line in lines:
        words = line.strip().split(' ')
        if words[0] == 'cut':
            deck = cut(int(words[1]), deck)
            continue
        if words[1] == 'into':
            deck = deal_into(deck)
            continue
        if words[1] == 'with':
            deck = increment(int(words[3]), deck)
            continue
    for i, card in enumerate(deck):
        if card == position:
            return i


def pseudo_shuffle(lines, deck_size, position):
    for line in lines:
        words = line.strip().split(' ')
        if words[1] == 'into':
            position = deck_size - position - 1
        if words[0] == 'cut':
            position = position - int(words[1])
        if words[1] == 'with':
            position = int(words[3])*position
        position %= deck_size
    return position


def eqn_shuffle(lines, deck_size):
    m = 1
    b = 0
    for line in lines:
        words = line.strip().split(' ')
        if words[1] == 'into':
            m = -m
            b = deck_size -1 - b
        if words[0] == 'cut':
            b = b - int(words[1])
        if words[1] == 'with':
            m = int(words[3]) * m
            b = int(words[3]) * b
    return m % deck_size, b % deck_size


def test_deal_into_new_stack():
    deck = range(5)
    assert deal_into(deck) == deck[::-1]


def test_cut():
    deck = list(range(10))
    assert cut(3, deck) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert cut(-4, deck) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]


def test_increment():
    deck = list(range(10))
    assert increment(3, deck) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]


def test_sequence1():
    deck = list(range(10))
    deck = increment(7, deck)
    deck = deal_into(deck)
    deck = deal_into(deck)
    assert deck == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]


def test_sequence2():
    deck = list(range(10))
    deck = cut(6, deck)
    deck = increment(7, deck)
    deck = deal_into(deck)
    assert deck == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]


def test_submission():
    deck = list(range(10007))
    position = 2019
    with open('input_day_22.txt') as fp:
        lines = fp.read().split('\n')
    assert shuffle(lines, deck, position) == 6526
    assert pseudo_shuffle(lines, 10007, position) == 6526
    assert eqn_shuffle(lines, 10007) == (2183, 2129)
    m, b = eqn_shuffle(lines, 10007)
    assert (m * position + b) % 10007 == 6526


def test_submission2():
    deck_size = int('119315717514047')
    total_shuffles = 101741582076661
    final_position = 2020
    with open('input_day_22.txt') as fp:
        lines = fp.read().split('\n')
    m, b = eqn_shuffle(lines, deck_size)
    #assert (m, b) == (40286879916729, 37260864847148)
    mf = pow(m, total_shuffles, deck_size)
    mf_inv = pow(mf, deck_size-2, deck_size)
    mm1_inv = pow(m-1, deck_size-2, deck_size)
    bf = b * mm1_inv * (mf - 1) % deck_size
    initial = mf_inv * (final_position - bf) % deck_size
    assert initial == 79855812422607
    assert (mf * initial + bf) % deck_size == 2020