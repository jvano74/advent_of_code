from pathlib import Path
from collections import defaultdict


class Puzzle:
    """
    --- Day 8: Haunted Wasteland ---
    You're still riding a camel across Desert Island when you spot a sandstorm
    quickly approaching. When you turn to warn the Elf, she disappears before
    your eyes! To be fair, she had just finished warning you about ghosts a few
    minutes ago.

    One of the camel's pouches is labeled "maps" - sure enough, it's full of
    documents (your puzzle input) about how to navigate the desert. At least,
    you're pretty sure that's what they are; one of the documents contains a
    list of left/right instructions, and the rest of the documents seem to
    describe some kind of network of labeled nodes.

    It seems like you're meant to use the left/right instructions to navigate
    the network. Perhaps if you have the camel follow the same instructions, you
    can escape the haunted wasteland!

    After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You
    feel like AAA is where you are now, and you have to follow the left/right
    instructions until you reach ZZZ.

    This format defines each node of the network individually. For example:

    RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)

    Starting with AAA, you need to look up the next element based on the next
    left/right instruction in your input. In this example, start with AAA and go
    right (R) by choosing the right element of AAA, CCC. Then, L means to choose
    the left element of CCC, ZZZ. By following the left/right instructions, you
    reach ZZZ in 2 steps.

    Of course, you might not find ZZZ right away. If you run out of left/right
    instructions, repeat the whole sequence of instructions as necessary: RL
    really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation
    that takes 6 steps to reach ZZZ:

    LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)

    Starting at AAA, follow the left/right instructions. How many steps are
    required to reach ZZZ?

    Your puzzle answer was 19637.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The sandstorm is upon you and you aren't any closer to escaping the
    wasteland. You had the camel follow the instructions, but you've barely left
    your starting position. It's going to take significantly more steps to
    escape!

    What if the map isn't for people - what if the map is for ghosts? Are ghosts
    even bound by the laws of spacetime? Only one way to find out.

    After examining the maps a bit longer, your attention is drawn to a curious
    fact: the number of nodes with names ending in A is equal to the number
    ending in Z! If you were a ghost, you'd probably just start at every node
    that ends with A and follow all of the paths at the same time until they all
    simultaneously end up at nodes that end with Z.

    For example:

    LR

    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)

    Here, there are two starting nodes, 11A and 22A (because they both end with
    A). As you follow each left/right instruction, use that instruction to
    simultaneously navigate away from both nodes you're currently on. Repeat
    this process until all of the nodes you're currently on end with Z. (If only
    some of the nodes you're on end with Z, they act like any other node and you
    continue as normal.) In this example, you would proceed as follows:

    Step 0: You are at 11A and 22A.
    Step 1: You choose all of the left paths, leading you to 11B and 22B.
    Step 2: You choose all of the right paths, leading you to 11Z and 22C.
    Step 3: You choose all of the left paths, leading you to 11B and 22Z.
    Step 4: You choose all of the right paths, leading you to 11Z and 22B.
    Step 5: You choose all of the left paths, leading you to 11B and 22C.
    Step 6: You choose all of the right paths, leading you to 11Z and 22Z.

    So, in this example, you end up entirely on nodes that end in Z after 6
    steps.

    Simultaneously start on every node that ends with A. How many steps does it
    take before you're only on nodes that end with Z?

    Your puzzle answer was 8811050362409.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open(Path(__file__).parent / "2023_08_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")

RAW_SAMPLE_1 = [
    "RL",
    "",
    "AAA = (BBB, CCC)",
    "BBB = (DDD, EEE)",
    "CCC = (ZZZ, GGG)",
    "DDD = (DDD, DDD)",
    "EEE = (EEE, EEE)",
    "GGG = (GGG, GGG)",
    "ZZZ = (ZZZ, ZZZ)",
]

RAW_SAMPLE_2 = ["LLR", "", "AAA = (BBB, BBB)", "BBB = (AAA, ZZZ)", "ZZZ = (ZZZ, ZZZ)"]

RAW_SAMPLE_3 = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)",
]


class Wasteland:
    def __init__(self, raw_map) -> None:
        self.instructions = raw_map[0]
        self.left = dict()
        self.right = dict()
        for raw_node in raw_map[2:]:
            name, raw_branches = raw_node.split(" = ")
            self.left[name], self.right[name] = raw_branches[1:-1].split(", ")

    def navigate(self, start="AAA", end="ZZZ"):
        current = start
        moves = 0
        ins_len = len(self.instructions)
        while current != end:
            next_step = self.instructions[moves % ins_len]
            if next_step == "L":
                current = self.left[current]
            elif next_step == "R":
                current = self.right[current]
            else:
                raise Exception("Invalid direction")
            moves += 1
        return moves

    def ghost_navigate(self):
        current = [k for k in self.left.keys() if k[2] == "A"]
        number_of_ghosts = len(current)
        end_recurrance = defaultdict(list)
        moves = 0
        ins_len = len(self.instructions)
        while True:
            end = True
            for index, location in enumerate(current):
                if location[2] == "Z":
                    recurance_marker = (index, moves % ins_len, location)
                    end_recurrance[recurance_marker].append(
                        (moves // ins_len, ins_len, moves % ins_len)
                    )
                else:
                    end = False
            if end:
                return moves, end_recurrance
            looped = 0
            for key, value in end_recurrance.items():
                if len(value) > 3:
                    looped += 1
            if looped == number_of_ghosts:
                return moves, end_recurrance

            next_step = self.instructions[moves % ins_len]
            if next_step == "L":
                current = [self.left[g] for g in current]
            elif next_step == "R":
                current = [self.right[g] for g in current]
            else:
                raise Exception("Invalid direction")
            moves += 1


def test_wasteland():
    sample_wasteland_1 = Wasteland(RAW_SAMPLE_1)
    assert sample_wasteland_1.navigate() == 2
    sample_wasteland_2 = Wasteland(RAW_SAMPLE_2)
    assert sample_wasteland_2.navigate() == 6

    sample_wasteland_3 = Wasteland(RAW_SAMPLE_3)
    duration, recurance = sample_wasteland_3.ghost_navigate()
    assert duration == 6

    my_wasteland = Wasteland(RAW_INPUT)
    assert my_wasteland.navigate() == 19637
    duration, recurance = my_wasteland.ghost_navigate()
    cycle_length = len(my_wasteland.instructions)
    number_of_cycles = 1
    for k, v in recurance.items():
        number_of_cycles *= v[0][0]
    assert number_of_cycles * cycle_length == 8811050362409
