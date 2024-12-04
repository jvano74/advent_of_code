from collections import defaultdict


class Puzzle:
    """
--- Day 21: Dirac Dice ---

There's not much to do as you slowly descend to the bottom of the ocean. The submarine computer challenges you to
a nice game of Dirac Dice.

This game consists of a single die, two pawns, and a game board with a circular track containing ten spaces marked
1 through 10 clockwise. Each player's starting space is chosen randomly (your puzzle input). Player 1 goes first.

Players take turns moving. On each player's turn, the player rolls the die three times and adds up the results.
Then, the player moves their pawn that many times forward around the track (that is, moving clockwise on spaces
in order of increasing value, wrapping back around to 1 after 10). So, if a player is on space 7 and they roll
2, 2, and 1, they would move forward 5 times, to spaces 8, 9, 10, 1, and finally stopping on 2.

After each player moves, they increase their score by the value of the space their pawn stopped on. Players' scores
start at 0. So, if the first player starts on space 7 and rolls a total of 5, they would stop on space 2 and add 2
to their score (for a total score of 2). The game immediately ends as a win for any player whose score reaches at
least 1000.

Since the first game is a practice game, the submarine opens a compartment labeled deterministic dice and a 100-sided
die falls out. This die always rolls 1 first, then 2, then 3, and so on up to 100, after which it starts over at 1
again. Play using this die.

For example, given these starting positions:

Player 1 starting position: 4
Player 2 starting position: 8
This is how the game would go:

Player 1 rolls 1+2+3 and moves to space 10 for a total score of 10.
Player 2 rolls 4+5+6 and moves to space 3 for a total score of 3.
Player 1 rolls 7+8+9 and moves to space 4 for a total score of 14.
Player 2 rolls 10+11+12 and moves to space 6 for a total score of 9.
Player 1 rolls 13+14+15 and moves to space 6 for a total score of 20.
Player 2 rolls 16+17+18 and moves to space 7 for a total score of 16.
Player 1 rolls 19+20+21 and moves to space 6 for a total score of 26.
Player 2 rolls 22+23+24 and moves to space 6 for a total score of 22.
...after many turns...

Player 2 rolls 82+83+84 and moves to space 6 for a total score of 742.
Player 1 rolls 85+86+87 and moves to space 4 for a total score of 990.
Player 2 rolls 88+89+90 and moves to space 3 for a total score of 745.
Player 1 rolls 91+92+93 and moves to space 10 for a final score, 1000.

Since player 1 has at least 1000 points, player 1 wins and the game ends. At this point, the losing player had
745 points and the die had been rolled a total of 993 times; 745 * 993 = 739785.

Play a practice game using the deterministic 100-sided die. The moment either player wins, what do you get if you
multiply the score of the losing player by the number of times the die was rolled during the game?

To begin, get your puzzle input.


--- Part Two ---

Now that you're warmed up, it's time to play the real game.

A second compartment opens, this time labeled Dirac dice. Out of it falls a single three-sided die.

As you experiment with the die, you feel a little strange. An informational brochure in the compartment explains
that this is a quantum die: when you roll it, the universe splits into multiple copies, one copy for each possible
outcome of the die. In this case, rolling the die always splits the universe into three copies: one where the
outcome of the roll was 1, one where it was 2, and one where it was 3.

The game is played the same as before, although to prevent things from getting too far out of hand, the game now
ends when either player's score reaches at least 21.

Using the same starting positions as in the example above, player 1 wins in 444356092776315 universes, while
player 2 merely wins in 341960390180808 universes.

Using your given starting positions, determine every possible outcome. Find the player that wins in more
universes; in how many universes does that player win?
    """


RAW_INPUT = '''
Player 1 starting position: 6
Player 2 starting position: 3'''

INPUT = [6, 3]

SAMPLE = [4, 8]


class Game:
    def __init__(self, l_pos, r_pos):
        self.die = 0
        self.rolls = 0
        self.l_pos = l_pos
        self.r_pos = r_pos
        self.l_score = 0
        self.r_score = 0

    def roll(self):
        self.rolls += 1
        self.die = self.die % 100 + 1
        return self.die

    def take_turn(self, start):
        return (start - 1 + self.roll() + self.roll() + self.roll()) % 10 + 1

    def play(self):
        while True:
            self.l_pos = self.take_turn(self.l_pos)
            self.l_score += self.l_pos
            if self.l_score >= 1000:
                return self.r_score * self.rolls

            self.r_pos = self.take_turn(self.r_pos)
            self.r_score += self.r_pos
            if self.r_score >= 1000:
                return self.l_score * self.rolls


def test_game():
    sample_game = Game(4, 8)
    assert sample_game.play() == 739785
    my_game = Game(6, 3)
    assert my_game.play() == 752745


class QGame:
    def __init__(self, l_pos, r_pos):
        self.q_state = defaultdict(int)
        self.q_state[(l_pos, 0, r_pos, 0)] = 1
        self.final_state = defaultdict(int)

    def take_turn(self, first=True):
        distro = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
        next_state = defaultdict(int)
        for (l_pos, l_score, r_pos, r_score), freq in self.q_state.items():
            for roll, multiplicity in distro.items():
                if first:
                    next_pos = (l_pos + roll - 1) % 10 + 1
                    if l_score + next_pos >= 21:
                        self.final_state[(next_pos, l_score + next_pos, r_pos, r_score)] += multiplicity * freq
                    else:
                        next_state[(next_pos, l_score + next_pos, r_pos, r_score)] += multiplicity * freq
                else:
                    next_pos = (r_pos + roll - 1) % 10 + 1
                    if r_score + next_pos >= 21:
                        self.final_state[(l_pos, l_score, next_pos, r_score + next_pos)] += multiplicity * freq
                    else:
                        next_state[(l_pos, l_score, next_pos, r_score + next_pos)] += multiplicity * freq
        self.q_state = next_state

    def play(self):
        while len(self.q_state) > 0:
            self.take_turn(True)
            if len(self.q_state) > 0:
                self.take_turn(False)
        l_wins = sum(self.final_state[s] for s in self.final_state if s[1] >= 21)
        r_wins = sum(self.final_state[s] for s in self.final_state if s[3] >= 21)
        return max(l_wins, r_wins)


def test_quantum_game():
    sample_game = QGame(4, 8)
    assert sample_game.play() == 444356092776315
    my_game = QGame(6, 3)
    assert my_game.play() == 309196008717909
