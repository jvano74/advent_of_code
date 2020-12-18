from collections import deque, defaultdict


class MarbleGame:
    """
    --- Day 9: Marble Mania ---
    You talk to the Elves while you wait for your navigation system to initialize.
    To pass the time, they introduce you to their favorite marble game.

    The Elves play this game by taking turns arranging the marbles in a circle according to very particular rules.
    The marbles are numbered starting with 0 and increasing by 1 until every marble has a number.

    First, the marble numbered 0 is placed in the circle. At this point, while it contains only a single marble,
    it is still a circle: the marble is both clockwise from itself and counter-clockwise from itself. This marble
    is designated the current marble.

    Then, each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles
    that are 1 and 2 marbles clockwise of the current marble. (When the circle is large enough, this means that
    there is one marble between the marble that was just placed and the current marble.) The marble that was
    just placed then becomes the current marble.

    However, if the marble that is about to be placed has a number which is a multiple of 23, something
    entirely different happens. First, the current player keeps the marble they would have placed, adding
    it to their score. In addition, the marble 7 marbles counter-clockwise from the current marble is removed
    from the circle and also added to the current player's score. The marble located immediately clockwise
    of the marble that was removed becomes the new current marble.

    For example, suppose there are 9 players. After the marble with value 0 is placed in the middle,
    each player (shown in square brackets) takes a turn. The result of each of those turns would produce
    circles of marbles like this, where clockwise is to the right and the resulting current marble is in
    parentheses:

    [-] (0)
    [1]  0 (1)
    [2]  0 (2) 1
    [3]  0  2  1 (3)
    [4]  0 (4) 2  1  3
    [5]  0  4  2 (5) 1  3
    [6]  0  4  2  5  1 (6) 3
    [7]  0  4  2  5  1  6  3 (7)
    [8]  0 (8) 4  2  5  1  6  3  7
    [9]  0  8  4 (9) 2  5  1  6  3  7
    [1]  0  8  4  9  2(10) 5  1  6  3  7
    [2]  0  8  4  9  2 10  5(11) 1  6  3  7
    [3]  0  8  4  9  2 10  5 11  1(12) 6  3  7
    [4]  0  8  4  9  2 10  5 11  1 12  6(13) 3  7
    [5]  0  8  4  9  2 10  5 11  1 12  6 13  3(14) 7
    [6]  0  8  4  9  2 10  5 11  1 12  6 13  3 14  7(15)
    [7]  0(16) 8  4  9  2 10  5 11  1 12  6 13  3 14  7 15
    [8]  0 16  8(17) 4  9  2 10  5 11  1 12  6 13  3 14  7 15
    [9]  0 16  8 17  4(18) 9  2 10  5 11  1 12  6 13  3 14  7 15
    [1]  0 16  8 17  4 18  9(19) 2 10  5 11  1 12  6 13  3 14  7 15
    [2]  0 16  8 17  4 18  9 19  2(20)10  5 11  1 12  6 13  3 14  7 15
    [3]  0 16  8 17  4 18  9 19  2 20 10(21) 5 11  1 12  6 13  3 14  7 15
    [4]  0 16  8 17  4 18  9 19  2 20 10 21  5(22)11  1 12  6 13  3 14  7 15
    [5]  0 16  8 17  4 18(19) 2 20 10 21  5 22 11  1 12  6 13  3 14  7 15
    [6]  0 16  8 17  4 18 19  2(24)20 10 21  5 22 11  1 12  6 13  3 14  7 15
    [7]  0 16  8 17  4 18 19  2 24 20(25)10 21  5 22 11  1 12  6 13  3 14  7 15

    The goal is to be the player with the highest score after the last marble is used up. Assuming the
    example above ends after the marble numbered 25, the winning score is 23+9=32 (because player 5 kept
    marble 23 and removed marble 9, while no other player got any points in this very short example game).

    Here are a few more examples:

    10 players; last marble is worth 1618 points: high score is 8317
    13 players; last marble is worth 7999 points: high score is 146373
    17 players; last marble is worth 1104 points: high score is 2764
    21 players; last marble is worth 6111 points: high score is 54718
    30 players; last marble is worth 5807 points: high score is 37305

    What is the winning Elf's score?

    --- Part Two ---
    Amused by the speed of your answer, the Elves are curious:

    What would the new winning Elf's score be if the number of the last marble were 100 times larger?
    """
    def __init__(self, num_players, num_marbles):
        self.num_players = num_players
        self.ring = [0]
        self.current_marble_position = 0
        self.remaining_marbles = range(1, num_marbles + 1)
        self.player_scores = [0 for _ in range(num_players)]
        self.player_scores_details = defaultdict(list)

    def play(self, print_game_stage=False):
        # clear scores before playing
        self.player_scores = [0 for _ in self.player_scores]
        self.player_scores_details = defaultdict(list)
        for player, marble in enumerate(self.remaining_marbles):
            if marble % 23 == 0:
                self.player_scores[player % self.num_players] += marble
                self.player_scores_details[player % self.num_players].append(marble)
                second_marble_position = (self.current_marble_position - 7)
                second_marble_position %= len(self.ring)
                second_marble = self.ring.pop(second_marble_position)
                if print_game_stage:
                    print(f'SCORING {marble} and second marble {second_marble} from {second_marble_position}')
                self.player_scores[player % self.num_players] += second_marble
                self.player_scores_details[player % self.num_players].append(second_marble)
                self.current_marble_position = second_marble_position
            else:
                self.current_marble_position += 1
                self.current_marble_position %= len(self.ring)
                self.current_marble_position += 1
                self.ring.insert(self.current_marble_position, marble)
            if print_game_stage:
                fancy_ring = [str(m) for m in self.ring]
                fancy_ring[self.current_marble_position] = f'({fancy_ring[self.current_marble_position]})'
                print(f'[{(player % self.num_players) + 1}] {" ".join(fancy_ring)}')
        if print_game_stage:
            print(f'last marble {marble}')
        return max(self.player_scores)


INPUT = [416, 71975]  # 416 players; last marble is worth 71975 points
SAMPLES = [
    [9, 25, False, 32],
    [10, 1618, False, 8317],
    [13, 7999, False, 146373],
    [17, 1104, False, 2764],
    [21, 6111, False, 54718],
    [30, 5807, False, 37305]]


def test_marble_game():
    print()
    for test_case in SAMPLES:
        print(f'=== GAME {test_case[0]}, {test_case[1]} ===')
        sample_game = MarbleGame(test_case[0], test_case[1])
        assert sample_game.play(test_case[2]) == test_case[3]
        print(sample_game.player_scores)
        print(sample_game.player_scores_details)
    # my game
    print('\n=== MY GAME ===')
    #game = MarbleGame(INPUT[0], INPUT[1])
    game = MarbleGame(416, 71975)
    assert game.play() == 439341
    print(game.player_scores)
    print(game.player_scores_details)

    # 524 is too low - was using wrong input >:(INPUT[0] and INPUT[0]?)
    # game2 = MarbleGame(INPUT[0], INPUT[1]*100)
    # game2 = MarbleGame(416, 71975*100)
    # 416 =       13 * 2*2*2*2*2
    # 7197500 = 2879 * 2*2 * 5*5*5*5


def play_game(max_players, last_marble):
    """
    from https://www.reddit.com/r/adventofcode/comments/a4i97s/2018_day_9_solutions/
    """
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % max_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores.values()) if scores else 0


def test_play_game():
    max_players, last_marble = (416, 71975*100)
    assert play_game(max_players, last_marble) == 1
