from pathlib import Path
from typing import NamedTuple


class Puzzle:
    """
    --- Day 15: Warehouse Woes ---
    You appear back inside your own mini submarine! Each Historian drives their
    mini submarine in a different direction; maybe the Chief has his own
    submarine down here somewhere as well?

    You look up to see a vast school of lanternfish swimming past you. On closer
    inspection, they seem quite anxious, so you drive your mini submarine over
    to see if you can help.

    Because lanternfish populations grow rapidly, they need a lot of food, and
    that food needs to be stored somewhere. That's why these lanternfish have
    built elaborate warehouse complexes operated by robots!

    These lanternfish seem so anxious because they have lost control of the
    robot that operates one of their most important warehouses! It is currently
    running amok, pushing around boxes in the warehouse with no regard for
    lanternfish logistics or lanternfish inventory management strategies.

    Right now, none of the lanternfish are brave enough to swim up to an
    unpredictable robot so they could shut it off. However, if you could
    anticipate the robot's movements, maybe they could find a safe option.

    The lanternfish already have a map of the warehouse and a list of movements
    the robot will attempt to make (your puzzle input). The problem is that the
    movements will sometimes fail as boxes are shifted around, making the actual
    movements of the robot difficult to predict.

    For example:

    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########

    <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
    vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
    ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
    <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
    ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
    ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
    >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
    <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
    ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
    v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^

    As the robot (@) attempts to move, if there are any boxes (O) in the way,
    the robot will also attempt to push those boxes. However, if this action
    would cause the robot or a box to move into a wall (#), nothing moves
    instead, including the robot. The initial positions of these are shown on
    the map at the top of the document the lanternfish gave you.

    The rest of the document describes the moves (^ for up, v for down, < for
    left, > for right) that the robot will attempt to make, in order. (The moves
    form a single giant sequence; they are broken into multiple lines just to
    make copy-pasting easier. Newlines within the move sequence should be
    ignored.)

    Here is a smaller example to get started:

    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    <^^>>>vv<v>>v<<

    Were the robot to attempt the given sequence of moves, it would push around
    the boxes as follows:

    Initial state:
    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move <:
    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move ^:
    ########
    #.@O.O.#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move ^:
    ########
    #.@O.O.#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move >:
    ########
    #..@OO.#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move >:
    ########
    #...@OO#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move >:
    ########
    #...@OO#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move v:
    ########
    #....OO#
    ##..@..#
    #...O..#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move v:
    ########
    #....OO#
    ##..@..#
    #...O..#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move <:
    ########
    #....OO#
    ##.@...#
    #...O..#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move v:
    ########
    #....OO#
    ##.....#
    #..@O..#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move >:
    ########
    #....OO#
    ##.....#
    #...@O.#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move >:
    ########
    #....OO#
    ##.....#
    #....@O#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move v:
    ########
    #....OO#
    ##.....#
    #.....O#
    #.#.O@.#
    #...O..#
    #...O..#
    ########

    Move <:
    ########
    #....OO#
    ##.....#
    #.....O#
    #.#O@..#
    #...O..#
    #...O..#
    ########

    Move <:
    ########
    #....OO#
    ##.....#
    #.....O#
    #.#O@..#
    #...O..#
    #...O..#
    ########

    The larger example has many more moves; after the robot has finished those
    moves, the warehouse would look like this:

    ##########
    #.O.O.OOO#
    #........#
    #OO......#
    #OO@.....#
    #O#.....O#
    #O.....OO#
    #O.....OO#
    #OO....OO#
    ##########

    The lanternfish use their own custom Goods Positioning System (GPS for
    short) to track the locations of the boxes. The GPS coordinate of a box is
    equal to 100 times its distance from the top edge of the map plus its
    distance from the left edge of the map. (This process does not stop at wall
    tiles; measure all the way to the edges of the map.)

    So, the box shown below has a distance of 1 from the top edge of the map and
    4 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 +
    4 = 104.

    #######
    #...O..
    #......

    The lanternfish would like to know the sum of all boxes' GPS coordinates
    after the robot finishes moving. In the larger example, the sum of all
    boxes' GPS coordinates is 10092. In the smaller example, the sum is 2028.

    Predict the motion of the robot and boxes in the warehouse. After the robot
    is finished moving, what is the sum of all boxes' GPS coordinates?

    Your puzzle answer was 1492518.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    The lanternfish use your information to find a safe moment to swim in and
    turn off the malfunctioning robot! Just as they start preparing a festival
    in your honor, reports start coming in that a second warehouse's robot is
    also malfunctioning.

    This warehouse's layout is surprisingly similar to the one you just helped.
    There is one key difference: everything except the robot is twice as wide!
    The robot's list of movements doesn't change.

    To get the wider warehouse's map, start with your original map and, for each
    tile, make the following changes:

    If the tile is #, the new map contains ## instead.
    If the tile is O, the new map contains [] instead.
    If the tile is ., the new map contains .. instead.
    If the tile is @, the new map contains @. instead.

    This will produce a new warehouse map which is twice as wide and with wide
    boxes that are represented by []. (The robot does not change size.)

    The larger example from before would now look like this:

    ####################
    ##....[]....[]..[]##
    ##............[]..##
    ##..[][]....[]..[]##
    ##....[]@.....[]..##
    ##[]##....[]......##
    ##[]....[]....[]..##
    ##..[][]..[]..[][]##
    ##........[]......##
    ####################

    Because boxes are now twice as wide but the robot is still the same size and
    speed, boxes can be aligned such that they directly push two other boxes at
    once. For example, consider this situation:

    #######
    #...#.#
    #.....#
    #..OO@#
    #..O..#
    #.....#
    #######

    <vv<<^^<<^^

    After appropriately resizing this map, the robot would push around these
    boxes as follows:

    Initial state:
    ##############
    ##......##..##
    ##..........##
    ##....[][]@.##
    ##....[]....##
    ##..........##
    ##############

    Move <:
    ##############
    ##......##..##
    ##..........##
    ##...[][]@..##
    ##....[]....##
    ##..........##
    ##############

    Move v:
    ##############
    ##......##..##
    ##..........##
    ##...[][]...##
    ##....[].@..##
    ##..........##
    ##############

    Move v:
    ##############
    ##......##..##
    ##..........##
    ##...[][]...##
    ##....[]....##
    ##.......@..##
    ##############

    Move <:
    ##############
    ##......##..##
    ##..........##
    ##...[][]...##
    ##....[]....##
    ##......@...##
    ##############

    Move <:
    ##############
    ##......##..##
    ##..........##
    ##...[][]...##
    ##....[]....##
    ##.....@....##
    ##############

    Move ^:
    ##############
    ##......##..##
    ##...[][]...##
    ##....[]....##
    ##.....@....##
    ##..........##
    ##############

    Move ^:
    ##############
    ##......##..##
    ##...[][]...##
    ##....[]....##
    ##.....@....##
    ##..........##
    ##############

    Move <:
    ##############
    ##......##..##
    ##...[][]...##
    ##....[]....##
    ##....@.....##
    ##..........##
    ##############

    Move <:
    ##############
    ##......##..##
    ##...[][]...##
    ##....[]....##
    ##...@......##
    ##..........##
    ##############

    Move ^:
    ##############
    ##......##..##
    ##...[][]...##
    ##...@[]....##
    ##..........##
    ##..........##
    ##############

    Move ^:
    ##############
    ##...[].##..##
    ##...@.[]...##
    ##....[]....##
    ##..........##
    ##..........##
    ##############

    This warehouse also uses GPS to locate the boxes. For these larger boxes,
    distances are measured from the edge of the map to the closest edge of the
    box in question. So, the box shown below has a distance of 1 from the top
    edge of the map and 5 from the left edge of the map, resulting in a GPS
    coordinate of 100 * 1 + 5 = 105.

    ##########
    ##...[]...
    ##........

    In the scaled-up version of the larger example from above, after the robot
    has finished all of its moves, the warehouse would look like this:

    ####################
    ##[].......[].[][]##
    ##[]...........[].##
    ##[]........[][][]##
    ##[]......[]....[]##
    ##..##......[]....##
    ##..[]............##
    ##..@......[].[][]##
    ##......[][]..[]..##
    ####################

    The sum of these boxes' GPS coordinates is 9021.

    Predict the motion of the robot and boxes in this new, scaled-up warehouse.
    What is the sum of all boxes' final GPS coordinates?

    Your puzzle answer was 1512860.

    Both parts of this puzzle are complete! They provide two gold stars: **

    """


def clean_map(raw_lines: str):
    result = raw_lines.split("\n")
    return [ln.strip() for ln in result if ln.strip() != ""]


SAMPLE_MAP = clean_map(
    """
    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########
    """
)


def test_clean_map():
    assert SAMPLE_MAP == [
        "##########",
        "#..O..O.O#",
        "#......O.#",
        "#.OO..O.O#",
        "#..O@..O.#",
        "#O#..O...#",
        "#O..O..O.#",
        "#.OO.O.OO#",
        "#....O...#",
        "##########",
    ]


def clean_moves(raw_lines: str):
    result = raw_lines.split("\n")
    return "".join(ln.strip() for ln in result if ln.strip() != "")


SAMPLE_MOVES = clean_moves(
    """
    <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
    vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
    ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
    <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
    ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
    ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
    >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
    <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
    ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
    v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
    """
)

with open(Path(__file__).parent / "2024_15_input.txt") as fp:
    MY_MAP, MY_MOVES = fp.read().split("\n\n")
    MY_MAP = clean_map(MY_MAP)
    MY_MOVES = clean_moves(MY_MOVES)


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pt(self.x - other.x, self.y - other.y)


DIRECTIONS = {
    "^": Pt(0, -1),
    ">": Pt(1, 0),
    "<": Pt(-1, 0),
    "v": Pt(0, 1),
}


class Warehouse:
    def __init__(self, raw_map, scale_up=False):
        self.boxes = set()
        self.walls = set()
        self.x_max = 0
        self.y_max = 0
        self.scale_up = scale_up
        self.box_ends = set()

        for y, raw_line in enumerate(raw_map):
            self.y_max = max(y, self.y_max)
            for x, c in enumerate(raw_line):
                true_x = 2 * x if scale_up else x
                self.x_max = max(true_x, self.x_max)
                match c:
                    case "@":
                        self.robot = Pt(true_x, y)
                    case "O":
                        self.boxes.add(Pt(true_x, y))
                        if scale_up:
                            self.box_ends.add(Pt(true_x + 1, y))
                    case "#":
                        self.walls.add(Pt(true_x, y))
                        if scale_up:
                            self.walls.add(Pt(true_x + 1, y))
                            self.x_max = max(true_x + 1, self.x_max)

    def score(self):
        return sum(box.x + 100 * box.y for box in self.boxes)

    def display(self):
        for y in range(self.y_max + 1):
            raw_line = []
            for x in range(self.x_max + 1):
                pt = Pt(x, y)
                if pt == self.robot:
                    raw_line.append("@")
                elif pt in self.walls:
                    raw_line.append("#")
                elif pt in self.boxes:
                    raw_line.append("[" if self.scale_up else "O")
                elif pt in self.box_ends:
                    raw_line.append("]")
                else:
                    raw_line.append(".")
            print("".join(raw_line))

    def push_boxes(self, delta, new_robot):
        moved_history = {}
        moving_boxes = {new_robot if new_robot in self.boxes else new_robot - Pt(1, 0)}

        while moving_boxes:
            next_moving_boxes = set()
            for box in moving_boxes:
                if box in moved_history:
                    continue

                new_box = box + delta
                new_box_end = new_box + Pt(1, 0)

                if new_box in self.walls or new_box_end in self.walls:
                    return False

                moved_history[box] = new_box

                if new_box in self.boxes:
                    next_moving_boxes.add(new_box)
                if new_box in self.box_ends:
                    next_moving_boxes.add(new_box - Pt(1, 0))
                if new_box_end in self.boxes:
                    next_moving_boxes.add(new_box_end)
                if new_box_end in self.box_ends:
                    next_moving_boxes.add(new_box_end - Pt(1, 0))

            if next_moving_boxes:
                moving_boxes = next_moving_boxes
            else:
                for box in moved_history.keys():
                    self.boxes.remove(box)
                    self.box_ends.remove(box + Pt(1, 0))
                for new_box in moved_history.values():
                    self.boxes.add(new_box)
                    self.box_ends.add(new_box + Pt(1, 0))
                return True

    def move(self, directions, display=False):
        for direction in directions:
            if direction not in DIRECTIONS:
                continue
            delta = DIRECTIONS[direction]

            new_robot = self.robot + delta

            if self.scale_up:
                if new_robot in self.walls:
                    pass
                elif new_robot not in (self.boxes | self.box_ends):
                    self.robot = new_robot
                elif self.push_boxes(delta, new_robot):
                    self.robot = new_robot
            else:
                test_location = new_robot
                while test_location in self.boxes:
                    test_location += delta
                if test_location not in self.walls:
                    self.robot = new_robot
                    if new_robot in self.boxes:
                        self.boxes.remove(new_robot)
                        self.boxes.add(test_location)

            if display:
                print(f"Move {direction}:")
                self.display()


SMALL_MAP = clean_map(
    """
    #######
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########
    """
)

SMALL_MOVES = "<^^>>>vv<v>>v<<"


def test_part_1_sample():
    small_warehouse = Warehouse(SMALL_MAP)
    small_warehouse.move(SMALL_MOVES)
    assert small_warehouse.score() == 2028
    sample_warehouse = Warehouse(SAMPLE_MAP)
    sample_warehouse.display()
    sample_warehouse.move(SAMPLE_MOVES)
    assert sample_warehouse.score() == 10092


SMALL2_MAP = clean_map(
    """
    #######
    #...#.#
    #.....#
    #..OO@#
    #..O..#
    #.....#
    #######
    """
)

SMALL2_MOVES = "<vv<<^^<<^^"
SMALL2_MOVES2 = "<<vv<<^^"


def test_part_2_sample():
    sample2_warehouse = Warehouse(SMALL2_MAP, scale_up=True)
    # sample2_warehouse.display()
    sample2_warehouse.move(SMALL2_MOVES, display=False)
    assert sample2_warehouse.score() == 618

    sample2_warehouse = Warehouse(SMALL2_MAP, scale_up=True)
    sample2_warehouse.move(SMALL2_MOVES2, display=False)
    assert sample2_warehouse.score() == 616

    sample_warehouse = Warehouse(SAMPLE_MAP, scale_up=True)
    # sample_warehouse.display()
    sample_warehouse.move(SAMPLE_MOVES, display=False)
    # sample_warehouse.display()
    assert sample_warehouse.score() == 9021


def test_inputs():
    my_warehouse = Warehouse(MY_MAP)
    my_warehouse.move(MY_MOVES)
    assert my_warehouse.score() == 1492518
    my_warehouse = Warehouse(MY_MAP, scale_up=True)
    my_warehouse.move(MY_MOVES)
    assert my_warehouse.score() == 1512860
