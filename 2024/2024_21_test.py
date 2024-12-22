from queue import PriorityQueue
from itertools import product
from typing import NamedTuple
from functools import cache
from collections import defaultdict


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
        # min_transition = defaultdict(lambda: defaultdict(set))
        self.min_transition = dict()
        for start_pt, start_id in self.button.items():
            for end_pt, end_id in self.button.items():
                self.min_transition[f"{start_id}{end_id}"] = set()
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
                        self.min_transition[f"{start_id}{end_id}"].add(
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

    def action(self, action):
        if action == "A":
            return self.button[self.arm]
        new_arm = self.arm + DELTA[action]
        if new_arm not in self.button:
            raise Exception("Invalid state")
        self.arm = new_arm


ROBOT_TO_KEYPAD_TRANSITIONS = {
    "77": {"A"},
    "78": {">A"},
    "79": {">>A"},
    "74": {"vA"},
    "75": {"v>A", ">vA"},
    "76": {">>vA", "v>>A", ">v>A"},
    "71": {"vvA"},
    "72": {"v>vA", ">vvA", "vv>A"},
    "73": {"vv>>A", ">v>vA", ">>vvA", "v>>vA", ">vv>A", "v>v>A"},
    "70": {"vv>vA", "v>vvA", ">vvvA"},
    "7A": {
        "v>>vvA",
        "v>vv>A",
        "vv>>vA",
        ">vvv>A",
        ">v>vvA",
        "v>v>vA",
        "vv>v>A",
        ">>vvvA",
        ">vv>vA",
    },
    "87": {"<A"},
    "88": {"A"},
    "89": {">A"},
    "84": {"v<A", "<vA"},
    "85": {"vA"},
    "86": {"v>A", ">vA"},
    "81": {"vv<A", "<vvA", "v<vA"},
    "82": {"vvA"},
    "83": {"v>vA", ">vvA", "vv>A"},
    "80": {"vvvA"},
    "8A": {"vvv>A", "v>vvA", "vv>vA", ">vvvA"},
    "97": {"<<A"},
    "98": {"<A"},
    "99": {"A"},
    "94": {"<<vA", "<v<A", "v<<A"},
    "95": {"v<A", "<vA"},
    "96": {"vA"},
    "91": {"v<v<A", "<v<vA", "vv<<A", "<<vvA", "<vv<A", "v<<vA"},
    "92": {"vv<A", "<vvA", "v<vA"},
    "93": {"vvA"},
    "90": {"<vvvA", "vvv<A", "vv<vA", "v<vvA"},
    "9A": {"vvvA"},
    "47": {"^A"},
    "48": {"^>A", ">^A"},
    "49": {">^>A", "^>>A", ">>^A"},
    "44": {"A"},
    "45": {">A"},
    "46": {">>A"},
    "41": {"vA"},
    "42": {"v>A", ">vA"},
    "43": {">>vA", "v>>A", ">v>A"},
    "40": {"v>vA", ">vvA"},
    "4A": {">v>vA", ">>vvA", "v>>vA", ">vv>A", "v>v>A"},
    "57": {"<^A", "^<A"},
    "58": {"^A"},
    "59": {"^>A", ">^A"},
    "54": {"<A"},
    "55": {"A"},
    "56": {">A"},
    "51": {"v<A", "<vA"},
    "52": {"vA"},
    "53": {"v>A", ">vA"},
    "50": {"vvA"},
    "5A": {"v>vA", ">vvA", "vv>A"},
    "67": {"^<<A", "<^<A", "<<^A"},
    "68": {"<^A", "^<A"},
    "69": {"^A"},
    "64": {"<<A"},
    "65": {"<A"},
    "66": {"A"},
    "61": {"<<vA", "<v<A", "v<<A"},
    "62": {"v<A", "<vA"},
    "63": {"vA"},
    "60": {"vv<A", "<vvA", "v<vA"},
    "6A": {"vvA"},
    "17": {"^^A"},
    "18": {"^^>A", ">^^A", "^>^A"},
    "19": {"^^>>A", ">^>^A", ">^^>A", ">>^^A", "^>>^A", "^>^>A"},
    "14": {"^A"},
    "15": {"^>A", ">^A"},
    "16": {">^>A", "^>>A", ">>^A"},
    "11": {"A"},
    "12": {">A"},
    "13": {">>A"},
    "10": {">vA"},
    "1A": {">>vA", ">v>A"},
    "27": {"^<^A", "<^^A", "^^<A"},
    "28": {"^^A"},
    "29": {"^^>A", ">^^A", "^>^A"},
    "24": {"<^A", "^<A"},
    "25": {"^A"},
    "26": {"^>A", ">^A"},
    "21": {"<A"},
    "22": {"A"},
    "23": {">A"},
    "20": {"vA"},
    "2A": {"v>A", ">vA"},
    "37": {"<^<^A", "<^^<A", "<<^^A", "^<^<A", "^<<^A", "^^<<A"},
    "38": {"^<^A", "<^^A", "^^<A"},
    "39": {"^^A"},
    "34": {"^<<A", "<^<A", "<<^A"},
    "35": {"<^A", "^<A"},
    "36": {"^A"},
    "31": {"<<A"},
    "32": {"<A"},
    "33": {"A"},
    "30": {"v<A", "<vA"},
    "3A": {"vA"},
    "07": {"^^^<A", "^<^^A", "^^<^A"},
    "08": {"^^^A"},
    "09": {">^^^A", "^^^>A", "^>^^A", "^^>^A"},
    "04": {"^<^A", "^^<A"},
    "05": {"^^A"},
    "06": {"^^>A", ">^^A", "^>^A"},
    "01": {"^<A"},
    "02": {"^A"},
    "03": {"^>A", ">^A"},
    "00": {"A"},
    "0A": {">A"},
    "A7": {
        "<^^<^A",
        "^<^^<A",
        "^<^<^A",
        "^^^<<A",
        "^^<<^A",
        "^<<^^A",
        "^^<^<A",
        "<^^^<A",
        "<^<^^A",
    },
    "A8": {"^^^<A", "^<^^A", "<^^^A", "^^<^A"},
    "A9": {"^^^A"},
    "A4": {"<^<^A", "<^^<A", "^<^<A", "^<<^A", "^^<<A"},
    "A5": {"^<^A", "<^^A", "^^<A"},
    "A6": {"^^A"},
    "A1": {"^<<A", "<^<A"},
    "A2": {"<^A", "^<A"},
    "A3": {"^A"},
    "A0": {"<A"},
    "AA": {"A"},
}

OPT_ROBOT_TO_KEYPAD = {
    "77": {"A"},
    "78": {">A"},
    "79": {">>A"},
    "74": {"vA"},
    "75": {"v>A", ">vA"},
    "76": {">>vA", "v>>A", ">v>A"},
    "71": {"vvA"},
    "72": {">vvA", "vv>A"},
    "73": {"vv>>A", ">>vvA"},
    "70": {">vvvA"},
    "7A": {">>vvvA"},
    "87": {"<A"},
    "88": {"A"},
    "89": {">A"},
    "84": {"v<A", "<vA"},
    "85": {"vA"},
    "86": {"v>A", ">vA"},
    "81": {"vv<A", "<vvA"},
    "82": {"vvA"},
    "83": {">vvA", "vv>A"},
    "80": {"vvvA"},
    "8A": {"vvv>A", ">vvvA"},
    "97": {"<<A"},
    "98": {"<A"},
    "99": {"A"},
    "94": {"<<vA", "v<<A"},
    "95": {"v<A", "<vA"},
    "96": {"vA"},
    "91": {"vv<<A", "<<vvA"},
    "92": {"vv<A", "<vvA"},
    "93": {"vvA"},
    "90": {"<vvvA", "vvv<A"},
    "9A": {"vvvA"},
    "47": {"^A"},
    "48": {"^>A", ">^A"},
    "49": {"^>>A", ">>^A"},
    "44": {"A"},
    "45": {">A"},
    "46": {">>A"},
    "41": {"vA"},
    "42": {"v>A", ">vA"},
    "43": {">>vA", "v>>A"},
    "40": {">vvA"},
    "4A": {">>vvA"},
    "57": {"<^A", "^<A"},
    "58": {"^A"},
    "59": {"^>A", ">^A"},
    "54": {"<A"},
    "55": {"A"},
    "56": {">A"},
    "51": {"v<A", "<vA"},
    "52": {"vA"},
    "53": {"v>A", ">vA"},
    "50": {"vvA"},
    "5A": {">vvA", "vv>A"},
    "67": {"^<<A", "<<^A"},
    "68": {"<^A", "^<A"},
    "69": {"^A"},
    "64": {"<<A"},
    "65": {"<A"},
    "66": {"A"},
    "61": {"<<vA", "v<<A"},
    "62": {"v<A", "<vA"},
    "63": {"vA"},
    "60": {"vv<A", "<vvA"},
    "6A": {"vvA"},
    "17": {"^^A"},
    "18": {"^^>A", ">^^A"},
    "19": {"^^>>A", ">>^^A"},
    "14": {"^A"},
    "15": {"^>A", ">^A"},
    "16": {"^>>A", ">>^A"},
    "11": {"A"},
    "12": {">A"},
    "13": {">>A"},
    "10": {">vA"},
    "1A": {">>vA"},
    "27": {"<^^A", "^^<A"},
    "28": {"^^A"},
    "29": {"^^>A", ">^^A"},
    "24": {"<^A", "^<A"},
    "25": {"^A"},
    "26": {"^>A", ">^A"},
    "21": {"<A"},
    "22": {"A"},
    "23": {">A"},
    "20": {"vA"},
    "2A": {"v>A", ">vA"},
    "37": {"<<^^A", "^^<<A"},
    "38": {"<^^A", "^^<A"},
    "39": {"^^A"},
    "34": {"^<<A", "<<^A"},
    "35": {"<^A", "^<A"},
    "36": {"^A"},
    "31": {"<<A"},
    "32": {"<A"},
    "33": {"A"},
    "30": {"v<A", "<vA"},
    "3A": {"vA"},
    "07": {"^^^<A"},
    "08": {"^^^A"},
    "09": {">^^^A", "^^^>A"},
    "04": {"^^<A"},
    "05": {"^^A"},
    "06": {"^^>A", ">^^A"},
    "01": {"^<A"},
    "02": {"^A"},
    "03": {"^>A", ">^A"},
    "00": {"A"},
    "0A": {">A"},
    "A7": {"^^^<<A"},
    "A8": {"^^^<A", "<^^^A"},
    "A9": {"^^^A"},
    "A4": {"^^<<A"},
    "A5": {"<^^A", "^^<A"},
    "A6": {"^^A"},
    "A1": {
        "^<<A",
    },
    "A2": {"<^A", "^<A"},
    "A3": {"^A"},
    "A0": {"<A"},
    "AA": {"A"},
}

ROBOT_TO_ROBOT_TRANSITIONS = {
    "^^": {"A"},
    "^A": {">A"},
    "^<": {"v<A"},
    "^v": {"vA"},
    "^>": {">vA", "v>A"},
    "A^": {"<A"},
    "AA": {"A"},
    "A<": {"v<<A", "<v<A"},
    "Av": {"v<A", "<vA"},
    "A>": {"vA"},
    "<^": {">^A"},
    "<A": {">>^A", ">^>A"},
    "<<": {"A"},
    "<v": {">A"},
    "<>": {">>A"},
    "v^": {"^A"},
    "vA": {">^A", "^>A"},
    "v<": {"<A"},
    "vv": {"A"},
    "v>": {">A"},
    ">^": {"^<A", "<^A"},
    ">A": {"^A"},
    "><": {"<<A"},
    ">v": {"<A"},
    ">>": {"A"},
}

OPT_ROBOT_TO_ROBOT = {
    "AA": {"A"},
    "^^": {"A"},
    "vv": {"A"},
    "<<": {"A"},
    ">>": {"A"},
    "^A": {">A"},
    "^<": {"v<A"},
    "^v": {"vA"},
    "A^": {"<A"},
    "A<": {"v<<A"},
    "A>": {"vA"},
    "<^": {">^A"},
    "<A": {">>^A"},
    "<v": {">A"},
    "<>": {">>A"},
    "v^": {"^A"},
    "v<": {"<A"},
    "v>": {">A"},
    ">A": {"^A"},
    "><": {"<<A"},
    ">v": {"<A"},
    # "^>": {">vA", "v>A"},
    # "Av": {"v<A", "<vA"},
    # "vA": {">^A", "^>A"},
    # ">^": {"^<A", "<^A"},
    "^>": {"v>A"},
    "Av": {"<vA"},
    "vA": {">^A"},
    ">^": {"<^A"},
}


def test_build_transition_map():
    robot_to_robot = Robot(keypad_type="directional")
    robot_to_robot.build_transition_map()
    assert robot_to_robot.min_transition == ROBOT_TO_ROBOT_TRANSITIONS

    robot_to_keypad = Robot(keypad_type="keypad")
    robot_to_keypad.build_transition_map()
    assert robot_to_keypad.min_transition == ROBOT_TO_KEYPAD_TRANSITIONS


def keypad_to_robot(desired_output, opt=False):
    possible_inputs = []
    current_key = "A"
    for next_move in desired_output:
        routes = (
            OPT_ROBOT_TO_KEYPAD[f"{current_key}{next_move}"]
            if opt
            else ROBOT_TO_KEYPAD_TRANSITIONS[f"{current_key}{next_move}"]
        )
        possible_inputs.append(routes)
        current_key = next_move
    return {"".join(instructions) for instructions in product(*possible_inputs)}


def test_keyboard_to_robot():
    assert keypad_to_robot("029A") == {"<A^A>^^AvvvA", "<A^A^^>AvvvA", "<A^A^>^AvvvA"}


def robot_to_robot(desired_output, opt=False):
    possible_inputs = []
    current_key = "A"
    for next_move in desired_output:
        routes = (
            OPT_ROBOT_TO_ROBOT[f"{current_key}{next_move}"]
            if opt
            else ROBOT_TO_ROBOT_TRANSITIONS[f"{current_key}{next_move}"]
        )
        possible_inputs.append(routes)
        current_key = next_move
    return {"".join(instructions) for instructions in product(*possible_inputs)}


def test_keyboard_to_robot_to_robot():
    one_sequence = "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    robot_to_keypad = keypad_to_robot("029A")
    robot_to_robot_to_keypad = set()
    for instructions in robot_to_keypad:
        robot_to_robot_to_keypad |= robot_to_robot(instructions)
    assert one_sequence in robot_to_robot_to_keypad
    assert {len(instructions) for instructions in robot_to_robot_to_keypad} == {28, 30}


def keyboard_to_robot_chain(desired_output, number_of_robots=1, opt=False):
    current_instructions = keypad_to_robot(desired_output, opt)
    for _ in range(number_of_robots - 1):
        next_level = set()
        for instructions in current_instructions:
            next_level |= robot_to_robot(instructions, opt)
        min_len = min(len(instruction) for instruction in next_level)
        current_instructions = {
            instruction for instruction in next_level if len(instruction) == min_len
        }
    return current_instructions


def test_keyboard_to_robot_chain():
    one_sequence = "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    assert one_sequence in keyboard_to_robot_chain("029A", number_of_robots=2)
    another_sequence = (
        "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    )
    assert another_sequence in keyboard_to_robot_chain("029A", number_of_robots=3)


def score_keyboard_to_robot_chain(desired_output, number_of_robots=1):
    instructions = keyboard_to_robot_chain(desired_output, number_of_robots, opt=True)
    min_length = min(len(instruction) for instruction in instructions)
    return int(desired_output[:-1]) * min_length


def test_scores():
    assert score_keyboard_to_robot_chain("029A", number_of_robots=3) == 68 * 29
    assert score_keyboard_to_robot_chain("980A", number_of_robots=3) == 60 * 980
    assert score_keyboard_to_robot_chain("179A", number_of_robots=3) == 68 * 179
    assert score_keyboard_to_robot_chain("456A", number_of_robots=3) == 64 * 456
    assert score_keyboard_to_robot_chain("379A", number_of_robots=3) == 64 * 379


def test_my_scores_pt1():
    assert (
        sum(score_keyboard_to_robot_chain(code, number_of_robots=3) for code in CODES)
        == 137870
    )


def test_my_scores_pt2():
    assert (
        sum(score_keyboard_to_robot_chain(code, number_of_robots=26) for code in CODES)
        == 137870
    )
