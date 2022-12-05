import re
from collections import defaultdict


class Puzzle:
    """
        --- Day 5: Supply Stacks ---
    The expedition can depart as soon as the final supplies have been unloaded from the ships.
    Supplies are stored in stacks of marked crates, but because the needed supplies are buried
    under many other crates, the crates need to be rearranged.

    The ship has a giant cargo crane capable of moving crates between stacks. To ensure none
    of the crates get crushed or fall over, the crane operator will rearrange them in a
    series of carefully-planned steps. After the crates are rearranged, the desired crates
    will be at the top of each stack.

    The Elves don't want to interrupt the crane operator during this delicate procedure,
    but they forgot to ask her which crate will end up where, and they want to be ready
    to unload them as soon as possible so they can embark.

    They do, however, have a drawing of the starting stacks of crates and the rearrangement
    procedure (your puzzle input). For example:

        [D]
    [N] [C]
    [Z] [M] [P]
        1   2   3

    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2

    In this example, there are three stacks of crates. Stack 1 contains two crates:
    crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates;
    from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a
    single crate, P.

    Then, the rearrangement procedure is given. In each step of the procedure, a
    quantity of crates is moved from one stack to a different stack. In the first
    step of the above rearrangement procedure, one crate is moved from stack 2 to
    stack 1, resulting in this configuration:

    [D]
    [N] [C]
    [Z] [M] [P]
        1   2   3
    In the second step, three crates are moved from stack 1 to stack 3. Crates
    are moved one at a time, so the first crate to be moved (D) ends up below
    the second and third crates:

            [Z]
            [N]
        [C] [D]
        [M] [P]
        1   2   3
    Then, both crates are moved from stack 2 to stack 1. Again, because crates
    are moved one at a time, crate C ends up below crate M:

            [Z]
            [N]
    [M]     [D]
    [C]     [P]
        1   2   3

    Finally, one crate is moved from stack 1 to stack 2:

            [Z]
            [N]
            [D]
    [C] [M] [P]
        1   2   3
    The Elves just need to know which crate will end up on top of each stack;
    in this example, the top crates are C in stack 1, M in stack 2, and Z in
    stack 3, so you should combine these together and give the Elves the
    message CMZ.

    After the rearrangement procedure completes, what crate ends up on top of each stack?

    --- Part Two ---
    As you watch the crane operator expertly rearrange the crates, you notice the
    process isn't following your prediction.

    Some mud was covering the writing on the side of the crane, and you quickly wipe
    it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

    The CrateMover 9001 is notable for many new and exciting features: air conditioning,
    leather seats, an extra cup holder, and the ability to pick up and move multiple crates
    at once.

    Again considering the example above, the crates begin in the same configuration:

        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    Moving a single crate from stack 2 to stack 1 behaves the same as before:

    [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    However, the action of moving three crates from stack 1 to stack 3 means that those
    three moved crates stay in the same order, resulting in this new configuration:

            [D]
            [N]
        [C] [Z]
        [M] [P]
     1   2   3
    Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

            [D]
            [N]
    [C]     [Z]
    [M]     [P]
     1   2   3
    Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

            [D]
            [N]
            [Z]
    [M] [C] [P]
     1   2   3
    In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

    Before the rearrangement process finishes, update your simulation so that the Elves know where
    they should stand to be ready to unload the final supplies. After the rearrangement procedure
    completes, what crate ends up on top of each stack?
    """


with open("day_05_input.txt") as fp:
    RAW_INPUT = fp.read()

SAMPLE_RAW = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def split_raw_input(raw):
    raw_board, raw_moves = raw.split("\n\n")
    board = defaultdict(list)
    for row in reversed(raw_board.split("\n")):
        if row[:2] == " 1":
            continue
        for col, value in enumerate(row):
            if col % 4 == 1:
                idx = (col + 3) // 4
                if value != " ":
                    board[idx].append(value)
    moves = [
        [int(n) for n in re.findall("(\d+)", move_str)]
        for move_str in raw_moves.split("\n")
    ]
    return dict(board), moves


def test_split():
    board, moves = split_raw_input(SAMPLE_RAW)
    assert board == {
        1: ["Z", "N"],
        2: ["M", "C", "D"],
        3: ["P"],
    }
    assert moves == [[1, 2, 1], [3, 1, 3], [2, 2, 1], [1, 1, 2]]

    # Now for full puzzle
    board, moves = split_raw_input(RAW_INPUT)
    assert board == {
        1: ["Z", "T", "F", "R", "W", "J", "G"],
        2: ["G", "W", "M"],
        3: ["J", "N", "H", "G"],
        4: ["J", "R", "C", "N", "W"],
        5: ["W", "F", "S", "B", "G", "Q", "V", "M"],
        6: ["S", "R", "T", "D", "V", "W", "C"],
        7: ["H", "B", "N", "C", "D", "Z", "G", "V"],
        8: ["S", "J", "N", "M", "G", "C"],
        9: ["G", "P", "N", "W", "C", "J", "D", "L"],
    }
    assert len(moves) == 503
    assert moves[-1] == [5, 5, 8]
    assert moves[12] == [11, 1, 4]


def update_board(board_state, desired_move, rev=True):
    number, from_col_idx, to_col_idx = desired_move
    from_col = board_state[from_col_idx]
    board_state[from_col_idx], boxes = from_col[:-number], from_col[-number:]
    board_state[to_col_idx] += reversed(boxes) if rev else boxes
    return board_state


def test_update_board():
    board, moves = split_raw_input(SAMPLE_RAW)
    for move in moves:
        board = update_board(board, move)
    assert "".join(col[-1] for col in board.values()) == "CMZ"

    board, moves = split_raw_input(SAMPLE_RAW)
    for move in moves:
        board = update_board(board, move, rev=False)
    assert "".join(col[-1] for col in board.values()) == "MCD"

    # Now for full puzzle
    board, moves = split_raw_input(RAW_INPUT)
    top_strings = {
        # 0: 'GMGWMCVCL',
        # 1: 'GMGWVCVCL',
        # 2: 'BMGWVCHCL',
        # 3: 'BMGWVCHCL',
    }
    for cnt, move in enumerate(moves):
        if cnt in top_strings:
            print(f"\n\ncnt={cnt} move={move}")
            print(board)
            assert (
                "".join(col[-1] if len(col) > 0 else "-" for col in board.values())
                == top_strings[cnt]
            )
        board = update_board(board, move)

    # print(f"\n\n\nfinal state of board\n{board}")
    assert (
        "".join(col[-1] if len(col) > 0 else "-" for col in board.values())
        == "CWMTGHBDW"
    )

    board, moves = split_raw_input(RAW_INPUT)
    for cnt, move in enumerate(moves):
        board = update_board(board, move, rev=False)
    assert (
        "".join(col[-1] if len(col) > 0 else "-" for col in board.values())
        == "SSCGWJCRB"
    )
