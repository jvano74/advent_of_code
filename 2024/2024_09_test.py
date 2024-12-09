from pathlib import Path
from typing import List, NamedTuple
from collections import defaultdict


class Puzzle:
    """
    --- Day 9: Disk Fragmenter ---

    Another push of the button leaves you in the familiar hallways of some
    friendly amphipods! Good thing you each somehow got your own personal mini
    submarine. The Historians jet away in search of the Chief, mostly by driving
    directly into walls.

    While The Historians quickly figure out how to pilot these things, you
    notice an amphipod in the corner struggling with his computer. He's trying
    to make more contiguous free space by compacting all of the files, but his
    program isn't working; you offer to help.

    He shows you the disk map (your puzzle input) he's already generated. For
    example:

    2333133121414131402

    The disk map uses a dense format to represent the layout of files and free
    space on the disk. The digits alternate between indicating the length of a
    file and the length of free space.

    So, a disk map like 12345 would represent a one-block file, two blocks of
    free space, a three-block file, four blocks of free space, and then a
    five-block file. A disk map like 90909 would represent three nine-block
    files in a row (with no free space between them).

    Each file on disk also has an ID number based on the order of the files as
    they appear before they are rearranged, starting with ID 0. So, the disk map
    12345 has three files: a one-block file with ID 0, a three-block file with
    ID 1, and a five-block file with ID 2. Using one character for each block
    where digits are the file ID and . is free space, the disk map 12345
    represents these individual blocks:

    0..111....22222

    The first example above, 2333133121414131402, represents these individual
    blocks:

    00...111...2...333.44.5555.6666.777.888899

    The amphipod would like to move file blocks one at a time from the end of
    the disk to the leftmost free space block (until there are no gaps remaining
    between file blocks). For the disk map 12345, the process looks like this:

    0..111....22222
    02.111....2222.
    022111....222..
    0221112...22...
    02211122..2....
    022111222......

    The first example requires a few more steps:

    00...111...2...333.44.5555.6666.777.888899
    009..111...2...333.44.5555.6666.777.88889.
    0099.111...2...333.44.5555.6666.777.8888..
    00998111...2...333.44.5555.6666.777.888...
    009981118..2...333.44.5555.6666.777.88....
    0099811188.2...333.44.5555.6666.777.8.....
    009981118882...333.44.5555.6666.777.......
    0099811188827..333.44.5555.6666.77........
    00998111888277.333.44.5555.6666.7.........
    009981118882777333.44.5555.6666...........
    009981118882777333644.5555.666............
    00998111888277733364465555.66.............
    0099811188827773336446555566..............

    The final step of this file-compacting process is to update the filesystem
    checksum. To calculate the checksum, add up the result of multiplying each
    of these blocks' position with the file ID number it contains. The leftmost
    block is in position 0. If a block contains free space, skip it instead.

    Continuing the first example, the first few blocks' position multiplied by
    its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 =
    32, and so on. In this example, the checksum is the sum of these, 1928.

    Compact the amphipod's hard drive using the process he requested. What is
    the resulting filesystem checksum? (Be careful copy/pasting the input for
    this puzzle; it is a single, very long line.)

    Your puzzle answer was 6399153661894.

    --- Part Two ---
    Upon completion, two things immediately become clear. First, the disk
    definitely has a lot more contiguous free space, just like the amphipod
    hoped. Second, the computer is running much more slowly! Maybe introducing
    all of that file system fragmentation was a bad idea?

    The eager amphipod already has a new plan: rather than move individual
    blocks, he'd like to try compacting the files on his disk by moving whole
    files instead.

    This time, attempt to move whole files to the leftmost span of free space
    blocks that could fit the file. Attempt to move each file exactly once in
    order of decreasing file ID number starting with the file with the highest
    file ID number. If there is no span of free space to the left of a file that
    is large enough to fit the file, the file does not move.

    The first example from above now proceeds differently:

    00...111...2...333.44.5555.6666.777.888899
    0099.111...2...333.44.5555.6666.777.8888..
    0099.1117772...333.44.5555.6666.....8888..
    0099.111777244.333....5555.6666.....8888..
    00992111777.44.333....5555.6666.....8888..

    The process of updating the filesystem checksum is the same; now, this
    example's checksum would be 2858.

    Start over, now compacting the amphipod's hard drive using this new method
    instead. What is the resulting filesystem checksum?

    Your puzzle answer was 6421724645083.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


with open(Path(__file__).parent / "2024_09_input.txt") as fp:
    MY_DISK_MAP = fp.read()

SAMPLE_DISK_MAP = "2333133121414131402"


def expand(disk_map: str):
    block_id = 0
    result = []
    data = 1
    for block_size in disk_map:
        for _ in range(int(block_size)):
            result.append(block_id if data else ".")
        if data:
            block_id += 1
        data = 1 - data
    return result


def defrag(native_disk):
    result = []
    while native_disk:
        from_left = native_disk.pop(0)
        if from_left != ".":
            result.append(from_left)
            continue
        filling_from_right = True
        while filling_from_right:
            from_right = native_disk.pop()
            if from_right != ".":
                result.append(from_right)
                filling_from_right = False
    return result


def checksum(native_disk):
    return sum(pos * value for pos, value in enumerate(native_disk))


def test_expand():
    assert expand(SAMPLE_DISK_MAP) == [
        "." if c == "." else int(c)
        for c in "00...111...2...333.44.5555.6666.777.888899"
    ]
    assert defrag(expand(SAMPLE_DISK_MAP)) == [
        int(c) for c in "0099811188827773336446555566"
    ]
    assert checksum(defrag(expand(SAMPLE_DISK_MAP))) == 1928
    assert MY_DISK_MAP[:3] == "156"
    assert MY_DISK_MAP[-3:] == "746"
    assert checksum(defrag(expand(MY_DISK_MAP))) == 6399153661894
    # First attempt 90575306662 was too low,
    # Realized needed to allow for block_id with more than 1 digit


def expand2(disk_map: str):
    disk_map = [int(bs) for bs in disk_map]
    block_id = 0
    block_start = 0
    data = 1
    data_blocks = {}
    free_space = {}
    for block_size in disk_map:
        if data:
            data_blocks[block_id] = (block_start, block_size)
            block_id += 1
        else:
            if block_size:
                free_space[block_start] = block_size
        block_start += block_size
        data = 1 - data
    return data_blocks, free_space


def defrag2(data_blocks, free_space):
    data_order = sorted(
        (-start, block_id) for block_id, (start, _) in data_blocks.items()
    )
    for _, block_id in data_order:
        (block_start, block_size) = data_blocks[block_id]
        free_order = sorted(k for k in free_space.keys() if k < block_start)
        for potential_start in free_order:
            if block_size <= free_space[potential_start]:
                free_space_size = free_space.pop(potential_start)
                data_blocks[block_id] = (potential_start, block_size)

                remaining_free_size = free_space_size - block_size
                if remaining_free_size:
                    free_space[potential_start + block_size] = remaining_free_size
                break


def checksum2(native_disk):
    total = 0
    for block_id, (start, size) in native_disk.items():
        for delta in range(size):
            total += block_id * (start + delta)
    return total


def test_expand2():
    data_blocks, free_space = expand2(SAMPLE_DISK_MAP)
    assert data_blocks == {
        0: (0, 2),
        1: (5, 3),
        2: (11, 1),
        3: (15, 3),
        4: (19, 2),
        5: (22, 4),
        6: (27, 4),
        7: (32, 3),
        8: (36, 4),
        9: (40, 2),
    }
    assert free_space == {2: 3, 8: 3, 12: 3, 18: 1, 21: 1, 26: 1, 31: 1, 35: 1}
    defrag2(data_blocks, free_space)
    assert data_blocks == {
        0: (0, 2),
        1: (5, 3),
        2: (4, 1),
        3: (15, 3),
        4: (12, 2),
        5: (22, 4),
        6: (27, 4),
        7: (8, 3),
        8: (36, 4),
        9: (2, 2),
    }
    print(free_space)
    assert free_space == {18: 1, 21: 1, 26: 1, 31: 1, 35: 1, 14: 1}
    assert checksum2(data_blocks) == 2858

    data_blocks, free_space = expand2(MY_DISK_MAP)
    defrag2(data_blocks, free_space)
    assert checksum2(data_blocks) == 6421724645083
    # First pass 8554338581103 is too high
    # Realized I was allowing shifting to the right so fixed
    # Got 6421724645083 which was correct answer
