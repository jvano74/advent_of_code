from pathlib import Path


class Puzzle:
    """
    --- Day 20: Firewall Rules ---
    You'd like to set up a small hidden computer here so you can use it to get back into the network later. However,
    the corporate firewall only allows communication with certain external IP addresses.

    You've retrieved the list of blocked IPs from the firewall, but the list seems to be messy and poorly maintained,
    and it's not clear which IPs are allowed. Also, rather than being written in dot-decimal notation, they are written
    as plain 32-bit integers, which can have any value from 0 through 4294967295, inclusive.

    For example, suppose only the values 0 through 9 were valid, and that you retrieved the following blacklist:

    5-8
    0-2
    4-7

    The blacklist specifies ranges of IPs (inclusive of both the start and end value) that are not allowed.
    Then, the only IPs that this firewall allows are 3 and 9, since those are the only numbers not in any range.

    Given the list of blocked IPs you retrieved from the firewall (your puzzle input), what is the lowest-valued IP
    that is not blocked?

    --- Part Two ---
    How many IPs are allowed by the blacklist?
    """

    pass


with open(Path(__file__).parent / "2016_20_input.txt") as fp:
    INPUTS = [tuple(int(d) for d in line.strip().split("-")) for line in fp]


def lowest_non_blocked(blocked_ranges, current_min=0):
    for block_low, block_high in blocked_ranges:
        if block_low <= current_min < block_high:
            return lowest_non_blocked(blocked_ranges, block_high + 1)
    return current_min


def order_blocked(blocked_ranges):
    sorted_ranges = sorted(blocked_ranges)
    current_low, current_high = sorted_ranges[0]
    ranges = []
    count = 0
    for block_low, block_high in sorted_ranges[1:]:
        if block_low <= current_high + 1:
            current_high = max(current_high, block_high)
        else:
            ranges.append((current_low, current_high))
            count += current_high - current_low + 1
            current_low, current_high = block_low, block_high
    ranges.append((current_low, current_high))
    count += current_high - current_low + 1
    return count, ranges


def test_lowest_non_blocked():
    # assert lowest_non_blocked([(5, 8), (0, 2), (4, 7)]) == 3
    sorted_ranges = order_blocked([(5, 8), (0, 2), (4, 7)])
    assert sorted_ranges[1][0][1] + 1 == 3

    # assert lowest_non_blocked(INPUTS) == 22887907
    sorted_ranges = order_blocked(INPUTS)
    assert sorted_ranges[1][0][1] + 1 == 22887907
    open_ips = 4294967295 + 1 - sorted_ranges[0]
    assert open_ips == 109
