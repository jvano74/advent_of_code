from __future__ import annotations
from collections import defaultdict


class Puzzle:
    """
    --- Day 10: Balance Bots ---
    You come upon a factory in which many robots are zooming around handing
    small microchips to each other.

    Upon closer examination, you notice that each bot only proceeds when it has
    two microchips, and once it does, it gives each one to a different bot or
    puts it in a marked "output" bin. Sometimes, bots take microchips from
    "input" bins, too.

    Inspecting one of the microchips, it seems like they each contain a single
    number; the bots must use some logic to decide what to do with each chip.
    You access the local control computer and download the bots' instructions
    (your puzzle input).

    Some of the instructions specify that a specific-valued microchip should be
    given to a specific bot; the rest of the instructions indicate what a given
    bot should do with its lower-value or higher-value chip.

    For example, consider the following instructions:

    value 5 goes to bot 2
    bot 2 gives low to bot 1 and high to bot 0
    value 3 goes to bot 1
    bot 1 gives low to output 1 and high to bot 0
    bot 0 gives low to output 2 and high to output 0
    value 2 goes to bot 2

    - Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a
      value-2 chip and a value-5 chip.

    - Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and
      its higher one (5) to bot 0.

    - Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and
      gives the value-3 chip to bot 0.

    - Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in
      output 0.

    In the end, output bin 0 contains a value-5 microchip, output bin 1 contains
    a value-2 microchip, and output bin 2 contains a value-3 microchip. In this
    configuration, bot number 2 is responsible for comparing value-5 microchips
    with value-2 microchips.

    Based on your instructions, what is the number of the bot that is
    responsible for comparing value-61 microchips with value-17 microchips?

    --- Part Two ---
    What do you get if you multiply together the values of one chip in each of
    outputs 0, 1, and 2?
    """

    pass


class Bot:
    def __init__(self, give_low_to, give_high_to, monitor=set()):
        self.give_low_to = give_low_to
        self.give_high_to = give_high_to
        self.monitor = monitor
        self.chips = list()


class Board:
    def __init__(self, instructions, monitor=set()):
        self.bots = defaultdict(Bot)
        self.output = defaultdict(int)
        self.monitor = monitor
        self.monitor_results = []

        instructions = sorted(instructions)
        for inst in instructions:
            i = inst.split(" ")
            if i[0] == "bot":
                self.add_bot(int(i[1]), (i[5], int(i[6])), (i[-2], int(i[-1])))
            if i[0] == "value":
                self.add_chip((i[-2], int(i[-1])), int(i[1]))

    def add_chip(self, loc, chip):
        # print(f'add_chip {chip} to {loc}')
        if loc[0] == "output":
            self.output[loc[1]] = chip
        elif loc[0] == "bot":
            bot = self.bots[loc[1]]
            bot.chips.append(chip)
            if len(bot.chips) == 2:
                low, high = sorted(bot.chips)
                if low in self.monitor and high in self.monitor:
                    self.monitor_results.append(loc)
                bot.chips = list()
                self.add_chip(bot.give_low_to, low)
                self.add_chip(bot.give_high_to, high)

    def add_bot(self, bot, give_low_to, give_high_to):
        # print(f'add_bot {bot} gives low to {give_low_to} and high to {give_high_to}')
        self.bots[bot] = Bot(give_low_to, give_high_to)


SAMPLE = [
    "value 5 goes to bot 2",
    "bot 2 gives low to bot 1 and high to bot 0",
    "value 3 goes to bot 1",
    "bot 1 gives low to output 1 and high to bot 0",
    "bot 0 gives low to output 2 and high to output 0",
    "value 2 goes to bot 2",
]


with open("day_10_input.txt") as f:
    INPUTS = [line.strip() for line in f]


def test_board():
    sample = Board(SAMPLE, set([2, 5]))
    # print('\n\n')
    # print(sample.monitor_results)
    assert sample.monitor_results == [("bot", 2)]
    soln = Board(INPUTS, set([17, 61]))
    assert soln.monitor_results == [("bot", 147)]
    # print(soln.output)
    product = soln.output[0] * soln.output[1] * soln.output[2]
    assert product == 55637
