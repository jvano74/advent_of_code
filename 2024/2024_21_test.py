from queue import PriorityQueue
from itertools import product
from typing import NamedTuple
from functools import cache
from collections import defaultdict, Counter


class Puzzle:
    """
    --- Day 21: Keypad Conundrum ---
    As you teleport onto Santa's Reindeer-class starship, The Historians begin
    to panic: someone from their search party is missing. A quick life-form scan
    by the ship's computer reveals that when the missing Historian teleported,
    he arrived in another part of the ship.

    The door to that area is locked, but the computer can't open it; it can only
    be opened by physically typing the door codes (your puzzle input) on the
    numeric keypad on the door.

    The numeric keypad has four rows of buttons: 789, 456, 123, and finally an
    empty gap followed by 0A. Visually, they are arranged like this:

    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+

    Unfortunately, the area outside the door is currently depressurized and
    nobody can go near the door. A robot needs to be sent instead.

    The robot has no problem navigating the ship and finding the numeric keypad,
    but it's not designed for button pushing: it can't be told to push a
    specific button directly. Instead, it has a robotic arm that can be
    controlled remotely via a directional keypad.

    The directional keypad has two rows of buttons: a gap / ^ (up) / A
    (activate) on the first row and < (left) / v (down) / > (right) on the
    second row. Visually, they are arranged like this:

        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+

    When the robot arrives at the numeric keypad, its robotic arm is pointed at
    the A button in the bottom right corner. After that, this directional keypad
    remote control must be used to maneuver the robotic arm: the up / down /
    left / right buttons cause it to move its arm one button in that direction,
    and the A button causes the robot to briefly move forward, pressing the
    button being aimed at by the robotic arm.

    For example, to make the robot type 029A on the numeric keypad, one sequence
    of inputs on the directional keypad you could use is:

    < to move the arm from A (its initial position) to 0.
    A to push the 0 button.
    ^A to move the arm to the 2 button and push it.
    >^^A to move the arm to the 9 button and push it.
    vvvA to move the arm to the A button and push it.

    In total, there are three shortest possible sequences of button presses on
    this directional keypad that would cause the robot to type 029A:
    <A^A>^^AvvvA, <A^A^>^AvvvA, and <A^A^^>AvvvA.

    Unfortunately, the area containing this directional keypad remote control is
    currently experiencing high levels of radiation and nobody can go near it. A
    robot needs to be sent instead.

    When the robot arrives at the directional keypad, its robot arm is pointed
    at the A button in the upper right corner. After that, a second, different
    directional keypad remote control is used to control this robot (in the same
    way as the first robot, except that this one is typing on a directional
    keypad instead of a numeric keypad).

    There are multiple shortest possible sequences of directional keypad button
    presses that would cause this robot to tell the first robot to type 029A on
    the door. One such sequence is v<<A>>^A<A>AvA<^AA>A<vAAA>^A.

    Unfortunately, the area containing this second directional keypad remote
    control is currently -40 degrees! Another robot will need to be sent to type
    on that directional keypad, too.

    There are many shortest possible sequences of directional keypad button
    presses that would cause this robot to tell the second robot to tell the
    first robot to eventually type 029A on the door. One such sequence is
    <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A.

    Unfortunately, the area containing this third directional keypad remote
    control is currently full of Historians, so no robots can find a clear path
    there. Instead, you will have to type this sequence yourself.

    Were you to choose this sequence of button presses, here are all of the
    buttons that would be pressed on your directional keypad, the two robots'
    directional keypads, and the numeric keypad:

    <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    v<<A>>^A<A>AvA<^AA>A<vAAA>^A
    <A^A>^^AvvvA
    029A

    In summary, there are the following keypads:

    One directional keypad that you are using.
    Two directional keypads that robots are using.
    One numeric keypad (on a door) that a robot is using.

    It is important to remember that these robots are not designed for button
    pushing. In particular, if a robot arm is ever aimed at a gap where no
    button is present on the keypad, even for an instant, the robot will panic
    unrecoverably. So, don't do that. All robots will initially aim at the
    keypad's A key, wherever it is.

    To unlock the door, five codes will need to be typed on its numeric keypad.
    For example:

    029A
    980A
    179A
    456A
    379A

    For each of these, here is a shortest sequence of button presses you could
    type to cause the desired code to be typed on the numeric keypad:

    029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
    179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
    456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
    379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A

    The Historians are getting nervous; the ship computer doesn't remember
    whether the missing Historian is trapped in the area containing a giant
    electromagnet or molten lava. You'll need to make sure that for each of the
    five codes, you find the shortest sequence of button presses necessary.

    The complexity of a single code (like 029A) is equal to the result of
    multiplying these two values:

    The length of the shortest sequence of button presses you need to type on
    your directional keypad in order to cause the code to be typed on the
    numeric keypad; for 029A, this would be 68.

    The numeric part of the code (ignoring leading zeroes); for 029A, this would
    be 29.

    In the above example, complexity of the five codes can be found by
    calculating 68 * 29, 60 * 980, 68 * 179, 64 * 456, and 64 * 379. Adding
    these together produces 126384.

    Find the fewest number of button presses you'll need to perform in order to
    cause the robot in front of the door to type each code. What is the sum of
    the complexities of the five codes on your list?

    Your puzzle answer was 137870.

    --- Part Two ---
    Just as the missing Historian is released, The Historians realize that a
    second member of their search party has also been missing this entire time!

    A quick life-form scan reveals the Historian is also trapped in a locked
    area of the ship. Due to a variety of hazards, robots are once again
    dispatched, forming another chain of remote control keypads managing
    robotic-arm-wielding robots.

    This time, many more robots are involved. In summary, there are the
    following keypads:

    One directional keypad that you are using.
    25 directional keypads that robots are using.
    One numeric keypad (on a door) that a robot is using.

    The keypads form a chain, just like before: your directional keypad controls
    a robot which is typing on a directional keypad which controls a robot which
    is typing on a directional keypad... and so on, ending with the robot which
    is typing on the numeric keypad.

    The door codes are the same this time around; only the number of robots and
    directional keypads has changed.

    Find the fewest number of button presses you'll need to perform in order to
    cause the robot in front of the door to type each code. What is the sum of
    the complexities of the five codes on your list?


    """


SAMPLE_CODES = ["029A", "980A", "179A", "456A", "379A"]

CODES = ["805A", "170A", "129A", "283A", "540A"]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)

    def dist_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def nbhd(self, r=1):
        nbhd = set()
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if abs(dx) + abs(dy) <= r:
                    nbhd.add(self + Pt(dx, dy))
        return nbhd


DELTA = {
    "^": Pt(0, -1),
    "<": Pt(-1, 0),
    "v": Pt(0, 1),
    ">": Pt(1, 0),
}

MOVES = {v: k for k, v in DELTA.items()}


def validate_instructions(instructions):
    for invalid in (
        "<^<",
        "<^^<",
        "<^^^<",
        "<v<",
        "<vv<",
        "<vvv<",
        ">^>",
        ">^^>",
        ">^^^>",
        ">v>",
        ">vv>",
        ">vvv>",
        "^<^",
        "^<<^",
        "^>^",
        "^>>^",
        "v<v",
        "v<<v",
        "v>v",
        "v>>v",
    ):
        if invalid in instructions:
            return False
    return True


class Robot:
    def __init__(self, keypad_type: str):
        self.min_transition = None

        if keypad_type == "directional":
            self.button = {
                Pt(1, 0): "^",
                Pt(2, 0): "A",
                Pt(0, 1): "<",
                Pt(1, 1): "v",
                Pt(2, 1): ">",
            }
            self.arm = Pt(2, 0)
        elif keypad_type == "keypad":
            self.button = {
                Pt(0, 0): "7",
                Pt(1, 0): "8",
                Pt(2, 0): "9",
                Pt(0, 1): "4",
                Pt(1, 1): "5",
                Pt(2, 1): "6",
                Pt(0, 2): "1",
                Pt(1, 2): "2",
                Pt(2, 2): "3",
                Pt(1, 3): "0",
                Pt(2, 3): "A",
            }
            self.arm = Pt(2, 3)

    def build_transition_map(self):
        self.min_transition = dict()
        for start_pt, start_id in self.button.items():
            for end_pt, end_id in self.button.items():
                self.min_transition[f"{start_id}:{end_id}"] = set()
                boundary = PriorityQueue()
                min_steps = None
                boundary.put((0, start_pt, [start_pt], ""))
                while not boundary.empty():
                    steps, current_pt, path, instructions = boundary.get()
                    if min_steps is not None and steps > min_steps:
                        continue
                    if current_pt == end_pt:
                        if min_steps is None:
                            min_steps = steps
                        if steps > min_steps:
                            continue
                        if validate_instructions(instructions):
                            self.min_transition[f"{start_id}:{end_id}"].add(
                                f"{instructions}A"
                            )
                        continue
                    for next_pt in current_pt.nbhd():
                        if next_pt not in self.button:
                            continue
                        if next_pt in path:
                            continue
                        new_path = path[:]
                        new_path.append(next_pt)
                        new_instructions = f"{instructions}{MOVES[next_pt-current_pt]}"
                        boundary.put((steps + 1, next_pt, new_path, new_instructions))


ROBOT_TO_KEYPAD_TRANSITIONS = {
    "7:7": {"A"},
    "7:8": {">A"},
    "7:9": {">>A"},
    "7:4": {"vA"},
    "7:5": {">vA", "v>A"},
    "7:6": {">>vA", "v>>A"},
    "7:1": {"vvA"},
    "7:2": {">vvA", "vv>A"},
    "7:3": {">>vvA", "vv>>A"},
    "7:0": {">vvvA"},
    "7:A": {">>vvvA"},
    "8:7": {"<A"},
    "8:8": {"A"},
    "8:9": {">A"},
    "8:4": {"v<A", "<vA"},
    "8:5": {"vA"},
    "8:6": {">vA", "v>A"},
    "8:1": {"<vvA", "vv<A"},
    "8:2": {"vvA"},
    "8:3": {">vvA", "vv>A"},
    "8:0": {"vvvA"},
    "8:A": {">vvvA", "vvv>A"},
    "9:7": {"<<A"},
    "9:8": {"<A"},
    "9:9": {"A"},
    "9:4": {"<<vA", "v<<A"},
    "9:5": {"v<A", "<vA"},
    "9:6": {"vA"},
    "9:1": {"<<vvA", "vv<<A"},
    "9:2": {"<vvA", "vv<A"},
    "9:3": {"vvA"},
    "9:0": {"vvv<A", "<vvvA"},
    "9:A": {"vvvA"},
    "4:7": {"^A"},
    "4:8": {"^>A", ">^A"},
    "4:9": {">>^A", "^>>A"},
    "4:4": {"A"},
    "4:5": {">A"},
    "4:6": {">>A"},
    "4:1": {"vA"},
    "4:2": {">vA", "v>A"},
    "4:3": {">>vA", "v>>A"},
    "4:0": {">vvA"},
    "4:A": {">>vvA"},
    "5:7": {"^<A", "<^A"},
    "5:8": {"^A"},
    "5:9": {"^>A", ">^A"},
    "5:4": {"<A"},
    "5:5": {"A"},
    "5:6": {">A"},
    "5:1": {"v<A", "<vA"},
    "5:2": {"vA"},
    "5:3": {">vA", "v>A"},
    "5:0": {"vvA"},
    "5:A": {">vvA", "vv>A"},
    "6:7": {"<<^A", "^<<A"},
    "6:8": {"^<A", "<^A"},
    "6:9": {"^A"},
    "6:4": {"<<A"},
    "6:5": {"<A"},
    "6:6": {"A"},
    "6:1": {"<<vA", "v<<A"},
    "6:2": {"v<A", "<vA"},
    "6:3": {"vA"},
    "6:0": {"<vvA", "vv<A"},
    "6:A": {"vvA"},
    "1:7": {"^^A"},
    "1:8": {">^^A", "^^>A"},
    "1:9": {">>^^A", "^^>>A"},
    "1:4": {"^A"},
    "1:5": {"^>A", ">^A"},
    "1:6": {">>^A", "^>>A"},
    "1:1": {"A"},
    "1:2": {">A"},
    "1:3": {">>A"},
    "1:0": {">vA"},
    "1:A": {">>vA"},
    "2:7": {"<^^A", "^^<A"},
    "2:8": {"^^A"},
    "2:9": {">^^A", "^^>A"},
    "2:4": {"^<A", "<^A"},
    "2:5": {"^A"},
    "2:6": {"^>A", ">^A"},
    "2:1": {"<A"},
    "2:2": {"A"},
    "2:3": {">A"},
    "2:0": {"vA"},
    "2:A": {">vA", "v>A"},
    "3:7": {"^^<<A", "<<^^A"},
    "3:8": {"<^^A", "^^<A"},
    "3:9": {"^^A"},
    "3:4": {"<<^A", "^<<A"},
    "3:5": {"^<A", "<^A"},
    "3:6": {"^A"},
    "3:1": {"<<A"},
    "3:2": {"<A"},
    "3:3": {"A"},
    "3:0": {"v<A", "<vA"},
    "3:A": {"vA"},
    "0:7": {"^^^<A"},
    "0:8": {"^^^A"},
    "0:9": {"^^^>A", ">^^^A"},
    "0:4": {"^^<A"},
    "0:5": {"^^A"},
    "0:6": {">^^A", "^^>A"},
    "0:1": {"^<A"},
    "0:2": {"^A"},
    "0:3": {"^>A", ">^A"},
    "0:0": {"A"},
    "0:A": {">A"},
    "A:7": {"^^^<<A"},
    "A:8": {"<^^^A", "^^^<A"},
    "A:9": {"^^^A"},
    "A:4": {"^^<<A"},
    "A:5": {"<^^A", "^^<A"},
    "A:6": {"^^A"},
    "A:1": {"^<<A"},
    "A:2": {"^<A", "<^A"},
    "A:3": {"^A"},
    "A:0": {"<A"},
    "A:A": {"A"},
}

ROBOT_TO_ROBOT_TRANSITIONS = {
    "^:^": {"A"},
    "^:A": {">A"},
    "^:<": {"v<A"},
    "^:v": {"vA"},
    "^:>": {"v>A", ">vA"},
    "A:^": {"<A"},
    "A:A": {"A"},
    "A:<": {"v<<A"},
    "A:v": {"<vA", "v<A"},
    "A:>": {"vA"},
    "<:^": {">^A"},
    "<:A": {">>^A"},
    "<:<": {"A"},
    "<:v": {">A"},
    "<:>": {">>A"},
    "v:^": {"^A"},
    "v:A": {">^A", "^>A"},
    "v:<": {"<A"},
    "v:v": {"A"},
    "v:>": {">A"},
    ">:^": {"^<A", "<^A"},
    ">:A": {"^A"},
    ">:<": {"<<A"},
    ">:v": {"<A"},
    ">:>": {"A"},
}


def test_build_transition_map():
    robot_to_robot = Robot(keypad_type="directional")
    robot_to_robot.build_transition_map()
    assert robot_to_robot.min_transition == ROBOT_TO_ROBOT_TRANSITIONS

    robot_to_keypad = Robot(keypad_type="keypad")
    robot_to_keypad.build_transition_map()
    assert robot_to_keypad.min_transition == ROBOT_TO_KEYPAD_TRANSITIONS


def options_to_tuples(possible_inputs):
    set_of_options = {
        "".join(instructions) for instructions in product(*possible_inputs)
    }
    return tuple(sorted(set_of_options))


def keypad_to_robot(desired_output):
    possible_inputs = []
    current_key = "A"
    for next_move in desired_output:
        routes = ROBOT_TO_KEYPAD_TRANSITIONS[f"{current_key}:{next_move}"]
        possible_inputs.append(routes)
        current_key = next_move
    return options_to_tuples(possible_inputs)


def test_keyboard_to_robot():
    assert keypad_to_robot("029A") == ("<A^A>^^AvvvA", "<A^A^^>AvvvA")


@cache
def split_into_blocks(desired_output):
    blocks = []
    current_block = ""
    for target in desired_output:
        if target == "A":
            blocks.append(f"{current_block}A")
            current_block = ""
        else:
            current_block = f"{current_block}{target}"
    if current_block != "":
        blocks.append(current_block)
    # return Counter(blocks)
    return blocks


def test_split_into_blocks():
    # assert split_into_blocks("<A^A>^^AvvvA") == Counter(["<A", "^A", ">^^A", "vvvA"])
    assert split_into_blocks("<A^A>^^AvvvA") == ["<A", "^A", ">^^A", "vvvA"]


@cache
def robot_to_robot(desired_output):
    blocks = split_into_blocks(desired_output)
    if len(blocks) == 1:
        possible_inputs = []
        current_key = "A"
        for next_move in desired_output:
            routes = ROBOT_TO_ROBOT_TRANSITIONS[f"{current_key}:{next_move}"]
            possible_inputs.append(routes)
            current_key = next_move
        return options_to_tuples(possible_inputs)
        # return tuple(sorted(
        #         {"".join(instructions) for instructions in product(*possible_inputs)}
        #     )
    next_blocks = [robot_to_robot(block) for block in blocks]
    return tuple({"".join(instructions) for instructions in product(*next_blocks)})


def test_keyboard_to_robot_to_robot():
    one_sequence = "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    robot_to_keypad = keypad_to_robot("029A")
    robot_to_robot_to_keypad = set()
    for instructions in robot_to_keypad:
        robot_to_robot_to_keypad |= set(robot_to_robot(instructions))
    assert one_sequence in robot_to_robot_to_keypad
    assert {len(instructions) for instructions in robot_to_robot_to_keypad} == {28}


def keyboard_to_robot_chain(desired_output, number_of_robots=1):
    current_instructions = keypad_to_robot(desired_output)
    for _ in range(number_of_robots - 1):
        next_level = set()
        for instructions in current_instructions:
            next_level |= set(robot_to_robot(instructions))
        min_len = min(len(instruction) for instruction in next_level)
        current_instructions = tuple(
            instruction for instruction in next_level if len(instruction) == min_len
        )
    return current_instructions


def test_keyboard_to_robot_chain():
    one_sequence = "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    assert one_sequence in keyboard_to_robot_chain("029A", number_of_robots=2)
    # NOTE: Filtering non-efficient paths from my TRANSITION mappings the following
    # another_sequence doesn't get generated - so I've commented out the test
    # another_sequence = (
    #     "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    # )
    # assert another_sequence in keyboard_to_robot_chain("029A", number_of_robots=3)


def instructions_to_block_frequency(instruction, multiplier=1):
    return {
        k: v * multiplier for k, v in Counter(split_into_blocks(instruction)).items()
    }


def add_keypad_robot(run_frequency):
    next_block_frequency = defaultdict(list)
    for block, block_frequency in run_frequency.items():
        next_instructions_list = robot_to_robot(block)
        for next_instructions in next_instructions_list:
            next_block_frequency[block].append(
                instructions_to_block_frequency(next_instructions, block_frequency)
            )
    next_block_frequency_list = []
    for block_frequency_tuple in product(*next_block_frequency.values()):
        total_count = defaultdict(int)
        for block_frequency in block_frequency_tuple:
            for block, count in block_frequency.items():
                total_count[block] += count
        next_block_frequency_list.append(total_count)
    return next_block_frequency_list


def add_keypad_robot_to_frequency_list(run_frequency_list):
    next_frequencies = []
    for run_frequency in run_frequency_list:
        next_frequencies.extend(add_keypad_robot(run_frequency))
    return next_frequencies


def score_keyboard_to_robot_chain(desired_output, number_of_robots=1):
    instruction_block_options = []
    for keypad_option in keypad_to_robot(desired_output):
        instruction_block_options.append(Counter(split_into_blocks(keypad_option)))

    # FIRST PASS
    # possible_scores = []
    # for keypad_option in keypad_options:
    #     instruction_blocks = Counter(split_into_blocks(keypad_option))
    #     for _ in range(2, number_of_robots + 1):
    #         next_instruction_blocks = Counter()
    #         for block, count in instruction_blocks.items():
    #             next_move_options = robot_to_robot(block)
    #             if len(next_move_options) > 1:
    #                 for next_move in next_move_options:
    #                     next_move_blocks = Counter(split_into_blocks(next_move))
    #                     pass  # TODO: Identify the "best" next_move_blocks
    #             next_move_blocks = Counter(split_into_blocks(next_move_options[0]))
    #             for instruction, instruction_count in next_move_blocks.items():
    #                 next_instruction_blocks[instruction] += count * instruction_count
    #         instruction_blocks = next_instruction_blocks
    #     possible_scores.append(
    #         int(desired_output[:-1])
    #         * sum(len(k) * v for (k, v) in instruction_blocks.items())
    #     )
    # return min(possible_scores)

    # NEXT ATTEMPT
    for _ in range(2, number_of_robots + 1):
        instruction_block_options = add_keypad_robot_to_frequency_list(
            instruction_block_options
        )

    min_option = None
    for instruction_block in instruction_block_options:
        current_sum = sum(len(k) * v for (k, v) in instruction_block.items())
        if min_option is None or current_sum < min_option:
            min_option = current_sum
    return min_option
    # return int(desired_output[:-1]) * min_option


def test_scores():
    assert (
        score_keyboard_to_robot_chain("029A", number_of_robots=3) == 68
    )  # 68 * 29 = 1972
    assert (
        score_keyboard_to_robot_chain("980A", number_of_robots=3) == 60
    )  # 60 * 980 = 58800
    assert (
        score_keyboard_to_robot_chain("179A", number_of_robots=3) == 68
    )  # 68 * 179 = 12172
    assert (
        score_keyboard_to_robot_chain("456A", number_of_robots=3) == 64
    )  # 64 * 456 = 29184
    assert (
        score_keyboard_to_robot_chain("379A", number_of_robots=3) == 64
    )  # 64 * 379 = 24256


def test_my_scores_pt1():
    assert (
        sum(
            score_keyboard_to_robot_chain(code, number_of_robots=3) * int(code[:-1])
            for code in CODES
        )
        == 137_870
    )


def test_my_scores_pt2():
    assert (
        sum(
            score_keyboard_to_robot_chain(code, number_of_robots=26) * int(code[:-1])
            for code in CODES
        )
        == 900900_1386299471622162292811
    )
    # Initial answer of 630_001_796_303_072 was too high, but I think I had an extra robot in there.
    # After fixing that got 521_349_728_026_862 which was still too high, but the code also resulted
    # in a part 1 answer that was too high.
    #
    # After fixing misc stuff so part 1 was now correct got 193_606_477_851_200 which was still too high...
    #
    # Overall this part 2 was quite a mess - finally rewrote to use frequency blocks which I probably
    # should refactor to be more clean or native to speed up?
    #
    # But finally got
