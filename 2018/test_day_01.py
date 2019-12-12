def find_repeat(drifts):
    found = set([0])
    total = 0
    while True:
        for d in drifts:
            total += d
            if total in found:
                return total
            found.add(total)


def test_submission():
    with open('input_day_01.txt') as fp:
        raw_data = fp.read()
    freq_drifts = [int(f) for f in raw_data.split('\n')]
    assert sum(freq_drifts) == 420
    assert find_repeat([1,-1]) == 0
    assert find_repeat([3, 3, 4, -2, -4]) == 10
    assert find_repeat(freq_drifts) == 227