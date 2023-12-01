class Solution:
    """
    --- Day 17: No Such Thing as Too Much ---
    The elves bought too much eggnog again - 150 liters this time.
    To fit it all into your refrigerator, you'll need to move it into smaller containers.
    You take an inventory of the capacities of the available containers.

    For example, suppose you have containers of size 20, 15, 10, 5, and 5 liters.
    If you need to store 25 liters, there are four ways to do it:

    15 and 10
    20 and 5 (the first 5)
    20 and 5 (the second 5)
    15, 5, and 5
    Filling all containers entirely, how many different combinations of
    containers can exactly fit all 150 liters of eggnog?
    """


CONTAINERS = sorted(
    [11, 30, 47, 31, 32, 36, 3, 1, 5, 3, 32, 36, 15, 11, 46, 26, 28, 1, 19, 3],
    reverse=True,
)


def does_subset_equal_150(mask, list):
    sum = 0
    containers = 0
    for x in list:
        if mask == 0:
            return sum == 150, containers
        if mask % 2 == 1:
            sum += x
            containers += 1
            if sum > 150:
                return False, containers
        mask //= 2
    return sum == 150, containers


def test_subset():
    assert does_subset_equal_150(1, [100, 99, 50]) == (False, 1)
    assert does_subset_equal_150(5, [100, 99, 50]) == (True, 2)


def test_submission():
    count = 0
    min_containers = len(CONTAINERS)
    for n in range(pow(2, len(CONTAINERS))):
        fits, containers = does_subset_equal_150(n, CONTAINERS)
        if fits:
            min_containers = min(min_containers, containers)
            count += 1
    assert count == 4372
    assert min_containers == 4
    count = 0
    for n in range(pow(2, len(CONTAINERS))):
        fits, containers = does_subset_equal_150(n, CONTAINERS)
        if fits and containers == 4:
            count += 1
    assert count == 4
