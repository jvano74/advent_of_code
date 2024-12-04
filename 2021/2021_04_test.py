from pathlib import Path


class Puzzle:
    """
    --- Day 4: Giant Squid ---
    You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that
    you can't see any sunlight. What you can see, however, is a giant squid that has attached itself
    to the outside of your submarine.

    Maybe it wants to play bingo?

    Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen
    at random, and the chosen number is marked on all boards on which it appears. (Numbers may not
    appear on all boards.) If all numbers in any row or any column of a board are marked, that board
    wins. (Diagonals don't count.)

    The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass
    the time. It automatically generates a random order in which to draw numbers and a random set
    of boards (your puzzle input). For example:

    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7

    After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners,
    but the boards are marked as follows (shown here adjacent to each other to save space):

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

    After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

    Finally, 24 is drawn:

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

    At this point, the third board wins because it has at least one complete row or column of
    marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

    The score of the winning board can now be calculated. Start by finding the sum of all unmarked
    numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that
    was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

    To guarantee victory against the giant squid, figure out which board will win first. What will
    your final score be if you choose that board?

    To begin, get your puzzle input.

    """


SAMPLE_BALLS = [
    7,
    4,
    9,
    5,
    11,
    17,
    23,
    2,
    0,
    14,
    21,
    24,
    10,
    16,
    13,
    6,
    15,
    25,
    12,
    22,
    18,
    20,
    8,
    19,
    3,
    26,
    1,
]

SAMPLE_BOARD = [
    """22 13 17 11  0
        8  2 23  4 24
       21  9 14 16  7
        6 10  3 18  5
        1 12 20 15 19""",
    """ 3 15  0  2 22
        9 18 13 17  5
       19  8  7 25 23
       20 11 10 24  4
       14 21 16 12  6""",
    """14 21 17 24  4
       10 16 15  9 19
       18  8 23 26 20
       22 11 13  6  5
        2  0 12  3  7""",
]

with open(Path(__file__).parent / "2021_04_input.txt") as fp:
    RAW = fp.read().split("\n\n")
    INPUT_BALLS = [int(n) for n in RAW[0].split(",")]
    INPUT_BOARDS = RAW[1:]


class BingoBoard:
    def __init__(self, raw_board):
        self.board = []
        for ln in raw_board.split("\n"):
            self.board.append([int(d) for d in ln.split()])
        self.wins = []
        for i in range(5):
            self.wins.append(set(self.board[i]))
            self.wins.append(set(self.board[j][i] for j in range(5)))

    def winner_score(self, called):
        for w in self.wins:
            if w.issubset(called):
                remaining = 0
                for i in range(5):
                    for j in range(5):
                        if self.board[i][j] not in called:
                            remaining += self.board[i][j]
                return remaining * called[-1]
        return 0


def first_winner(raw_boards, raw_draws):
    input_boards = [BingoBoard(raw) for raw in raw_boards]
    for turn_number in range(4, len(raw_draws)):
        for board in input_boards:
            score = board.winner_score(raw_draws[0:turn_number])
            if score > 0:
                return score


def test_bingo_board():
    board = BingoBoard(SAMPLE_BOARD[0])
    board2 = BingoBoard(SAMPLE_BOARD[1])
    board3 = BingoBoard(SAMPLE_BOARD[2])
    assert board.winner_score(SAMPLE_BALLS[0:11]) == 0
    assert board.winner_score(SAMPLE_BALLS[0:12]) == 0
    assert board2.winner_score(SAMPLE_BALLS[0:12]) == 0
    assert board3.winner_score(SAMPLE_BALLS[0:12]) == 4512


def test_first_winner():
    assert first_winner(SAMPLE_BOARD, SAMPLE_BALLS) == 4512
    assert first_winner(INPUT_BOARDS, INPUT_BALLS) == 25410


def last_winner(raw_boards, raw_draws):
    input_boards = [BingoBoard(raw) for raw in raw_boards]
    last_score = 0
    winners = dict()
    winning_order = []
    for turn_number in range(4, len(raw_draws)):
        for board_number, board in enumerate(input_boards):
            if board_number not in winners:
                score = board.winner_score(raw_draws[0:turn_number])
                if score > 0:
                    winners[board_number] = score
                    winning_order.append((turn_number, board_number))
                    last_score = score
    return last_score


def test_last_winner():
    assert last_winner(SAMPLE_BOARD, SAMPLE_BALLS) == 1924
    assert last_winner(INPUT_BOARDS, INPUT_BALLS) == 2730
