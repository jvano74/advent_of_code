import math
from collections import defaultdict


class Puzzle:
    """
    --- Day 20: Infinite Elves and Infinite Houses ---
    To keep the Elves busy, Santa has them deliver some presents by hand, door-to-door. He sends them down a street
    with infinite houses numbered sequentially: 1, 2, 3, 4, 5, and so on.

    Each Elf is assigned a number, too, and delivers presents to houses based on that number:

    The first Elf (number 1) delivers presents to every house: 1, 2, 3, 4, 5, ....
    The second Elf (number 2) delivers presents to every second house: 2, 4, 6, 8, 10, ....
    Elf number 3 delivers presents to every third house: 3, 6, 9, 12, 15, ....

    There are infinitely many Elves, numbered starting with 1. Each Elf delivers presents equal to ten times his or
    her number at each house.

    So, the first nine houses on the street end up like this:

    House 1 got 10 presents.
    House 2 got 30 presents.
    House 3 got 40 presents.
    House 4 got 70 presents.
    House 5 got 60 presents.
    House 6 got 120 presents.
    House 7 got 80 presents.
    House 8 got 150 presents.
    House 9 got 130 presents.

    The first house gets 10 presents: it is visited only by Elf 1, which delivers 1 * 10 = 10 presents.
    The fourth house gets 70 presents, because it is visited by Elves 1, 2, and 4,
    for a total of 10 + 20 + 40 = 70 presents.

    What is the lowest house number of the house to get at least as many presents as the number in your puzzle input?

    Your puzzle input is 33100000.

    --- Part Two ---
    The Elves decide they don't want to visit an infinite number of houses. Instead, each Elf will stop after
    delivering presents to 50 houses. To make up for it, they decide to deliver presents equal to eleven times
    their number at each house.

    With these changes, what is the new lowest house number of the house to get at least as many presents as
    the number in your puzzle input?
    """
    pass


def prime_factors(n):
    factors = {}
    while n % 2 == 0:
        if 2 not in factors:
            factors[2] = 1
        else:
            factors[2] += 1
        n = n / 2
    for i in range(3, math.ceil(math.sqrt(n+1)), 2):
        while n % i == 0:
            if i not in factors:
                factors[i] = 1
            else:
                factors[i] += 1
            n = n / i
    if n > 2:
        factors[n] = 1
    return factors


def test_prime_factors():
    assert prime_factors(1) == {}
    assert prime_factors(2) == {2: 1}
    assert prime_factors(3) == {3: 1}
    assert prime_factors(4) == {2: 2}
    assert prime_factors(5) == {5: 1}
    assert prime_factors(6) == {2: 1, 3: 1}
    assert prime_factors(7) == {7: 1}
    assert prime_factors(8) == {2: 3}
    assert prime_factors(9) == {3: 2}


def present_sum_from_prime_factors(n, present_multiplier=10):
    factors = prime_factors(n)
    result = 1
    for factor in factors:
        sum_factor = sum(pow(factor, i) for i in range(factors[factor]+1))
        result *= sum_factor
    return present_multiplier * result


def test_present_sum_from_prime_factors():
    assert present_sum_from_prime_factors(1, 1) == 1
    assert present_sum_from_prime_factors(2, 1) == 3
    assert present_sum_from_prime_factors(3, 1) == 4
    assert present_sum_from_prime_factors(4, 1) == 7
    assert present_sum_from_prime_factors(5, 1) == 6
    assert present_sum_from_prime_factors(6, 1) == 12
    assert present_sum_from_prime_factors(7, 1) == 8
    assert present_sum_from_prime_factors(8, 1) == 15
    assert present_sum_from_prime_factors(9, 1) == 13


def get_lazy_presents(n, max_houses=1, num_mult=11):
    lazy_sum = 0
    for i in range(1, max_houses+1):
        if n % i == 0:
            lazy_sum += n // i
    return num_mult*lazy_sum


def min_house(total, multiplier=10, starting_house=1, ending_house=None, max_houses=None):
    house = starting_house
    if max_houses is None:
        while present_sum_from_prime_factors(house, multiplier) < total:
            if ending_house is not None and house > ending_house:
                raise Exception('Past ending house.')
            house += 1
    else:
        while get_lazy_presents(house, max_houses, multiplier) < total:
            if ending_house is not None and house > ending_house:
                raise Exception('Past ending house.')
            house += 1
    return house


def test_min_house():
    assert min_house(33_100_000) == 776_160


def test_min_house2():
    # We can use the above infinite elf case to determine a good starting house for the 50 house case
    # We will need to go at least as far as an infinite elf case with an 11 gift give
    # starting_house = min_house(33_100_000, 11)
    # assert starting_house == 720_720  # note a bit lower than the 10 gift give
    starting_house = 720_720
    last_house = 33_100_000 // 11
    assert min_house(33_100_000, 11, starting_house, last_house, 50) == 786_240
